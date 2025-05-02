import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys

def calculate_wavelength(fringes, positions):
    """
    使用线性拟合计算波长
    
    参数:
    fringes -- 干涉环圈数列表
    positions -- 位移距离列表 (mm)
    
    返回:
    wavelength -- 计算得到的波长(nm)
    wavelength_uncertainty -- 波长标准不确定度(nm)
    r_squared -- 拟合优度R²
    """
    # 转换为numpy数组以便进行计算
    fringes = np.array(fringes)
    positions = np.array(positions)
    
    # 线性回归拟合
    slope, intercept, r_value, p_value, std_err = stats.linregress(fringes, positions)
    
    # 波长 = 斜率 * 2 * 1000000 (转换为纳米)
    wavelength = slope * 2 * 1000000
    
    # 计算A类不确定度 - 斜率的标准不确定度转换为波长的不确定度
    wavelength_uncertainty_A = std_err * 2 * 1000000
    
    # 计算B类不确定度 - 假设读数不确定度为0.0001mm，k=2
    reading_uncertainty = 0.0001 / 2
    wavelength_uncertainty_B = reading_uncertainty * 2 * 1000000 / (max(fringes) - min(fringes))
    
    # 合成标准不确定度
    combined_uncertainty = np.sqrt(wavelength_uncertainty_A**2 + wavelength_uncertainty_B**2)
    
    # 扩展不确定度(k=2, P=95%)
    expanded_uncertainty = 2 * combined_uncertainty
    
    r_squared = r_value**2
    
    return wavelength, expanded_uncertainty, slope, std_err, r_squared

def plot_data_and_fit(fringes, positions, slope, intercept, wavelength, wavelength_uncertainty, r_squared):
    """绘制数据点和拟合直线"""
    plt.figure(figsize=(10, 6))
    
    # 绘制原始数据点
    plt.scatter(fringes, positions, color='blue', label='实验数据')
    
    # 绘制拟合直线
    x_fit = np.linspace(min(fringes), max(fringes), 100)
    y_fit = slope * x_fit + intercept
    plt.plot(x_fit, y_fit, color='red', label='线性拟合')
    
    # 添加标签和标题
    plt.xlabel('干涉环圈数')
    plt.ylabel('镜面位移 (mm)')
    plt.title('迈克尔逊干涉实验数据分析')
    
    # 在图中添加拟合结果
    result_text = f"波长 = {wavelength:.2f} ± {wavelength_uncertainty:.2f} nm\n"
    result_text += f"斜率 = {slope:.8f} mm/圈\n"
    result_text += f"R² = {r_squared:.6f}"
    plt.annotate(result_text, xy=(0.05, 0.95), xycoords='axes fraction', 
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                 va='top')
    
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()

def process_data():
    print("=" * 50)
    print("迈克尔逊干涉实验数据处理程序")
    print("=" * 50)
    
    # 获取数据输入方式
    print("\n请选择数据输入方式:")
    print("1. 一对一输入圈数和位置")
    print("2. 批量输入多组数据")
    
    choice = input("请输入选择 (1 或 2): ")
    
    fringes = []
    positions = []
    
    if choice == '1':
        # 一对一输入
        print("\n请输入数据 (每行输入一组'圈数 位置'，输入空行结束):")
        print("例如：0 0.09212")
        
        while True:
            line = input().strip()
            if not line:  # 空行结束输入
                break
                
            try:
                parts = line.split()
                fringe = float(parts[0])
                position = float(parts[1])
                fringes.append(fringe)
                positions.append(position)
                print(f"已添加: 圈数={fringe}, 位置={position}mm")
            except:
                print("输入格式错误，请重新输入")
    
    elif choice == '2':
        # 批量输入
        print("\n请输入圈数数据 (用空格分隔):")
        fringes_input = input().strip()
        fringes = [float(f) for f in fringes_input.split()]
        
        print("请输入对应的位置数据 (用空格分隔)，单位mm:")
        positions_input = input().strip()
        positions = [float(p) for p in positions_input.split()]
        
        # 检查数据长度是否一致
        if len(fringes) != len(positions):
            print("错误：圈数和位置的数据点数量不一致")
            return
    
    else:
        print("无效选择，程序退出")
        return
    
    # 检查数据点数量
    if len(fringes) < 2:
        print("错误：至少需要2个数据点进行拟合")
        return
    
    print("\n输入的数据:")
    print("序号  圈数     位置(mm)")
    print("-" * 25)
    for i, (f, p) in enumerate(zip(fringes, positions)):
        print(f"{i+1:<5} {f:<8} {p:<10.6f}")
    
    # 计算波长
    wavelength, wavelength_uncertainty, slope, std_err, r_squared = calculate_wavelength(fringes, positions)
    
    # 显示结果
    print("\n=== 计算结果 ===")
    print(f"斜率 = {slope:.8f} ± {std_err:.8f} mm/圈")
    print(f"波长 = {wavelength:.2f} ± {wavelength_uncertainty:.2f} nm (k=2, P=95%)")
    print(f"R² = {r_squared:.6f}")
    
    # 显示不确定度计算过程
    print("\n=== 不确定度分析 ===")
    print("1. 标准差计算")
    print("2. 总体标准不确定度")
    print(f"3. 扩展不确定度(k=2, P=95%): {wavelength_uncertainty:.2f} nm")
    
    # 绘制图形
    fig = plot_data_and_fit(fringes, positions, slope, intercept=0, 
                           wavelength=wavelength, wavelength_uncertainty=wavelength_uncertainty, 
                           r_squared=r_squared)
    
    # 显示图形
    plt.show()
    
    # 询问是否保存图形
    save_choice = input("\n是否保存分析图形？(y/n): ")
    if save_choice.lower() == 'y':
        filename = input("请输入保存的文件名(默认为'michelson_analysis.png'): ")
        if not filename:
            filename = 'michelson_analysis.png'
        fig.savefig(filename, dpi=300)
        print(f"图形已保存为: {filename}")

    print("\n处理完成!")

if __name__ == "__main__":
    process_data()