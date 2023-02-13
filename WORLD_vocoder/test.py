import pyworld as pw
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import os
import soundfile as sf




# 提取语音特征
x, fs = sf.read('normal_woman.wav')

# f0 : ndarray
#     F0 contour. 基频等高线
# sp : ndarray
#     Spectral envelope. 频谱包络
# ap : ndarray
#     Aperiodicity. 非周期性
f0, sp, ap = pw.wav2world(x, fs)    # use default options


#分布提取参数
#使用DIO算法计算音频的基频F0

_f0, t = pw.dio( x, fs, f0_floor= 50.0, f0_ceil= 600.0, channels_in_octave= 2, frame_period=pw.default_frame_period)

#使用CheapTrick算法计算音频的频谱包络

_sp = pw.cheaptrick( x, _f0, t, fs)

#计算aperiodic参数

_ap = pw.d4c( x, _f0, t, fs)

#基于以上参数合成音频

_y = pw.synthesize(_f0, _sp, _ap, fs, pw.default_frame_period)

#写入音频文件

sf. write( 'D:\\output.wav', _y, fs)


plt.plot(f0)
plt.show()
plt.imshow(np.log(sp), cmap='gray')
plt.show()
plt.imshow(ap, cmap='gray')

# 合成原始语音
synthesized = pw.synthesize(f0, sp, ap, fs, pw.default_frame_period)

# 1.输出原始语音
sf.write('D:\\output.wav', synthesized, fs)

# 2.变高频-更类似女性
high_freq = pw.synthesize(f0*2.0, sp, ap, fs)  # 周波数を2倍にすると1オクターブ上がる

sf.write('D:\\output_women.wav', high_freq, fs)

# 3.直接修改基频，变为机器人发声
robot_like_f0 = np.ones_like(f0)*100  # 100は適当な数字
robot_like = pw.synthesize(robot_like_f0, sp, ap, fs)

sf.write('D:\\output_robot.wav', robot_like, fs)

# 4.提高基频，同时频谱包络后移？更温柔的女性？
female_like_sp = np.zeros_like(sp)
for f in range(female_like_sp.shape[1]):
    female_like_sp[:, f] = sp[:, int(f/1.2)]
female_like = pw.synthesize(f0*2, female_like_sp, ap, fs)

sf.write('D:\\output_gentle.wav', female_like, fs)


