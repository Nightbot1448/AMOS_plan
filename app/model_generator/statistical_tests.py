import numpy as np
from critical_stat_values import cochrain, student, fisher

def cochrain_test(prac_cochrain, df_numerator, df_denominator, p_value=0.01):
    print('Оценка воспроизводимости критерием Кохрена')
    enumerator_idx, denominator_idx = None, None
    try:
        enumerator_idx = cochrain.enumerators.index(df_numerator)
        denominator_idx = cochrain.denominators.index(df_denominator)
    except ValueError as ex:
        print(ex)
    if enumerator_idx is not None and denominator_idx is not None:
        cochrain_crit = (
            cochrain.cochrain_05 if p_value == 0.05 \
                else cochrain.cochrain_01)[denominator_idx][enumerator_idx]
        print('Наблюдаемое значение: ', round(prac_cochrain, 3))
        print('Критическое значение: ', round(cochrain_crit, 3))
        return True, prac_cochrain < cochrain_crit, cochrain_crit
    else:
        print('Не удалось найти значение в таблице')
    return False, None, None

def student_test(prac_student_values, df, p_value=0.01):
    print('Проверка значимости оценок параметров критерием Стьдента')
    df_idx = None
    try:
        df_idx = student.df.index(df)
    except ValueError as ex:
        print(ex)
    if df_idx is not None:
        crit_t_value = (student.students_05 if p_value == 0.05 \
                else student.students_01)[df_idx]
        # > критерия == значимые
        print('Наблюдаемые значения:', np.round(prac_student_values, 3))
        print('Критическое значение:', round(crit_t_value, 3))
        return True, prac_student_values > crit_t_value, crit_t_value
    else:
        print('Не удалось найти значение в таблице')
    return False, None, None

def fisher_test(prac_fisher_value, df_enumerator, df_denominator, p_value=0.01):
    print('Проверка адекватности критерием Фишера')
    enumerator_idx, denominator_idx = None, None
    try:
        enumerator_idx = fisher.enumerators.index(df_enumerator)
        denominator_idx = fisher.denominators.index(df_denominator)
    except ValueError as ex:
        print(ex)
    if enumerator_idx is not None and denominator_idx is not None:
        crit_f_value = (fisher.fisher_05 if p_value == 0.05 \
                else fisher.fisher_01)[denominator_idx][enumerator_idx]
        print('Наблюдаемые значения:', round(prac_fisher_value, 3))
        print('Критическое значение:', round(crit_f_value,3))
        return True, prac_fisher_value < crit_f_value, crit_f_value
    else:
        print('Не удалось найти значение в таблице')
    return False, None, None
