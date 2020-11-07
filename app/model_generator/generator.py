import numpy as np
import statistical_tests
import debug_output

class FullFactorModel:
    def variant_1(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 1
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 1
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 0.5

    def variant_2(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 10
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 1
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 1
    
    def variant_3(self):
        b_range = 10
        self.b_coef = np.random.rand(4)*b_range
        self.__cos_coef = 1
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 10
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 1
    
    # 4

    def variant_5(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 1
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 0.5
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    def variant_6(self):
        b_range = 1000
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 100
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 0.7
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    def variant_7(self):
        b_range = 10
        self.b_coef = np.random.rand(4)*b_range-b_range/2
        self.__cos_coef = 0.1
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 0.7
        self.__noise__main_2 = self.__noise__main_1 * 10
        self.__noise_additional = self.__noise__main_1 * 1

    # 8


    # repr: __noise__main_2 / __noise__main_1
    # sign: __noise__main_1 & b_range
    # adeq: __cos_coef & __noise__main

    def variant_X(self):
        b_range = 10
        self.b_coef = np.random.rand(4)*b_range
        self.__cos_coef = 1
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + self.__cos_coef*np.cos(self.basis_function_values[:,-1])[:,np.newaxis]
        self.__noise__main_1 = 10
        self.__noise__main_2 = self.__noise__main_1 * 1
        self.__noise_additional = self.__noise__main_1 * 1


    def __init__(self, count_of_parallel_experiments, count_of_factors, normalized_points, generate_variant, debug_print=False):
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        self.count_of_parallel_experiments = count_of_parallel_experiments
        
        self.additional_experiment_experiment_conducted = False
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

        # TODO поменять на зависимость от варианта
        generate_variant(self)
        
    def main_experiment(self):
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        noise = np.random.normal(0,self.__noise__main_1,(self.y_vals.shape[0]-1, self.y_vals.shape[1]))
        noise = np.vstack((noise, np.random.normal(0,self.__noise__main_2,(1, self.y_vals.shape[1]))))
        self.y_vals += noise

    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """
        #TODO заменить на рассчет по модели
        y_val = np.array([1, 0, 0, 0])@self.b_coef + self.__cos_coef*np.cos(0)
        y_vals = np.array([y_val for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
        y_vals += np.random.normal(0,self.__noise_additional, y_vals.shape)
        self.y_vals = np.vstack((self.y_vals, y_vals))
    
    def points_mean_var(self):
        y_prac_mean = self.y_vals.mean(1)
        y_prac_var = ((self.y_vals - y_prac_mean[:,np.newaxis])**2).sum(1)/(self.count_of_parallel_experiments - 1)
        return y_prac_mean, y_prac_var

    def cochran_value(self, var):
        return var.max()/var.sum()

    def student_values(self):
        return np.abs(self.prac_b_coef)/np.sqrt(self.var_params_of_model)

    def fisher_value(self):
        df_adequacy = self.count_of_points - self.significant_coef.sum() \
            + self.additional_experiment_experiment_conducted
        if self.adequacy_var is None:
            if df_adequacy == 0:
                if self.y_vals.shape[0] == self.count_of_points:
                    self.additional_experiment()
                    self.additional_experiment_experiment_conducted = True
                self.adequacy_var = self.count_of_parallel_experiments \
                    * (self.y_vals[-1].mean() - self.prac_b_coef[0])**2
            else:
                mean, _ = self.points_mean_var()
                self.adequacy_var = np.sum((self.model_response - mean)**2) * \
                    self.count_of_parallel_experiments/(self.count_of_points - self.significant_coef.sum())
        return self.adequacy_var/self.reproducibility_var

    def reproducibility_check(self):
        """
            Проверка воспроизводимости
            Тест Кохрена
        """
        # Среднее и дисперсия
        _, var = self.points_mean_var()
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        df_numerator = self.count_of_parallel_experiments - 1
        df_denominator = self.count_of_points
        prac_cochrain_val = self.cochran_value(var)
        reproducible_success, reproducible_result, cochrain_critical_value = statistical_tests.cochrain_test(
            prac_cochrain_val, df_numerator, df_denominator, 0.01
        )
        if self.debug_print:
            debug_output.print_reproducibility_check(
                self, reproducible_success, reproducible_result, cochrain_critical_value
            )
        return reproducible_result
    
    def get_estimate_parameters(self):
        'Вычисление параметорв модели'
        mean, var = self.points_mean_var()
        self.prac_b_coef = self.basis_function_values @ mean[:4] / self.count_of_points
        self.model_response = self.basis_function_values@self.prac_b_coef
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)

    def significance_estimate_parameters(self):
        'Значимость оценок параметров. Критерий Стьюдента'        
        df = self.count_of_points * (self.count_of_parallel_experiments - 1)
        prac_student_test = self.student_values()
        student_test_success, student_test_result, student_crit = statistical_tests.student_test(
            prac_student_test, df, 0.01
        )

        if student_test_success:
            self.significant_coef = student_test_result
        return df, student_test_success, prac_student_test, student_crit

    def remove_insignificant_coefs(self):
        'Удаление незначимых коэффициентов'
        self.significant_b_coef = self.prac_b_coef[self.significant_coef]
        self.significant_points = self.basis_function_values[:, self.significant_coef]

    def update_model_response(self):
        'Обновление отклика модели после удаления незначимых коэффициентов'
        #ASK лучше чем что должно было получиться
        # before = self.model_response.copy()
        self.model_response = self.significant_points@self.significant_b_coef
        # print('До удалениея незначимых:  ', np.round(before,3))
        # print('После удаления незначимых:', np.round(self.model_response,3))
        # print('Отклик модели без шума:   ', np.round(np.squeeze(self.y_mean),3))
        # diff_before = np.squeeze(self.y_mean)-before
        # diff_after = np.squeeze(self.y_mean)-self.model_response
        # print('Разность до удаления:     ', np.round(diff_before,3), round(np.abs(diff_before).sum(),3))
        # print('Разность после удаления:  ', np.round(diff_after,3), round(np.abs(diff_after).sum(),3))

    def object_model(self):
        self.get_estimate_parameters()
        df_student, student_test_success, prac_student_values, student_crit = \
            self.significance_estimate_parameters()
        
        if student_test_success:
            if np.logical_not(self.significant_coef).any():
                self.remove_insignificant_coefs()
                self.update_model_response()

        if self.debug_print:
            debug_output.print_object_model(self, student_test_success, student_crit)
        return not np.logical_not(self.significant_coef).any()

    def adequacy_check(self):
        'Адекватность. Критерий Фишера.'
        prac_fisher_test = self.fisher_value()

        df_numerator = self.count_of_points - self.significant_coef.sum()\
             + self.additional_experiment_experiment_conducted
        df_denominator = self.count_of_points * (self.count_of_parallel_experiments - 1)
        fisher_test_success, fisher_test_result, fisher_crit_value = \
            statistical_tests.fisher_test(prac_fisher_test, df_numerator, df_denominator, 0.01)
        if self.debug_print:
            debug_output.print_adequacy_check(
                self, fisher_test_success, fisher_test_result, fisher_crit_value
            )
        return fisher_test_result

if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    normalized_points = np.array([
        [ 1,  1],
        [-1,  1],
        [ 1, -1],
        [-1, -1],
    ])
    stat = True
    variant = FullFactorModel.variant_X
    if stat:
        repr_res, sign_res, adeq_res, res = [], [], [], []
        sz = 1000
        for _ in range(sz):
            f = FullFactorModel(count_of_parallel_experiments, counts_of_factors, normalized_points, variant)
            f.main_experiment()
            repr_ = f.reproducibility_check()
            sign_ = f.object_model()
            adeq_ = f.adequacy_check()
            repr_res.append(repr_)
            sign_res.append(sign_)
            adeq_res.append(adeq_)
            res.append((repr_, sign_, adeq_) == (True, False, True))
        
        print('Repr', np.sum(repr_res)/sz)
        print('Sign', np.sum(sign_res)/sz)
        print('Adeq', np.sum(adeq_res)/sz)
        print('Res ', np.sum(res)/sz)
        
    else:
        f = FullFactorModel(count_of_parallel_experiments, counts_of_factors, normalized_points, variant)
        f.main_experiment()
        print(np.round(f.y_vals,3))
        print(f.y_vals.mean(1))
        print(f.reproducibility_check())
        print(f.object_model())
        print(f.adequacy_check())
