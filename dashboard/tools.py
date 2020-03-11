import threading


def is_color(x):
    '''
    True if a tuple of three or four ints is given
    :param x: the item
    :return: Boolean
    '''
    if type(x) is tuple:
        if 4 >= len(x) >= 3:
            for e in x:
                if type(e) is not int:
                    return False
            return True
    return False


def concurrent(func):
    '''
    For functions that run concurrently
    :param func:
    :return:
    '''
    def decorator(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return decorator