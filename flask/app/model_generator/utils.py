def is_valid_planning_area(planning_area, max_diff=100):
    #TODO: test
    check_flag = True
    for factor in planning_area:
        if len(factor) != 2: return False
        check_flag = check_flag and abs(factor[0]-factor[1]) < max_diff and abs(factor[0]+factor[1]) < max_diff
    return check_flag
