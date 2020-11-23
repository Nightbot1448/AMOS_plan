from enum import IntEnum

class UserState(IntEnum):
    start = 0
    init_completed = 1
    main_experiment = 2
    mean_var = 3
    reproduciblility = 4
    estimate_parametrs = 5
    sign_of_coefs = 6
    check_df_adequacy = 7
    adequacy = 8
    additional_completed = 9
    adequacy_with_additional_completed = 10