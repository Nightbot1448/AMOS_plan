from flask import Blueprint, jsonify, request
from collections import defaultdict
import json

from model_generator.generator import MODEL_TASKS
from model_generator.utils import is_valid_planning_area

bp = Blueprint('api', __name__, url_prefix='/api')
USER = defaultdict(None)


@bp.route('/check/task', methods=['GET'])
def check_task():
    """
    Validate and set task_id

    error = True if task_id is invalid else False
    """
    task_id = request.args.get('task_id', '0')
    if task_id.isdigit() and int(task_id) in MODEL_TASKS:
        USER['task'] = int(task_id)
        valid_task_id = True
    else:
        valid_task_id = False

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
    planning_area = request.json['data']['pa_points']
    if is_valid_planning_area(planning_area):
        USER['planning_area'] = planning_area
        valid_planning_area = True
    else:
        valid_planning_area = False
    
    return jsonify({
        'data': {},
        'message': '' if valid_planning_area else 'Invalid planning area {}'.format(planning_area),
        'error': not valid_planning_area        
    })


@bp.after_request
def after_request(response):
    print(USER)
    return response
