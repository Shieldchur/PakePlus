import pandas as pd
import tkinter as tk
from tkinter import messagebox

# 读取文件
file_path = '分数位次转换.xlsx'
try:
    df = pd.read_excel(file_path)
    df = df.sort_values(by=['位次'], ascending=True)
    df = df.dropna(subset=['分数', '位次'])
except FileNotFoundError:
    messagebox.showerror('错误', '未找到文件：分数位次转换.xlsx')
    raise

def convert():
    score_text = score_entry.get()
    rank_text = rank_entry.get()
    try:
        if score_text and not rank_text:
            score = float(score_text)
            matching_rows = df[df['分数'] == score]
            if not matching_rows.empty:
                result = matching_rows['位次'].max()
            else:
                result = '未找到匹配分数'
            messagebox.showinfo('转换结果', f'对应的位次是: {result}')
        elif rank_text and not score_text:
            rank = float(rank_text)
            higher_rows = df[df['位次'] >= rank]
            if not higher_rows.empty:
                result = higher_rows.iloc[0]['分数']
            else:
                result = '未找到合适位次'
            messagebox.showinfo('转换结果', f'对应的分数是: {result}')
        else:
            messagebox.showerror('错误', '请只填写分数或位次其中一项')
    except ValueError:
        messagebox.showerror('错误', '请输入有效的数字')

# 创建主窗口
root = tk.Tk()
root.title('分数位次转换器')

# 创建分数输入框
score_label = tk.Label(root, text='分数')
score_label.pack(pady=5)
score_entry = tk.Entry(root, width=30)
score_entry.pack(pady=5)

# 创建位次输入框
rank_label = tk.Label(root, text='位次')
rank_label.pack(pady=5)
rank_entry = tk.Entry(root, width=30)
rank_entry.pack(pady=5)

# 删除多余的输入框和选择框代码
# entry = tk.Entry(root, width=30)
# entry.pack(pady=10)
# var = tk.StringVar(root)
# var.set('分数转位次')
# option_menu = tk.OptionMenu(root, var, '分数转位次', '位次转分数')
# option_menu.pack(pady=10)

# 创建转换按钮
convert_button = tk.Button(root, text='匹配', command=convert)
convert_button.pack(pady=20)

# 运行主循环
root.mainloop()