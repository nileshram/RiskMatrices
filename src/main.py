'''
Created on 22 Apr 2020

@author: nilesh
'''
from risk.engine import RiskEngine 


if __name__ == "__main__":
    risk_engine = RiskEngine(product="sterling", scenario="steepener")
    #compute risk matrices
    total_portfolio_matrix = risk_engine.run_pricing_and_risk()
#     #extract the heatplot figures from model
#     w_portfolio_matrix = risk_engine._models["w"]["graph"]
#     m_portfolio_matrix = risk_engine._models["m"]["graph"]
#     g_portfolio_matrix = risk_engine._models["g"]["graph"]
#     b_portfolio_matrix = risk_engine._models["b"]["graph"]
#     portfolio_matrix = risk_engine._models["all"]["graph"]

    