# Gridworld EcoJAX environment

from functools import partial
import os
from time import sleep
from typing import Any, Dict, List, Tuple, Type, TypeVar

import jax
import jax.numpy as jnp
import numpy as np
from jax import random
from jax.scipy.signal import convolve2d
from flax import struct
from jax.debug import breakpoint as jbreakpoint

from ecojax.core import EcoInformation
from ecojax.environment import BaseEcoEnvironment
from ecojax.metrics import Aggregator
from ecojax.spaces import EcojaxSpace, Discrete, Continuous
from ecojax.types import ActionAgent, ObservationAgent, StateEnv
from ecojax.utils import (
    DICT_COLOR_TAG_TO_RGB,
    instantiate_class,
    jprint,
    jprint_and_breakpoint,
    sigmoid,
    logit,
    try_get,
)
from ecojax.video import VideoRecorder


@struct.dataclass
class MetricsLifespan:
    metric_cumulative: jnp.ndarray


@struct.dataclass
class StateEnvGridworld(StateEnv):
    # The current timestep of the environment
    timestep: int

    # The current map of the environment, of shape (H, W, C) where C is the number of channels used to represent the environment
    map: jnp.ndarray  # (height, width, dim_tile) in R

    # The latitude of the sun (the row of the map where the sun is). It represents entirely the sun location.
    latitude_sun: int

    # Where the agents are, of shape (n_max_agents, 2). positions_agents[i, :] represents the (x,y) coordinates of the i-th agent in the map. Ghost agents are still represented in the array (in position (0,0)).
    positions_agents: jnp.ndarray  # (n_max_agents, 2) in [0, height-1] x [0, width-1]
    # The orientation of the agents, of shape (n_max_agents,) and of values in {0, 1, 2, 3}. orientation_agents[i] represents the index of its orientation in the env.
    # The orientation of an agent will have an impact on the way the agent's surroundings are perceived, because a certain rotation will be performed on the agent's vision in comparison to the traditional map[x-v:x+v+1, y-v:y+v+1, :] vision.
    # The angle the agent is facing is given by orientation_agents[i] * 90 degrees (modulo 360 degrees), where 0 is facing north.
    orientation_agents: jnp.ndarray  # (n_max_agents,) in {0, 1, 2, 3}
    # Whether the agents exist or not, of shape (n_max_agents,) and of values in {0, 1}. are_existing_agents[i] represents whether the i-th agent actually exists in the environment and should interact with it.
    # An non existing agent is called a Ghost Agent and is only kept as a placeholder in the positions_agents array, in order to keep the array of positions_agents of shape (n_max_agents, 2).
    are_existing_agents: jnp.ndarray  # (n_max_agents,) in {0, 1}
    # The energy level of the agents, of shape (n_max_agents,). energy_agents[i] represents the energy level of the i-th agent.
    energy_agents: jnp.ndarray  # (n_max_agents,) in [0, +inf)
    # The age of the agents
    age_agents: jnp.ndarray  # (n_max_agents,) in [0, +inf)


@struct.dataclass
class ObservationAgentGridworld(ObservationAgent):

    # The visual field of the agent, of shape (2v+1, 2v+1, n_channels_map) where n_channels_map is the number of channels used to represent the environment.
    visual_field: jnp.ndarray  # (2v+1, 2v+1, n_channels_map) in R

    # The energy level of an agent, of shape () and in [0, +inf).
    energy: jnp.ndarray

    # The age of an agent, of shape () and in [0, +inf).
    age: jnp.ndarray


@struct.dataclass
class ActionAgentGridworld(ActionAgent):

    # The direction of the agent, of shape () and in {0, 3}. direction represents the direction the agent wants to take.
    direction: jnp.ndarray

    # Whether the agent wants to eat, of shape () and in {0, 1}. eat represents whether the agent wants to eat the plant on its cell.
    # If an agent eats, it won't be able to move this turn.
    do_eat: jnp.ndarray


