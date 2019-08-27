# coding=utf-8
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # data
    resolution = [640, 1080, 2160, 3240, 4320, 5400]
    time_c = [0.1301220000, 0.3745460000, 1.6027140000, 3.7148040000, 6.7814290000, 10.7174690000]
    time_p = [0.437288045883, 0.84491610527, 2.92119812965, 6.4361000061, 11.2685480118, 17.6098928452]

    plt.plot(resolution, time_c, label='c++ time')
    plt.plot(resolution, time_p, label='python time')
    plt.xlabel('resolution(pixel)')
    plt.ylabel('time(second)')
    plt.legend()
    plt.show()
