"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 18 Jul 2019
Author : nish

"""
import os
import json
import logging.config
from kernel.computation import RiskComputationKernel
from ipykernel.kernelapp import IPKernelApp

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
    log.info("Initialising Kernel For Risk Matrix Computation")
    try:
        IPKernelApp.launch_instance(kernel_class=RiskComputationKernel)
    except Exception as e:
        print(e)