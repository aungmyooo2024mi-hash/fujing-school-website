from flask import Flask, request, jsonify, session
from flask_cors import CORS
import datetime
import re
import pandas as pd  
import os            

app = Flask(__name__)
app.secret_key = "POL_school_cybersecurity_key_2026"

# 允许跨域时带上 Cookie/Session 凭证
CORS(app, supports_credentials=True)

# 管理员账号密码
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"  

# 报读年级翻译官
GRADE_TRANSLATION = {
    "preschool": "幼儿部（小/中/大班）",
    "primary_low": "小学低年级（1-3年级）",
    "primary_high": "小学高年级（4-6年级）",
    "junior_middle": "初中部（7-9年级）",
    "senior_high": "高中部（10-12年级）"
}

# --------- 1. 权限与状态接口 ---------
@app.route('/api/login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "请输入账号密码"}), 400
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        session['user'] = username
        return jsonify({"status": "success", "message": "登录成功"})
    return jsonify({"status": "error", "message": "账号或密码不正确！"})

@app.route('/api/check_login', methods=['GET'])
def check_login_status():
    if session.get('logged_in'):
        return jsonify({"status": "success", "is_logged_in": True})
    return jsonify({"status": "success", "is_logged_in": False})

@app.route('/api/logout', methods=['POST'])
def admin_logout():
    session.clear()
    return jsonify({"status": "success", "message": "已安全退出后台"})


# --------- 2. 新生报名接口（🌟 升级：Excel 永久存盘版） ---------
@app.route('/api/register_student', methods=['POST'])  
def enroll_student():
    data = request.json
    if not data: return jsonify({"status": "error", "message": "报名数据为空"}), 400

    student_name = data.get('student_name', '').strip()
    student_age = data.get('student_age', '')
    enroll_grade_key = data.get('enroll_grade', '').strip() 
    parent_phone = data.get('parent_phone', '').strip()
    parent_wechat = data.get('parent_wechat', '').strip()
    live_area = data.get('live_area', '').strip()
    enroll_remark = data.get('enroll_remark', '').strip()

    if not student_name or not enroll_grade_key or not parent_phone or not live_area:
        return jsonify({"status": "error", "message": "提交失败：必填项信息不完整"}), 200

    grade_chinese = GRADE_TRANSLATION.get(enroll_grade_key, enroll_grade_key)
    excel_file = "新生报名表.xlsx"

    try:
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file, keep_default_na=False)
        else:
            df = pd.DataFrame(columns=["报名时间", "学生姓名", "年龄", "报读年级", "家长电话", "微信/联系方式", "居住区域", "备注说明"])

        new_row = {
            "报名时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "学生姓名": student_name, "年龄": student_age, "报读年级": grade_chinese,
            "家长电话": parent_phone, "微信/联系方式": parent_wechat, "居住区域": live_area, "备注说明": enroll_remark
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_file, index=False)
        return jsonify({"status": "success", "message": "您的预报名申请已成功提交！学校招生办会尽快与您联系。"})
    except Exception as e:
        return jsonify({"status": "error", "message": "服务器保存报名表失败，请联系管理员"})


# --------- 3. 师资招聘接口（🌟 升级：Excel 永久存盘版） ---------
@app.route('/api/apply_teacher', methods=['POST'])
def apply_teacher():
    data = request.json
    teacher_name = data.get('teacher_name', '').strip()
    subject_apply = data.get('subject_apply', '').strip() 
    phone = data.get('phone', '').strip()

    if not teacher_name or not subject_apply or not phone:
        return jsonify({"status": "error", "message": "提交失败：信息不完整"}), 200

    excel_file = "教师应聘表.xlsx"
    try:
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file, keep_default_na=False)
        else:
            df = pd.DataFrame(columns=["投递时间", "应聘老师", "意向科目", "电话号码"])

        new_row = {
            "投递时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "应聘老师": teacher_name, "意向科目": subject_apply, "电话号码": phone
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_file, index=False)
        return jsonify({"status": "success", "message": "简历提交成功！感谢您对华文教育的支持。"})
    except Exception as e:
        return jsonify({"status": "error", "message": "服务器保存简历失败"})


