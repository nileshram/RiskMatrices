"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 22 Jul 2019
Author : nish

"""
from os import path
from os.path import dirname

PROJECT_BASE = dirname(dirname(dirname(__file__)))
RISK = path.join(PROJECT_BASE, "docs", "ice_result_set.csv")
CONFIG = path.join(PROJECT_BASE, "conf", "config.json")
LOG = path.join(PROJECT_BASE, "conf", "log_config.json")
SQL = path.join(PROJECT_BASE, "sql", "short_end_portfolio_data.sql")
