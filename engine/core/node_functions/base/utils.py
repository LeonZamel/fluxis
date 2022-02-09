from simpleeval import simple_eval
import numpy as np
import pandas as pd

"""
def parse_parameters_for_eval(parameters_raw):
    parameters = {}
    # TODO: Recursive parsing?
    for (key, value) in parameters_raw.items():
        if isinstance(value, pd.Series):
            parameters[key] = np.array(value)
        elif isinstance(value, str):
            parameters[key] = str.encode(value)
        else:
            parameters[key] = value

    return parameters

"""


def safe_eval_on_dataframe(expression, dataframe):
    return simple_eval(expression, names=dict(dataframe.items()))
