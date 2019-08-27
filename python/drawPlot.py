# coding=utf-8
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # data
    resolution = [640, 1080, 2160, 3240, 4320, 5400]
    time_c = [0.1301220000, 0.3745460000, 1.6027140000, 3.7148040000, 6.7814290000, 10.7174690000]
    time_p = [0.437288045883, 0.84491610527, 2.92119812965, 6.4361000061, 11.2685480118, 17.6098928452]
    time_myfij = [1.48796010017, 1.89210796356, 3.82191801071, 7.24730587006, 11.8356029987, 17.7910351753]
    time_speedup = [0.436141014099, 0.865988016129, 2.9277279377, 6.43741798401, 11.252366066, 17.5700788498]

    plt.figure(1)
    plt.plot(resolution, time_c, label='c++ time')
    plt.plot(resolution, time_p, label='python time')
    plt.xlabel('resolution(pixel)')
    plt.ylabel('time(second)')
    plt.legend()

    plt.figure(2)
    plt.plot(resolution, time_myfij, label='My Fij time')
    plt.plot(resolution, time_speedup, label='SpeedUp time')
    plt.xlabel('resolution(pixel)')
    plt.ylabel('time(second)')
    plt.legend()

    plt.figure(3)
    plt.plot(resolution, time_c, label='C++ time')
    plt.plot(resolution, time_myfij, label='My Fij time')
    plt.plot(resolution, time_speedup, label='SpeedUp time')
    plt.xlabel('resolution(pixel)')
    plt.ylabel('time(second)')
    plt.legend()
    plt.show()
