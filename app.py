from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. 模拟的“成绩数据库”
# ==========================================
MOCK_STUDENT_DB = {
    "10002026": {
        "name": "李字明",
        "class": "高三班",
        "password": "password123",
        "scores": [
            {"subject": "语文", "score": 70.5},
            {"subject": "数学", "score": 84.5},
            {"subject": "历史", "score": 94},
            {"subject": "地理", "score": 58},
            {"subject": "化学", "score": 92.4},
            {"subject": "英文", "score": 95}
        ]
    }
}

# ==========================================
# 🌟 新增：报读年级的“中英翻译官”词典
# ==========================================
GRADE_TRANSLATION = {
    "preschool": "幼儿部（小/中/大班）",
    "primary_low": "小学低年级（1-3年级）",
    "primary_high": "小学高年级（4-6年级）",
    "junior_middle": "初中部（7-9年级）",
    "senior_high": "高中部（10-12年级/高一至高三）",
    "intensive_class": "华文加强班（业余强化学习）"
}

# 模拟数据存贮箱
MOCK_REGISTRATION_LIST = []
MOCK_JOB_APPLICATION_LIST = []


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

    if len(student_id) > 20 or len(student_name) > 20:
        return jsonify({"status": "error", "message": "输入参数长度异常"}), 200

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


# --------- 接口二：新生报名接收接口 (加入中文翻译优化) ---------
@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "表单数据为空"}), 400

    student_name = data.get('student_name', '').strip()
    student_age = data.get('student_age', '')
    enroll_grade = data.get('enroll_grade', '').strip() # 此时拿到的是 'senior_high'
    parent_phone = data.get('parent_phone', '').strip()
    parent_wechat = data.get('parent_wechat', '').strip()
    live_area = data.get('live_area', '').strip()
    enroll_remark = data.get('enroll_remark', '').strip()

    if not student_name or not student_age or not enroll_grade or not parent_phone or not live_area:
        return jsonify({"status": "error", "message": "❌ 提交失败：带 * 的必填项不能为空！"}), 200

    if len(student_name) > 20 or len(parent_phone) > 20:
        return jsonify({"status": "error", "message": "❌ 安全警告：输入文本过长"}), 200

    if not re.match(r'^[0-9+\-]+$', parent_phone):
        return jsonify({"status": "error", "message": "❌ 提交失败：联系电话格式不合法"}), 200

    # 🌟 使用翻译词典将英文代号变成中文显示
    # .get(key, default) 的意思是：如果词典里有对应的中文就换掉，没有就显示原来的英文
    grade_chinese = GRADE_TRANSLATION.get(enroll_grade, enroll_grade)

    print(f"\n[👶 收到新预约报名]")
    print(f" ├─ 学生姓名: {student_name} ({student_age}岁)")
    print(f" ├─ 报读年级: {grade_chinese} (后台标识: {enroll_grade})")  # 这里的输出就变成漂亮的中文啦！
    print(f" ├─ 家长电话: {parent_phone} | 微信: {parent_wechat if parent_wechat else '未填'}")
    print(f" ├─ 现居住地: {live_area}")
    print(f" └─ 备注说明: {enroll_remark if enroll_remark else '无'}")

    new_record = {
        "student_name": student_name,
        "student_age": student_age,
        "enroll_grade": enroll_grade, # 数据库里建议依然保存规范的英文
        "parent_phone": parent_phone,
        "parent_wechat": parent_wechat,
        "live_area": live_area,
        "enroll_remark": enroll_remark
    }
    MOCK_REGISTRATION_LIST.append(new_record)
    print(f"📈 当前全校累计预约登记人数: {len(MOCK_REGISTRATION_LIST)} 人")

    return jsonify({"status": "success", "message": "🎉 恭喜！您的预约申请已成功提交至学校后台，招生办老师将尽快与您联络！"})


# --------- 接口三：教师招聘表单接收 ---------
@app.route('/api/apply_teacher', methods=['POST'])
def apply_teacher():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "招聘数据为空"}), 400

    teacher_name = data.get('teacher_name', '').strip()
    subject_apply = data.get('subject_apply', '').strip() 
    phone = data.get('phone', '').strip()

    if not teacher_name or not subject_apply or not phone:
        return jsonify({"status": "error", "message": "提交失败：表单信息不完整"}), 200

    if not re.match(r'^[0-9+\-]+$', phone):
        return jsonify({"status": "error", "message": "提交失败：联系电话包含非法字符"}), 200

    print(f"\n[💼 收到教师应聘] 老师姓名:{teacher_name} | 应聘科目:{subject_apply} | 电话:{phone}")

    new_application = {
        "teacher_name": teacher_name,
        "subject_apply": subject_apply,
        "phone": phone
    }
    MOCK_JOB_APPLICATION_LIST.append(new_application)
    print(f"当前应聘老师总数: {len(MOCK_JOB_APPLICATION_LIST)}人")

    return jsonify({"status": "success", "message": "简历提交成功！感谢您对华文教育的支持，我们会尽快联系您。"})


# --------- 接口四：教务处查看大盘通道 ---------
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({
        "status": "success",
        "total_registrations": len(MOCK_REGISTRATION_LIST),
        "total_applications": len(MOCK_JOB_APPLICATION_LIST),
        "registrations_data": MOCK_REGISTRATION_LIST,
        "applications_data": MOCK_JOB_APPLICATION_LIST
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)