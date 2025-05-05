import matplotlib
matplotlib.use('TkAgg')  # 可能需要 'Qt5Agg' 视情况而定
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tkinter import Tk, filedialog
from datetime import datetime
import re

# 初始化文件选择对话框
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="选择血氧数据文件",
    filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
)
root.destroy()

if not file_path:
    print("未选择文件，程序退出")
    exit()


# 读取数据文件
def parse_data(filepath):
    data = {
        'user_id': '未知',
        'gender': '未知',
        'age': '未知',
        'timestamps': [],
        'spo2_values': []
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        # 解析用户信息
        for line in f:
            if line.startswith('用户ID:'):
                data['user_id'] = line.split(': ')[1].strip()
            elif line.startswith('性别:'):
                data['gender'] = line.split(': ')[1].strip()
            elif line.startswith('年龄:'):
                data['age'] = line.split(': ')[1].strip()
            elif re.match(r'\d{2}:\d{2}:\d{2}', line):  # 检测到时间数据行
                break

        # 解析数据部分
        for line in f:
            if ',' in line:
                time_str, value_str = line.strip().split(',')
                data['timestamps'].append(
                    datetime.strptime(time_str.strip(), "%H:%M:%S")
                )
                data['spo2_values'].append(float(value_str.strip()))

    return data


# 解析数据
try:
    dataset = parse_data(file_path)
except Exception as e:
    print(f"文件解析失败: {str(e)}")
    exit()

# 配置可视化参数
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表
fig, ax = plt.subplots(figsize=(12, 6))

# 转换时间格式
times = mdates.date2num(dataset['timestamps'])

# 绘制主曲线
ax.plot(times, dataset['spo2_values'],
        color='#e74c3c',
        linewidth=1.5,
        marker='o',
        markersize=5,
        markerfacecolor='white',
        markeredgewidth=1.5)

# 设置时间轴格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=15))
plt.xticks(rotation=45)

# 设置纵轴范围
plt.ylim(90, 100)

# 添加用户信息框
info_text = f"用户ID: {dataset['user_id']}\n性别: {dataset['gender']}\n年龄: {dataset['age']}"
ax.text(0.98, 0.95, info_text,
        transform=ax.transAxes,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# 添加图表元素
plt.title("血氧饱和度动态监测曲线", pad=20, fontsize=14)
plt.xlabel("采样时间", labelpad=10)
plt.ylabel("血氧饱和度 (%)", labelpad=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 自动调整布局
plt.tight_layout()

# 可选保存图表
save_path = f"血氧曲线_{dataset['user_id']}.png"
fig.savefig(save_path, dpi=300)
print(f"图表已成功保存到 {save_path}")

# 显示图表
plt.show()
