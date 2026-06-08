from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 允许跨域，保证前端网页能正常送数据过来
CORS(app)

# ==========================================
# 1. 模拟的“成绩数据库”
# ==========================================
MOCK_STUDENT_DB = {
    "10002026": {
        "name": "张小明",
        "class": "高一甲班",
        "password": "password123",
        "scores": [
            {"subject": "高级华文", "score": 95},
            {"subject": "中缅实用翻译", "score": 88},
            {"subject": "中国历史文化", "score": 58}
        ]
    }
}

# ==========================================
# 2. 模拟的“报名与招聘收件箱”（用列表来存）
# ==========================================
MOCK_REGISTRATION_LIST = []  # 存新生报名数据
MOCK_JOB_APPLICATION_LIST = [] # 存老师应聘数据


# --------- 接口一：学生成绩查询 ---------
@app.route('/api/query_score', methods=['POST'])
def query_score():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "未接收到有效请求"}), 400
    
    student_id = data.get('student_id', '').strip()
    student_name = data.get('student_name', '').strip()
    class_name = data.get('class_name', '').strip()
    password = data.get('password', '')

    print(f"\n[🔍 收到查询请求] 学号:{student_id} | 姓名:{student_name}")

    if student_id not in MOCK_STUDENT_DB:
        return jsonify({"status": "error", "message": "未找到该学生编号"}), 200

    student_info = MOCK_STUDENT_DB[student_id]

    if (student_info["name"] != student_name or 
        student_info["class"] != class_name or 
        student_info["password"] != password):
        return jsonify({"status": "error", "message": "学生信息与密码不匹配"}), 200

    return jsonify({
        "status": "success",
        "student_name": student_info["name"],
        "class_name": student_info["class"],
        "scores": student_info["scores"]
    })


# --------- 接口二：新生报名表单接收 ---------
@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "表单数据为空"}), 400

    # 提取前端传过来的新生信息
    child_name = data.get('child_name', '').strip()
    parent_phone = data.get('parent_phone', '').strip()
    grade_apply = data.get('grade_apply', '').strip() # 申请就读年级

    # 后端打印一下，假装我们收到了
    print(f"\n[👶 收到新生报名] 孩子姓名:{child_name} | 家长电话:{parent_phone} | 申请年级:{grade_apply}")

    # 【模拟存入数据库】把数据丢进列表里
    new_record = {
        "child_name": child_name,
        "parent_phone": parent_phone,
        "grade_apply": grade_apply
    }
    MOCK_REGISTRATION_LIST.append(new_record)

    # 打印一下现在全校一共有多少人报名了
    print(f"当前报名总人数: {len(MOCK_REGISTRATION_LIST)}人")

    # 告诉前端：后台已经成功登记啦！
    return jsonify({"status": "success", "message": "恭喜，新生报名资料已成功提交，请等待学校通知！"})


# --------- 接口三：教师招聘表单接收 ---------
@app.route('/api/apply_teacher', methods=['POST'])
def apply_teacher():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "招聘数据为空"}), 400

    teacher_name = data.get('teacher_name', '').strip()
    subject_apply = data.get('subject_apply', '').strip() # 应聘科目
    phone = data.get('phone', '').strip()

    print(f"\n[💼 收到教师应聘] 老师姓名:{teacher_name} | 应聘科目:{subject_apply} | 电话:{phone}")

    # 【模拟存入数据库】
    new_application = {
        "teacher_name": teacher_name,
        "subject_apply": subject_apply,
        "phone": phone
    }
    MOCK_JOB_APPLICATION_LIST.append(new_application)

    print(f"当前应聘老师总数: {len(MOCK_JOB_APPLICATION_LIST)}人")

    return jsonify({"status": "success", "message": "简历提交成功！感谢您对华文教育的支持，我们会尽快联系您。"})


if __name__ == '__main__':
    # 启动后端
    app.run(host='127.0.0.1', port=5000, debug=True)