# --------- 4. 权限受控接口：读取报名和招聘列表（🌟 新增：供管理后台查看） ---------
@app.route('/api/admin/get_data', methods=['GET'])
def admin_get_data():
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "越权访问被拒绝"}), 403
    
    enroll_list = []
    teacher_list = []
    
    if os.path.exists("新生报名表.xlsx"):
        df = pd.read_excel("新生报名表.xlsx", keep_default_na=False)
        enroll_list = df.to_dict(orient='records')
        
    if os.path.exists("教师应聘表.xlsx"):
        df = pd.read_excel("教师应聘表.xlsx", keep_default_na=False)
        teacher_list = df.to_dict(orient='records')

    return jsonify({
        "status": "success",
        "enrollments": enroll_list[::-1], # 倒序排列，最新的显示在最前面
        "teachers": teacher_list[::-1]
    })


# --------- 5. 校园新闻接口 ---------
@app.route('/api/news', methods=['GET'])
def get_school_news():
    excel_news_file = "校园新闻.xlsx"
    if not os.path.exists(excel_news_file): return jsonify({"status": "success", "data": []})
    try:
        df = pd.read_excel(excel_news_file, keep_default_na=False)
        df.columns = [str(col).strip() for col in df.columns]
        if 'id' in df.columns and not df.empty:
            df['id'] = pd.to_numeric(df['id'])
            df = df.sort_values(by='id', ascending=False)
        news_list = []
        for _, row in df.iterrows():
            news_list.append({
                "id": int(row.get('id', 0)), "tag": str(row.get('tag', '校园')).strip(),
                "date": str(row.get('date', '')).strip(), "title": str(row.get('title', '')).strip(),
                "summary": str(row.get('summary', '')).strip(), "url": str(row.get('url', '#')).strip(),
                "urgent": True if str(row.get('urgent', '0')).strip() == '1' else False
            })
        return jsonify({"status": "success", "data": news_list})
    except: return jsonify({"status": "error", "message": "新闻加载失败"})


@app.route('/api/add_news', methods=['POST'])
def add_school_news():
    if not session.get('logged_in'): return jsonify({"status": "error", "message": "拒绝访问"}), 403
    data = request.json
    tag, title, summary, url = data.get('tag','校园'), data.get('title',''), data.get('summary',''), data.get('url','#')
    urgent_input = data.get('urgent', '0')

    excel_news_file = "校园新闻.xlsx"
    try:
        if os.path.exists(excel_news_file):
            df = pd.read_excel(excel_news_file, keep_default_na=False)
            next_id = int(df['id'].max()) + 1 if not df.empty else 1
        else:
            df = pd.DataFrame(columns=["id", "tag", "date", "title", "summary", "urgent", "url"])
            next_id = 1
        new_row = {
            "id": next_id, "tag": tag, "date": datetime.date.today().strftime("%Y-%m-%d"),
            "title": title, "summary": summary, "urgent": "1" if urgent_input == "1" else "0", "url": url
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_news_file, index=False)
        return jsonify({"status": "success", "message": "发布成功！"})
    except: return jsonify({"status": "error", "message": "Excel写入失败"})

# --------- 接口：成绩查询（保持原样不动） ---------
@app.route('/api/query_score', methods=['POST'])
def query_score():
    data = request.json
    student_id = data.get('student_id', '').strip()
    student_name = data.get('student_name', '').strip()
    class_name = data.get('class_name', '').strip()
    password = data.get('password', '')

    excel_file_name = f"{class_name}.xlsx"
    if not os.path.exists(excel_file_name):
        return jsonify({"status": "error", "message": f"未找到【{class_name}】的成绩单"}), 200
    try:
        df = pd.read_excel(excel_file_name, skiprows=1, keep_default_na=False)
        df.columns = [str(col).strip() for col in df.columns]
        matched = df[(df['编号'].astype(str).str.strip() == str(student_id)) & (df['姓名'].astype(str).str.strip() == student_name)]
        if matched.empty: return jsonify({"status": "error", "message": "信息验证失败"}), 200
        if password != "123": return jsonify({"status": "error", "message": "查询密码错误"}), 200
        
        target_subjects = ["语文", "数学", "生物", "历史", "地理", "物理", "化学", "英语", "书法", "电脑", "总积分"]
        scores_list = [{"subject": sub, "score": float(matched.iloc[0][sub])} for sub in target_subjects if sub in matched.iloc[0] and matched.iloc[0][sub] != ""]
        return jsonify({"status": "success", "student_name": student_name, "class_name": class_name, "scores": scores_list})
    except: return jsonify({"status": "error", "message": "系统读取失败"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)