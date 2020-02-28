'''
Created on 28 Feb 2020

@author: nish
'''

class StreamHandler:
    """
    Class docs: This message handling class is for the 
    messages on the shell ROUTER/DEALER sockers
    """
    
    def __init__(self):
        self.valid_fields = ['status', 'name', 'text', 'payload']
    
    def check_class_method(self, obj, method):
        if hasattr(obj, method):
            message = "sending request: {} to be executed on the kernel\n".format(method)
        else:
            message = "kernel does not support the method: {} - please check\n".format(method)
        return message
    
    @staticmethod
    def create_ack(request):
        message = "received request to execute: {} on kernel\n".format(request)
        stream_content = {"name" : "stdout",
                          "text" : message}
        return stream_content

    @staticmethod
    def create_error_message(request):
        message = "could not send request to execute: {} on kernel\n".format(request)
        stream_content = {"name" : "stdout",
                          "text" : message}
        return stream_content
        
    @staticmethod
    def create_success_message(request):
        message = "successfully executed request on kernel\n".format(request)
        stream_content = {"name" : "stdout",
                          "text" : message}
        return stream_content
    
    @staticmethod
    def create_empty_stream():
        stream_content = {"name" : "",
                          "ename" : "",
                          "evalue" : "",
                          "traceback" : ""}
        
        return stream_content
    
    @staticmethod
    def create_empty_reponse(execution_count):
        response = {'status': '',
                # The base class increments the execution count
                'execution_count': execution_count,
                'user_expressions': {},
               }
        return response

    @staticmethod
    def generate_ok_response(execution_count):
        response = StreamHandler.create_empty_reponse(execution_count)
        response['status'] = 'ok'
        return response

    @staticmethod
    def generate_error_response(execution_count):
        response = StreamHandler.create_empty_reponse(execution_count)
        response['status'] = 'error'
        response['evalue'] = 'AttributeError'
        return response

    

    
    
    