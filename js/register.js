document.getElementById('enrollForm').addEventListener('submit', function (event) {
  // 1. 坚决阻止原表单的弹窗与页面刷新行为，把控制权交给 JS
  event.preventDefault();

  // 抓取提交按钮，用来做防止连击的控制
  const submitBtn = this.querySelector('.submit-btn');

  // 2. 严格对应你最新 HTML 中的 id 抓取输入值
  const studentName = document.getElementById('student_name').value.trim();
  const studentAge = document.getElementById('student_age').value;
  const enrollGrade = document.getElementById('grade_apply').value; // 💡 完美对齐最新 HTML 的 grade_apply！
  const parentPhone = document.getElementById('parent_phone').value.trim();
  const parentWechat = document.getElementById('parent_wechat').value.trim();
  const liveArea = document.getElementById('live_area').value.trim();
  const enrollRemark = document.getElementById('enroll_remark').value.trim();

  // 3. 把抓到的内容整整齐齐地打包成 JSON
  const enrollData = {
    student_name: studentName,
    student_age: parseInt(studentAge), // 确保年龄作为数字送给后端
    enroll_grade: enrollGrade,        // 传给后端的键名为 enroll_grade 匹配你的 app.py
    parent_phone: parentPhone,
    parent_wechat: parentWechat,
    live_area: liveArea,
    enroll_remark: enrollRemark
  };

  // 4. 锁定提交按钮，给家长一个友好的等待文字
  submitBtn.disabled = true;
  submitBtn.innerText = '正在提交申请... / Submitting...';

  console.log("🚀 数据封装成功，正准备跨时空发射到 Python 后端：", enrollData);

  // 5. 用 fetch 投递给 Python 后端 (端口5000)
  fetch('http://127.0.0.1:5000/api/register_student', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(enrollData) // 转化为字符串发射
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('网络响应不正常，请检查后端是否开启！');
      }
      return response.json();
    })
    .then(data => {
      if (data.status === 'success') {
        // 后端验证通过：弹出后端返回的温馨成功信息
        alert("🎉 提交成功！\n" + data.message);
        document.getElementById('enrollForm').reset(); // 自动清空表单数据
      } else {
        // 后端拦截提示（比如电话格式错、必填项空）
        alert("❌ 提交失败：\n" + data.message);
      }
    })
    .catch(error => {
      // 捕获各种断网或者 Flask 没开的极端崩溃情况
      alert("⚠️ 系统提示：无法连接到学校教务系统服务器，请确保本地 Python 后端 app.py 已经运行！");
      console.error('错误详情:', error);
    })
    .finally(() => {
      // 无论成功还是失败，最后都要把按钮和文字恢复原状
      submitBtn.disabled = false;
      submitBtn.innerText = '提交预约申请 / Submit';
    });
});