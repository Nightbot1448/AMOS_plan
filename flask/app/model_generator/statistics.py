import numpy as np
import scipy.stats


cochrain_critical_values = np.genfromtxt('./app/model_generator/cochrain_values.csv', delimiter=',')
cochrain_K = [2,3,4,5]
cochrain_N = [2,3,4,5,6,7,8,9,10,12,15,20,24,30]


def t(alpha, gl):
    return scipy.stats.t.ppf(1-(alpha/2), gl)

t_df = [1,2,4,8,12,16,20,24,28,30,32,34,36,40,44,48,50,55,60,65,70,80,90,100,120,150]
t_values_01 = list(t(0.01,t_df))
t_values_05 = list(t(0.05,t_df))

