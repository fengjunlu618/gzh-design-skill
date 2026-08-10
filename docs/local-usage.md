# 本机使用经验 (2026-08 实测)

gzh-design-skill 从 isjiamu/gzh-design-skill git clone 到
/root/.hermes/skills/gzh-design-skill (实体目录, 非软链)。脚本绝对路径:
`/root/.hermes/skills/gzh-design-skill/scripts/`。

## 排版闭环 (每篇必走)

1. 读 references/theme-index.md 选主题 (教程/测评→摸鱼绿, 深度分析→红白,
   设计/科技→石墨, 随笔→禅意, 工具对比→票据, 复盘→橄榄手记)。
2. 读所选 theme-*.md + common-components.md, HTML 一律从组件库取, 不手写。
3. 装配 → 存 `{名}_排版_{主题}({标识}).html`。
4. `python3 <SKILL_ROOT>/scripts/validate_gzh_html.py <html>` → ERROR 清零。
5. 半角标点 WARNING 同样修到 0 (最高频返工点) — 用
   `scripts/fix_halfwidth_punct.py <html>` 批量修, 再校验。
6. `python3 <SKILL_ROOT>/scripts/wrap_preview.py <html>` → 预览页。

## 半角标点批量修复 (实测有效)

validate 抓出的 WARNING 通常是正文里的半角 `, : ? !` 和 ASCII 直引号。
直接全文 sed 会误伤 CSS 属性和代码块, 必须用脚本, 三个保护:
- 跳过含 `SF Mono` / `Consolas` 的行 (深色代码块内容保持半角)
- 数字间冒号保留 (如 9:16 比例)
- 直引号只替换紧贴中文短语两侧的 `"..."` (成对闭合), 换中文弯引号

## 视觉验收兜底

用户要求真实视觉验收。本机路径:
1. 无头 Chrome 截图: `google-chrome --headless --disable-gpu --no-sandbox
   --screenshot=shot.png --window-size=480,1400 --hide-scrollbars
   "file:///...预览.html"` (480 宽模拟手机)。
2. 当前主模型 (deepseek 系) 的辅助 vision 端点只收 text, vision_analyze 会报
   `unknown variant image_url` — 这是模型限制, 不是图片问题。兜底用浏览器
   DOM 检查: browser_navigate 打开 file:// 预览页, browser_console 执行
   `JSON.stringify({docW: document.documentElement.scrollWidth, winW: window.innerWidth, overflow: scrollWidth>innerWidth, sections: querySelectorAll('section').length, leafSpans: querySelectorAll('span[leaf]').length})`
   确认无横向溢出 + 组件齐全, 并把截图路径交给用户自己看。

## 编码与响应式 (用户实测踩坑, 必须做)

- **片段中文乱码**: 干净正文是纯 section 片段、无 `<meta charset>`, 用户工具按
  GBK 解析会满屏乱码 (用户报过「中文是乱码啊」)。交付前给两个产物文件都加
  **UTF-8 BOM** (`open(p,'wb').write(b'\xef\xbb\xbf'+data)`), BOM 不影响微信
  粘贴 (粘的是富文本不是文件字节)。validate 脚本不受 BOM 影响。
- **响应式验收**: 片段无 viewport meta (平台合规, 不能加), 真机直接打开会按
  980px 布局缩放成小字 (用户报过「没有做到响应式设计」)。正确入口是预览页
  (有 viewport)。预览模板 `assets/preview-template.html` 已加**视口切换按钮**
  (自适应 / 📱375 / 💻768 / 🖥1280, JS 函数 gzhSetWidth), 用它验收响应式;
  交付时明确告知用户: 看效果用 `_预览.html`, 片段文件只用于粘贴。

## 其它实测结论

- component_lint.py 在仓库根跑: 9/11 库干净, ERROR×0 (2 个 WARN 是主题库
  特征虚线框, 属预期)。
- 校验脚本对违规 HTML (style/div/class) 能确定性拦截并精确报位置, 可放心
  依赖; 成品判定 "✅ 完全合规" 才交付。
- 署名区默认 `{{作者名}}` 占位, 用户没给署名就保留占位并提示替换, 不写死。
