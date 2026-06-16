from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
import datetime
import re
import pandas as pd  
import os            

app = Flask(__name__)
# 🌟 核心安全配置：配置加密密钥（可以随便打一串字母和数字），用于保护登录 Session 不被篡改
app.secret_key = "POL_school_cybersecurity_key_2026"

# 允许跨域时带上 Cookie/Session 凭证
CORS(app, supports_credentials=True)

# 🌟 设置后台的管理账户和密码（你可以自己修改）
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"  # 学校老师登录的密码

# ==========================================
# 内存容器（预报名与招聘使用）
# ==========================================
MOCK_STUDENT_DB = {}
MOCK_ENROLLMENT_LIST = []
MOCK_JOB_APPLICATION_LIST = []

GRADE_TRANSLATION = {
    "preschool": "幼儿部（小/中/大班）",
    "primary_low": "小学低年级（1-3年级）",
    "primary_high": "小学高年级（4-6年级）",
    "junior_middle": "初中部（7-9年级）",
    "senior_high": "高中部（10-12年级）"
}

# --------- 🌟 新增：后台登录接口 ---------
@app.route('/api/login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "请输入账号密码"}), 400
        
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # 登录成功，在服务器内存里记录下这个人的登录状态
        session['logged_in'] = True
        session['user'] = username
        print(f"🔓 [管理员登录成功] 账号: {username}")
        return jsonify({"status": "success", "message": "登录成功，正在跳转..."})
    else:
        print(f"❌ [登录失败尝试] 账号: {username} | 密码: {password}")
        return jsonify({"status": "error", "message": "账号或密码不正确！"})

# --------- 🌟 新增：检查登录状态接口 ---------
@app.route('/api/check_login', methods=['GET'])
def check_login_status():
    if session.get('logged_in'):
        return jsonify({"status": "success", "is_logged_in": True})
    return jsonify({"status": "success", "is_logged_in": False})

# --------- 🌟 新增：安全登出接口 ---------
@app.route('/api/logout', methods=['POST'])
def admin_logout():
    session.clear() # 清空登录状态
    return jsonify({"status": "success", "message": "已安全退出后台"})


# --------- 接口一：成绩查询接口（免密或根据规则校验） ---------
@app.route('/api/query_score', methods=['POST'])
def query_score():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "请求数据为空"}), 400

    student_id = data.get('student_id', '').strip()
    student_name = data.get('student_name', '').strip()
    class_name = data.get('class_name', '').strip()
    password = data.get('password', '')

    if not student_id or not student_name or not class_name or not password:
        return jsonify({"status": "error", "message": "所有查询信息均为必填项"}), 200

    excel_file_name = f"{class_name}.xlsx"

    if not os.path.exists(excel_file_name):
        return jsonify({"status": "error", "message": f"查询失败：未找到【{class_name}】的成绩单"}), 200

    try:
        df = pd.read_excel(excel_file_name, skiprows=1, keep_default_na=False)
        df.columns = [str(col).strip() for col in df.columns]

        matched_rows = df[
            (df['编号'].astype(str).str.strip() == str(student_id)) & 
            (df['姓名'].astype(str).str.strip() == student_name)
        ]

        if matched_rows.empty:
            return jsonify({"status": "error", "message": "学生信息验证失败"}), 200

        student_row = matched_rows.iloc[0]
        if password != "123":
            return jsonify({"status": "error", "message": "查询密码不正确"}), 200

        target_subjects = ["语文", "数学", "生物", "历史", "地理", "物理", "化学", "英语", "书法", "电脑", "总积分"]
        scores_list = []

        for sub in target_subjects:
            if sub in student_row:
                val = student_row[sub]
                score_num = float(val) if val != "" else 0.0
                scores_list.append({"subject": sub, "score": score_num})

        return jsonify({
            "status": "success",
            "student_name": str(student_row['姓名']).strip(),
            "class_name": class_name,
            "scores": scores_list
        })
    except Exception as e:
        return jsonify({"status": "error", "message": "服务器读取成绩单失败"})


# --------- 接口四：校园新闻动态接口（前台公开访问，无需密码） ---------
@app.route('/api/news', methods=['GET'])
def get_school_news():
    excel_news_file = "校园新闻.xlsx"
    if not os.path.exists(excel_news_file):
        return jsonify({"status": "success", "data": []})

    try:
        df = pd.read_excel(excel_news_file, keep_default_na=False)
        df.columns = [str(col).strip() for col in df.columns]

        if 'id' in df.columns and not df.empty:
            df['id'] = pd.to_numeric(df['id'])
            df = df.sort_values(by='id', ascending=False)

        news_list = []
        for _, row in df.iterrows():
            is_urgent = True if str(row.get('urgent', '0')).strip() == '1' else False
            news_item = {
                "id": int(row.get('id', 0)),
                "tag": str(row.get('tag', '校园')).strip(),
                "date": str(row.get('date', '')).strip(),
                "title": str(row.get('title', '')).strip(),
                "summary": str(row.get('summary', '')).strip(),
                "url": str(row.get('url', '#')).strip()
            }
            if is_urgent:
                news_item["urgent"] = True
            news_list.append(news_item)

        return jsonify({"status": "success", "data": news_list})
    except Exception as e:
        return jsonify({"status": "error", "message": "校园新闻加载失败"})


# --------- 接口五：学校管理层发布新闻接口（🌟 增加密码防线保护） ---------
@app.route('/api/add_news', methods=['POST'])
def add_school_news():
    # 🌟 安全检查：如果发现请求者没有登录 Session 记录，直接无情拒绝！
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "拒绝访问：您尚未登录后台系统，无权发布新闻！"}), 403

    data = request.json
    tag = data.get('tag', '校园').strip()
    title = data.get('title', '').strip()
    summary = data.get('summary', '').strip()
    urgent_input = data.get('urgent', '0')  
    url = data.get('url', '#').strip()  

    if not title or not summary:
        return jsonify({"status": "error", "message": "标题和内容简述为必填项"}), 200

    excel_news_file = "校园新闻.xlsx"

    try:
        if os.path.exists(excel_news_file):
            df = pd.read_excel(excel_news_file, keep_default_na=False)
            df.columns = [str(col).strip() for col in df.columns]
            next_id = int(df['id'].max()) + 1 if not df.empty else 1
        else:
            df = pd.DataFrame(columns=["id", "tag", "date", "title", "summary", "urgent", "url"])
            next_id = 1

        today_str = datetime.date.today().strftime("%Y-%m-%d")

        new_row = {
            "id": next_id, "tag": tag, "date": today_str, "title": title,
            "summary": summary, "urgent": "1" if str(urgent_input) == "1" else "0", "url": url
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_news_file, index=False)
        return jsonify({"status": "success", "message": f"文章《{title}》已成功发布！"})
    except Exception as e:
        return jsonify({"status": "error", "message": "服务器写入文章失败"})


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 彬乌伦佛经学校 带有密码安防机制的后端系统已就绪！")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)