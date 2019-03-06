import os
import pandas as pd
import glob

def get_data():
    # ディレクトリの移動
    first_dir = os.getcwd() 
    to_dir = first_dir + "/応答確認/"
    os.chdir(to_dir)

    # txtファイル一覧取得
    data_file_names = glob.glob("*/result_files/*.txt")
    
    col_name_list = []
    # 全部くっつけたcsvファイルとして出力
    for index, data_file_name in enumerate(data_file_names):
        # カラムの名前を設定する
        col_name = data_file_name.split("/")
        col_name_len = len(col_name)
        file_name = col_name[col_name_len - 1]
        file_name_row = file_name.split("_")
        file_name_row[len(file_name_row) - 1] = file_name_row[len(file_name_row) - 1].split(".")[0]
        file_name = file_name_row[2] + "_" + file_name_row[3]
        col_name_list.append(file_name)
        # txtファイルを読み込み、くっつけていく
        if index == 0:
            df = pd.read_csv(data_file_name, delimiter="\t")
            df = df.rename(columns={'potentials(V)': file_name})
        else:
            new_df = pd.read_csv(data_file_name, delimiter="\t")
            df[file_name] = new_df["potentials(V)"]

    os.chdir(first_dir)
    df.to_csv("all_result.csv", index=False)
    return df, col_name_list
    
    
if __name__ == "__main__":
    df = get_data()
    print("success")
    print(df[0].size)