import numpy as np
from generator import FullFactorModel
from userState import UserState

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
        
        self.user_state = UserState.start
        self.user_state = UserState.init_completed
        
        self.model = FullFactorModel(count_of_parallel_experiments, count_of_factors, normalized_points, variant, False)
        
        main_results = self.model.y_vals
        self.user_state = UserState.main_experiment

        mean_var = self.model.points_mean_var()
        self.user_state = UserState.mean_var

        self.model.reproducibility_check(0.05)
        self.user_state = UserState.reproduciblility
        keys = ['cochrain', 'is_reproducible','reproducibility_var']
        res = self.model.get_results()
        reproducibility = {key: res.get(key, None) for key in keys}
        
        self.model.get_estimate_parameters()
        self.user_state = UserState.estimate_parametrs
        keys = ['model_params', 'model_params_var', 'student']
        res = self.model.get_results()
        estimate_parameters = {key: res.get(key, None) for key in keys}
        
        self.model.check_params_significance(0.05)
        self.user_state = UserState.sign_of_coefs
        keys = ['is_sign', 'sign_coef', 'student']
        res = self.model.get_results()
        sign = {key: res.get(key, None) for key in keys}

        df_model_adeq = self.model.df_adequacy()
        self.user_state = UserState.check_df_adequacy

        additional_experiment = None
        if df_model_adeq == 0:
            self.model.additional_experiment()
            self.user_state = UserState.additional_completed
            additional_experiment = self.model.y_vals[-1]
        
        self.model.adequacy_check(0.05)

        self.results = self.model.get_results()
        self.user_state += 1
        keys = ['fisher', 'is_additional_experiment_conducted', 'is_adequacy', 'adequcy_var']
        res = self.model.get_results()
        adequacy = {key: res.get(key, None) for key in keys}

        print('main_results', main_results, end='\n\n')
        print('mean_var', mean_var, end='\n\n')
        print('reproducibility', reproducibility, end='\n\n')
        print('estimate_parameters', estimate_parameters, end='\n\n')
        print('sign', sign, end='\n\n')
        print('df_model_adeq', df_model_adeq, end='\n\n')
        print('additional_experiment', additional_experiment, end='\n\n')
        print('adequacy', adequacy, end='\n\n')


if __name__ == "__main__":
    gapi = GeneratorApi(variant=FullFactorModel.variant_1)
    