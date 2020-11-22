from enum import Enum

class UserState(Enum):
    start = 0
    init_completed = 1
    main_experiment = 2
    mean_var = 3
    reproduciblility = 4
    sign_of_coefs = 5
    adequacy = 6
    additional_completed = 7 # TODO порядок и элементы
    adequacy_with_additional_completed = 8