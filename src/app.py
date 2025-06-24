from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# 读取文件
file_path = '分数位次转换.xlsx'
try:
    df = pd.read_excel(file_path)
    df = df.sort_values(by=['位次'], ascending=True)
    df = df.dropna(subset=['分数', '位次'])
except FileNotFoundError:
    print('未找到文件：分数位次转换.xlsx')
    df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    data = request.get_json()
    logging.debug(f'接收到的数据: {data}')
    score = data.get('score')
    rank = data.get('rank')
    try:
        if score is not None and rank is None:
            score = float(score)
            logging.debug(f'正在查找分数 {score} 对应的位次')
            matching_rows = df[df['分数'] == score]
            if not matching_rows.empty:
                result = matching_rows['位次'].max()
                if isinstance(result, np.int64):
                    result = int(result)
            else:
                result = '未找到匹配分数'
            logging.debug(f'分数 {score} 对应的位次结果: {result}')
            return jsonify({'result': result})
        elif rank is not None and score is None:
            rank = float(rank)
            logging.debug(f'正在查找位次 {rank} 对应的分数')
            higher_rows = df[df['位次'] >= rank]
            if not higher_rows.empty:
                result = higher_rows.iloc[0]['分数']
                if isinstance(result, np.int64):
                    result = int(result)
            else:
                result = '未找到合适位次'
            logging.debug(f'位次 {rank} 对应的分数结果: {result}')
            return jsonify({'result': result})
        else:
            logging.debug('用户输入不符合要求，需要只填写分数或位次其中一项')
            return jsonify({'error': '请只填写分数或位次其中一项'}), 400
    except ValueError as e:
        logging.error(f'输入值转换出错: {e}')
        return jsonify({'error': '请输入有效的数字'}), 400
    except Exception as e:
        logging.error(f'发生未知错误: {e}')
        return jsonify({'error': '发生未知错误，请重试'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)