from functools import wraps


def check_null(args_to_check=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args_to_check:
                if any(arg is None for arg in args) or any(arg is None for arg in kwargs.values()):
                    return None
                return func(*args, **kwargs)

            for arg_name in args_to_check:
                if arg_name in kwargs:
                    if kwargs[arg_name] is None:
                        return None
                elif arg_name in func.__code__.co_varnames:
                    index = func.__code__.co_varnames.index(arg_name)
                    if args and len(args) > index:
                        arg_value = args[index]
                        if arg_value is None:
                            return None
                
            return func(*args, **kwargs)
        return wrapper
    return decorator
