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
    
    def __init__(self):
        self.risk_engine = RiskEngine(product="sterling", scenario="BOE")

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

# if __name__ == '__main__':
#     from ipykernel.kernelapp import IPKernelApp
#     IPKernelApp.launch_instance(kernel_class=RiskComputationKernel)