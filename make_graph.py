from integrate_data import get_data
import matplotlib.pyplot as plt
import re

# グローバル変数
LEGEND_FONT_SIZE = 14
POTENTIAL_YLIM = [10e-8, 10e3]
RATE_YLIM = [-50, 10]
LABEL_SIZE = 20


# 凡例を作成
def make_legend(col_name_all):
    height_list = ["height500", "height10", "height20", "height50", "height4", "height0",]
    loop_types = ["looptype1", "looptype2", "looptype3"]
    loop_type_detail = {"looptype1": "3x3", "looptype2": "10x10", "looptype3": "20x5"}
    graph_label = {}
    for col_name in col_name_all:
        for height in height_list:
            if height in col_name:
                label = col_name.replace(height, re.match('.*?(\d+)', height).group(1) + "m")
                break

        for loop_type in loop_types:
            if loop_type in label:
                label = label.replace(loop_type, loop_type_detail[loop_type])

        label = label.replace("_", " ")
        label = label.replace(re.search("devide.*", label).group(), "")

        graph_label[col_name] = label
        
    return graph_label

# looptype, 高度比較
def compare_height(df, col_name_all, loop_type, legend):
    base_label = "height500_" + loop_type + "_devide"
    if loop_type == "looptype3":
        base_label += "40x10"
    else:
        base_label += "20x20"
    base = df[base_label]
    col_name_loop_type = [col_name for col_name in col_name_all if loop_type in col_name]
    col_name_loop_type.sort()
    fig = plt.figure(figsize=(20,10),dpi=200)
    fig.subplots_adjust(wspace=0.25)
    ax1 = fig.add_subplot(1, 2, 1) 
    for col_name in col_name_loop_type:
        ax1.plot(df["time(ms)"], df[col_name], label=legend[col_name])

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
    ax1.set_ylabel("EMF[V]", fontsize = LABEL_SIZE*1.2)
    ax1.set_ylim(POTENTIAL_YLIM[0], POTENTIAL_YLIM[1])
    ax1.legend(fontsize=LEGEND_FONT_SIZE)
    ax1.grid(linewidth = 0.5, linestyle='--', which="both")
    ax1.tick_params(labelsize = LABEL_SIZE)

    ax2 = fig.add_subplot(1, 2, 2)
    for col_name in col_name_loop_type:
        rate_of_change = 100*((df[col_name]-base)/base)
        ax2.plot(df["time(ms)"], rate_of_change, label=legend[col_name])

    ax2.set_xscale("log")
    ax2.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
    ax2.set_ylabel("Rate of change[%]", fontsize = LABEL_SIZE*1.2)
    ax2.set_ylim(RATE_YLIM[0], RATE_YLIM[1])
    ax2.legend(fontsize=LEGEND_FONT_SIZE)
    ax2.grid(linewidth = 0.5, linestyle='--', which="both")
    ax2.tick_params(labelsize = LABEL_SIZE)
    
    fig.suptitle('{}'.format(loop_type), fontsize=16)
    fig.savefig("{}.png".format(loop_type))
    
# 3種類ループ×6種類高度
def output_graph_all(df, col_name_all, legend):
    fig = plt.figure(figsize=(10,10),dpi=200)
    fig.subplots_adjust(wspace=0.25)
    ax1 = fig.add_subplot(1, 1, 1) 
    for col_name in col_name_all:
        ax1.plot(df["time(ms)"], df[col_name], label=legend[col_name])

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
    ax1.set_ylabel("EMF[V]", fontsize = LABEL_SIZE*1.2)
    ax1.set_ylim(POTENTIAL_YLIM[0], POTENTIAL_YLIM[1])
    ax1.legend(fontsize=LEGEND_FONT_SIZE)
    ax1.grid(linewidth = 0.5, linestyle='--', which="both")
    ax1.tick_params(labelsize = LABEL_SIZE)
    fig.savefig("all.png")
    