class GridworldEnv(BaseEcoEnvironment):
    """A Gridworld environment."""

    def __init__(
        self,
        config: Dict[str, Any],
        n_agents_max: int,
        n_agents_initial: int,
    ) -> None:
        """Initialize an instance of the Gridworld environment. This class allows to deal in a comprehensive way with a Gridworld environment
        that represents the world with which the agents interact. It is purely agnostic of the agents and their learning algorithms.

        In order to apply JAX transformation to such an OOP class, the following principles are applied:
        - the environmental parameters than are not changing during the simulation are stored in the class attributes, e.g. self.width, self.period_sun, etc.
        - the environmental objects that will change of value through the simulation are stored in the state, which is an object from a class inheriting the flax.struct.dataclass,
          which allows to apply JAX transformations to the object.

        The pipeline of the environment is the following:
        >>> env = GridworldEnv(config, n_agents_max, n_agents_initial)
        >>> (
        >>>     observations_agents,
        >>>     eco_information,
        >>>     done,
        >>>     info,
        >>> ) = env.reset(key_random)
        >>> 
        >>> while not done:
        >>> 
        >>>     env.render()
        >>> 
        >>>     actions = ...
        >>> 
        >>>     key_random, subkey = random.split(key_random)
        >>>     (
        >>>         observations_agents,
        >>>         eco_information,
        >>>         done_env,
        >>>         info_env,
        >>>     ) = env.step(
        >>>         key_random=subkey,
        >>>         actions=actions,
        >>>     )
        >>>    

        Args:
            config (Dict[str, Any]): the configuration of the environment
            n_agents_max (int): the maximum number of agents the environment can handle
            n_agents_initial (int): the initial number of agents in the environment. They are for now randomly placed in the environment.
        """
        self.config = config
        self.n_agents_max = n_agents_max
        self.n_agents_initial = n_agents_initial
        assert (
            self.n_agents_initial <= self.n_agents_max
        ), "n_agents_initial must be less than or equal to n_agents_max"
        # Environment Parameters
        self.width: int = config["width"]
        self.height: int = config["height"]
        self.is_terminal: bool = config["is_terminal"]
        self.period_logging: int = int(max(1, self.config["period_logging"]))
        self.list_names_channels: List[str] = [
            "sun",
            "plants",
            "agents",
        ]
        self.dict_name_channel_to_idx: Dict[str, int] = {
            name_channel: idx_channel
            for idx_channel, name_channel in enumerate(self.list_names_channels)
        }
        self.n_channels_map: int = len(self.dict_name_channel_to_idx)
        # Metrics parameters
        self.names_measures: List[str] = sum(
            [names for type_measure, names in config["metrics"]["measures"].items()], []
        )
        # Video parameters
        self.cfg_video = config["metrics"]["config_video"]
        self.do_video: bool = self.cfg_video["do_video"]
        self.n_steps_between_videos: int = self.cfg_video["n_steps_between_videos"]
        self.n_steps_per_video: int = self.cfg_video["n_steps_per_video"]
        self.n_steps_between_frames: int = self.cfg_video["n_steps_between_frames"]
        assert (
            self.n_steps_per_video <= self.n_steps_between_videos
        ) or not self.do_video, "len_video must be less than or equal to freq_video"
        self.fps_video: int = self.cfg_video["fps_video"]
        self.dir_videos: str = self.cfg_video["dir_videos"]
        os.makedirs(self.dir_videos, exist_ok=True)
        self.height_max_video: int = self.cfg_video["height_max_video"]
        self.width_max_video: int = self.cfg_video["width_max_video"]
        self.dict_name_channel_to_color_tag: Dict[str, str] = self.cfg_video[
            "dict_name_channel_to_color_tag"
        ]
        self.dict_idx_channel_to_color_tag: Dict[int, str] = {
            idx_channel: self.dict_name_channel_to_color_tag[name_channel]
            for name_channel, idx_channel in self.dict_name_channel_to_idx.items()
        }
        # Sun Parameters
        self.period_sun: int = config["period_sun"]
        self.method_sun: str = config["method_sun"]
        self.radius_sun_effect: int = config["radius_sun_effect"]
        self.radius_sun_perception: int = config["radius_sun_perception"]
        # Plants Dynamics
        self.proportion_plant_initial: float = config["proportion_plant_initial"]
        self.logit_p_base_plant_growth: float = logit(config["p_base_plant_growth"])
        self.logit_p_base_plant_death: float = logit(config["p_base_plant_death"])
        self.factor_sun_effect: float = config["factor_sun_effect"]
        self.factor_plant_reproduction: float = config["factor_plant_reproduction"]
        self.radius_plant_reproduction: int = config["radius_plant_reproduction"]
        self.kernel_plant_reproduction = jnp.ones(
            (
                config["radius_plant_reproduction"],
                config["radius_plant_reproduction"],
            )
        ) / (config["radius_plant_reproduction"] ** 2)
        self.factor_plant_asphyxia: float = config["factor_plant_asphyxia"]
        self.radius_plant_asphyxia: int = config["radius_plant_asphyxia"]
        self.kernel_plant_asphyxia = jnp.ones(
            (config["radius_plant_asphyxia"], config["radius_plant_asphyxia"])
        ) / (config["radius_plant_asphyxia"] ** 2)
        # Agents Parameters
        self.vision_range_agent: int = config["vision_range_agent"]
        self.grid_indexes_vision_x, self.grid_indexes_vision_y = jnp.meshgrid(
            jnp.arange(-self.vision_range_agent, self.vision_range_agent + 1),
            jnp.arange(-self.vision_range_agent, self.vision_range_agent + 1),
            indexing="ij",
        )
        self.age_max: int = config["age_max"]
        self.energy_initial: float = config["energy_initial"]
        self.energy_food: float = config["energy_food"]
        self.energy_thr_death: float = config["energy_thr_death"]
        self.energy_req_reprod: float = config["energy_req_reprod"]
        self.energy_cost_reprod: float = config["energy_cost_reprod"]
        self.do_active_reprod: bool = config["do_active_reprod"]
        # Other
        self.fill_value: int = self.n_agents_max

    def reset(
        self,
        key_random: jnp.ndarray,
    ) -> Tuple[
        StateEnvGridworld,
        ObservationAgentGridworld,
        EcoInformation,
        bool,
        Dict[str, Any],
    ]:
        idx_sun = self.dict_name_channel_to_idx["sun"]
        idx_plants = self.dict_name_channel_to_idx["plants"]
        idx_agents = self.dict_name_channel_to_idx["agents"]
        H, W = self.height, self.width
        # Initialize the map
        map = jnp.zeros(shape=(H, W, self.n_channels_map))
        # Initialize the sun
        if self.method_sun != "none":
            latitude_sun = H // 2
            latitudes = jnp.arange(H)
            distance_from_sun = jnp.minimum(
                jnp.abs(latitudes - latitude_sun),
                H - jnp.abs(latitudes - latitude_sun),
            )
            effect = jnp.clip(1 - distance_from_sun / self.radius_sun_effect, 0, 1)
            effect_map = jnp.repeat(effect[:, None], W, axis=1)
            map = map.at[:, :, idx_sun].set(effect_map)
        else:
            latitude_sun = None
        # Initialize the plants
        key_random, subkey = jax.random.split(key_random)
        map = map.at[:, :, idx_plants].set(
            jax.random.bernoulli(
                key=subkey,
                p=self.proportion_plant_initial,
                shape=(H, W),
            )
        )
        # Initialize the agents
        key_random, subkey = jax.random.split(key_random)
        are_existing_agents = jnp.array(
            [i < self.n_agents_initial for i in range(self.n_agents_max)],
            dtype=jnp.bool_,
        )
        positions_agents = jax.random.randint(
            key=subkey,
            shape=(self.n_agents_max, 2),
            minval=0,
            maxval=max(H, W),
        )
        positions_agents %= jnp.array([H, W])
        map = map.at[
            positions_agents[are_existing_agents, 0],
            positions_agents[are_existing_agents, 1],
            idx_agents,
        ].add(1)
        key_random, subkey = jax.random.split(key_random)
        orientation_agents = jax.random.randint(
            key=subkey,
            shape=(self.n_agents_max,),
            minval=0,
            maxval=4,
        )
        energy_agents = jnp.ones(self.n_agents_max) * self.energy_initial
        age_agents = jnp.ones(self.n_agents_max)

        # Initialize the state
        self.state = StateEnvGridworld(
            timestep=0,
            map=map,
            latitude_sun=latitude_sun,
            positions_agents=positions_agents,
            orientation_agents=orientation_agents,
            are_existing_agents=are_existing_agents,
            energy_agents=energy_agents,
            age_agents=age_agents,
        )

        # Initialize the metrics
        self.aggregators_lifespan: List[Aggregator] = []
        for config_agg in self.config["metrics"]["aggregators_lifespan"]:
            agg = instantiate_class(**config_agg)
            self.aggregators_lifespan.append(agg)
        self.aggregators_population: List[Aggregator] = []
        for config_agg in self.config["metrics"]["aggregators_population"]:
            agg = instantiate_class(**config_agg)
            self.aggregators_population.append(agg)

        # Initialize ecological informations
        are_newborns_agents = jnp.zeros(self.n_agents_max, dtype=jnp.bool_)
        are_dead_agents = jnp.zeros(self.n_agents_max, dtype=jnp.bool_)
        indexes_parents_agents = jnp.full((self.n_agents_max, 1), self.fill_value)
        eco_information = EcoInformation(
            are_newborns_agents=are_newborns_agents,
            indexes_parents=indexes_parents_agents,
            are_just_dead_agents=are_dead_agents,
        )

        # Return the information required by the agents
        observations_agents, _ = self.get_observations_agents(state=self.state)
        return (
            observations_agents,
            eco_information,
            False,
            {},
        )

    def step(
        self,
        key_random: jnp.ndarray,
        actions: jnp.ndarray,
    ) -> Tuple[
        ObservationAgentGridworld,
        EcoInformation,
        bool,
        Dict[str, Any],
    ]:
        timestep = self.state.timestep
        # Apply the step function to the environment
        (
            self.state,
            observations_agents,
            eco_information,
            done,
            info,
            self.aggregators_lifespan,
            self.aggregators_population,
        ) = self.step_jitted(
            key_random=key_random,
            state=self.state,
            actions=actions,
            aggregators_lifespan=self.aggregators_lifespan,
            aggregators_population=self.aggregators_population,
        )

        # Set metrics to numpy arrays for logging
        if timestep % self.period_logging == 0:
            info["metrics"] = {
                key: np.array(value) for key, value in info["metrics"].items()
            }
        else:
            info["metrics"] = {}

        # Return the information required by the agents
        return (
            observations_agents,
            eco_information,
            done,
            info,
        )

    @partial(jax.jit, static_argnums=(0,))
    def step_jitted(
        self,
        key_random: jnp.ndarray,
        state: StateEnvGridworld,
        actions: jnp.ndarray,
        aggregators_lifespan: List[Aggregator],
        aggregators_population: List[Aggregator],
    ) -> Tuple[
        StateEnvGridworld,
        ObservationAgentGridworld,
        EcoInformation,
        bool,
        Dict[str, Any],
        List[Aggregator],
        List[Aggregator],
    ]:
        """The jitted part of the step function, that takes constant-shaped inputs and outputs.

        Args:
            key_random (jnp.ndarray): the random key used to generate random numbers
            state (StateEnvGridworld): the state of the environment at timestep t
            actions (jnp.ndarray): the actions of the agents reacting to the environment at timestep t
            aggregators_lifespan (List[Aggregator]): the aggregators for the lifespan metrics at timestep t
            aggregators_population (List[Aggregator]): the aggregators for the population metrics at timestep t

        Returns:
            state_new (StateEnvGridworld): the new state of the environment at timestep t+1
            observations_agents (ObservationAgentGridworld): the observations of the agents at timestep t+1
            eco_information (EcoInformation): the ecological information of the environment regarding what happened at t. It should contain the following:
                1) are_newborns_agents (jnp.ndarray): a boolean array indicating which agents are newborns at this step
                2) indexes_parents_agents (jnp.ndarray): an array indicating the indexes of the parents of the newborns at this step
                3) are_dead_agents (jnp.ndarray): a boolean array indicating which agents are dead at this step (i.e. they were alive at t but not at t+1)
                    Note that an agent index could see its are_dead_agents value be False while its are_newborns_agents value is True, if the agent die and another agent is born at the same index
            done (bool): whether the environment is done
            dict_metrics (Dict[str, Any]): the metrics of the environment. It is attached to timestep t
            aggregators_lifespan (List[Aggregator]): the aggregators for the lifespan metrics at timestep t+1
            aggregators_population (List[Aggregator]): the aggregators for the population metrics at timestep t+1
        """

        # Initialize the measures dictionnary. This will be used to store the measures of the environment at this step.
        dict_measures_all: Dict[str, jnp.ndarray] = {}

        # ============ (1) Agents interaction with the environment ============
        # Apply the actions of the agents on the environment
        key_random, subkey = jax.random.split(key_random)
        state_new, dict_measures = self.step_action_agents(
            state=state, actions=actions, key_random=subkey
        )
        dict_measures_all.update(dict_measures)

        # ============ (2) Agents reproduce ============
        key_random, subkey = jax.random.split(key_random)
        state_new, are_newborns_agents, indexes_parents_agents, dict_measures = (
            self.step_reproduce_agents(
                state=state_new, actions=actions, key_random=subkey
            )
        )
        dict_measures_all.update(dict_measures)

        # ============ (3) Extract the observations of the agents (and some updates) ============

        # Make some last updates to the state
        map_agents_new = jnp.zeros(state_new.map.shape[:2])
        map_agents_new = map_agents_new.at[
            state_new.positions_agents[:, 0], state_new.positions_agents[:, 1]
        ].add(state_new.are_existing_agents)
        state_new: StateEnvGridworld = state_new.replace(
            map=state_new.map.at[:, :, self.dict_name_channel_to_idx["agents"]].set(
                map_agents_new
            )
        )
        # Extract the observations of the agents
        observations_agents, dict_measures = self.get_observations_agents(
            state=state_new
        )
        dict_measures_all.update(dict_measures)

        # Update the time
        state_new = state_new.replace(
            timestep=state_new.timestep + 1,
            age_agents=state_new.age_agents + 1,
        )

        # ============ (4) Get the ecological information ============
        are_just_dead_agents = state.are_existing_agents & (
            ~state_new.are_existing_agents | (state_new.age_agents < state.age_agents)
        )
        eco_information = EcoInformation(
            are_newborns_agents=are_newborns_agents,
            indexes_parents=indexes_parents_agents,
            are_just_dead_agents=are_just_dead_agents,
        )

        # ============ (5) Check if the environment is done ============
        if self.is_terminal:
            done = ~jnp.any(state_new.are_existing_agents)
        else:
            done = False

        # ============ (6) Compute the metrics ============

        # Compute some measures
        key_random, subkey = jax.random.split(key_random)
        dict_measures = self.compute_measures(
            state=state, actions=actions, state_new=state_new, key_random=subkey
        )
        dict_measures_all.update(dict_measures)

        # Set the measures to NaN for the agents that are not existing
        for name_measure, measures in dict_measures_all.items():
            if name_measure not in self.config["metrics"]["measures"]["environmental"]:
                dict_measures_all[name_measure] = jnp.where(
                    state.are_existing_agents,
                    measures,
                    jnp.nan,
                )

        # Aggregate the measures over the lifespan
        dict_metrics_lifespan = {}
        for agg in aggregators_lifespan:
            dict_metrics_lifespan.update(
                agg.aggregate(
                    dict_measures=dict_measures_all,
                    are_alive=state.are_existing_agents,
                    are_just_dead=are_just_dead_agents,
                    ages=state.age_agents,
                )
            )

        # Aggregate the measures over the population
        dict_metrics_population = {}
        for agg in aggregators_population:
            dict_metrics_population.update(
                agg.aggregate(
                    dict_measures=dict_metrics_lifespan,
                    are_alive=state.are_existing_agents,
                    are_just_dead=are_just_dead_agents,
                    ages=state.age_agents,
                )
            )

        # Get the final metrics
        dict_metrics = {
            **dict_measures_all,
            **dict_metrics_lifespan,
            **dict_metrics_population,
        }

        # Arrange metrics in right format
        for name_metric in list(dict_metrics.keys()):
            *names, name_measure = name_metric.split("/")
            if len(names) == 0:
                name_metric_new = name_measure
            else:
                name_metric_new = f"{name_measure}/{' '.join(names[::-1])}"
            dict_metrics[name_metric_new] = dict_metrics.pop(name_metric)
        info = {"metrics": dict_metrics}

        # Return the new state and observations
        return (
            state_new,
            observations_agents,
            eco_information,
            done,
            info,
            aggregators_lifespan,
            aggregators_population,
        )

    def get_observation_space_dict(self) -> Dict[str, EcojaxSpace]:
        return {
            "visual_field": Continuous(
                shape=(
                    2 * self.vision_range_agent + 1,
                    2 * self.vision_range_agent + 1,
                    self.n_channels_map,
                ),
                low=None,
                high=None,
            ),
            "energy": Continuous(shape=(), low=0, high=None),
            "age": Continuous(shape=(), low=0, high=None),
        }

    def get_action_space_dict(self) -> Dict[str, EcojaxSpace]:
        return {
            "direction": Discrete(n=4),
            "do_eat": Discrete(n=2),
        }

    def get_class_observation_agent(self) -> Type[ObservationAgent]:
        return ObservationAgentGridworld

    def get_class_action_agent(self) -> Type[ActionAgent]:
        return ActionAgentGridworld

    def render(self) -> None:
        """The rendering function of the environment. It saves the RGB map of the environment as a video."""
        if self.cfg_video["do_video"]:
            t = self.state.timestep
            if t % self.n_steps_between_videos == 0:
                self.video_writer = VideoRecorder(
                    filename=f"{self.dir_videos}/video_t{t}.mp4",
                    fps=self.fps_video,
                )
            t_current_video = (
                t - (t // self.n_steps_between_videos) * self.n_steps_between_videos
            )
            if (t_current_video < self.n_steps_per_video) and (
                t_current_video % self.n_steps_between_frames == 0
            ):
                self.video_writer.add(self.get_RGB_map(state=self.state))
            if t_current_video == self.n_steps_per_video - 1:
                self.video_writer.close()

    # ================== Helper functions ==================

    @partial(jax.jit, static_argnums=(0,))
    def get_RGB_map(self, state: StateEnvGridworld) -> Any:
        """A function for rendering the environment. It returns the RGB map of the environment.

        Args:
            state (StateEnvGridworld): the state of the environment

        Returns:
            Any: the RGB map of the environment
        """
        RGB_image_blended = self.blend_images(
            images=state.map,
            dict_idx_channel_to_color_tag=self.dict_idx_channel_to_color_tag,
        )
        H, W, C = RGB_image_blended.shape
        upscale_factor = min(self.height_max_video / H, self.width_max_video / W)
        upscale_factor = int(upscale_factor)
        assert upscale_factor >= 1, "The upscale factor must be at least 1"
        RGB_image_upscaled = jax.image.resize(
            RGB_image_blended,
            shape=(H * upscale_factor, W * upscale_factor, C),
            method="nearest",
        )
        return RGB_image_upscaled

    def blend_images(
        self, images: jnp.ndarray, dict_idx_channel_to_color_tag: Dict[int, tuple]
    ) -> jnp.ndarray:
        """Apply a color to each channel of a list of grey images and blend them together

        Args:
            images (np.ndarray): the array of grey images, of shape (height, width, channels)
            dict_idx_channel_to_color_tag (Dict[int, tuple]): a mapping from channel index to color tag.
                A color tag is a tuple of 3 floats between 0 and 1

        Returns:
            np.ndarray: the blended image, of shape (height, width, 3), with the color applied to each channel,
                with pixel values between 0 and 1
        """
        # Initialize an empty array to store the blended image
        blended_image = jnp.zeros(images.shape[:2] + (3,), dtype=jnp.float32)

        # Iterate over each channel and apply the corresponding color
        for channel_idx, color_tag in dict_idx_channel_to_color_tag.items():
            # Get the color components
            color = jnp.array(DICT_COLOR_TAG_TO_RGB[color_tag], dtype=jnp.float32)

            # Normalize the color components
            # color /= jnp.max(color)

            blended_image += color * images[:, :, channel_idx][:, :, None]

        # Clip the pixel values to be between 0 and 1
        blended_image = jnp.clip(blended_image, 0, 1)

        # Turn black pixels (value of 0 in the 3 channels) to "color_background" pixels
        tag_color_background = try_get(self.config, "color_background", default="gray")
        assert (
            tag_color_background in DICT_COLOR_TAG_TO_RGB
        ), f"Unknown color tag: {tag_color_background}"
        color_empty = DICT_COLOR_TAG_TO_RGB[tag_color_background]
        blended_image = jnp.where(
            jnp.sum(blended_image, axis=-1, keepdims=True) == 0,
            jnp.array(color_empty, dtype=jnp.float32) * jnp.ones_like(blended_image),
            blended_image,
        )

        return blended_image

    def step_grow_plants(
        self, state: StateEnvGridworld, key_random: jnp.ndarray
    ) -> jnp.ndarray:
        """Modify the state of the environment by growing the plants."""
        idx_sun = self.dict_name_channel_to_idx["sun"]
        idx_plants = self.dict_name_channel_to_idx["plants"]
        map_plants = state.map[:, :, self.dict_name_channel_to_idx["plants"]]
        map_n_plant_in_radius_plant_reproduction = convolve2d(
            map_plants,
            self.kernel_plant_reproduction,
            mode="same",
        )
        map_n_plant_in_radius_plant_asphyxia = convolve2d(
            map_plants,
            self.kernel_plant_asphyxia,
            mode="same",
        )
        map_sun = state.map[:, :, idx_sun]
        logits_plants = (
            self.logit_p_base_plant_growth * (1 - map_plants)
            + (1 - self.logit_p_base_plant_death) * map_plants
            + self.factor_sun_effect * map_sun
            + self.factor_plant_reproduction * map_n_plant_in_radius_plant_reproduction
            - self.factor_plant_asphyxia * map_n_plant_in_radius_plant_asphyxia
        )
        logits_plants = jnp.clip(logits_plants, -10, 10)
        map_plants_probs = sigmoid(x=logits_plants)
        key_random, subkey = jax.random.split(key_random)
        map_plants = jax.random.bernoulli(
            key=subkey,
            p=map_plants_probs,
            shape=map_plants.shape,
        )
        return state.replace(map=state.map.at[:, :, idx_plants].set(map_plants))

    def step_update_sun(
        self, state: StateEnvGridworld, key_random: jnp.ndarray
    ) -> StateEnvGridworld:
        """Modify the state of the environment by updating the sun.
        The method of updating the sun is defined by the attribute self.method_sun.
        """
        # Update the latitude of the sun depending on the method
        idx_sun = self.dict_name_channel_to_idx["sun"]
        H, W, C = state.map.shape
        if self.method_sun == "none":
            return state
        elif self.method_sun == "fixed":
            return state
        elif self.method_sun == "random":
            latitude_sun = jax.random.randint(
                key=key_random,
                minval=0,
                maxval=H,
                shape=(),
            )
        elif self.method_sun == "brownian":
            latitude_sun = state.latitude_sun + (
                jax.random.normal(
                    key=key_random,
                    shape=(),
                )
                * H
                / 2
                / jax.numpy.sqrt(self.period_sun)
            )
        elif self.method_sun == "sine":
            latitude_sun = H // 2 + H // 2 * jax.numpy.sin(
                2 * jax.numpy.pi * state.timestep / self.period_sun
            )
        elif self.method_sun == "linear":
            latitude_sun = H // 2 + H * state.timestep // self.period_sun
        else:
            raise ValueError(f"Unknown method_sun: {self.method_sun}")
        latitude_sun = jax.numpy.round(latitude_sun).astype(jnp.int32)
        latitude_sun = latitude_sun % H
        shift = latitude_sun - state.latitude_sun
        return state.replace(
            latitude_sun=latitude_sun,
            map=state.map.at[:, :, idx_sun].set(
                jnp.roll(state.map[:, :, idx_sun], shift, axis=0)
            ),
        )

    def get_single_agent_new_position_and_orientation(
        self,
        agent_position: jnp.ndarray,
        agent_orientation: jnp.ndarray,
        action: ActionAgentGridworld,
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Get the new position and orientation of a single agent.
        Args:
            agent_position (jnp.ndarray): the position of the agent, of shape (2,)
            agent_orientation (jnp.ndarray): the orientation of the agent, of shape ()
            action (ActionAgentGridworld): the action of the agent, as a ActionAgentGridworld of components of shape ()

        Returns:
            jnp.ndarray: the new position of the agent, of shape (2,)
            jnp.ndarray: the new orientation of the agent, of shape ()
        """
        # Compute the new position and orientation of the agent
        H, W, c = self.state.map.shape
        direction = action.direction
        agent_orientation_new = (agent_orientation + direction) % 4
        angle_new = agent_orientation_new * jnp.pi / 2
        d_position = jnp.array([jnp.cos(angle_new), -jnp.sin(angle_new)]).astype(
            jnp.int32
        )
        agent_position_new = agent_position + d_position
        agent_position_new = agent_position_new % jnp.array([H, W])

        # If agent is eating, it won't move
        do_eat = action.do_eat
        agent_position_new = jnp.where(do_eat, agent_position, agent_position_new)
        agent_orientation_new = jnp.where(
            do_eat, agent_orientation, agent_orientation_new
        )

        # Return the new position and orientation of the agent
        return agent_position_new, agent_orientation_new

    def step_action_agents(
        self,
        state: StateEnvGridworld,
        actions: ActionAgentGridworld,
        key_random: jnp.ndarray,
    ) -> Tuple[StateEnvGridworld, Dict[str, jnp.ndarray]]:
        """Modify the state of the environment by applying the actions of the agents."""

        H, W, C = state.map.shape
        idx_plants = self.dict_name_channel_to_idx["plants"]
        idx_agents = self.dict_name_channel_to_idx["agents"]
        map_plants = state.map[..., idx_plants]
        map_agents = state.map[..., idx_agents]
        dict_measures: Dict[str, jnp.ndarray] = {}

        # ====== Compute the new positions and orientations of all the agents ======
        get_many_agents_new_position_and_orientation = jax.vmap(
            self.get_single_agent_new_position_and_orientation, in_axes=(0, 0, 0)
        )
        positions_agents_new, orientation_agents_new = (
            get_many_agents_new_position_and_orientation(
                state.positions_agents,
                state.orientation_agents,
                actions,
            )
        )

        # ====== Perform the eating action of the agents ======
        map_agents_try_eating = (
            jnp.zeros_like(map_agents)
            .at[positions_agents_new[:, 0], positions_agents_new[:, 1]]
            .add(actions.do_eat & state.are_existing_agents)
        )  # map of the number of (existing) agents trying to eat at each cell

        map_food_energy_bonus_available_per_agent = (
            self.energy_food * map_plants / jnp.maximum(1, map_agents_try_eating)
        )  # map of the energy available at each cell per (existing) agent trying to eat
        food_energy_bonus = map_food_energy_bonus_available_per_agent[
            positions_agents_new[:, 0], positions_agents_new[:, 1]
        ]
        if "amount_food_eaten" in self.names_measures:
            dict_measures["amount_food_eaten"] = food_energy_bonus
        energy_agents_new = state.energy_agents + food_energy_bonus

        # Remove plants that have been eaten
        map_plants -= map_agents_try_eating * map_plants
        map_plants = jnp.clip(map_plants, 0, 1)

        # ====== Update the physical status of the agents ======
        energy_agents_new -= 1
        are_existing_agents_new = (
            (energy_agents_new > self.energy_thr_death)
            & state.are_existing_agents
            & (state.age_agents < self.age_max)
        )

        # Update the state
        state = state.replace(
            map=state.map.at[:, :, idx_plants].set(map_plants),
            positions_agents=positions_agents_new,
            orientation_agents=orientation_agents_new,
            energy_agents=energy_agents_new,
            are_existing_agents=are_existing_agents_new,
        )

        # Update the sun
        key_random, subkey = jax.random.split(key_random)
        state = self.step_update_sun(state=state, key_random=subkey)
        # Grow plants
        key_random, subkey = jax.random.split(key_random)
        state = self.step_grow_plants(state=state, key_random=subkey)

        # Return the new state, as well as some metrics
        return state, dict_measures

    def step_reproduce_agents(
        self,
        state: StateEnvGridworld,
        actions: ActionAgentGridworld,
        key_random: jnp.ndarray,
    ) -> Tuple[StateEnvGridworld, jnp.ndarray, jnp.ndarray]:
        """Reproduce the agents in the environment."""
        dict_measures = {}

        # Detect which agents are trying to reproduce
        are_existing_agents = state.are_existing_agents
        are_agents_trying_reprod = (
            state.energy_agents > self.energy_req_reprod
        ) & are_existing_agents
        if self.do_active_reprod:
            are_agents_trying_reprod &= actions.do_reproduce

        # # For test
        # are_existing_agents = jnp.array([False, False, False, False, True, True, True, True, True, False])
        # are_agents_trying_reprod = jnp.array([False, False, False, False, False, False, False, False, False, False])

        # Compute the number of newborns. If there are more agents trying to reproduce than there are ghost agents, only the first n_ghost_agents agents will be able to reproduce.
        n_agents_trying_reprod = jnp.sum(are_agents_trying_reprod)
        n_ghost_agents = jnp.sum(~are_existing_agents)
        n_newborns = jnp.minimum(n_agents_trying_reprod, n_ghost_agents)

        # Compute which agents are actually reproducing
        try_reprod_mask = are_agents_trying_reprod.astype(
            jnp.int32
        )  # 1_(agent i tries to reproduce) for i
        cumsum_repro_attempts = jnp.cumsum(
            try_reprod_mask
        )  # number of agents that tried to reproduce before agent i
        are_agents_reproducing = (
            cumsum_repro_attempts <= n_newborns
        ) & are_agents_trying_reprod  # whether i tried to reproduce and is allowed to reproduce

        if "amount_children" in self.names_measures:
            dict_measures["amount_children"] = are_agents_reproducing

        # Get the indices of the ghost agents. To have constant (n_max_agents,) shape, we fill the remaining indices with the value self.n_agents_max (which will have no effect as an index of (n_agents_max,) array)
        indices_ghost_agents_FILLED = jnp.where(
            ~are_existing_agents,
            size=self.n_agents_max,
            fill_value=self.fill_value,
        )[
            0
        ]  # placeholder_indices = [i1, i2, ..., i(n_ghost_agents), f, f, ..., f] of shape (n_max_agents,)

        # Get the indices of the ghost agents that will become newborns and define the newborns
        indices_newborn_agents_FILLED = jnp.where(
            jnp.arange(self.n_agents_max) < n_newborns,
            indices_ghost_agents_FILLED,
            self.n_agents_max,
        )  # placeholder_indices = [i1, i2, ..., i(n_newborns), f, f, ..., f] of shape (n_max_agents,), with n_newborns <= n_ghost_agents

        are_newborns_agents = (
            jnp.zeros(self.n_agents_max, dtype=jnp.bool_)
            .at[indices_newborn_agents_FILLED]
            .set(True)
        )  # whether agent i is a newborn

        # Get the indices of are_reproducing agents
        indices_had_reproduced_FILLED = jnp.where(
            are_agents_reproducing,
            size=self.n_agents_max,
            fill_value=self.fill_value,
        )[0]

        agents_parents = jnp.full(
            shape=(self.n_agents_max, 1), fill_value=self.fill_value, dtype=jnp.int32
        )
        agents_parents = agents_parents.at[indices_newborn_agents_FILLED].set(
            indices_had_reproduced_FILLED[:, None]
        )

        # Decrease the energy of the agents that are reproducing
        energy_agents_new = (
            state.energy_agents - are_agents_reproducing * self.energy_cost_reprod
        )

        # Initialize the newborn agents
        are_existing_agents_new = are_existing_agents | are_newborns_agents
        energy_agents_new = energy_agents_new.at[indices_newborn_agents_FILLED].set(
            self.energy_initial
        )
        age_agents_new = state.age_agents.at[indices_newborn_agents_FILLED].set(0)
        positions_agents_new = state.positions_agents.at[
            indices_newborn_agents_FILLED
        ].set(state.positions_agents[indices_had_reproduced_FILLED])

        # Update the state
        state = state.replace(
            energy_agents=energy_agents_new,
            are_existing_agents=are_existing_agents_new,
            age_agents=age_agents_new,
            positions_agents=positions_agents_new,
        )
        return (
            state,
            are_newborns_agents,
            agents_parents,
            dict_measures,
        )

    def get_observations_agents(
        self, state: StateEnvGridworld
    ) -> Tuple[ObservationAgentGridworld, Dict[str, jnp.ndarray]]:
        """Extract the observations of the agents from the state of the environment.

        Args:
            state (StateEnvGridworld): the state of the environment

        Returns:
            observation_agents (ObservationAgentGridworld): the observations of the agents
            dict_measures (Dict[str, jnp.ndarray]): a dictionary of the measures of the environment
        """

        def get_single_agent_visual_field(
            agent_position: jnp.ndarray,
            agent_orientation: jnp.ndarray,
        ) -> ObservationAgentGridworld:
            """Get the visual field of a single agent.

            Args:
                agent_position (jnp.ndarray): the position of the agent, of shape (2,)
                agent_orientation (jnp.ndarray): the orientation of the agent, of shape ()

            Returns:
                ObservationAgentGridworld: the observation of the agent
            """
            H, W, c = state.map.shape

            # Get the visual field of the agent
            visual_field_x = agent_position[0] + self.grid_indexes_vision_x
            visual_field_y = agent_position[1] + self.grid_indexes_vision_y
            vis_field = state.map[
                visual_field_x % H,
                visual_field_y % W,
            ]
            # Rotate the visual field according to the orientation of the agent
            vis_field = jnp.select(
                [
                    agent_orientation == 0,
                    agent_orientation == 1,
                    agent_orientation == 2,
                    agent_orientation == 3,
                ],
                [
                    vis_field,
                    jnp.rot90(vis_field, k=1, axes=(0, 1)),
                    jnp.rot90(vis_field, k=2, axes=(0, 1)),
                    jnp.rot90(vis_field, k=3, axes=(0, 1)),
                ],
            )
            # Return the visual field of the agent
            return vis_field

        # Vectorize the function to get the observation of many agents
        get_many_agents_visual_field = jax.vmap(
            get_single_agent_visual_field, in_axes=0
        )

        # Compute the observations of all the agents
        visual_field = get_many_agents_visual_field(
            state.positions_agents,
            state.orientation_agents,
        )

        # Create the observation of the agents
        observations = ObservationAgentGridworld(
            visual_field=visual_field,
            energy=state.energy_agents,
            age=state.age_agents,
        )

        dict_measures = {}

        # print(f"Map : {state.map[..., 0]}")
        # print(f"Agents positions : {state.positions_agents}")
        # print(f"Agents orientations : {state.orientation_agents}")
        # print(f"First agent obs : {observations.visual_field[0, ..., 2]}, shape : {observations.visual_field[0, ...].shape}")
        # raise ValueError("Stop")

        return observations, dict_measures

    def compute_measures(
        self,
        state: StateEnvGridworld,
        actions: ActionAgentGridworld,
        state_new: StateEnvGridworld,
        key_random: jnp.ndarray,
    ) -> Dict[str, jnp.ndarray]:
        """Get the measures of the environment.

        Args:
            state (StateEnvGridworld): the state of the environment
            actions (ActionAgentGridworld): the actions of the agents
            state_new (StateEnvGridworld): the new state of the environment
            key_random (jnp.ndarray): the random key

        Returns:
            Dict[str, jnp.ndarray]: a dictionary of the measures of the environment
        """
        dict_measures = {}
        idx_plants = self.dict_name_channel_to_idx["plants"]
        for name_measure in self.names_measures:
            # Environment measures
            if name_measure == "n_agents":
                measures = jnp.sum(state.are_existing_agents)
            elif name_measure == "n_plants":
                measures = jnp.sum(state.map[..., idx_plants])
            # Immediate measures
            elif name_measure == "do_action_eat":
                measures = actions.do_eat
            elif name_measure == "do_action_reproduce":
                raise NotImplementedError("Do action reproduce is not implemented yet")
            elif name_measure == "do_action_forward":
                measures = actions.direction == 0
            elif name_measure == "do_action_left":
                measures = actions.direction == 1
            elif name_measure == "do_action_right":
                measures = actions.direction == 3
            elif name_measure == "do_action_backward":
                measures = actions.direction == 2
            # State measures
            elif name_measure == "energy":
                measures = state.energy_agents
            elif name_measure == "age":
                measures = state.age_agents
            elif name_measure == "x":
                measures = state.positions_agents[:, 0]
            elif name_measure == "y":
                measures = state.positions_agents[:, 1]
            elif name_measure == "density_agents_observed":
                raise NotImplementedError(
                    "Density of agents observed is not implemented yet"
                )
            elif name_measure == "density_plants_observed":
                raise NotImplementedError(
                    "Density of plants observed is not implemented yet"
                )
            else:
                continue
            # Behavior measures
            pass

            dict_measures[name_measure] = measures

        # Return the dictionary of measures
        return dict_measures
