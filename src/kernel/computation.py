'''
Created on 27 Feb 2020

@author: nish
'''
from ipykernel.kernelbase import Kernel
from risk.engine import RiskEngine

class RiskComputationKernel(Kernel):
    implementation = 'Risk Computation'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Atlantic Trading London Ltd. Risk Computation Kernel"
    
    def __init__(self, **kwargs):
        super(RiskComputationKernel, self).__init__(**kwargs)
        self.risk_engine = RiskEngine(product="sterling", scenario="BOE")

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            message = self._perform_check(code)
            stream_content = {'name': 'stdout', 'text': message}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        
        #perform execution here
        request = "".join(("self.risk_engine", ".", code, "()"))
        exec(request)
        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
    
    def _perform_check(self, code):
        if hasattr(self.risk_engine, code):
            message = "Sending request: {} to be executed on Kernel".format(code)
        else:
            raise AttributeError("Risk Kernel does not support the following method")
            message = "Risk Kernel does not support the following method: {}".format(code)
        return message
            