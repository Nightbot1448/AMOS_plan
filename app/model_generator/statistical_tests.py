import numpy as np
from statistics import *

def cochrain_test(prac_cochrain, count_of_parallel_experiments, count_of_points):
    print('Оценка воспроизводимости критерием Кохрена')
    prac_cochrain_crit = None
    numerator_val_cochran = count_of_parallel_experiments - 1
    denominator_val_cochran = count_of_points
    K_cochrain_index, N_cochrain_index = None, None
    try:
        K_cochrain_index = cochrain_K.index(numerator_val_cochran)
        N_cochrain_index = cochrain_N.index(denominator_val_cochran)
    except ValueError as ex:
        print(ex)
    if K_cochrain_index is not None and N_cochrain_index is not None:
        prac_cochrain_crit = cochrain_critical_values[N_cochrain_index][K_cochrain_index]
        print('Наблюдаемое значение: ', round(prac_cochrain, 3))
        print('Критическое значение: ', round(prac_cochrain_crit, 3))
        if (prac_cochrain < prac_cochrain_crit):
            return True
    else:
        print('Не удалось найти значение в таблице')
    return False

def student_test(prac_student_values, count_of_parallel_experiments, count_of_points):
    print('Проверка значимости оценок параметров критерием Стьдента')
    
    student_df = count_of_points * (count_of_parallel_experiments - 1)
    crit_t_value_idx = None
    try:
        crit_t_value_idx = t_df.index(student_df)
    except ValueError as ex:
        print(ex)
    if crit_t_value_idx is not None:
        # > критерия == значимые
        crit_t_value = t_values_01[crit_t_value_idx]
        print('Наблюдаемые значения:', np.round(prac_student_values, 3))
        print('Критическое значение:', round(crit_t_value, 3))
        return True, prac_student_values > crit_t_value
    else:
        print('Не удалось найти значение в таблице')
    return False, None

def fisher_test(prac_fisher_value, df_fisher):
    print('Проверка адекватности критерием Фишера')
    print('Наблюдаемые значения:', round(prac_fisher_value, 3))
    
    # TODO доделать тест Фишера (нет таблицы критических значений)
    return None, None
    # try:
    #     crit_f_value_idx = f_df.index(student_df) # get fisher crit value idx
    # except ValueError as ex:
    #     print(ex)
    # if crit_t_value_idx is not None:
    #     # > критерия == значимые
    #     crit_f_value = f_values_01[crit_t_value_idx] get fisher crit value
    #     print('Критическое значение:', round(crit_f_value,3))
    #     return True, prac_fisher_value > crit_f_value
    # else:
    #     print('Не удалось найти значение в таблице')
    # return False, None
