import numpy as np
import scipy.stats
from statistics import *

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, count_of_factors):
        # b0 + b1 * x1 + b2 * x2 + b12 * x1 * x2 
        # TODO: chagne model to non parabaloid
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        # points = np.ones((2**count_of_factors, count_of_factors))
        # TODO: change to input
        points = np.array([
            [ 1,  1],
            [ 1, -1],
            [-1,  1],
            [-1, -1],
        ])

        self.count_of_parallel_experiments = count_of_parallel_experiments
        # TODO: generate model coefs
        self.b_coef = np.array([ 2.245, 8.585, 39.945, 180.077])
        
        self.coef = np.hstack((np.array([1]*4)[:, np.newaxis], points, (points[:,0] * points[:,1])[:, np.newaxis]))
        self.y_mean = (self.coef@self.b_coef)[:,np.newaxis]
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        self.y_vals += np.random.normal(0,1,self.y_vals.shape)
        
    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """
        self.y_mean = np.vstack((self.y_mean,[3]))
        y_vals = np.array([self.y_mean[-1] for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
        y_vals += np.random.normal(0,1, y_vals.shape)
        print(self.y_vals.shape, y_vals.shape)
        self.y_vals = np.vstack((self.y_vals, y_vals))

        print(self.y_vals.round(3))
    
    def points_mean_var(self):
        y_prac_mean = self.y_vals.mean(1)
        y_prac_var = ((self.y_vals - self.y_mean)**2).sum(1)/(self.count_of_parallel_experiments - 1)
        return y_prac_mean, y_prac_var

    def cochran_value(self, var):
        
        return var.max()/var.sum()


    def reproducibility_check(self):
        """
            Проверка воспроизводимости
            Тест Кохрена
        """
        # Среднее и дисперсия
        mean, var = self.points_mean_var()
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        prac_cochrain = self.cochran_value(var)
        prac_cochrain_crit = None
        numerator_val_cochran = self.count_of_parallel_experiments - 1
        denominator_val_cochran = self.y_mean.size
        K_cochrain_index, N_cochrain_index = None, None
        try:
            K_cochrain_index = cochrain_K.index(numerator_val_cochran)
            N_cochrain_index = cochrain_N.index(denominator_val_cochran)
        except ValueError as ex:
            print(ex)
        if K_cochrain_index is not None and N_cochrain_index is not None:
            prac_cochrain_crit = cochrain_critical_values[N_cochrain_index][K_cochrain_index]
            print('Оценка воспроизводимости критерием Кохрена')
            print('Оценка: ', round(prac_cochrain,4))
            print('Критическое значение: ', prac_cochrain_crit)
            if (prac_cochrain < prac_cochrain_crit):
                print('Воспроизводится')
            else:
                print('Не воспроизводится')
            
            print('Дисперсия ошибки (воспроизводимости эксперимента):', round(self.reproducibility_var,4))

    def significance_estimate_parameters(self):
        """
            Значимость оценок параметров. Критерий Стьюдента
        """        
        mean, var = self.points_mean_var()
        prac_model_coef = self.coef @ mean / self.count_of_points
        
        var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)
        print(round(var_params_of_model,4))

        # Наблюдаемое значение критерия Стьюдента =
        # асболютное значение коэф. / корень из дисперсии параметра модели var_params_of_model
        prac_student_test = np.abs(prac_model_coef)/np.sqrt(var_params_of_model)
        print(prac_student_test)

        student_df = self.count_of_points * (count_of_parallel_experiments - 1)
        crit_t_value_idx = None
        try:
            crit_t_value_idx = t_df.index(student_df)
        except ValueError as ex:
            print(ex)
        if crit_t_value_idx is not None:
            # > критерия == значимые
            crit_t_value = t_values_01[crit_t_value_idx]
            print('Проверка значимости оценок параметров критерием Стьдента')
            print(np.round(prac_model_coef, 4))
            print(np.round(prac_student_test, 4))
            is_significant = prac_student_test > crit_t_value
            self.count_of_significant_coef = is_significant.sum()
            print(is_significant)
            if np.logical_not(is_significant).any():
                print('Есть незначимый коэффициент')
            else:
                print('Все коэффициенты значимы')

            #TODO: удаление и перерасчет при необходимости
    def adequacy(self):
        """
            Адекватность. Критерий Фишера.
        """
        df_adequacy = self.count_of_points - self.count_of_significant_coef
        if df_adequacy == 0:
            print('Нужен дополнительный эксперимент')
            self.additional_experiment()
            
            # self.count_of_parallel_experiments = 

        # else:




if __name__ == '__main__':
    np.random.seed(0)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors)
    f.reproducibility_check()
    f.significance_estimate_parameters()
    f.adequacy()