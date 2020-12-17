from flask import Blueprint, jsonify, request
from collections import defaultdict
import numpy as np
import json

from model_generator import utils
from model_generator.userState import UserState
from model_generator.generator import FullFactorModel
from model_generator.critical_stat_values.cochrain import COCHRAIN_TABLES
from model_generator.critical_stat_values.student import STUDENT_TABLE
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
    Validate and set planning_area

    error = True if planning_area is invalid else False
    """
    USER.set_state(UserState.init_completed)
    
    if not USER.task:
        return jsonify(dict(data={}, message="Task_id isn't set", error=True))

    planning_area = utils.get_from_request_json(request.json, 'pa_points', [])
    valid_planning_area = utils.is_valid_planning_area(planning_area)
    USER.planning_area = planning_area if valid_planning_area else None
   
    return jsonify({
        'data': {},
        'message': '' if valid_planning_area else 'Invalid planning area {}'.format(planning_area),
        'error': not valid_planning_area        
    })


@bp.route('/check/plan_points_number', methods=['POST'])
def check_plan_points_number():
    """
    Validate and set plan_points_number

    error = True if plan_points_number is invalid else False
    """
    USER.set_state(UserState.init_completed)
    
    if not USER.planning_area:
        return jsonify(dict(data={}, message="Planning_area isn't set", error=True))

    plan_points_number = utils.get_from_request_json(request.json, 'plan_points_number', 0)
    valid_plan_points_number = utils.is_valid_plan_points_number(plan_points_number)
    USER.plan_points_number = plan_points_number if valid_plan_points_number else None
   
    return jsonify({
        'data': {},
        'message': '' if valid_plan_points_number else 'Invalid plan_points_number {}'.format(plan_points_number),
        'error': not valid_plan_points_number        
    })


@bp.route('/check/plan_points_and_number_experiment', methods=['POST'])
def check_plan_points():
    """
    Validate and set plan_points and number_experiment

    error = True if plan_points or number_experiment is invalid else False
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
    Validate factor_point and return y_vals[i]

    error = True if factor_point is invalid else False
    """
    USER.set_state(UserState.init_completed)
    
    if USER.plan_points is None:
        return jsonify(dict(data={}, message="Plan_points and number_experiment aren't set", error=True))

    factor_point = utils.get_from_request_json(request.json, 'factor_point', [])
    valid_factor_point, index = utils.is_valid_factor_point(factor_point, USER.planning_area, USER.plan_points[0])
    if not valid_factor_point:
        return jsonify({
            'data': {},
            'message': '' if valid_factor_point else 'Invalid point {} for factor X{}'.format(factor_point[index], index+1),
            'error': not valid_factor_point        
        })

    y_val = USER.model.y_vals[0][USER.factor_point_index]
    USER.factor_point_index += 1
    USER.set_state(UserState.main_experiment if USER.factor_point_index == 2 else UserState.init_completed)
    USER.factor_point_index %= 2
    return jsonify(dict(data={'y': y_val}, message = '', error=False))


@bp.route('/get/factor_points', methods=['GET'])
def get_factor_points():
    """
    Check that user entered first factor_points, and return y_vals[i]

    error = True if first factor_points don't exist
    """
    if USER.state >= UserState.main_experiment: # or == ?
        USER.state = UserState.mean_var
        return jsonify(dict(data={'y_vals': USER.model.y_vals.tolist()}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Your didn't enter first factor_points", error=True))


@bp.route('/check/mean_var', methods=['POST'])
def check_mean_var():
    """
    Validate mean and var for first point factor

    error = True if mean/var is invalid else False
    """
    if USER.state >= UserState.mean_var: # or == ?
        means, vars = USER.model.points_mean_var()
        
        mean = utils.get_from_request_json(request.json, 'mean', 0)
        var = utils.get_from_request_json(request.json, 'var', 0)
        # Delete this
        print(means[0])
        print(vars[0])

        if not utils.is_valid_mean(mean, means[0]):
            return jsonify(dict(data={}, message = "Mean is invalid ({})".format(mean), error=True))
        if not utils.is_valid_var(var,vars[0]):
            return jsonify(dict(data={}, message = "Var is invalid ({})".format(mean), error=True))
        
        USER.means_vars = dict(means=means.tolist(), vars=vars.tolist())
        USER.state = UserState.reproduciblility
        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/get/means_vars', methods=['GET'])
def get_means_vars():
    """
    Check that user entered first mean/var, and return points_mean_var

    error = True if first mean/var don't entered
    """
    if USER.means_vars: # when we reset it?
        return jsonify(dict(data={'means': USER.means_vars['means'], 'vars': USER.means_vars['vars']}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Your didn't enter first mean/var", error=True))


@bp.route('/set/significance_level', methods=['POST'])
def set_significance_level():
    """
    Check that means_vars is set, and check reproducibility

    error = True if means_vars isn't set else False
    """
    if USER.means_vars: # when we reset it?
        significance = utils.get_from_request_json(request.json, 'significance', 0)
        if utils.is_valid_significance(significance):
            USER.cochrain_significance = significance
            USER.model.reproducibility_check(significance)
            USER.reproduce_res = USER.model.get_reproducibility_info()
            return jsonify(dict(data={'sum_var': sum(USER.means_vars['vars'])}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message="Significance is invalid ({})".format(significance), error=True))
    else:
        return jsonify(dict(data={}, message = "Your didn't enter first mean/var", error=True))


@bp.route('/check/cochrain', methods=['POST'])
def check_cochrain():
    """
    Validate cochrain and get table

    error = True if cochrain is invalid else False
    """
    if USER.reproduce_res: # when we reset it?
        cochrain = utils.get_from_request_json(request.json, 'cochrain', 0)
        if utils.is_valid_cochrain(cochrain, USER.reproduce_res['cochrain']):
            USER.cochrain_status = 1
            return jsonify(dict(data=COCHRAIN_TABLES[USER.cochrain_significance], message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Сochrain is invalid ({})".format(cochrain), error=True))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set significance level", error=True))


@bp.route('/check/cochrain_freedom_degree', methods=['POST'])
def check_cochrain_freedom_degree():
    if USER.cochrain_status > 0: # when we reset it?
        df_numerator = utils.get_from_request_json(request.json, 'df_numerator', 0)
        df_denominator = utils.get_from_request_json(request.json, 'df_denominator', 0)
        if not utils.is_valid_int(df_numerator, USER.reproduce_res['cochrain']['df_numerator']):
            return jsonify(dict(data={}, message = "Numerator is invalid ({})".format(df_numerator), error=True))
        if not utils.is_valid_int(df_denominator, USER.reproduce_res['cochrain']['df_denominator']):
            return jsonify(dict(data={}, message = "Denominator is invalid ({})".format(df_denominator), error=True))
        USER.cochrain_status = 2
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set cochrain", error=True))


@bp.route('/get/cochrain', methods=['GET'])
def get_cochrain():
    if USER.cochrain_status > 1:
        USER.cochrain_status = 3
        return jsonify(dict(data={'prac_cochrain': USER.reproduce_res['cochrain']['prac_value'],
            'crit_cochrain': USER.reproduce_res['cochrain']['crit_value']}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set freedom degrees", error=True))


@bp.route('/check/is_reproducible', methods=['POST'])
def check_reproducible():
    if USER.cochrain_status > 2:
        USER.cochrain_status = 4
        is_reproducible = utils.get_from_request_json(request.json, 'is_reproducible')
        if is_reproducible == USER.reproduce_res['is_reproducible']:
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "is_reproducible is invalid ({})".format(is_reproducible), error=True))
    else:   
        return jsonify(dict(data={}, message = "Your didn't /get/cochrain", error=True))


@bp.route('/check/reproducible_var', methods=['POST'])
def check_reproducible_var():
    if USER.cochrain_status > 3:
        USER.cochrain_status = 5
        reproducible_var = utils.get_from_request_json(request.json, 'reproducible_var')
        if not utils.is_valid_anything(reproducible_var, USER.reproduce_res['reproducibility_var']):
            return jsonify(dict(data={}, message = "Reproducible_var is invalid ({})".format(reproducible_var), error=True))
        USER.state = UserState.estimate_parametrs
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set is_reproducible", error=True))


@bp.route('/get/reproducible_info', methods=['GET'])
def get_reproducible_info():
    if USER.cochrain_status > 4:
        #USER.cochrain_status = 6
        return jsonify(dict(data={
            'level': USER.cochrain_significance,
            'prac_val': USER.reproduce_res['cochrain']['prac_value'],
            'crit_val': USER.reproduce_res['cochrain']['crit_value'],
            'is_reproducible': USER.reproduce_res['cochrain']['is_reproducible'],
            'reproducible_var': USER.reproduce_res['cochrain']['reproducible_var']
        }, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set reproducible_var", error=True))


@bp.route('/check/param_num', methods=['POST'])
def check_param_num():
    if USER.state >= UserState.estimate_parametrs:
        param_num = utils.get_from_request_json(request.json, 'param_num')
        if not utils.is_valid_param_num(param_num):
            return jsonify(dict(data={}, message = "Param_num is invalid ({})".format(param_num), error=True))

        USER.model.get_estimate_parameters()
        USER.model_params = USER.model.get_model_params_info()

        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/check/const_param', methods=['POST'])
def check_const_param():
    if USER.model_params:
        const_param = utils.get_from_request_json(request.json, 'const_param')
        if not utils.is_valid_anything(const_param, USER.model_params['model_params'][0]):
            return jsonify(dict(data={}, message = "Const_param estimation is invalid ({})".format(const_param), error=True))

        var_const_param = utils.get_from_request_json(request.json, 'var_const_param')
        if not utils.is_valid_anything(var_const_param, USER.model_params['model_params_var']):
            return jsonify(dict(data={}, message = "Const_param variance is invalid ({})".format(var_const_param), error=True))

        USER.model_params['next_param'] = True
        return jsonify(dict(data={}, message = '', error=False))


@bp.route('/check/next_param', methods=['POST'])
def check_next_param():
    # DUBLICATE check_const_param
    if USER.model_params and USER.model_params.get('next_param'):
        const_param = utils.get_from_request_json(request.json, 'next_param')
        if not utils.is_valid_anything(const_param, USER.model_params['model_params'][3]):
            return jsonify(dict(data={}, message = "b12_param estimation is invalid ({})".format(const_param), error=True))

        var_const_param = utils.get_from_request_json(request.json, 'var_b12_param')
        if not utils.is_valid_anything(var_const_param, USER.model_params['model_params_var']):
            return jsonify(dict(data={}, message = "b12_param variance is invalid ({})".format(var_const_param), error=True))
        
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
        return jsonify(dict(data={}, message = "Params aren't set", error=True))


@bp.route('/set/significance_level_student', methods=['POST'])
def set_significance_level_student():
    """
    Check that params is set, and check reproducibility

    error = True if params aren't set else False
    """
    if USER.model_params and USER.model_params.get('get_param'):
        significance = utils.get_from_request_json(request.json, 'significance', 0)
        if utils.is_valid_significance(significance):
            USER.model_params['significance'] = significance
            USER.model.check_params_significance(significance)
            USER.model_params.update(USER.model.get_model_params_sing())    # add 'is_sign' and 'sign_coef'
            return jsonify(dict(data={}, message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Significance is invalid ({})".format(significance), error=True))
    else:
        return jsonify(dict(data={}, message = "Your didn't enter params", error=True))


@bp.route('/get/params_for_check', methods=['GET'])
def get_params_for_check():
    if USER.model_params and USER.model_params.get('significance'):
        USER.model_params['params_for_check'] = utils.get_model_params_for_check((0,1,2,3), USER.model_params['is_sign'])
        return jsonify(dict(data={'params': USER.model_params['params_for_check']}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set significance level", error=True))


@bp.route('/check/params_for_check', methods=['POST'])
def check_params_for_check():
    if USER.model_params and USER.model_params.get('params_for_check'):
        first_param = utils.get_from_request_json(request.json, 'first_param', 0)
        if not utils.is_valid_anything(first_param, USER.model_params['student']['prac_value'][USER.model_params['params_for_check'][0]]):
            return jsonify(dict(data={}, message = "first_param is invalid ({})".format(first_param), error=True))
        
        second_param = utils.get_from_request_json(request.json, 'second_param', 0)
        if not utils.is_valid_anything(second_param, USER.model_params['student']['prac_value'][USER.model_params['params_for_check'][1]]):
            return jsonify(dict(data={}, message = "second_param is invalid ({})".format(first_param), error=True))
        
        USER.model_params['is_param_checked'] = True
        return jsonify(dict(data={}, message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't /get/params_for_check", error=True))


@bp.route('/get/student_table', methods=['GET'])
def get_student_table():
    if USER.model_params and USER.model_params.get('is_param_checked'):
        return jsonify(dict(data=STUDENT_TABLE[USER.model_params['significance']], message = '', error=False))
    else:   
        return jsonify(dict(data={}, message = "Your didn't check model_params", error=True))


@bp.route('/check/df_student', methods=['POST'])
def check_df_student():
    if USER.model_params and USER.model_params.get('is_param_checked'):
        df_student = utils.get_from_request_json(request.json, 'df_student', 0)
        if not utils.is_valid_int(df_student, USER.model_params['student']['df']):
            return jsonify(dict(data={}, message = "df_student is invalid ({})".format(df_student), error=True))
        USER.model_params['df_student_checked'] = True
        return jsonify(dict(data={'prac': USER.model_params['student']['prac_value'][0], 'crit_val': USER.model_params['student']['crit_value']}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Your didn't check model_params", error=True))


@bp.route('/check/sign_param', methods=['POST'])
def check_sign_param():
    if USER.model_params and USER.model_params.get('df_student_checked'):
        is_sign = utils.get_from_request_json(request.json, 'is_sign', None)
        if is_sign != USER.model_params['is_sign'][0]:
            return jsonify(dict(data={}, message = "sign_param is invalid ({})".format(sign_param), error=True))
        USER.model_params['sign_param_checked'] = True
        return jsonify(dict(data={}, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Your didn't check model_params", error=True))


@bp.route('/get/sign_params', methods=['GET'])
def get_sign_params():
    if USER.model_params and USER.model_params.get('sign_param_checked'):
        return jsonify(dict(data={
            'params': USER.model_params['model_params'],
            'prac': USER.model_params['student']['prac_value'],
            'is_sign': USER.model_params['is_sign']
        }, message = '', error=False))
    else:
        return jsonify(dict(data={}, message = "Your didn't check sign_param", error=True))


@bp.after_request
def after_request(response):
    print(USER)
    return response
