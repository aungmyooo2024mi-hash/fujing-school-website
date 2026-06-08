document.getElementById('enrollForm').addEventListener('submit', function (event) {
  // 1. 坚决阻止原表单的弹窗与页面刷新行为，把控制权交给 JS
  event.preventDefault();

  // 2. 严格对应你 HTML 中的 id 抓取输入值
  const studentName = document.getElementById('student_name').value.trim();
  const studentAge = document.getElementById('student_age').value;
  const enrollGrade = document.getElementById('enroll_grade').value;
  const parentPhone = document.getElementById('parent_phone').value.trim();
  const parentWechat = document.getElementById('parent_wechat').value.trim();
  const liveArea = document.getElementById('live_area').value.trim();
  const enrollRemark = document.getElementById('enroll_remark').value.trim();

  // 3. 把抓到的内容整整齐齐地打包成 JSON
  const enrollData = {
    student_name: studentName,
    student_age: parseInt(studentAge), // 确保年龄作为数字送给后端
    enroll_grade: enrollGrade,
    parent_phone: parentPhone,
    parent_wechat: parentWechat,
    live_area: liveArea,
    enroll_remark: enrollRemark
  };

  console.log("准备发射数据到后端：", enrollData);

  // 4. 用 fetch 跨时空投递给 Python 后端 (端口5000)
  fetch('http://127.0.0.1:5000/api/register_student', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(enrollData) // 转化为字符串发射
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('网络响应不正常');
      }
      return response.json();
    })
    .then(data => {
      // 5. 接收 Python 吐出来的回应
      if (data.status === 'success') {
        alert(data.message); // 弹出 Python 发来的带有 🎉 的成功祝贺信
        document.getElementById('enrollForm').reset(); // 自动清空网页表单
      } else {
        alert(data.message); // 如果触发了网安拦截，弹出拦截原因
      }
    })
    .catch(error => {
      console.error('联调失败原因:', error);
      alert('无法连接到服务器。请检查：1. Python后端是否运行 2. 终端有没有报错');
    });
});