"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 18 Jul 2019
Author : nish

"""
import os
import json
import logging.config
from risk.engine import RiskEngine

def _configure_log():
    logconfjson = os.path.join("conf", "log_config.json")
    if os.path.exists(logconfjson) and os.path.isfile(logconfjson):
        with open(logconfjson, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config["log"])
    else:
        logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    _configure_log()
    log = logging.getLogger("risk_matrix_log")
    log.info("Initialising Program For Risk Matrix Computation")
    
    try:
        risk_engine = RiskEngine()
        risk_engine.run_pricing()
    except Exception as e:
        print(e)