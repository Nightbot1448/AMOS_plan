import numpy as np
import statistical_tests
import debug_output

class FullFactorModel:
    def variant_1(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 1
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 1
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 0.5

    def variant_2(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 10
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 1
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 1
    
    def variant_3(self):
        b_range = 10
        self.b_coef = np.random.rand(4)*b_range
        self.__cos_coef = 1
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 10
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 1
    
    def variant_4(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 1
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 0.5
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    def variant_5(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 100
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 0.7
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    def variant_6(self):
        b_range = 10
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 0.1
        self.__y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 1.2
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    def __check_sign(self):
        self.main_experiment()
        self.reproducibility_check()
        self.get_estimate_parameters()
        _, success, result,_ = self.significance_estimate_parameters()
        flag = success and self.significant_coef.sum() > 1
        if flag:
            self.drop_checked()
            return True
        else:
            self.__drop_all()
            return False

    def drop_checked(self):
        self.reproducibility_var = None
        self.adequacy_var = None
        self.prac_b_coef = None
        self.model_response = None
        self.var_params_of_model = None
        self.additional_experiment_conducted = False
        self.__results = {}

    def __drop_all(self):
        self.b_coef = None
        self.y_vals = None
        self.drop_checked()

    def __init__(self, count_of_parallel_experiments, count_of_factors, normalized_points, generate_variant, debug_print=False):
        self.__results = {}

        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        self.count_of_parallel_experiments = count_of_parallel_experiments
        
        self.additional_experiment_conducted = False
        self.debug_print = debug_print
        
        self.reproducibility_var = None
        self.adequacy_var = None
        self.var_params_of_model = None

        self.basis_function_values = np.hstack((
            np.array([1]*4)[:, np.newaxis],
            normalized_points,
            (normalized_points[:,0] * normalized_points[:,1])[:, np.newaxis]
        ))

        # TODO центрирование и нормирование 
        # points = np.ones((2**count_of_factors, count_of_factors))
        self.variant = generate_variant
        self.variant(self)
        while not self.__check_sign():
            self.variant(self)

        # self.object_model()
        # self.adequacy_check()
        
    def main_experiment(self):
        self.y_vals = np.hstack([self.__y_mean for _ in range(self.count_of_parallel_experiments)])
        noise = np.random.normal(0,self.__noise__main_1,(self.y_vals.shape[0]-1, self.y_vals.shape[1]))
        noise = np.vstack((noise, np.random.normal(0,self.__noise__main_2,(1, self.y_vals.shape[1]))))
        self.y_vals += noise

    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """
        if not self.additional_experiment_conducted:
            y_val = np.array([1, 0, 0, 0])@self.b_coef + self.__cos_coef*np.cos(0)
            y_vals = np.array([y_val for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
            y_vals += np.random.normal(0,self.__noise_additional, y_vals.shape)
            self.y_vals = np.vstack((self.y_vals, y_vals))
            
            # self.y_vals = np.vstack((self.y_vals, np.array([17.26,17.26,17.26])))
            
            self.additional_experiment_conducted = True
        else:
            print('Дополнительный эксперимент уже был проведен')
    
    def points_mean_var(self):
        y_prac_mean = self.y_vals.mean(1)
        y_prac_var = ((self.y_vals - y_prac_mean[:,np.newaxis])**2).sum(1)/(self.count_of_parallel_experiments - 1)
        return y_prac_mean, y_prac_var

    def cochran_value(self, var):
        return var.max()/var.sum()

    def student_values(self):
        return np.abs(self.prac_b_coef)/np.sqrt(self.var_params_of_model)

    def df_adequacy(self):
        return self.count_of_points - self.significant_coef.sum() \
            + self.additional_experiment_conducted
    
    def fisher_value(self):
        df_adequacy = self.df_adequacy()
        if self.adequacy_var is None:
            if df_adequacy == 0 and self.y_vals.shape[0] == self.count_of_points:
                self.additional_experiment()
            if self.additional_experiment_conducted:
                self.adequacy_var = self.count_of_parallel_experiments \
                    * (self.y_vals[-1].mean() - self.prac_b_coef[0])**2
            else:
                mean, _ = self.points_mean_var()
                self.adequacy_var = np.sum((self.model_response - mean)**2) * \
                    self.count_of_parallel_experiments/(self.count_of_points - self.significant_coef.sum())
        return self.adequacy_var/self.reproducibility_var

    def reproducibility_check(self, p_value=0.01):
        """
            Проверка воспроизводимости
            Тест Кохрена
        """
        # Среднее и дисперсия
        mean, var = self.points_mean_var()
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        df_numerator = self.count_of_parallel_experiments - 1
        df_denominator = self.count_of_points
        prac_cochrain_val = self.cochran_value(var)
        reproducible_success, reproducible_result, cochrain_critical_value = statistical_tests.cochrain_test(
            prac_cochrain_val, df_numerator, df_denominator, p_value
        )

        self.__results.update({
            'mean': mean,
            'var': var,
            'cochrain': {
                'prac_value': prac_cochrain_val,
                'df_numerator': df_numerator,
                'df_denominator': df_denominator,
                'crit_value': cochrain_critical_value,
            },
            'is_reproducible': reproducible_result,
            'reproducibility_var': self.reproducibility_var
        })

        if self.debug_print:
            debug_output.print_reproducibility_check(
                self, reproducible_success, reproducible_result, cochrain_critical_value
            )
        return reproducible_result
    
    def get_estimate_parameters(self):
        'Вычисление параметров модели'
        mean, var = self.points_mean_var()
        self.prac_b_coef = self.basis_function_values @ mean[:4] / self.count_of_points
        self.model_response = self.basis_function_values@self.prac_b_coef
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)
        
        self.__results.update({
            'model_params': self.prac_b_coef,
            'model_params_var': self.var_params_of_model,
            'student': {
                'model_response': self.model_response
                }
            })

    def significance_estimate_parameters(self, p_value=0.01):
        'Значимость оценок параметров. Критерий Стьюдента'        
        df = self.count_of_points * (self.count_of_parallel_experiments - 1)
        prac_student_test = self.student_values()
        student_test_success, student_test_result, student_crit = statistical_tests.student_test(
            prac_student_test, df, p_value
        )

        if student_test_success:
            self.significant_coef = student_test_result
        return df, student_test_success, prac_student_test, student_crit

    def update_b_coef(self):
        mean, _ = self.points_mean_var()
        self.prac_b_coef = self.basis_function_values[:,self.significant_coef] @ \
            mean[:4][self.significant_coef] / self.count_of_points

    def remove_insignificant_coefs(self):
        'Удаление незначимых коэффициентов'
        self.significant_b_coef = self.prac_b_coef[self.significant_coef]
        self.significant_points = self.basis_function_values[:, self.significant_coef]

    def update_model_response(self):
        'Обновление отклика модели после удаления незначимых коэффициентов'
        #ASK лучше чем что должно было получиться
        # TODO пересчитать коэффициенты B
        # TODO пересчитать по канону МНК
        # before = self.model_response.copy()

        self.model_response = self.significant_points@self.significant_b_coef
        # print('До удалениея незначимых:  ', np.round(before,3))
        # print('После удаления незначимых:', np.round(self.model_response,3))
        # print('Отклик модели без шума:   ', np.round(np.squeeze(self.__y_mean),3))
        # diff_before = np.squeeze(self.__y_mean)-before
        # diff_after = np.squeeze(self.__y_mean)-self.model_response
        # print('Разность до удаления:     ', np.round(diff_before,3), round(np.abs(diff_before).sum(),3))
        # print('Разность после удаления:  ', np.round(diff_after,3), round(np.abs(diff_after).sum(),3))

    def check_params_significance(self, p_value=0.01):
        df_student, student_test_success, prac_student_values, student_crit = \
            self.significance_estimate_parameters(p_value)
        
        if student_test_success:
            if np.logical_not(self.significant_coef).any():
                self.update_b_coef()
                self.remove_insignificant_coefs()
                self.update_model_response()

        if 'student' in self.__results.keys():
            self.__results['student'].update({
                'prac_value': self.student_values(),
                'df': df_student,
                'crit_value': student_crit,
            })
        else:
            self.__results.update({'student': {
                'prac_value': self.student_values(),
                'df': df_student,
                'crit_value': student_crit,
            }})
        self.__results.update({
            'is_sign': self.significant_coef,
            'sign_coef': self.significant_b_coef \
                if np.logical_not(self.significant_coef).any() \
                else self.prac_b_coef
        })

        return student_test_success, student_crit

    def object_model(self):
        self.get_estimate_parameters()
        student_test_success, student_crit = self.check_params_significance()

        if self.debug_print:
            debug_output.print_object_model(self, student_test_success, student_crit)
        return not np.logical_not(self.significant_coef).any()

    def adequacy_check(self, p_value = 0.01):
        'Адекватность. Критерий Фишера.'
        prac_fisher_test = self.fisher_value()

        df_numerator = self.count_of_points - self.significant_coef.sum()\
             + self.additional_experiment_conducted
        df_denominator = self.count_of_points * (self.count_of_parallel_experiments - 1)
        fisher_test_success, fisher_test_result, fisher_crit_value = \
            statistical_tests.fisher_test(prac_fisher_test, df_numerator, df_denominator, p_value)
        self.__results.update({
            'fisher': {
                'model_response': self.model_response,
                'prac_value': prac_fisher_test,
                'df_numerator': df_numerator,
                'df_denominator': df_denominator,
                'crit_value': fisher_crit_value,
            },
            'is_additional_experiment_conducted': self.additional_experiment_conducted,
            'is_adequacy': fisher_test_result,
            'adequcy_var': self.adequacy_var
        })

        if self.debug_print:
            debug_output.print_adequacy_check(
                self, fisher_test_success, fisher_test_result, fisher_crit_value
            )
        return fisher_test_result
    
    def get_results(self):
        return self.__results

if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    count_of_parallel_experiments = 3
    counts_of_factors = 2

    normalized_points = np.array([
        [ 1,  1],
        [-1,  1],
        [ 1, -1],
        [-1, -1],
    ])

    variant = FullFactorModel.variant_1

    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors, normalized_points, variant, False)

    f.drop_checked()
    f.y_vals = np.array([
        [ 119.28,  117.95,  141.81],
        [-187.31, -187.31, -187.31],
        [  32.69,   17.53,   17.53],
        [ -12.47,  -12.47,  -12.47]
    ])

    f.points_mean_var()
    f.reproducibility_check(0.05)
    f.get_results()
    f.get_estimate_parameters()
    f.get_results()
    f.check_params_significance(0.05)
    f.get_results()
    if f.df_adequacy() == 0:
        f.additional_experiment()
    f.adequacy_check(0.05)
    print(f.get_results())
