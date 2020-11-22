import numpy as np
from generator import FullFactorModel

default_normalized_points = np.array([
        [ 1,  1],
        [-1,  1],
        [ 1, -1],
        [-1, -1],
    ])

class GeneratorApi():
    def __init__(self, count_of_parallel_experiments = 5,\
        count_of_factors = 2, normalized_points = default_normalized_points,\
        variant = FullFactorModel.variant_1, debug_print=False):
    
        np.set_printoptions(suppress=True)
        # np.random.seed(0)
        self.model = FullFactorModel(count_of_parallel_experiments, count_of_factors, normalized_points, variant, False)

        # f.additional_experiment_conducted = False
        # f.adequacy_var = None
        # f.y_vals = np.array([
        #     [99.21, 137.20, 115.62, 97.58, 97.58],
        #     [-342.42,-342.42,-325.05,-325.05,-325.05],
        #     [-105.05,-105.05,-105.05,-94.26,-94.26],
        #     [265.74,265.74,265.74,265.74,238.11]
        # ])

        self.model.reproducibility_check()
        self.model.object_model()
        self.model.adequacy_check()

        self.results = self.model.get_results()

if __name__ == "__main__":
    gapi = GeneratorApi()
    print(gapi.model.get_results())
    