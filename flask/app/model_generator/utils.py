from model_generator.generator import MODEL_TASKS


def get_from_request_json(request_json, key, default_value=None): return request_json.get('data', {}).get(key, default_value)


def get_model_by_task_id(task_id): return MODEL_TASKS.get(task_id, None)


def is_valid_task_id(task_id): return bool(get_model_by_task_id(task_id))


def is_valid_planning_area(planning_area, max_diff=100):
    #TODO: test
    check_flag = True
    for factor in planning_area:
        if len(factor) != 2: return False
        check_flag = check_flag and abs(factor[0]-factor[1]) < max_diff and abs(factor[0]+factor[1]) < max_diff
    return check_flag


def is_valid_plan_points_number(plan_points_number, default_number=4): return plan_points_number == default_number


def is_valid_plan_points(plan_points, plan_points_number=4):
    return len(set((tuple(point) for point in plan_points if all(map(lambda x: x in (-1, 1), point))))) == len(plan_points) == plan_points_number


def is_valid_experiments_number(experiments_number): return 0 < experiments_number < 10


def equal_float(a, b, max_diff_percent=0.01): return abs(a-b)/a < max_diff_percent


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


def is_valid_var(var, calc_var, max_diff_percent=0.01): return equal_float(var, calc_var, max_diff_percent)


def is_valid_significance(significance): return significance in (0.01, 0.05)


def is_valid_cochrain(cochrain, calc_cochrain, max_diff_percent=0.01): return equal_float(cochrain, cochrain, max_diff_percent)


def is_valid_anything(user, calc, max_diff_percent=0.01): return equal_float(user, calc, max_diff_percent)