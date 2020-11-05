import numpy as np
import statistical_tests

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, count_of_factors):
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        self.additional_experiment_experiment_conducted = False
        # points = np.ones((2**count_of_factors, count_of_factors))
        
        # TODO центрирование и нормирование 
        normalized_points = np.array([
            [ 1,  1],
            [ 1, -1],
            [-1,  1],
            [-1, -1],
        ])

        self.count_of_parallel_experiments = count_of_parallel_experiments
        # TODO поменять на незалоченные значения (?)
        self.b_coef = np.random.rand(4)*500-250
        self.model_coef = np.hstack((
            np.array([1]*4)[:, np.newaxis],
            normalized_points,
            (normalized_points[:,0] * normalized_points[:,1])[:, np.newaxis]
        ))

        
        # b0 + b1 * x1 + b2 * x2 + b12 * x1 * x2 ##1 + cos(x1*x2)
        # TODO change model to non parabaloid
        self.y_mean = (self.model_coef@self.b_coef)[:,np.newaxis] \
             + np.cos(self.model_coef[:,-1])[:,np.newaxis] + np.sin(self.model_coef[:,-1])[:,np.newaxis]
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        noise = np.random.normal(0,10,(self.y_vals.shape[0]-1, self.y_vals.shape[1]))
        noise = np.vstack((noise, np.random.normal(0,30,(1, self.y_vals.shape[1]))))
        # print('noise:')
        # print(np.round(noise,3))
        self.y_vals += noise
        
    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """

        #TODO заменить на рассчет по модели 
        y_vals = np.array([self.b_coef[0] for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
        y_vals += np.random.normal(0,30, y_vals.shape)
        self.y_vals = np.vstack((self.y_vals, y_vals))

        # print(self.y_vals.round(3))
    
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

        if df_adequacy == 0:
            if self.y_vals.shape[0] == self.count_of_points:
                self.additional_experiment()
                self.additional_experiment_experiment_conducted = True
            self.adequacy_var = self.count_of_parallel_experiments * (self.y_vals[-1].mean() - self.prac_b_coef[0])**2
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
        print('--------------------------------------------------------------')
        # Среднее и дисперсия
        mean, var = self.points_mean_var()
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        df_numerator = self.count_of_parallel_experiments - 1
        df_denominator = self.count_of_points
        reproducible_success, reproducible_result = statistical_tests.cochrain_test(
            self.cochran_value(var), 
            df_numerator,
            df_denominator,
            0.01
        )
        if reproducible_success:
            print('Эксперимент{} воспроизводим'.format('' if reproducible_result else ' не'))
            
        print('Дисперсия ошибки (воспроизводимости) эксперимента:', round(self.reproducibility_var,4))
    
    def get_estimate_parameters(self):
        'Вычисление параметорв модели'
        mean, var = self.points_mean_var()
        self.prac_b_coef = self.model_coef @ mean / self.count_of_points
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)
        print('Дисперсия параметра модели:', np.round(self.var_params_of_model,4))

    def remove_insignificant_coefs(self):
        'Удаление незначимых коэффициентов'
        self.significant_b_coef = self.prac_b_coef[self.significant_coef]
        self.significant_points = self.model_coef[:, self.significant_coef]
        print('Значимые коэффициенты:', np.round(self.significant_b_coef,3))

    def update_model_response(self):
        'Обновление отклика модели после удаления незначимых коэффициентов'
        
        self.model_response = self.significant_points@self.significant_b_coef
        old_res = self.model_coef@self.prac_b_coef
        mean, var = self.points_mean_var()
        #ASK лучше чем что должно было получиться
        # print('update_model_response')
        # print('До удалениея незначимых:                     ', np.round(old_res.reshape(-1),3))
        # print('После удаления незначимых:                   ', np.round(self.model_response.reshape(-1),3))
        # print('Средние значения оклика                      ', np.round(mean,3))
        # print('Сгенерированные коэфициенты значения оклика: ', np.round(np.squeeze(self.y_mean),3))

    def significance_estimate_parameters(self):
        """
            Значимость оценок параметров. Критерий Стьюдента
        """
        print('--------------------------------------------------------------')
        self.get_estimate_parameters()
        df = self.count_of_points * (self.count_of_parallel_experiments - 1)
        prac_student_test = self.student_values()
        student_test_success, student_test_result = statistical_tests.student_test(
            prac_student_test, df, 0.01
        )

        if student_test_success:
            self.significant_coef = student_test_result
            if np.logical_not(self.significant_coef).any():
                print('Есть незначимые коэффициенты.')
                #ASK перерасчет при необходимости (?)
                self.remove_insignificant_coefs()
                self.update_model_response()
            else:
                print('Все коэффициенты значимы')

    def adequacy_check(self):
        print('--------------------------------------------------------------')
        """
            Адекватность. Критерий Фишера.
        """
        self.prac_fisher_test = self.fisher_value()
        print('Дисперсия адекватности:', round(self.adequacy_var,3))

        df_enumerator = self.count_of_points - self.significant_coef.sum()\
             + self.additional_experiment_experiment_conducted
        df_denominator = self.count_of_points * (self.count_of_parallel_experiments - 1)
        fisher_test_success, fisher_test_result = \
            statistical_tests.fisher_test(self.prac_fisher_test, df_enumerator, df_denominator, 0.01)

        if fisher_test_success:
            print('Модель{} адекватна'.format('' if fisher_test_result else ' не'))


if __name__ == '__main__':
    # np.random.seed(0)
    # np.set_printoptions(suppress=True)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors)
    
    f.reproducibility_check()
    f.significance_estimate_parameters()
    f.adequacy_check()
