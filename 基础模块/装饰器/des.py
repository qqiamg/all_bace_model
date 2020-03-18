#例子1
def des(fun):
    def start():
        print('start1')
        a = fun() + 5
        print('start2')
        return a
    def next():
        z = start()
        # z = 'a'
        print(z)
        print('next1')
    return next

@des
def test():
    num = 1+1
    print(num)
    return num

test()

import functools
print("++++++++++++++++++++++++++++++")
#例子2
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        print('args = {}'.format(*args))
        return func(*args, **kwargs)

    return wrapper

@log
def test(p):
    print(test.__name__ + " param: " + p)

test("I'm a param")

#例子3
import functools

print("++++++++++++++++++++++++++++++")
def log_with_param(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('call %s():' % func.__name__)
            print('args = {}'.format(*args))
            print('log_param = {}'.format(text))
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_with_param("param")
def test_with_param(p):
    print(test_with_param.__name__)

test_with_param("I'm a param")