import numpy as np
from .critical_stat_values import cochrain, student, fisher

def cochrain_test(prac_cochrain, df_numerator, df_denominator, p_value=0.01):
    numerator_idx, denominator_idx = None, None
    try:
        numerator_idx = cochrain.numerators.index(df_numerator)
        denominator_idx = cochrain.denominators.index(df_denominator)
    except ValueError as ex:
        print('cochrain_test df:', ex)
    if numerator_idx is not None and denominator_idx is not None:
        cochrain_crit = (
            cochrain.cochrain_05 if p_value == 0.05 \
                else cochrain.cochrain_01)[denominator_idx][numerator_idx]
        return True, prac_cochrain < cochrain_crit, cochrain_crit
    return False, None, None

def student_test(prac_student_values, df, p_value=0.01):
    df_idx = None
    try:
        df_idx = student.df.index(df)
    except ValueError as ex:
        print('student_test df:',ex)
    if df_idx is not None:
        crit_t_value = (student.students_05 if p_value == 0.05 \
                else student.students_01)[df_idx]
        return True, prac_student_values > crit_t_value, crit_t_value
    return False, None, None

def fisher_test(prac_fisher_value, df_numerator, df_denominator, p_value=0.01):
    numerator_idx, denominator_idx = None, None
    try:
        numerator_idx = fisher.numerators.index(df_numerator)
        denominator_idx = fisher.denominators.index(df_denominator)
    except ValueError as ex:
        print('fisher_test df:',ex)
    if numerator_idx is not None and denominator_idx is not None:
        crit_f_value = (fisher.fisher_05 if p_value == 0.05 \
                else fisher.fisher_01)[denominator_idx][numerator_idx]
        return True, prac_fisher_value < crit_f_value, crit_f_value
    return False, None, None
