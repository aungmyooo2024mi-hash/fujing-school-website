document.getElementById('queryForm').addEventListener('submit', function (event) {
  // 1. 阻止表单默认的刷新页面行为
  event.preventDefault();

  // 精准抓取提交按钮，用来做防连击控制
  const submitBtn = this.querySelector('.btn-submit');

  // 2. 对应你 HTML 里的四个 input 元素的 id，精准抓取用户输入的值
  const studentId = document.getElementById('studentId').value.trim();
  const studentName = document.getElementById('studentName').value.trim();
  const className = document.getElementById('className').value.trim();
  const password = document.getElementById('password').value;

  // 获取页面上的横幅提示和错误框元素
  const messageBanner = document.getElementById('messageBanner');
  const errorMsg = document.getElementById('errorMsg');
  const resultPanel = document.getElementById('resultPanel');
  const scoreTableBody = document.getElementById('scoreTableBody');

  // 3. 初始重置状态：隐藏之前的成绩和错误，展示“正在查询”的小横幅
  errorMsg.style.display = 'none';
  resultPanel.style.display = 'none';
  messageBanner.className = 'message-banner loading';
  messageBanner.innerText = '⏳ 正在安全连接教务系统，请稍候...';
  messageBanner.style.display = 'block';

  // 🔒 【新增防连击】禁用提交按钮，并把文字改为加载状态
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerText = '正在安全验证...';
  }

  // 4. 打包数据准备发往 Python 后端
  const queryData = {
    student_id: studentId,
    student_name: studentName,
    class_name: className,
    password: password
  };

  // 5. 用 fetch 请求你刚才写好的 Python app.py 查分接口
  fetch('http://127.0.0.1:5000/api/query_score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(queryData)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('网络响应异常，状态码: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      // 隐藏“正在查询”的提示横幅
      messageBanner.style.display = 'none';

      if (data.status === 'success') {
        // 6. 后端拦截验证通过！把真实学生的姓名和班级塞进你的白卡片
        document.getElementById('resName').innerText = data.student_name;
        document.getElementById('resClass').innerText = data.class_name;

        // 清空表格里上一次查询留下的老数据
        scoreTableBody.innerHTML = '';

        // 💡【新增空数据防呆】检查是否有成绩录入
        if (!data.scores || data.scores.length === 0) {
          scoreTableBody.innerHTML = `<tr><td colspan="2" style="color:#666; font-style:italic;">暂无该学期的考试成绩记录</td></tr>`;
        } else {
          // 7. 循环遍历 Python 返回的科目和分数列表，动态生成表格行
          data.scores.forEach(item => {
            const tr = document.createElement('tr');

            // 🌟 核心修正：强行将后端传来的数据转换为真正的浮点数字，防止字符串对比失败
            const validScore = parseFloat(item.score);

            // 根据真正的数字进行红绿判断
            let scoreStyleClass = 'score-high'; // 默认及格绿
            if (validScore < 60) {
              scoreStyleClass = 'score-low';  // 小于60分强行变成不及格红
            }

            // 塞入对应的行（在此处顺手补齐了“ 分”字后缀 💡）
            tr.innerHTML = `
                      <td>${item.subject}</td>
                      <td class="${scoreStyleClass}">${item.score} 分</td>
                  `;
            scoreTableBody.appendChild(tr);
          });
        }

        // 渐显展示出你的成绩面板
        resultPanel.style.display = 'block';

      } else {
        // 8. 密码错误或信息不匹配，触发你的红色错误弹窗框
        errorMsg.innerText = '❌ 查询失败：' + data.message;
        errorMsg.style.display = 'block';
      }
    })
    .catch(error => {
      // 防御：当 Python 后端根本没开或者挂掉时，优雅报错
      messageBanner.style.display = 'none';
      errorMsg.innerText = '❌ 无法连接到学校教务服务器，请检查 Python 后端服务是否正常启动！';
      errorMsg.style.display = 'block';
      console.error('全栈对接链路故障:', error);
    })
    .finally(() => {
      // 🔑【恢复按钮】无论请求成功还是挂掉，最后都要把按钮和文字变回来
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = '立即验证并查询';
      }
    });
});