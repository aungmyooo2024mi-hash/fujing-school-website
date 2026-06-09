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
    "senior_high": "高中部（10-12年级）"
}

# 模拟的其他全局内存数据库容器
MOCK_ENROLLMENT_LIST = []
MOCK_JOB_APPLICATION_LIST = []


# --------- 接口一：成绩查询接口 ---------
@app.route('/api/query_score', methods=['POST'])
def query_score():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "请求数据为空"}), 400

    student_id = data.get('student_id', '').strip()
    
    # 🛠️ 【核心修复】：将驼峰命名改为下划线，从而完美匹配前端 query.js 发来的数据
    student_name = data.get('student_name', '').strip()
    class_name = data.get('class_name', '').strip()
    
    password = data.get('password', '')

    # 基础空值拦截
    if not student_id or not student_name or not class_name or not password:
        return jsonify({"status": "error", "message": "所有查询信息均为必填项"}), 200

    print(f"\n[🔍 收到查询请求] 学号:{student_id} | 姓名:{student_name} | 班级:{class_name}")

    # 1. 验证学号是否存在
    if student_id not in MOCK_STUDENT_DB:
        return jsonify({"status": "error", "message": "未找到该学号对应的学生信息"}), 200

    student_info = MOCK_STUDENT_DB[student_id]

    # 2. 验证姓名和班级是否精准匹配
    if student_info["name"] != student_name or student_info["class"] != class_name:
        return jsonify({"status": "error", "message": "学生姓名或班级信息不匹配，请重新核对"}), 200

    # 3. 验证密码
    if student_info["password"] != password:
        return jsonify({"status": "error", "message": "查询密码不正确"}), 200

    # 4. 验证完全通过，安全返回数据给前端
    print(f" 成功：验证通过！正在将【{student_name}】的成绩单下发至前端。")
    return jsonify({
        "status": "success",
        "student_name": student_info["name"],
        "class_name": student_info["class"],
        "scores": student_info["scores"]
    })


# --------- 接口二：新生报名接口（全面升级兼容版） ---------
@app.route('/api/register_student', methods=['POST'])  
def enroll_student():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "报名数据为空"}), 400

    # 2. 精准抓取你 register.js 发出的所有好料
    student_name = data.get('student_name', '').strip()
    student_age = data.get('student_age')
    enroll_grade_key = data.get('enroll_grade', '').strip() 
    parent_phone = data.get('parent_phone', '').strip()
    parent_wechat = data.get('parent_wechat', '').strip()
    live_area = data.get('live_area', '').strip()
    enroll_remark = data.get('enroll_remark', '').strip()

    # 3. 基础必填项安全拦截
    if not student_name or not enroll_grade_key or not parent_phone or not live_area:
        return jsonify({"status": "error", "message": "提交失败：标有 * 的必填项信息不完整"}), 200

    if not re.match(r'^[0-9+\\-]+$', parent_phone):
        return jsonify({"status": "error", "message": "提交失败：家长联系电话格式不正确"}), 200

    # 4. 智能翻译年级标签（适配你前端对应的 preschool, primary_low 等值）
    grade_chinese = GRADE_TRANSLATION.get(enroll_grade_key, f"未知年级({enroll_grade_key})")

    # 5. 后台打印出极其漂亮的结构化日志
    print("\n" + "="*50)
    print(f"[👶 收到完整新生预报名申请]")
    print(f" 👤 学生姓名: {student_name} ({student_age} 岁)")
    print(f" 📚 报读年级: {grade_chinese}")
    print(f" 📞 家长电话: {parent_phone}")
    print(f" 💬 家长微信: {parent_wechat if parent_wechat else '未填写'}")
    print(f" 📍 现居住地: {live_area}")
    print(f" 📝 补充备注: {enroll_remark if enroll_remark else '无'}")
    print("="*50)

    # 6. 存入内存模拟数据库
    new_student = {
        "student_name": student_name,
        "student_age": student_age,
        "enroll_grade": grade_chinese,
        "parent_phone": parent_phone,
        "parent_wechat": parent_wechat,
        "live_area": live_area,
        "enroll_remark": enroll_remark
    }
    MOCK_ENROLLMENT_LIST.append(new_student)
    print(f"💡 当前全校已预报名学生总数: {len(MOCK_ENROLLMENT_LIST)}人")

    return jsonify({
        "status": "success", 
        "message": f"【{student_name}】同学的预报名申请已成功提交！学校招生办会尽快通过电话或微信与您取得联系。"
    })
# --------- 接口三：师资招聘接口 ---------
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

    if not re.match(r'^[0-9+\\-]+$', phone):
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


# --------- 接口四：校园新闻动态模拟接口 ---------
@app.route('/api/news', methods=['GET'])
def get_school_news():
    news_list = [
        {"id": 1, "tag": "招聘", "date": "2026-06-01", "title": "师资招聘公告", "summary": "学校现面向社会招聘优秀华文教师，详情请查看官方微信公众号或联系教务处。"},
        {"id": 2, "tag": "招生", "date": "2026-05-20", "title": "新生报名须知", "summary": "2026学年度新学期招生工作已正式开启，请各位家长及时点击上方入口或到校提交资料。", "urgent": True},
        {"id": 3, "tag": "校园", "date": "2026-05-15", "title": "校园活动通知", "summary": "为丰富同学们的课余生活，近期学校将举办夏季校园运动会，欢迎全体师生积极参与。"}
    ]
    return jsonify({"status": "success", "data": news_list})


if __name__ == '__main__':
    # 终端打印亮眼的启动成功提示
    print("=" * 60)
    print("🚀 彬乌伦佛经学校 教务系统后台本地开发服务已成功启动！")
    print("🔗 成绩查询接口：http://127.0.0.1:5000/api/query_score")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)