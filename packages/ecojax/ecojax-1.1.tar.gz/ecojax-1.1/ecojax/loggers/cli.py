from ecojax.loggers import BaseLogger

from tensorboardX import SummaryWriter
from typing import Dict, List, Tuple, Type, Union


class LoggerCLI(BaseLogger):

    def log_scalars(
        self,
        dict_scalars: Dict[str, float],
        timestep: int,
    ):
        print(f"Step {timestep} : {dict_scalars}")

    def log_histograms(
        self,
        *args,
        **kwargs,
    ) -> None:
        pass
    
    def close(self):
        pass
