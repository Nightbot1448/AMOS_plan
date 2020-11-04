import numpy as np
import scipy.stats
from statistics import *
import statistical_tests

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, count_of_factors):
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
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
        self.y_mean = (self.model_coef@self.b_coef)[:,np.newaxis] #\
            # + np.cos(self.model_coef[:,-1])[:,np.newaxis] + np.sin(self.model_coef[:,-1])[:,np.newaxis]
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
        df_adequacy = self.count_of_points - self.significant_coef.sum()

        if df_adequacy == 0:
            if self.y_vals.shape[0] == self.count_of_points:
                self.additional_experiment()
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
        # Среднее и дисперсия
        mean, var = self.points_mean_var()
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        is_reproducible = statistical_tests.cochrain_test(
            self.cochran_value(var), 
            self.count_of_parallel_experiments,
            self.count_of_points
        )
            
        print('Дисперсия ошибки (воспроизводимости эксперимента):', round(self.reproducibility_var,4))
    
    def get_estimate_parameters(self):
        mean, var = self.points_mean_var()
        self.prac_b_coef = self.model_coef @ mean / self.count_of_points
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)
        print('Дисперсия параметра модели:', np.round(self.var_params_of_model,4))

    def remove_insignificant_coefs(self):
        self.significant_b_coef = self.prac_b_coef[self.significant_coef]
        self.significant_points = self.model_coef[:, self.significant_coef]
        print('Значимые коэффициенты:', self.significant_b_coef)
        # print(self.significant_b_coef)
    
# 225.74600
# 226.96600

    def update_model_response(self):
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
        self.get_estimate_parameters()
        # Наблюдаемое значение критерия Стьюдента =
        # асболютное значение коэф. / корень из дисперсии параметра модели var_params_of_model
        prac_student_test = self.student_values()
        student_test_success, student_test_result = statistical_tests.student_test(
            prac_student_test,
            self.count_of_parallel_experiments,
            self.count_of_points
        )

        if student_test_success:
            self.significant_coef = student_test_result
            if np.logical_not(self.significant_coef).any():
                print('Есть незначимые коэффициенты. Надо удалить')
                #ASK перерасчет при необходимости (?)
                self.remove_insignificant_coefs()
                self.update_model_response()
            else:
                print('Все коэффициенты значимы')

    

    def adequacy_check(self):
        """
            Адекватность. Критерий Фишера.
        """
        self.prac_fisher_test = self.fisher_value()
        print('Дисперсия адекватности:', self.adequacy_var)

        df_adequacy = self.count_of_points - self.significant_coef.sum()
        fisher_test_success, fisher_test_result = statistical_tests.fisher_test(self.prac_fisher_test, df_adequacy)


if __name__ == '__main__':
    # np.random.seed(0)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors)
    
    f.reproducibility_check()
    f.significance_estimate_parameters()
    f.adequacy_check()

