from flask import Blueprint, jsonify, request
from collections import defaultdict
import numpy as np
import json

from model_generator import utils
from model_generator.generator import FullFactorModel
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
    if not USER.task:
        return jsonify(dict(data={}, message="Task_id isn't set", error=True))

    planning_area = utils.get_from_request_json(request.json, 'pa_points', [])
    valid_planning_area = utils.is_valid_planning_area(planning_area)
    if valid_planning_area: USER.planning_area = planning_area
   
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
    if not USER.planning_area:
        return jsonify(dict(data={}, message="Planning_area isn't set", error=True))

    plan_points_number = utils.get_from_request_json(request.json, 'plan_points_number', 0)
    valid_plan_points_number = utils.is_valid_plan_points_number(plan_points_number)
    if valid_plan_points_number: USER.plan_points_number = plan_points_number
   
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
    if not USER.plan_points_number:
        return jsonify(dict(data={}, message="Plan_points_number isn't set", error=True))
    
    plan_points = utils.get_from_request_json(request.json, 'plan_points', [])
    valid_plan_points = utils.is_valid_plan_points(plan_points)
    if not valid_plan_points: 
        return jsonify({
            'data': {},
            'message': '' if valid_plan_points else 'Invalid plan_points {}'.format(plan_points),
            'error': not valid_plan_points        
        })

    experiments_number = utils.get_from_request_json(request.json, 'number_of_experiments', 0)
    valid_experiments_number = utils.is_valid_experiments_number(experiments_number)
    if not valid_experiments_number: 
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

    return jsonify(dict(data={}, message=str(USER.model), error=False))


@bp.route('/check/factor_point', methods=['POST'])
def check_factor_point():
    """
    Validate factor_point and return y_vals[i]

    error = True if factor_point is invalid else False
    """
    if not USER.plan_points:
        return jsonify(dict(data={}, message="Plan_points and number_experiment aren't set", error=True))

    if USER.factor_point_index == 2:
        # reset USER.factor_point_index ?
        return jsonify(dict(data={'y_vals': USER.model.y_vals.tolist()}, message = '', error=False))

    factor_point = utils.get_from_request_json(request.json, 'factor_point', [])
    valid_factor_point, index = utils.is_valid_factor_point(factor_point, USER.planning_area, USER.plan_points[0])
    if not valid_factor_point:
        return jsonify({
            'data': {},
            'message': '' if valid_factor_point else 'Invalid point {} for factor X{}'.format(factor_point[index], index+1),
            'error': not valid_factor_point        
        })

    USER.factor_point_index += 1
    if USER.factor_point_index == 2:
        # reset USER.factor_point_index ?
        return jsonify(dict(data={'y_vals': USER.model.y_vals.tolist()}, message = '', error=False))
    else: 
        return jsonify(dict(data={'y': USER.model.y_vals[0][USER.factor_point_index]}, message = '', error=False))
    

@bp.after_request
def after_request(response):
    print(USER)
    return response
