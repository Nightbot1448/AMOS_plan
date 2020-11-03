import numpy as np
import scipy.stats
from statistics import *

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, count_of_factors):
        # b0 + b1 * x1 + b2 * x2 + b12 * x1 * x2 ##1 + cos(x1*x2)
        # TODO change model to non parabaloid
        self.count_of_factors = count_of_factors
        self.count_of_points = 2**count_of_factors
        # points = np.ones((2**count_of_factors, count_of_factors))
        
        # TODO центрирование и нормирование 
        # TODO change to input
        points = np.array([
            [ 1,  1],
            [ 1, -1],
            [-1,  1],
            [-1, -1],
        ])

        self.count_of_parallel_experiments = count_of_parallel_experiments
        # TODO поменять на незалоченные значения (?)
        self.b_coef = np.random.rand(4)*500-250

        
        self.coef = np.hstack((np.array([1]*4)[:, np.newaxis], points, (points[:,0] * points[:,1])[:, np.newaxis]))
        self.y_mean = (self.coef@self.b_coef)[:,np.newaxis]# + np.cos(self.coef[:,-1])[:,np.newaxis] + np.sin(self.coef[:,-1])[:,np.newaxis]
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        noise = np.random.normal(0,10,(self.y_vals.shape[0]-1, self.y_vals.shape[1]))
        noise = np.vstack((noise, np.random.normal(0,30,(1, self.y_vals.shape[1]))))
        print('noise:')
        print(np.round(noise,3))
        self.y_vals += noise
        
    def additional_experiment(self):
        """
            Дополнительный эксперимент. 
            Проводится по центральной точке
        """

        # --------------------------------------------------
        self.y_mean = np.vstack((self.y_mean,[self.b_coef[0]]))
        # --------------------------------------------------
        y_vals = np.array([self.y_mean[-1] for _ in range(self.count_of_parallel_experiments)]).reshape(1,-1)
        y_vals += np.random.normal(0,1, y_vals.shape)
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
        # print(mean)
        # print(var)
        self.reproducibility_var = var.mean()
        # Тест Кохрена
        prac_cochrain = self.cochran_value(var)
        prac_cochrain_crit = None
        numerator_val_cochran = self.count_of_parallel_experiments - 1
        denominator_val_cochran = self.count_of_points
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
    
    def get_estimate_parameters(self):
        mean, var = self.points_mean_var()
        self.prac_model_coef = self.coef @ mean / self.count_of_points
        self.var_params_of_model = self.reproducibility_var \
            / (self.count_of_points * self.count_of_parallel_experiments)
        print('Дисперсия параметра модели:', self.var_params_of_model)

    def significance_estimate_parameters(self):
        """
            Значимость оценок параметров. Критерий Стьюдента
        """
        self.get_estimate_parameters()
        # Наблюдаемое значение критерия Стьюдента =
        # асболютное значение коэф. / корень из дисперсии параметра модели var_params_of_model
        prac_student_test = np.abs(self.prac_model_coef)/np.sqrt(self.var_params_of_model)

        student_df = self.count_of_points * (self.count_of_parallel_experiments - 1)
        crit_t_value_idx = None
        try:
            crit_t_value_idx = t_df.index(student_df)
        except ValueError as ex:
            print(ex)
        if crit_t_value_idx is not None:
            # > критерия == значимые
            crit_t_value = t_values_01[crit_t_value_idx]
            critstr = \
                'Проверка значимости оценок параметров критерием Стьдента, критическое значение:'
            print(critstr, round(crit_t_value,3))
            print('Значения параметров:' ,np.round(self.prac_model_coef, 4))
            print('Значения критерия:  ', np.round(prac_student_test, 4))
            self.significant_coef = prac_student_test > crit_t_value
            print('Значимость:', self.significant_coef)
            # self.count_of_significant_coef = is_significant.sum()
            if np.logical_not(self.significant_coef).any():
                print('Есть незначимый коэффициент. Надо его удалить')
                print(self.prac_model_coef[self.significant_coef])
                print(self.coef[:,self.significant_coef])
                #TODO удаление и перерасчет при необходимости
            else:
                print('Все коэффициенты значимы')

    def adequacy(self):
        """
            Адекватность. Критерий Фишера.
        """
        df_adequacy = self.count_of_points - self.significant_coef.sum()

        print('------------')
        print(df_adequacy)
        print('------------')

        if df_adequacy == 0:
            print('Нужен дополнительный эксперимент')
            self.additional_experiment()
            self.adequacy_var = self.count_of_parallel_experiments * (self.y_vals[-1].mean() - self.b_coef[0])**2
            print('Дисперсия адекватности', round(self.adequacy_var, 3))
            self.prac_fisher_test = self.adequacy_var/self.reproducibility_var
            print('Наблюдаемое значение критерия Фишера', round(fisher_test_res,3))
            
            # Если наблюдаемое значение больше критического, то модель неадекватна 
        # else:





if __name__ == '__main__':
    # np.random.seed(0)
    count_of_parallel_experiments = 5
    counts_of_factors = 2

    f = FullFactorModel(count_of_parallel_experiments, counts_of_factors)\
    
    f.reproducibility_check()
    f.significance_estimate_parameters()
    f.adequacy()