def des(fun):
    def start():
        print('start1')
        a = fun() + 5
        print('start2')
        return a
    def next():
        z = start()
        print(z)
        print('next1')
    return next

@des
def test():
    num = 1+1
    print(num)
    return num

test()