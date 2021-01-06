from flask import Blueprint, jsonify, request
from collections import defaultdict
import numpy as np
import json

from model_generator import utils
from model_generator.userState import UserState
from model_generator.generator import FullFactorModel
from model_generator.critical_stat_values.cochrain import COCHRAIN_TABLES
from model_generator.critical_stat_values.student import STUDENT_TABLE
from model_generator.critical_stat_values.fisher import FISHER_TABLES
from api_user import APIUser


bp = Blueprint('api', __name__, url_prefix='/api')
USER = APIUser()


@bp.route('/check/task', methods=['GET'])
def check_task():
    """
    Validate and set task_id

    error = True if task_id is invalid else False
    """
    task_id = request.args.get('task_id', None)

    USER.reset()
    valid_task_id = utils.is_valid_task_id(task_id)
    if valid_task_id: USER.task = utils.get_model_by_task_id(task_id)

    return jsonify({
        'data': {},
        'message': '' if valid_task_id else 'Invalid task_id #{}'.format(task_id),
        'error': not valid_task_id        
    })


@bp.route('/check/planning_area', methods=['POST'])
def check_planning_area():
    """
    Проверяет и устанавливает область планирования

    error = True если область планирования указана неверно
    """
    USER.set_state(UserState.init_completed)
    
    if not USER.task:
        return jsonify(dict(data={}, message="Не выбран вариант!", error=True))

    planning_area = utils.get_from_request_json(request.json, 'pa_points', [])
    valid_planning_area = utils.is_valid_planning_area(planning_area)
    USER.planning_area = planning_area if valid_planning_area else None
   
    return jsonify({
        'data': {},
        'message': '' if valid_planning_area else 'Неверная область планирования! {}'.format(planning_area),
        'error': not valid_planning_area        
    })


@bp.route('/check/plan_points_number', methods=['POST'])
def check_plan_points_number():
    """
    Проверяет и устанавливает количество точек планирования

    error = True если количество точек планирования неверно (должно быть 4)
    """
    USER.set_state(UserState.init_completed)
    
    if not USER.planning_area:
        return jsonify(dict(data={}, message="Область планирования не установлена!", error=True))

    plan_points_number = utils.get_from_request_json(request.json, 'plan_points_number', 0)
    valid_plan_points_number = utils.is_valid_plan_points_number(plan_points_number)
    USER.plan_points_number = plan_points_number if valid_plan_points_number else None
   
    return jsonify({
        'data': {},
        'message': '' if valid_plan_points_number else 'Неверное количество точек планирования! {}'.format(plan_points_number),
        'error': not valid_plan_points_number        
    })


@bp.route('/check/plan_points_and_number_experiment', methods=['POST'])
def check_plan_points():
    """
    Проверяет и устанавливает точки планирования и количество параллельных опытов

    error = True если точки планирования/количество параллельных опытов неверные
    """
    def reset():
        USER.plan_points = None
        USER.experiments_number = None
    
    USER.set_state(UserState.init_completed)
    
    if not USER.plan_points_number:
        return jsonify(dict(data={}, message="Plan_points_number isn't set", error=True))
    
    plan_points = utils.get_from_request_json(request.json, 'plan_points', [])
    valid_plan_points = utils.is_valid_plan_points(plan_points)
    if not valid_plan_points:
        reset()
        return jsonify({
            'data': {},
            'message': '' if valid_plan_points else 'Invalid plan_points {}'.format(plan_points),
            'error': not valid_plan_points        
        })

    experiments_number = utils.get_from_request_json(request.json, 'number_of_experiments', 0)
    valid_experiments_number = utils.is_valid_experiments_number(experiments_number)
    if not valid_experiments_number:
        reset()
        return jsonify({
            'data': {},
            'message': '' if valid_experiments_number else 'Invalid experiments_number {}'.format(experiments_number),
            'error': not valid_experiments_number        
        })

    USER.plan_points = np.array(plan_points)
    USER.experiments_number = experiments_number
    
    # generate
    USER.model = FullFactorModel(USER.experiments_number, USER.factor_number, USER.plan_points, USER.task, True)

    print(USER.model.y_vals)

    return jsonify(dict(data={}, message='', error=False))