# 曳航高度ごとの変化率の比較
def compare_looptype(df, col_name_all, legend):
    height_list = ["0", "4", "10", "20", "50"]
    for height in height_list:
        # 500を削除
        col_name_all = [col_name for col_name in col_name_all if not "500" in col_name]
        col_name_flag = "height" + height
        col_height_name = [col_name for col_name in col_name_all if col_name_flag in col_name]
        fig = plt.figure(figsize=(20, 10),dpi=200)
        fig.subplots_adjust(wspace=0.25)
        ax1 = fig.add_subplot(1, 2, 1)
        for col_name in col_height_name:
            ax1.plot(df["time(ms)"], df[col_name], label=legend[col_name])
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
        ax1.set_ylabel("EMF[V]", fontsize = LABEL_SIZE*1.2)
        ax1.set_ylim(POTENTIAL_YLIM[0], POTENTIAL_YLIM[1])
        ax1.legend(fontsize=LEGEND_FONT_SIZE)
        ax1.grid(linewidth = 0.5, linestyle='--', which="both")
        ax1.tick_params(labelsize = LABEL_SIZE)
            
        ax2 = fig.add_subplot(1, 2, 2) 
        for col_name in col_height_name:
            base = col_name.replace("height"+height, "height500")
            ax2.plot(df["time(ms)"], 100*(df[col_name] - df[base])/df[base], label=legend[col_name])
            
        ax2.set_xscale("log")
        ax2.set_ylim(RATE_YLIM[0], RATE_YLIM[1])
        ax2.grid(linewidth = 0.5, linestyle='--', which="both")
        ax2.legend(fontsize=LEGEND_FONT_SIZE)
        ax2.tick_params(labelsize = LABEL_SIZE)
        ax2.set_ylabel("Rate of change[%]", fontsize = LABEL_SIZE*1.2)
        ax2.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
        fig.savefig("{}.png".format("height"+height+"m"))
        
def compare_old_new_equipment(df, col_name_all, legend):
    base_old = "height500_looptype1_devide20x20"
    current_equipment = "height4_looptype1_devide20x20"
    base_new = "height500_looptype3_devide40x10"
    col_compare_list = [col_name for col_name in col_name_all if "looptype3" in col_name]
    col_compare_list.append(current_equipment)
    col_compare_list = [col_name for col_name in col_compare_list if not "height0" in col_name]
    fig = plt.figure(figsize=(20,10),dpi=200)
    fig.subplots_adjust(wspace=0.25)
    ax1 = fig.add_subplot(1, 2, 1)
    for col_name in col_compare_list:
        ax1.plot(df["time(ms)"], df[col_name], label=legend[col_name])

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("time[ms]")
    ax1.set_ylabel("EMF[V]")
    ax1.legend(fontsize=LEGEND_FONT_SIZE)
    ax1.set_ylim(POTENTIAL_YLIM[0], POTENTIAL_YLIM[1])
    ax1.grid(linewidth = 0.5, linestyle='--', which="both")
    ax1.tick_params(labelsize = LABEL_SIZE)

    ax2 = fig.add_subplot(1, 2, 2)
    base_change_rate = 100*(df[current_equipment] - df[base_old]) / df[base_old]

    for col_name in col_compare_list:
        if "looptype3" in col_name:
            change_rate = 100*(df[col_name] - df[base_new]) / df[base_new]
        else:
            change_rate = base_change_rate
        ax2.plot(df["time(ms)"], change_rate, label=legend[col_name])

    ax2.set_xscale("log")
    ax2.set_xlabel("time[ms]", fontsize = LABEL_SIZE*1.2)
    ax2.set_ylabel("Rate of change[%]", fontsize = LABEL_SIZE*1.2)
    ax2.legend(fontsize=LEGEND_FONT_SIZE)
    ax2.set_ylim(RATE_YLIM[0], RATE_YLIM[1])
    ax2.grid(linewidth = 0.5, linestyle='--', which="both")
    ax2.tick_params(labelsize = LABEL_SIZE)
    fig.savefig("compare_new_old_looptype.png")
    
    
if __name__=="__main__":
    # 計算データの取得
    df, col_name_list = get_data()
    
    # ループタイプの名称
    loop_types = ["looptype1", "looptype2", "looptype3"]
    
    # 5×20の分割を削除
    col_name_all = [col_name for col_name in col_name_list if not col_name.endswith("devide5x20")]
    col_name_all.sort()
    
    # 凡例の作成
    legend = make_legend(col_name_all)
    
    # 全ての計算結果を同じグラフに出力
    output_graph_all(df, col_name_all, legend)
    
    # looptypeごとに曳航高度比較のグラフ出力
    for loop_type in loop_types:
        compare_height(df, col_name_all, loop_type, legend)
        
    # 高さごとにlooptype比較のグラフ出力
    compare_looptype(df, col_name_all, legend)
    
    compare_old_new_equipment(df, col_name_all, legend)