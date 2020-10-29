import numpy as np

cochrain_critical_values = np.genfromtxt('cochrain_values.csv', delimiter=',')
cochrain_K = [2,3,4,5]
cochrain_N = [2,3,4,5,6,7,8,9,10,12,15,20,24,30]

class FullFactorModel:
    def __init__(self, count_of_parallel_experiments, points):
        # b0 + b1 * x1 + b2 * x2 + b12 * x1 * x2
        # TODO: chagne model to non parabaloid
        
        self.count_of_parallel_experiments = count_of_parallel_experiments
        self.b_coef = np.array([ 2.245, 8.585, 39.945, 180.077])
        self.coef = np.hstack((np.array([1]*4)[:, np.newaxis], points, (points[:,0] * points[:,1])[:, np.newaxis]))
        self.y_mean = (self.coef@self.b_coef)[:,np.newaxis]
        self.y_vals = np.hstack([self.y_mean for _ in range(count_of_parallel_experiments)])
        self.y_vals += np.random.normal(0,1,self.y_vals.shape)
        
    def reproducibility_mean_var(self):
        y_prac_mean = self.y_vals.mean(1)
        y_prac_var = ((self.y_vals - self.y_mean)**2).sum(1)/(self.y_vals.shape[1] - 1)
        return y_prac_mean, y_prac_var

    def cochran_value(self, var):
        return var.max()/var.sum()



if __name__ == '__main__':
    np.random.seed(0)
    count_of_parallel_experiments = 5
    points = np.array([
        [ 1,  1],
        [ 1, -1],
        [-1,  1],
        [-1, -1],
    ])

    f = FullFactorModel(count_of_parallel_experiments, points)

    # Воспроизводимость
    # Среднее и дисперсия
    mean, var = f.reproducibility_mean_var()
    
    # Проверка воспроизводимости
    prac_cochrain = f.cochran_value(var)
    prac_cochrain_crit = None
    numerator_val_cochran = f.count_of_parallel_experiments - 1
    denominator_val_cochran = f.y_mean.size
    K_index, N_index = None, None
    try:
        K_index = cochrain_K.index(numerator_val_cochran)
        N_index = cochrain_N.index(denominator_val_cochran)
    except ValueError as ex:
        print(ex)
    if K_index is not None and N_index is not None:
        prac_cochrain_crit = cochrain_critical_values[N_index][K_index]
        print('Оценка воспроизводимости критерием Кохрена')
        print('Оценка: ', round(prac_cochrain,4))
        print('Критическое значение: ', prac_cochrain_crit)
        if (prac_cochrain < prac_cochrain_crit):
            print('Воспроизводится')
        else:
            print('Не воспроизводится')