@bp.route('/check/factor_point', methods=['POST'])
def check_factor_point():
    """
    Проверяет значения факторов и возвращает i-ое значение

    error = True если занчения факторов неверное
    """
    USER.set_state(UserState.init_completed)
    
    if USER.plan_points is None:
        return jsonify(dict(data={}, message="Точки планирования и количечтсво параллельныъ экспериментов не установлены", error=True))

    factor_point = utils.get_from_request_json(request.json, 'factor_point', [])
    valid_factor_point, index = utils.is_valid_factor_point(factor_point, USER.planning_area, USER.plan_points[0])
    if not valid_factor_point:
        return jsonify({
            'data': {},
            'message': '' if valid_factor_point else 'Неверная точка {} для фактора factor X{}'.format(factor_point[index], index+1),
            'error': not valid_factor_point        
        })

    y_val = USER.model.y_vals[0][USER.factor_point_index]
    means, vars = USER.model.points_mean_var()
    print(means[0])
    print(vars[0])
    USER.factor_point_index += 1
    USER.set_state(UserState.main_experiment if USER.factor_point_index == 2 else UserState.init_completed)
    USER.factor_point_index %= 2
    return jsonify(dict(data={'y': y_val}, message = '', error=False))


@bp.route('/get/factor_points', methods=['GET'])
def get_factor_points():
    """
    Проверяет что пользователь ввел первые значения факторов и возвращает все значения

    error = True если первые значения факторов не введены
    """
    if USER.state >= UserState.main_experiment: # or == ?
        USER.state = UserState.mean_var
        return jsonify(dict(data={'y_vals': USER.model.y_vals.tolist()}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не ввели первые значения факторов", error=True))


@bp.route('/check/mean_var', methods=['POST'])
def check_mean_var():
    """
    Проверяет среднее и дисперсию отклика в первой точке
    
    error = True если среднее/дисперсия неверны
    """
    if USER.state >= UserState.mean_var: # or == ?
        means, vars = USER.model.points_mean_var()
        
        mean = utils.get_from_request_json(request.json, 'mean', 0)
        var = utils.get_from_request_json(request.json, 'var', 0)
        # Delete this
        print(means[0])
        print(vars[0])

        message = ''
        if not utils.is_valid_mean(mean, means[0]):
            message += "Среднее неверно ({})\n".format(mean)
        if not utils.is_valid_var(var,vars[0]):
            message += "Дисперсия неверна ({})".format(var)

        if message:
            return jsonify(dict(data={}, message=message, error=True))
        
        USER.means_vars = dict(means=means.tolist(), vars=vars.tolist())
        USER.state = UserState.reproduciblility
        return jsonify(dict(data={}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = 'Вы не готовы к проверке среднего и вариации факторов', error=True))


@bp.route('/get/means_vars', methods=['GET'])
def get_means_vars():
    """
    Проверя что пользователь ввел среднее/дисперсию в первой точке и возвращает все значения средних/дисперсий 
    Check that user entered first mean/var, and return points_mean_var

    error = True если среднее/дисперсия в первой точке не введены
    """
    if USER.means_vars: # when we reset it?
        return jsonify(dict(data={'means': USER.means_vars['means'], 'vars': USER.means_vars['vars']}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не ввели среднее/дисперсию в первой точке", error=True))


@bp.route('/set/significance_level', methods=['POST'])
def set_significance_level():
    """
    Проверяет верность уровня и делает проверку воспроизводимости

    error = True если предыдущие шаги не выполнены
    """
    if USER.means_vars: # when we reset it?
        significance = utils.get_from_request_json(request.json, 'significance', 0)
        if utils.is_valid_significance(significance):
            USER.cochrain_significance = significance
            USER.model.reproducibility_check(significance)
            USER.reproduce_res = USER.model.get_reproducibility_info()
            return jsonify(dict(data={'sum_var': sum(USER.means_vars['vars'])}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message="Уровень значимости неверный ({})".format(significance), error=True))
    else:
        return jsonify(dict(data={}, message = "Вы не ввели среднее/дисперсию в первой точке", error=True))


@bp.route('/check/cochrain', methods=['POST'])
def check_cochrain():
    """
    Проверяет практическое значение критерия Кохрена и возвращает таблицу значений 

    error = True если практическое значение неверно
    """
    if USER.reproduce_res: # when we reset it?
        cochrain = utils.get_from_request_json(request.json, 'cochrain', 0)
        print(USER.reproduce_res['cochrain']['prac_value'])
        if utils.is_valid_cochrain(cochrain, USER.reproduce_res['cochrain']['prac_value']):
            USER.cochrain_status = 1
            return jsonify(dict(data=COCHRAIN_TABLES[USER.cochrain_significance], message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Практическое значение критерия Кохрена неверно ({})".format(cochrain), error=True))
    else:   
        return jsonify(dict(data={}, message = "Вы не установили уровень знамичости", error=True))


@bp.route('/check/cochrain_freedom_degree', methods=['POST'])
def check_cochrain_freedom_degree():
    if USER.cochrain_status > 0: # when we reset it?
        df_numerator = utils.get_from_request_json(request.json, 'df_numerator', 0)
        df_denominator = utils.get_from_request_json(request.json, 'df_denominator', 0)
        
        message = ''
        if not utils.is_valid_int(df_numerator, USER.reproduce_res['cochrain']['df_numerator']):
            message += "Число степеней свободы числителя неверно ({})\n".format(df_numerator)
        if not utils.is_valid_int(df_denominator, USER.reproduce_res['cochrain']['df_denominator']):
            message += "Число степеней свободы знаменателя неверно ({})".format(df_denominator)

        if message:
            return jsonify(dict(data={}, message=message, error=True))
        
        USER.cochrain_status = 2
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не установили значение критерия Кохрена", error=True))


@bp.route('/get/cochrain', methods=['GET'])
def get_cochrain():
    if USER.cochrain_status > 1:
        USER.cochrain_status = 3
        return jsonify(dict(data={'prac_cochrain': USER.reproduce_res['cochrain']['prac_value'],
            'crit_cochrain': USER.reproduce_res['cochrain']['crit_value']}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не указали число степеней свободы", error=True))


@bp.route('/check/is_reproducible', methods=['POST'])
def check_reproducible():
    if USER.cochrain_status > 2:
        USER.cochrain_status = 4
        is_reproducible = utils.get_from_request_json(request.json, 'is_reproducible')
        if is_reproducible == USER.reproduce_res['is_reproducible']:
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Ошибаетесь! ({})".format(is_reproducible), error=True))
    else:   
        return jsonify(dict(data={}, message = "Получите таблицу значений критерия Кохрена", error=True))


@bp.route('/check/reproducible_var', methods=['POST'])
def check_reproducible_var():
    if USER.cochrain_status > 3:
        USER.cochrain_status = 5
        reproducible_var = utils.get_from_request_json(request.json, 'reproducible_var')
        if not utils.is_valid_anything(reproducible_var, USER.reproduce_res['reproducibility_var']):
            return jsonify(dict(data={}, message = "Дисперсия воспроизводимости неверная ({})".format(reproducible_var), error=True))
        USER.state = UserState.estimate_parametrs
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не ответили на вопрос о воспроизводимости эксперимента", error=True))


@bp.route('/get/reproducible_info', methods=['GET'])
def get_reproducible_info():
    if USER.cochrain_status > 4:
        #USER.cochrain_status = 6
        return jsonify(dict(data={
            'level': USER.cochrain_significance,
            'prac_val': USER.reproduce_res['cochrain']['prac_value'],
            'crit_val': USER.reproduce_res['cochrain']['crit_value'],
            'is_reproducible': USER.reproduce_res['is_reproducible'].tolist(),
            'reproducible_var': USER.reproduce_res['reproducibility_var'].tolist()
        }, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не проверили дисперсию воспроизмодимости!", error=True))


@bp.route('/check/param_num', methods=['POST'])
def check_param_num():
    if USER.state >= UserState.estimate_parametrs:
        param_num = utils.get_from_request_json(request.json, 'param_num')
        if not utils.is_valid_param_num(param_num):
            return jsonify(dict(data={}, message = "Количество параметров модели неверное! ({})".format(param_num), error=True))

        USER.model.get_estimate_parameters()
        USER.model_params = USER.model.get_model_params_info()

        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/check/const_param', methods=['POST'])
def check_const_param():
    if USER.model_params:
        const_param = utils.get_from_request_json(request.json, 'const_param')
        var_const_param = utils.get_from_request_json(request.json, 'var_const_param')

        message = ''
        if not utils.is_valid_anything(const_param, USER.model_params['model_params'][0]):
            message += "Оценка постоянного параметра неверная! ({})\n".format(const_param)
        if not utils.is_valid_anything(var_const_param, USER.model_params['model_params_var']):
            message += "Дисперсия постоянного параметра неверная! ({})".format(var_const_param)

        if message:
            return jsonify(dict(data={}, message=message, error=True))

        USER.model_params['next_param'] = True
        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/check/next_param', methods=['POST'])
def check_next_param():
    # DUBLICATE check_const_param
    if USER.model_params and USER.model_params.get('next_param'):
        const_param = utils.get_from_request_json(request.json, 'next_param')
        var_const_param = utils.get_from_request_json(request.json, 'var_b12_param')
        message = ''
        if not utils.is_valid_anything(const_param, USER.model_params['model_params'][3]):
            message += "Оценка постоянного параметра неверная! ({})\n".format(const_param)
        if not utils.is_valid_anything(var_const_param, USER.model_params['model_params_var']):
            message += "Дисперсия постоянного параметра неверная! ({})".format(var_const_param)

        if message:
            return jsonify(dict(data={}, message=message, error=True))


        USER.model_params['get_param'] = True
        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/get/params', methods=['GET'])
def get_param():
    if USER.model_params and USER.model_params.get('get_param'):
        return jsonify(dict(data={
            'params': USER.model_params.get('model_params').tolist(),
            'var': USER.model_params.get('model_params_var').tolist()
        }, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Значения параметров не установлены!", error=True))


@bp.route('/set/significance_level_student', methods=['POST'])
def set_significance_level_student():
    """
    Проверка значимости параметров
    """
    if USER.model_params and USER.model_params.get('get_param'):
        significance = utils.get_from_request_json(request.json, 'significance', 0)
        if utils.is_valid_significance(significance):
            USER.model_params['significance'] = significance
            USER.model.check_params_significance(significance)
            USER.model_params.update(USER.model.get_model_params_sing())    # add 'is_sign' and 'sign_coef'
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Уровень значимости неверен! ({})".format(significance), error=True))
    else:
        return jsonify(dict(data={}, message = "Вы не ввели значения параметров!", error=True))


@bp.route('/get/params_for_check', methods=['GET'])
def get_params_for_check():
    if USER.model_params and USER.model_params.get('significance'):
        USER.model_params['params_for_check'] = utils.get_model_params_for_check((0,1,2,3), USER.model_params['is_sign'].tolist())
        return jsonify(dict(data={'params': USER.model_params['params_for_check']}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не установили уровень значимости!", error=True))


@bp.route('/check/params_for_check', methods=['POST'])
def check_params_for_check():
    if USER.model_params and USER.model_params.get('params_for_check'):
        first_param = utils.get_from_request_json(request.json, 'first_param', 0)
        second_param = utils.get_from_request_json(request.json, 'second_param', 0)

        message = ''
        if not utils.is_valid_anything(first_param, USER.model_params['student']['prac_value'][USER.model_params['params_for_check'][0]]):
            message += "Первый параметр неверен ({})\n".format(first_param)
        if not utils.is_valid_anything(second_param, USER.model_params['student']['prac_value'][USER.model_params['params_for_check'][1]]):
            message += "Второй параметр неверен ({})".format(second_param)

        if message:
            return jsonify(dict(data={}, message=message, error=True))

        USER.model_params['is_param_checked'] = True
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не получили индексы параметров для проверки", error=True))


@bp.route('/get/student_table', methods=['GET'])
def get_student_table():
    if USER.model_params and USER.model_params.get('is_param_checked'):
        return jsonify(dict(data=STUDENT_TABLE[USER.model_params['significance']], message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Вы не проверили параметры модели", error=True))


@bp.route('/check/df_student', methods=['POST'])
def check_df_student():
    if USER.model_params and USER.model_params.get('is_param_checked'):
        df_student = utils.get_from_request_json(request.json, 'df_student', 0)
        if not utils.is_valid_int(df_student, USER.model_params['student']['df']):
            return jsonify(dict(data={}, message = "Число степеней свободы критерия Стьюдента неверное ({})".format(df_student), error=True))
        USER.model_params['df_student_checked'] = True
        return jsonify(dict(data={'prac': USER.model_params['student']['prac_value'].tolist(), 'crit_val': USER.model_params['student']['crit_value']}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не проверили параметры модели", error=True))


@bp.route('/check/sign_param', methods=['POST'])
def check_sign_param():
    if USER.model_params and USER.model_params.get('df_student_checked'):
        is_sign = utils.get_from_request_json(request.json, 'is_sign', None)
        if is_sign != USER.model_params['is_sign'][0]:
            return jsonify(dict(data={}, message = "Указанная значимость неверна! ({})".format(is_sign), error=True))
        USER.model_params['sign_param_checked'] = True

        return jsonify(dict(data={}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не проверили параметры модели", error=True))


@bp.route('/get/sign_params', methods=['GET'])
def get_sign_params():
    if USER.model_params and USER.model_params.get('df_student_checked'):
        USER.set_state(UserState.check_df_adequacy)
        return jsonify(dict(data={
            'params': USER.model_params['model_params'].tolist(),
            'prac': USER.model_params['student']['prac_value'].tolist(),
            'is_sign': USER.model_params['is_sign'].tolist()
        }, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не проверили значимость параметров!", error=True))


## additional experiment

@bp.route('/check/need_additional_experiment', methods=['POST'])
def check_need_additional_experiment():
    if USER.state >= UserState.check_df_adequacy:
        if USER.model.df_adequacy():
            USER.set_state(UserState.additional_completed)
            return jsonify(dict(data={'is_additional_experiment_needed': False},
                message = "Дополнительный эксперимент не требуется! Число степеней свободы дисперсии адекватности = {}".format(USER.model.df_adequacy()),
                error=False))
        else:
            USER.set_state(UserState.additional_started)
            return jsonify(dict(data={'is_additional_experiment_needed': True},
                message = "Нужен дополнительный эксперимент! Число степеней свободы дисперсии адекватности = {}. Доп. эксперимент проводится в центре области планирования".format(USER.model.df_adequacy()),
                error=False))
    else:
        return jsonify(dict(data={}, message = "Вы не проверили значимость параметров!", error=True))


@bp.route('/check/additional_experiment_point', methods=['POST'])
def check_additional_experiment_area():
    if USER.state == UserState.additional_started:
        exp_point = utils.get_from_request_json(request.json, 'additional_experiment_point', (-999999, -999999))
        X1, X2 = USER.planning_area[0][0], USER.planning_area[1][0]
        message = ''
        if not utils.is_valid_anything(X1, exp_point[0]):
            message += 'Значение X1 неверное! ({})\n'.format(exp_point[0])
        if not utils.is_valid_anything(X2, exp_point[1]):
            message += 'Значение X2 неверное! ({})'.format(exp_point[1])
        
        if not message:
            USER.model.additional_experiment()
            USER.set_state(UserState.additional_completed)
            additional_experiment = USER.model.y_vals[-1]
            return jsonify(dict(data={'y': additional_experiment, 'y_vals': USER.model.y_vals.tolist()}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = message, error=True))
    else:
        return jsonify(dict(data={}, message = "Дополнительный эксперимент не требуется, либо вы зашли сюда слишком рано!", error=True))
##


@bp.route('/set/significance_level_fisher', methods=['POST'])
def set_significance_level_fisher():
    """
    Check that we can go to adequacy and set level

    error = True if can't go to adequacy else False
    """
    if USER.state >= UserState.additional_completed:
        significance = utils.get_from_request_json(request.json, 'significance', 0)
        if utils.is_valid_significance(significance):
            df_model_adeq = USER.model.df_adequacy()
            
            USER.model.adequacy_check(significance)
            USER.adequacy = USER.model.get_adequacy_info()
            USER.adequacy['significance'] = significance
            if df_model_adeq:
                return jsonify(dict(
                    data={'df_adequacy_before_test': int(USER.adequacy['df_adequacy_before_test']), 'df_adequacy_after_test': int(USER.adequacy['df_adequacy_after_test'])},
                    message = 'Число степеней свободы дисперсии адекватности = {}. Поздравляем, доп. эксперимент не нужен'.format(df_model_adeq), error=False))
            else:
                return jsonify(dict(
                    data={'df_adequacy_before_test': int(USER.adequacy['df_adequacy_before_test']), 'df_adequacy_after_test': int(USER.adequacy['df_adequacy_after_test'])},
                    message = 'Число степеней свободы дисперсии адекватности = {}. Нужно провести доп. эксперимент'.format(df_model_adeq), error=False))
        else:
            return jsonify(dict(data={}, message = "Significance is invalid ({})".format(significance), error=True))
    else:
        return jsonify(dict(data={}, message = "Вы ещё не готовы к проверке адекватности! Проверьте, нужен ли вам дополнительный эксперимент?", error=True))


@bp.route('/check/adequacy_var', methods=['POST'])
def check_adequacy_var():
    if USER.adequacy:
        adequacy_var = utils.get_from_request_json(request.json, 'adequacy_var', -1)
        if utils.is_valid_anything(adequacy_var, USER.adequacy['adequcy_var']):
            USER.adequacy['adequacy_var_checked'] = True
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Значение дисперсии адекватности неверное ({})".format(adequacy_var), error=True))
    else:
        return jsonify(dict(data={}, message = "Вы ещё не готовы к проверке дисперсии адекватности", error=True))


@bp.route('/check/prac_fisher', methods=['POST'])
def check_prac_fisher():
    if USER.adequacy and USER.adequacy.get('adequacy_var_checked'):
        prac_fisher = utils.get_from_request_json(request.json, 'prac_fisher', -1)
        if utils.is_valid_anything(prac_fisher, USER.adequacy['fisher']['prac_value']):
            USER.adequacy['prac_fisher_checked'] = True
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Практическое значение критерия Фишера неверное ({})".format(prac_fisher), error=True))
    else:
        return jsonify(dict(data={}, message = "Вы ещё не готовы к проверке значения критерия Фишера", error=True))


@bp.route('/get/fisher_table', methods=['GET'])
def get_fisher_table():
    if USER.adequacy.get('significance'):
        return jsonify(dict(data=FISHER_TABLES[USER.adequacy['significance']], message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Не установлен уровень значимости для критерия Фишера", error=True))


@bp.route('/check/fisher_freedom_degree', methods=['POST'])
def check_fisher_freedom_degree():
    if USER.adequacy and USER.adequacy.get('prac_fisher_checked'):
        df_numerator = utils.get_from_request_json(request.json, 'df_numerator', 0)
        df_denominator = utils.get_from_request_json(request.json, 'df_denominator', 0)

        message = ''
        if not utils.is_valid_int(df_numerator, USER.adequacy['fisher']['df_numerator']):
            message += "Число степеней свободы числителя неверно ({})\n".format(df_numerator)
        if not utils.is_valid_int(df_denominator, USER.adequacy['fisher']['df_denominator']):
            message += "Число степеней свободы знаменателя неверно ({})".format(df_denominator)

        if message:
            return jsonify(dict(data={}, message=message, error=True))

        USER.adequacy['df_checked'] = True
        return jsonify(dict(data=
            {
                'crit_value': USER.adequacy['fisher']['crit_value'],
                'prac_value': USER.adequacy['fisher']['prac_value']
            }, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Вы ещё не готовы к проверке степеней свободы критерия Фишера", error=True))


@bp.route('/check/is_adequacy', methods=['POST'])
def check_is_adequacy():
    if USER.adequacy and USER.adequacy.get('df_checked'):
        is_adequacy = utils.get_from_request_json(request.json, 'is_adequacy')
        if is_adequacy == USER.adequacy['is_adequacy']:
            return jsonify(dict(data={}, message = 'Поздравляем, работа закончена', error=False))
        else:
            return jsonify(dict(data={}, message = "Неверно!", error=True))
    else:
        return jsonify(dict(data={}, message = "Вы ещё не готовы к проверке адекватности", error=True))


@bp.after_request
def after_request(response):
    print(USER)
    return response
