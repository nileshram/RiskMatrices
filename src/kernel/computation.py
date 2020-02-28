'''
Created on 27 Feb 2020

@author: nish
'''
from ipykernel.kernelbase import Kernel
from risk.engine import RiskEngine
from kernel.handler import StreamHandler

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
        self.stream_handler = StreamHandler()

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            stream_content = self.stream_handler.create_ack(code)
            self.send_response(self.iopub_socket, 'stream', stream_content)
        
        #perform execution here
        if hasattr(self.risk_engine, code):
            request = "".join(("self.risk_engine", ".", code, "()"))
            exec(request)
            response = self.stream_handler.generate_ok_response(self.execution_count)
            success_message = self.stream_handler.create_success_message(code)
            self.send_response(self.iopub_socket, 'stream', success_message)
        else:
            response = self.stream_handler.generate_error_response(self.execution_count)
            error_message = self.stream_handler.create_error_message(code)
            self.send_response(self.iopub_socket, 'stream', error_message)
        return response

    def do_shutdown(self, restart):
        del self.risk_engine
        del self.stream_handler
        self.shell.exit_now = True
        return dict(status='ok', restart=restart)

            