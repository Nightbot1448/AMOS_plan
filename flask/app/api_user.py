from dataclasses import dataclass
from model_generator.generator import FullFactorModel
from model_generator.userState import UserState
import numpy as np


@dataclass
class APIUser:
    state: UserState = UserState.start
    task: str = None
    factor_number: int = 2
    planning_area: list = None
    plan_points_number: int = None
    plan_points: np.array = None
    experiments_number: int = None
    model: FullFactorModel = None
    factor_point_index: int = 0
    means_vars: int = 0  # dict
    reproduce_res: int = 0  # dict
    cochrain_significance: float = None
    cochrain_status: int = 0
    model_params: int = None  # dict

    def reset(self):
        self.state = UserState.start
        self.task = None
        self.factor_number  = 2
        self.planning_area  = None
        self.plan_points_number = None
        self.plan_points = None
        self.experiments_number = None
        self.model = None
        self.factor_point_index = 0
        self.means_vars = {}
        self.reproduce_res = {}
        self.cochrain_significance = None
        self.cochrain_status = None
        self.model_params = {}

    def set_state(self, state): self.state = state
