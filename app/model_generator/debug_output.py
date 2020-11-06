import numpy as np

def print_reproducibility_check(self, reproducible_success, reproducible_result, cochrain_critical_value):
    print('--------------------------------------------------------------')
    mean, var = self.points_mean_var()
    df_numerator = self.count_of_parallel_experiments - 1
    df_denominator = self.count_of_points
    prac_cochrain_val = self.cochran_value(var)
    print('Средние значения:                     ', np.round(mean, 3))
    print('Дисперсия:                            ', np.round(var, 3))
    print('\nОценка воспроизводимости критерием Кохрена')
    print('Наблюдаемое значение критерия Кохрена:', np.round(prac_cochrain_val, 3))
    print('Число степеней свободы числ. и знам. :', df_numerator, df_denominator)
    if reproducible_success:
        print('Критическое значение критерия Кохрена:', np.round(cochrain_critical_value, 3))
        print('Эксперимент{} воспроизводим'.format('' if reproducible_result else ' не'))
    else:
        print('Не удалось найти значение в таблице')
        
    print('Дисперсия ошибки (воспроизводимости) эксперимента:', round(self.reproducibility_var,4))

def print_object_model(self, student_test_success, student_crit):
    df_student = self.count_of_points * (self.count_of_parallel_experiments - 1)
    prac_student_values = self.student_values()
    print('--------------------------------------------------------------')
    print('Параметры модели:            ', np.round(self.prac_b_coef, 3))
    print('Дисперсия параметра модели:  ', np.round(self.var_params_of_model,3))
    print('\nПроверка значимости оценок параметров критерием Стьдента')
    print('Наблюдаемые значения:', np.round(prac_student_values, 3))
    print('Число степеней свободы:', df_student)
    print('Критическое значение:', round(student_crit, 3))
    if student_test_success:
        if np.logical_not(self.significant_coef).any():
            print('Есть незначимые коэффициенты.')
            print('Значимые коэффициенты:', np.round(self.significant_b_coef,3))
        else:
            print('Все коэффициенты значимы')
    else:
        print('Не удалось найти значение в таблице')

def print_adequacy_check(self, fisher_test_success, fisher_test_result, fisher_crit):
    prac_fisher_value = self.fisher_value()
    df_numerator = self.count_of_points - self.significant_coef.sum()\
            + self.additional_experiment_experiment_conducted
    df_denominator = self.count_of_points * (self.count_of_parallel_experiments - 1)

    print('--------------------------------------------------------------')
    print('Дисперсия адекватности:', round(self.adequacy_var,3))
    print('\nПроверка адекватности критерием Фишера')
    print('Отклик модели', np.round(self.model_response, 3))
    print('Наблюдаемое значения:', round(prac_fisher_value, 3))
    print('Число степеней свободы числ. и знам. :', df_numerator, df_denominator)
    print('Критическое значение:', round(fisher_crit,3))
    if fisher_test_success:
        print('Модель{} адекватна'.format('' if fisher_test_result else ' не'))