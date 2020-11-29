from gidtools.gidfiles import pathmaker
import os
from timeit import Timer
from statistics import stdev, mean, median, mode, variance
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def a():
    x = pathmaker(THIS_FILE_DIR, '../')


def b():
    u = os.path.normpath(os.path.join(THIS_FILE_DIR, 'other_file'))


if __name__ == '__main__':
    t = Timer(a)
    tb = Timer(b)
    n = 100
    sig_pl = 3
    os_list = []
    gid_list = []
    for i in range(n):
        gid_list.append(t.timeit(1000000))
        os_list.append(tb.timeit(1000000))
        if (i + 1) % 1 == 0:
            print(f"{str(i+1)} rounds done")

    for name, _list in [('gid', gid_list), ('os', os_list)]:
        print('\n\n')
        print(f"{name} stdev: " + str(round(stdev(_list), sig_pl)))
        print(f"{name} mean: " + str(round(mean(_list), sig_pl)))
        print(f"{name} median: " + str(round(median(_list), sig_pl)))
        print(f"{name} mode: " + str(round(mode(_list), sig_pl)))
        print(f"{name} variance: " + str(round(variance(_list), sig_pl)))
        print(f"{name} max: " + str(round(max(_list), sig_pl)))
        print(f"{name} min: " + str(round(min(_list), sig_pl)))
        print('\n ############################## \n\n')
