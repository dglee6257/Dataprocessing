import os
import inspect
import pandas as pd
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# Simple way to get the OS name (e.g., 'posix', 'nt', 'java')
if os.name == "nt":
    plt.rcParams["font.family"] = "Malgun Gothic"  # 폰트를 맑은 고딕으로 설정
else:
    plt.rcParams["font.family"] = "NanumGothic"  # 리눅스에서는 나눔고딕으로 설정

fm = matplotlib.font_manager.FontManager()
assert plt.rcParams["font.family"][0] in fm.get_font_names(), f"Font {plt.rcParams['font.family']} is not available"

local_folder = Path("datatest")
github_folder = Path("https://raw.githubusercontent.com/dglee6257/Dataprocessing/main/datatest/")


def read_csv(path, **kwargs) -> pd.DataFrame:
    """read csv file from local folder if exists, otherwise from github folder"""
    try:
        df = pd.read_csv(local_folder / path, **kwargs)
    except FileNotFoundError:
        df = pd.read_csv(github_folder / path, **kwargs)
    return df


def read_excel(path, **kwargs) -> pd.DataFrame:
    """read csv file from local folder if exists, otherwise from github folder"""
    try:
        df = pd.read_excel(local_folder / path, **kwargs)
    except FileNotFoundError:
        df = pd.read_excel(github_folder / path, **kwargs)
    return df


class dotdict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = attrdict() or d = attrdict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def attr(obj):
    """Returns obj's state_types, callable_signatures, state_values, and callables_bounded"""
    all_attr = {}
    for attribute in dir(obj):
        if not attribute.startswith("_"):
            try:
                all_attr[attribute] = getattr(obj, attribute)
            except AttributeError:
                continue

    methods = dict([(k, v) for k, v in all_attr.items() if callable(v)])

    signatures = {}
    for k, v in all_attr.items():
        if callable(v):
            try:
                signatures[k] = inspect.signature(v)  # may occur ValueError
            except ValueError:
                signatures[k] = "No signature available for built-in method"

    state_keys = sorted(list(set(all_attr.keys()) - set(methods.keys())))
    state_types = dict([(k, type(getattr(obj, k))) for k in state_keys])
    state_values = dict([(k, getattr(obj, k)) for k in state_keys])

    return dotdict(state_types), dotdict(signatures), dotdict(state_values), dotdict(methods)
