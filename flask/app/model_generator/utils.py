from model_generator.generator import MODEL_TASKS
from numpy import random as nprandom


def get_from_request_json(request_json, key, default_value=None): return request_json.get('data', {}).get(key, default_value)


def get_model_by_task_id(task_id): return MODEL_TASKS.get(task_id, None)

def get_model_params_for_check(params, is_sign):
    if all(is_sign): return nprandom.choice(params, size=2, replace=False).tolist()
    not_sign_index = is_sign.index(False)
    return (params[not_sign_index], params[(not_sign_index+1) % len(params)]) 

def is_valid_task_id(task_id): return bool(get_model_by_task_id(task_id))


def is_valid_planning_area(planning_area, max_diff=100):
    check_flag = True
    for factor in planning_area:
        if len(factor) != 2: return False
        check_flag = check_flag and abs(factor[0]-factor[1]) < max_diff and abs(factor[0]+factor[1]) < max_diff
    return check_flag


def is_valid_plan_points_number(plan_points_number, default_number=4): return plan_points_number == default_number


def is_valid_plan_points(plan_points, plan_points_number=4):
    return len(set((tuple(point) for point in plan_points if all(map(lambda x: x in (-1, 1), point))))) == len(plan_points) == plan_points_number


def is_valid_experiments_number(experiments_number): return 2 <= experiments_number <= 5


def equal_float(a, b, max_diff=0.01, not_neg=False):
    if not_neg and b < 0: return False
    
    if 0 <= abs(a) <= 1:
        return a - max_diff <= b <= a + max_diff
    
    max_diff_percent = 100*max_diff*3 if 1 < abs(a) < 10 else 100*max_diff
    return abs((a-b)/a) * 100 < max_diff_percent


def is_valid_factor_point(factor_point, planning_area, plan_point):
    """
    factor_point = [f1,f2]
    planning_area = [[m1, d1], [m2, d2]]
    plan_point = [±1, ±1] 
    """
    for i, point in enumerate(factor_point):
        factor = planning_area[i][0] + planning_area[i][1] * plan_point[i] 
        if not equal_float(factor, point):
            return False, i
    return True, -1


def is_valid_mean(mean, calc_mean, max_diff_percent=0.01): return equal_float(calc_mean, mean, max_diff_percent)


def is_valid_var(var, calc_var, max_diff_percent=0.01): return equal_float(var, calc_var, max_diff_percent, not_neg=True)


def is_valid_significance(significance): return significance in (0.01, 0.05)


def is_valid_cochrain(cochrain, calc_cochrain, max_diff=0.025): return equal_float(cochrain, calc_cochrain, max_diff, not_neg=True)


def is_valid_anything(user, calc, max_diff_percent=0.01): return equal_float(user, calc, max_diff_percent)


def is_valid_param_num(user_num): return user_num == 4


def is_valid_int(user, calc): return user == calc