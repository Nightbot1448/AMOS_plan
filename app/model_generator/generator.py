import numpy as np
import statistical_tests
import debug_output

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, count_of_factors, normalized_points):
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        self.additional_experiment_experiment_conducted = False
        
        # TODO центрирование и нормирование точек
        
        self.count_of_parallel_experiments = count_of_parallel_experiments
        # TODO поменять на зависимость от варианта
        self.b_coef = np.random.rand(4)*500-250 
        self.basis_function_values = np.hstack((
            np.array([1]*4)[:, np.newaxis],
            normalized_points,
            (normalized_points[:,0] * normalized_points[:,1])[:, np.newaxis]
        ))
        
        self.reproducibility_var = None
        self.adequacy_var = None
        self.var_params_of_model = None

    
    def main_experiment(self):
        # b0 + b1 * x1 + b2 * x2 + b12 * x1 * x2 + cos(x1*x2) + sin(x1*x2)
        # TODO change model to non parabaloid
        self.y_mean = (self.basis_function_values@self.b_coef)[:,np.newaxis] \
             + np.cos(self.basis_function_values[:,-1])[:,np.newaxis] + np.sin(self.basis_function_values[:,-1])[:,np.newaxis]
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        noise = np.random.normal(0,10,(self.y_vals.shape[0]-1, self.y_vals.shape[1]))
        noise = np.vstack((noise, np.random.normal(0,30,(1, self.y_vals.shape[1]))))
        self.y_vals += noise

    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """

        #TODO заменить на рассчет по модели 
        # y_vals = np.array([self.b_coef[0] for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
        # y_vals += np.random.normal(0,30, y_vals.shape)
        y_vals = np.array([0.93, 0.93, 0.93, 0.93, 0.93])
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
            prac_cochrain_val, 
            df_numerator,
            df_denominator,
            0.01
        )
        debug_output.print_reproducibility_check(
            self, reproducible_success, reproducible_result, cochrain_critical_value
        )
    
    def get_estimate_parameters(self):
        'Вычисление параметорв модели'
        mean, var = self.points_mean_var()
        self.prac_b_coef = self.basis_function_values @ mean[:4] / self.count_of_points
        self.model_response = self.basis_function_values@self.prac_b_coef
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)

    def remove_insignificant_coefs(self):
        'Удаление незначимых коэффициентов'
        self.significant_b_coef = self.prac_b_coef[self.significant_coef]
        self.significant_points = self.basis_function_values[:, self.significant_coef]

    def update_model_response(self):
        'Обновление отклика модели после удаления незначимых коэффициентов'
        
        self.model_response = self.significant_points@self.significant_b_coef
        old_res = self.basis_function_values@self.prac_b_coef
        mean, var = self.points_mean_var()
        #ASK лучше чем что должно было получиться
        # print('update_model_response')
        # print('До удалениея незначимых:                     ', np.round(old_res.reshape(-1),3))
        # print('После удаления незначимых:                   ', np.round(self.model_response.reshape(-1),3))
        # print('Средние значения оклика:                     ', np.round(mean,3))
        # print('Сгенерированные коэфициенты значения оклика: ', np.round(np.squeeze(self.y_mean),3))
        # print('diff: ', mean-old_res.reshape(-1))
        
    def object_model(self):
        self.get_estimate_parameters()
        df_student, student_test_success, prac_student_values, student_crit = \
            self.significance_estimate_parameters()
        
        if student_test_success:
            if np.logical_not(self.significant_coef).any():
                self.remove_insignificant_coefs()
                self.update_model_response()
        debug_output.print_object_model(self, student_test_success, student_crit)

    def significance_estimate_parameters(self):
        """
            Значимость оценок параметров. Критерий Стьюдента
        """
        df = self.count_of_points * (self.count_of_parallel_experiments - 1)
        prac_student_test = self.student_values()
        student_test_success, student_test_result, student_crit = statistical_tests.student_test(
            prac_student_test, df, 0.01
        )

        if student_test_success:
            self.significant_coef = student_test_result
        return df, student_test_success, prac_student_test, student_crit

    def adequacy_check(self):
        """
            Адекватность. Критерий Фишера.
        """
        prac_fisher_test = self.fisher_value()

        df_enumerator = self.count_of_points - self.significant_coef.sum()\
             + self.additional_experiment_experiment_conducted
        df_denominator = self.count_of_points * (self.count_of_parallel_experiments - 1)
        fisher_test_success, fisher_test_result, fisher_crit_value = \
            statistical_tests.fisher_test(prac_fisher_test, df_enumerator, df_denominator, 0.01)

        debug_output.print_adequacy_check(
            self, fisher_test_success, fisher_test_result, fisher_crit_value
        )


if __name__ == '__main__':
    # np.random.seed(0)
    np.set_printoptions(suppress=True)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    normalized_points = np.array([
        [ 1,  1],
        [-1,  1],
        [ 1, -1],
        [-1, -1],
    ])
    
    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors, normalized_points)

    f.main_experiment()
    
    f.reproducibility_check()
    f.object_model()
    f.adequacy_check()
