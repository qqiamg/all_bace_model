import taichi as ti

# ti.cfg.arch = ti.cuda # Run on GPU by default
# #
# n = 320
# pixels = ti.var(dt=ti.f32, shape=(n * 2, n))
#
# @ti.func
# def complex_sqr(z):
#   return ti.Vector([z[0] * z[0] - z[1] * z[1], z[1] * z[0] * 2])
#
# @ti.kernel
# def paint(t: ti.f32):
#   for i, j in pixels: # Parallized over all pixels
#     c = ti.Vector([-0.8, ti.sin(t) * 0.2])
#     z = ti.Vector([float(i) / n - 1, float(j) / n - 0.5]) * 2
#     iterations = 0
#     while z.norm() < 20 and iterations < 50:
#       z = complex_sqr(z) + c
#       iterations += 1
#     pixels[i, j] = 1 - iterations * 0.02
#
# gui = ti.GUI("Fractal", (n * 2, n))
#
# for i in range(1000000):
#   paint(i * 0.03)
#   gui.set_image(pixels)
#   gui.show()

# @ti.kernel
# def fill():
#   for i in range(10): # parallelized
#     x[i] += i
#
#     s = 0
#     for j in range(5): # serialized in each parallel thread
#       s += j
#     y[i] = s

# x = ['','','']
# @ti.kernel
# def fill_3d():
#     # Parallelized for all 3 <= i < 8, 1 <= j < 6, 0 <= k < 9
#     for i,j in ti.ndrange((3, 8),9):
#         print(i)
#         print(j)
#         # print(k)
#         # x[i, j, k] = i + j + k
#
# fill_3d()


ti.cfg.arch = ti.cuda # Run on GPU by default
#
n = 320
pixels = ti.var(dt=ti.f32, shape=(n * 2, n))
# @ti.kernel
# def f():
#     print(pixels)
# f()

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


