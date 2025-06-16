import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.font_manager import FontProperties

def print_available_noto_fonts():
    print("🔍 正在搜索已注册的 Noto 字体名：")
    found = False
    for font in fm.fontManager.ttflist:
        if 'Noto' in font.name or 'CJK' in font.name:
            print(f"✅ 注册字体名: {font.name} ({font.fname})")
            found = True
    if not found:
        print("⚠️ 未找到任何已注册的 Noto 字体")

def get_font_property():
    # 尝试用注册字体名
    preferred_fonts = ['Noto Sans CJK SC', 'NotoSansCJKsc', 'Noto Sans CJK SC Regular']
    for name in preferred_fonts:
        try:
            prop = FontProperties(family=name)
            # 通过 fontManager 找到文件路径
            if fm.findfont(prop, fallback_to_default=False):
                print(f"✅ 使用字体名: {name}")
                return prop
        except Exception as e:
            pass

    # 否则尝试通过文件路径加载
    font_path = os.path.expanduser("~/Library/Fonts/NotoSansCJKsc-Regular.otf")
    if os.path.exists(font_path):
        print(f"✅ 通过路径加载字体文件: {font_path}")
        return FontProperties(fname=font_path)
    else:
        print(f"❌ 字体文件路径不存在: {font_path}")
        return None

def draw_plot_with_chinese(font_prop):
    plt.figure(figsize=(6, 4))
    plt.title("中文字体测试：你好，世界", fontproperties=font_prop)
    plt.xlabel("横轴：时间", fontproperties=font_prop)
    plt.ylabel("纵轴：幅度", fontproperties=font_prop)
    plt.plot([0, 1, 2], [1, 4, 9], label="样例数据")
    plt.legend(prop=font_prop)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("font_test_result.png")
    print("✅ 图像已保存为 font_test_result.png")
    plt.show()

if __name__ == '__main__':
    print("== 检查字体安装 ==")
    print_available_noto_fonts()
    print("\n== 设置字体 ==")
    font_prop = get_font_property()
    if font_prop:
        print("\n== 绘图测试 ==")
        draw_plot_with_chinese(font_prop)
    else:
        print("❌ 无法设置中文字体，请检查字体是否安装成功")
