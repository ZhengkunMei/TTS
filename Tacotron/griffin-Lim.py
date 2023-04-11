import librosa

# 加载音频文件
y, sr = librosa.load('input.wav')

# 计算HOSA谱
n_fft = 2048  # 每个帧的FFT点数
hop_length = 512  # 帧移量
win_length = n_fft  # 窗口长度
n_hosa = 4  # HOSA的阶数
hosa = librosa.hosa(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=win_length, n_hosa=n_hosa)

# 显示HOSA谱
librosa.display.specshow(hosa, x_axis='time', y_axis='hosa', sr=sr, hop_length=hop_length)

