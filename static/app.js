(() => {
  const MAX_FILES = 10;
  const state = {
    files: [], // { file: File, previewUrl: string }
  };

  const el = {
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('fileInput'),
    fileSummary: document.getElementById('fileSummary'),
    fileCount: document.getElementById('fileCount'),
    clearFilesBtn: document.getElementById('clearFilesBtn'),
    previewGrid: document.getElementById('previewGrid'),
    gameId: document.getElementById('gameId'),
    stage: document.getElementById('stage'),
    uploadForm: document.getElementById('uploadForm'),
    submitBtn: document.getElementById('submitBtn'),
    resultArea: document.getElementById('resultArea'),
    copyJsonBtn: document.getElementById('copyJsonBtn'),
    toast: document.getElementById('toast'),
    backdrop: document.getElementById('backdrop'),
  };

  function showToast(message) {
    el.toast.textContent = message;
    el.toast.classList.remove('hidden');
    setTimeout(() => el.toast.classList.add('hidden'), 2400);
  }

  function setLoading(loading) {
    if (loading) el.backdrop.classList.remove('hidden');
    else el.backdrop.classList.add('hidden');
    el.submitBtn.disabled = !!loading;
  }

  function refreshSummary() {
    const count = state.files.length;
    el.fileCount.textContent = String(count);
    el.fileSummary.classList.toggle('hidden', count === 0);
  }

  function renderPreviews() {
    el.previewGrid.innerHTML = '';
    state.files.forEach((item, idx) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'preview-item';
      const img = document.createElement('img');
      img.src = item.previewUrl;
      const badge = document.createElement('div');
      badge.className = 'preview-caption';
      badge.textContent = `第 ${idx + 1} 张`; // 展示顺序
      const removeBtn = document.createElement('button');
      removeBtn.className = 'remove-btn';
      removeBtn.type = 'button';
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        URL.revokeObjectURL(item.previewUrl);
        state.files.splice(idx, 1);
        refreshSummary();
        renderPreviews();
      });
      wrapper.appendChild(img);
      wrapper.appendChild(badge);
      wrapper.appendChild(removeBtn);
      el.previewGrid.appendChild(wrapper);
    });
  }

  function addFiles(fileList) {
    const incoming = Array.from(fileList || []);
    if (!incoming.length) return;
    const total = state.files.length + incoming.length;
    if (total > MAX_FILES) {
      showToast(`最多只能上传 ${MAX_FILES} 张图片`);
      return;
    }
    for (const f of incoming) {
      if (!f.type.startsWith('image/')) {
        showToast('仅支持图片文件');
        continue;
      }
      const previewUrl = URL.createObjectURL(f);
      state.files.push({ file: f, previewUrl });
    }
    refreshSummary();
    renderPreviews();
  }

  // Drag & drop
  el.dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    el.dropzone.classList.add('dragover');
  });
  el.dropzone.addEventListener('dragleave', () => {
    el.dropzone.classList.remove('dragover');
  });
  el.dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    el.dropzone.classList.remove('dragover');
    addFiles(e.dataTransfer.files);
  });
  el.fileInput.addEventListener('change', (e) => addFiles(e.target.files));

  el.clearFilesBtn.addEventListener('click', () => {
    state.files.forEach((i) => URL.revokeObjectURL(i.previewUrl));
    state.files = [];
    refreshSummary();
    renderPreviews();
  });

  // 复制 JSON
  el.copyJsonBtn.addEventListener('click', async () => {
    const pre = el.resultArea.querySelector('pre');
    if (!pre) { showToast('暂无可复制内容'); return; }
    try {
      await navigator.clipboard.writeText(pre.textContent || '');
      showToast('已复制到剪贴板');
    } catch {
      showToast('复制失败');
    }
  });

  function renderErrorTable(errorList) {
    if (!errorList || !Array.isArray(errorList.errors)) {
      el.resultArea.classList.add('empty');
      el.resultArea.classList.remove('success');
      el.resultArea.innerHTML = '<div class="empty-tip">未返回有效的错误列表</div>';
      return;
    }
    function formatErrorType(t) {
      switch (Number(t)) {
        case 1: return '最终排名错误';
        case 2: return '游戏内排名错误';
        case 3: return '队伍淘汰数错误';
        default: return '未知类型';
      }
    }
    const errors = Array.isArray(errorList.errors) ? errorList.errors : [];
    if (errors.length === 0) {
      el.resultArea.classList.remove('empty');
      el.resultArea.classList.add('success');
      el.resultArea.innerHTML = '<div class="success-tip">✅ 校验通过，API 数据正确。未发现错误项。</div>';
      return;
    }
    const rows = errors.map((e, i) => {
      const typeClass = `error-type-${e.error_type || 0}`;
      return `<tr>
        <td><span class="badge ${typeClass}">#${i + 1}</span></td>
        <td>${formatErrorType(e.error_type)}</td>
        <td>${escapeHtml(e.team)}</td>
        <td>${escapeHtml(e.original_data)}</td>
        <td>${escapeHtml(e.correct_data)}</td>
      </tr>`;
    }).join('');
    el.resultArea.classList.remove('empty');
    el.resultArea.classList.remove('success');
    el.resultArea.innerHTML = `
      <table class="error-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>类型</th>
            <th>队伍</th>
            <th>原始数据</th>
            <th>正确数据</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
      <details style="margin-top:10px;">
        <summary>查看原始返回 JSON</summary>
        <pre style="white-space: pre-wrap;">${escapeHtml(JSON.stringify({ error_list: errorList }, null, 2))}</pre>
      </details>
    `;
  }

  function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  // 表单提交：重命名 + 上传
  el.uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const gameId = el.gameId.value.trim();
    const stage = el.stage.value.trim();
    if (!gameId) { showToast('请填写 Game ID'); return; }
    if (!stage) { showToast('请填写 Stage'); return; }
    if (state.files.length === 0) { showToast('请至少选择一张图片'); return; }

    // 构造 FormData，并按顺序重命名文件名为 {game_id}_rank_{number}.jpg
    const formData = new FormData();
    formData.append('game_id', gameId);
    formData.append('stage', stage);

    // 上传前将用户选择顺序作为 number 序号
    state.files.forEach((item, idx) => {
      const ext = getFileExtension(item.file.name) || 'jpg';
      const numbered = `${gameId}_rank_${idx + 1}.${ext}`;
      const renamed = new File([item.file], numbered, { type: item.file.type });
      formData.append('files', renamed);
    });

    try {
      setLoading(true);
      const resp = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(text || `上传失败: ${resp.status}`);
      }
      const data = await resp.json();
      // 兼容两种返回：{ error_list: {...} } 或直接 {...}
      const errorList = data.error_list?.errors ? data.error_list : data;
      renderErrorTable(errorList);
      showToast('上传并校验成功');
    } catch (err) {
      console.error(err);
      el.resultArea.classList.add('empty');
      el.resultArea.innerHTML = `<div class="empty-tip">请求失败：${escapeHtml(err.message || String(err))}</div>`;
      showToast('请求失败');
    } finally {
      setLoading(false);
    }
  });

  function getFileExtension(name) {
    const dot = name.lastIndexOf('.');
    if (dot === -1) return '';
    return name.slice(dot + 1).toLowerCase();
  }
})();


