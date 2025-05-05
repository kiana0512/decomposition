"""
相关信号应用仿真 - 时延估计（最终修正版）
包含理论分析的代码注释和结果可视化
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# ========================= 参数设置 =========================
fs = 1000           # 采样率 (Hz)，决定时间分辨率
T = 1               # 信号时长 (s)，影响频率分辨率
t = np.arange(0, T, 1/fs)  # 时间序列
f0 = 10             # 基频 (Hz)，控制信号变化速率
D_true = 0.25       # 真实时延 (s)，用于验证算法精度
SNR = 10            # 信噪比 (dB)，控制噪声水平

# ======================== 信号生成模块 ========================
# 使用线性调频信号(LFM)因其良好的自相关特性：
x = np.sin(2 * np.pi * f0 * t * t)  # 频率随时间平方增长

# 生成接收信号（时延+噪声）：
delay_samples = int(D_true * fs)
y = np.roll(x, delay_samples)

# 添加高斯白噪声：
signal_power = np.mean(y**2)
noise_power = signal_power / (10 ** (SNR / 10))
noise = np.random.normal(0, np.sqrt(noise_power), len(y))
y += noise

# ====================== 互相关计算模块 =======================
corr = correlate(y, x, mode='full')
lags = np.arange(-len(x)+1, len(x))

# ====================== 时延估计模块 ========================
max_index = np.argmax(corr)
D_estimated = lags[max_index] / fs

# ====================== 结果可视化模块 ======================
# 解决方案1：使用非交互式后端（推荐用于脚本运行）
import matplotlib
matplotlib.use('Agg')  # 设置为非交互式后端
# 设置matplotlib的字体属性，使其支持中文显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 重新创建图形对象
plt.figure(figsize=(12, 10))

# 子图1：原始信号对比
plt.subplot(3, 1, 1)
plt.plot(t, x, label='发射信号')
plt.plot(t, y, label='接收信号（含噪声）', alpha=0.7)
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.title(f'原始信号对比 (SNR={SNR}dB)')
plt.legend()
plt.grid(True)

# 子图2：完整互相关函数
plt.subplot(3, 1, 2)
plt.plot(lags/fs, corr)
plt.axvline(D_estimated, color='r', linestyle='--',
           label=f'估计时延: {D_estimated:.3f}s')
plt.xlabel('滞后时间 (s)')
plt.ylabel('相关系数')
plt.title('互相关函数')
plt.legend()
plt.grid(True)

# 子图3：峰值区域放大
plt.subplot(3, 1, 3)
window = 50
plt.plot(lags[max_index-window:max_index+window]/fs,
        corr[max_index-window:max_index+window],
        'b-o', markersize=4)
plt.axvline(D_true, color='g', linestyle='--',
           label=f'真实时延: {D_true}s')
plt.axvline(D_estimated, color='r', linestyle=':',
           label='估计时延')
plt.xlabel('滞后时间 (s)')
plt.ylabel('相关系数')
plt.title('峰值区域放大（分辨率分析）')
plt.legend()
plt.grid(True)

plt.tight_layout()

# ==================== 结果输出与保存 ====================
# 解决方案2：直接保存图像文件（避免显示操作）
output_path = 'correlation_result.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()  # 显式关闭图形

print(f"[运行结果已保存至 {output_path}]")
print("[时延估计结果]")
print(f"真实时延: {D_true:.3f} s")
print(f"估计时延: {D_estimated:.3f} s")
print(f"绝对误差: {abs(D_true - D_estimated):.5f} s")
print(f"理论分辨率: {1/fs:.3f} s")

"""
关键修改说明：
1. 强制使用非交互式后端（'Agg'），避免GUI相关错误
2. 使用savefig直接保存图像，不进行屏幕显示
3. 添加了plt.close()确保内存释放
4. 输出结果包含图像保存路径信息

运行方式：
1. 在命令行直接执行：
   python your_script.py
2. 在Jupyter中需要移除matplotlib.use('Agg')设置
3. 生成的correlation_result.png包含完整分析结果
"""