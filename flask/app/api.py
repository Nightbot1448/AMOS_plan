from flask import Blueprint, jsonify, request
from collections import defaultdict
import numpy as np
import json

from model_generator import utils
from model_generator.userState import UserState
from model_generator.generator import FullFactorModel
from model_generator.criticalsts_values.cochraun import COCHRAIN_TABLES
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
        
        y_prac_mean, y_prac_var = USER.model.points_mean_var()
        USER.means_vars = dict(means=y_prac_mean.tolist(), vars=y_prac_var.tolist())
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
            return jsonify(dict(data={}, message = "Significance is invalid ()".format(significance), error=True))
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
            return jsonify(dict(data=COCHRAIN_TABLES[cochrain], message = '', error=False))
        else:
            return jsonify(dict(data={}, message = "Сochrain is invalid ({})".format(cochrain), error=True))
    else:   
        return jsonify(dict(data={}, message = "Your didn't set significance level", error=True))


@bp.route('/check/cochrain_freedom_degree', methods=['POST'])
def check_cochrain_freedom_degree():
    if USER.cochrain_status > 0: # when we reset it?
        df_numerator = utils.get_from_request_json(request.json, 'df_numerator', 0)
        df_denominator = utils.get_from_request_json(request.json, 'df_denominator', 0)
        if not utils.is_valid_anything(df_numerator, USER.reproduce_res['cochrain']['df_numerator']):
            return jsonify(dict(data={}, message = "Numerator is invalid ({})".format(df_numerator), error=True))
        if not utils.is_valid_anything(df_denominator, USER.reproduce_res['cochrain']['df_denominator']):
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


@bp.route('/get/reproducible_info', methods=['POST'])
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

@bp.after_request
def after_request(response):
    print(USER)
    return response
