import random
from datetime import datetime, timedelta
import os

# 用户参数
duration_minutes = 10  # 采样时长（分钟）
interval_seconds = 3  # 采样间隔（秒）
total_samples = (duration_minutes * 60) // interval_seconds

# 生成随机用户信息
user_id = f"U{random.randint(1000, 9999)}"
gender = random.choice(["男", "女"])
age = random.randint(18, 90)

# 生成血氧数据
spo2_values = []
base_spo2 = random.uniform(96.0, 99.0)

for _ in range(total_samples):
    # 让血氧值更稳定，减少极端值
    fluctuation = random.gauss(0, 0.8)  # 以 0 为均值，标准差 0.8
    current_spo2 = base_spo2 + fluctuation

    # 限制血氧值在合理范围
    current_spo2 = max(90.0, min(100.0, current_spo2))
    spo2_values.append(round(current_spo2, 1))

# 生成时间序列
start_time = datetime.now().replace(microsecond=0)
timestamps = [start_time + timedelta(seconds=i * interval_seconds) for i in range(total_samples)]

# 选择保存路径
save_dir = "spo2_data"
os.makedirs(save_dir, exist_ok=True)
filename = os.path.join(save_dir, f"血氧数据_{user_id}.txt")

# 写入文件
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"用户ID: {user_id}\n")
    f.write(f"性别: {gender}\n")
    f.write(f"年龄: {age}\n\n")
    f.write("采样时间,血氧值(%)\n")

    for time, value in zip(timestamps, spo2_values):
        f.write(f"{time.strftime('%H:%M:%S')}, {value}\n")

print(f"数据已成功生成到文件: {filename}")
