
'''
create exceptions based on your inputs.
Capture and handle system exceptions
Create custom user-based exceptions
'''


'''
These are some of the inbuilt exceptions in Python
ArithmeticError	    Raised when numeric calculations fails
    OverflowError	    Raised when result of an arithmetic operation is too large to be represented
    FloatingPointError	Raised when a floating point calculation fails
    ZeroDivisionError	Raised when division or modulo by zero takes place for all numeric types
AssertionError	    Raised when Assert statement fails
ImportError	        Raised when the imported module is not found
IndexError	        Raised when index of a sequence is out of range
KeyboardInterrupt	Raised when the user interrupts program execution, generally by pressing Ctrl+c
IndentationError	Raised when there is incorrect indentation
SyntaxError	        Raised by parser when syntax error is encountered
KeyError	        Raised when the specified key is not found in the dictionary
NameError	        Raised when an identifier is not found in the local or global namespace
TypeError	        Raised when a function or operation is applied to an object of incorrect type
ValueError	        Raised when a function gets argument of correct type but improper value
IOError	            Raised when an input/ output operation fails
RuntimeError	    Raised when a generated error does not fall into any category
'''

class ApplicationException(Exception):
    """Base class for exceptions in this module."""
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    pass


class UnAcceptedLenError(ApplicationException):
    """
    give the data as input to the exception
    """
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)



def exception_handler(exc_type, logger, silence=False):
    def handler_wrapper(func):
        @functools.wraps(func)
        def handle_exception(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exc_type as e:
                logger.error('Error in {}() : {}'.format(func.__name__, str(e)))
                if silence:
                    return None
                raise e
            return result

        return handle_exception

    return handler_wrapper