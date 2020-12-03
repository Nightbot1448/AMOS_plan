from dataclasses import dataclass
from model_generator.generator import FullFactorModel
import numpy as np


@dataclass
class APIUser:
    task: str = None
    factor_number: int = 2
    planning_area: list = None
    plan_points_number: int = None
    plan_points: np.array = None
    experiments_number: int = None
    model: FullFactorModel = None
    factor_point_index: int = -1
