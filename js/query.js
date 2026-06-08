document.getElementById('queryForm').addEventListener('submit', function (e) {
  // 1. 阻止表单默认的刷新页面提交行为
  e.preventDefault();

  // 2. 获取用户输入的值（已扩展为 4 个字段）
  const studentId = document.getElementById('studentId').value.trim();
  const studentName = document.getElementById('studentName').value.trim();
  const className = document.getElementById('className').value.trim();
  const password = document.getElementById('password').value;

  const messageBanner = document.getElementById('messageBanner');
  const errorMsg = document.getElementById('errorMsg');
  const resultPanel = document.getElementById('resultPanel');
  const scoreTableBody = document.getElementById('scoreTableBody');

  // 初始化：隐藏之前的提示、错误横幅和结果，并清空表格
  if (messageBanner) messageBanner.style.display = 'none';
  errorMsg.style.display = 'none';
  resultPanel.style.display = 'none';
  scoreTableBody.innerHTML = '';

  // 【前端基础验证】
  // 验证 1：非空检查
  if (!studentId || !studentName || !className || !password) {
    showError("⚠️ 所有字段均为必填项，请填写完整！");
    return;
  }

  // 验证 2：学生编号格式过滤（可以根据学校实际的编号规则调整正则，这里允许数字和字母）
  if (!/^[a-zA-Z0-9]+$/.test(studentId)) {
    showError("❌ 编号格式不正确，只能包含数字和字母！");
    return;
  }

  // 显示加载中状态（如果 HTML 中保留了 messageBanner）
  if (messageBanner) {
    messageBanner.className = 'message-banner loading';
    messageBanner.innerText = '⏳ 正在安全加密通道中查询，请稍候...';
    messageBanner.style.display = 'block';
  }

  // 3. 使用 Fetch 发送异步请求到后端 API
  // 此时将 4 个字段一并打包发送，供后端进行多条件复合验证（更安全！）
  fetch('http://127.0.0.1:5000/api/query_score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      student_id: studentId,
      student_name: studentName,
      class_name: className,
      password: password
    })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('网络异常或服务器错误');
      }
      return response.json();
    })
    .then(data => {
      // 隐藏加载状态横幅
      if (messageBanner) messageBanner.style.display = 'none';

      if (data.status === 'success') {
        // 4. 解析数据并渲染到 DOM 中
        // 优先使用后端返回的权威数据，若后端未返回则降级显示用户输入的数据
        document.getElementById('resName').innerText = data.student_name || studentName;
        document.getElementById('resClass').innerText = data.class_name || className;

        // 遍历成绩数组，动态生成表格行
        data.scores.forEach(item => {
          // 根据分数高低赋予不同的前端样式（比如低于60分标红，高于90分标绿）
          let scoreClass = '';
          if (item.score >= 90) scoreClass = 'class="score-high"';
          else if (item.score < 60) scoreClass = 'class="score-low"';

          const row = `<tr>
                        <td>${item.subject}</td>
                        <td ${scoreClass}>${item.score}</td>
                       </tr>`;
          scoreTableBody.insertAdjacentHTML('beforeend', row);
        });

        // 显示成绩面板
        resultPanel.style.display = 'block';
      } else {
        // 显示后端返回的错误原因（如：信息不匹配、密码错误等）
        showError(`❌ ${data.message}`);
      }
    })
    .catch(error => {
      if (messageBanner) messageBanner.style.display = 'none';
      showError('❌ 无法连接到服务器，请稍后再试。');
      console.error('Error:', error);
    });

  // 提取公共的错误显示函数
  function showError(msg) {
    errorMsg.innerText = msg;
    errorMsg.style.display = 'block'; document.getElementById('queryForm').addEventListener('submit', function (e) {
      // 1. 阻止表单默认的刷新页面提交行为
      e.preventDefault();

      // 2. 获取用户输入的值（已扩展为 4 个字段）
      const studentId = document.getElementById('studentId').value.trim();
      const studentName = document.getElementById('studentName').value.trim();
      const className = document.getElementById('className').value.trim();
      const password = document.getElementById('password').value;

      const messageBanner = document.getElementById('messageBanner');
      const errorMsg = document.getElementById('errorMsg');
      const resultPanel = document.getElementById('resultPanel');
      const scoreTableBody = document.getElementById('scoreTableBody');

      // 初始化：隐藏之前的提示、错误横幅和结果，并清空表格
      if (messageBanner) messageBanner.style.display = 'none';
      errorMsg.style.display = 'none';
      resultPanel.style.display = 'none';
      scoreTableBody.innerHTML = '';

      // 【前端基础验证】
      // 验证 1：非空检查
      if (!studentId || !studentName || !className || !password) {
        showError("⚠️ 所有字段均为必填项，请填写完整！");
        return;
      }

      // 验证 2：学生编号格式过滤（可以根据学校实际的编号规则调整正则，这里允许数字和字母）
      if (!/^[a-zA-Z0-9]+$/.test(studentId)) {
        showError("❌ 编号格式不正确，只能包含数字和字母！");
        return;
      }

      // 显示加载中状态（如果 HTML 中保留了 messageBanner）
      if (messageBanner) {
        messageBanner.className = 'message-banner loading';
        messageBanner.innerText = '⏳ 正在安全加密通道中查询，请稍候...';
        messageBanner.style.display = 'block';
      }

      // 3. 使用 Fetch 发送异步请求到后端 API
      // 此时将 4 个字段一并打包发送，供后端进行多条件复合验证（更安全！）
      fetch('http://127.0.0.1:5000/api/query_score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          student_name: studentName,
          class_name: className,
          password: password
        })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('网络异常或服务器错误');
          }
          return response.json();
        })
        .then(data => {
          // 隐藏加载状态横幅
          if (messageBanner) messageBanner.style.display = 'none';

          if (data.status === 'success') {
            // 4. 解析数据并渲染到 DOM 中
            // 优先使用后端返回的权威数据，若后端未返回则降级显示用户输入的数据
            document.getElementById('resName').innerText = data.student_name || studentName;
            document.getElementById('resClass').innerText = data.class_name || className;

            // 遍历成绩数组，动态生成表格行
            data.scores.forEach(item => {
              // 根据分数高低赋予不同的前端样式（比如低于60分标红，高于90分标绿）
              let scoreClass = '';
              if (item.score >= 90) scoreClass = 'class="score-high"';
              else if (item.score < 60) scoreClass = 'class="score-low"';

              const row = `<tr>
                        <td>${item.subject}</td>
                        <td ${scoreClass}>${item.score}</td>
                       </tr>`;
              scoreTableBody.insertAdjacentHTML('beforeend', row);
            });

            // 显示成绩面板
            resultPanel.style.display = 'block';
          } else {
            // 显示后端返回的错误原因（如：信息不匹配、密码错误等）
            showError(`❌ ${data.message}`);
          }
        })
        .catch(error => {
          if (messageBanner) messageBanner.style.display = 'none';
          showError('❌ 无法连接到服务器，请稍后再试。');
          console.error('Error:', error);
        });

      // 提取公共的错误显示函数
      function showError(msg) {
        errorMsg.innerText = msg;
        errorMsg.style.display = 'block';
      }
    });
  }
});