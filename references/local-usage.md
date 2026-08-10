# 本机实测经验（2026-08 完整排版闭环）

gzh-design-skill 位于 /root/.hermes/skills/gzh-design-skill（git clone 实体目录）。
脚本绝对路径: `<skill>/scripts/`。

## 排版闭环（每篇必走）

1. 读 references/theme-index.md 选主题（教程/测评→摸鱼绿, 深度分析→红白, 设计/科技→石墨, 随笔→禅意, 工具对比→票据, 复盘→橄榄手记）。
2. 读所选 theme-*.md + common-components.md，HTML 一律从组件库取，不手写。
3. 装配 → 存 `{名}_排版_{主题}({标识}).html`。
4. `python3 <SKILL_ROOT>/scripts/validate_gzh_html.py <html>` → ERROR 清零。
5. 半角标点 WARNING 同样修到 0（最高频返工点）— 用 `scripts/fix_halfwidth_punct.py` 批量修再校验。
6. `python3 <SKILL_ROOT>/scripts/wrap_preview.py <html>` → 预览页。
7. 两个产物都加 UTF-8 BOM。

## 半角标点批量修复保护规则（sed 会误伤，必须用脚本）

- 跳过含 `SF Mono` / `Consolas` 的行（深色代码块内容保持半角）
- 数字间冒号保留（如 9:16 比例）
- 直引号只替换紧贴中文短语两侧的成对 `"..."` → 中文弯引号
- 只在 `>文本<` 标签节点内替换，不动 style 属性

## 视觉验收兜底（辅助 vision 模型只收 text 时）

- 无头 Chrome 截图: `google-chrome --headless --disable-gpu --no-sandbox --screenshot=shot.png --window-size=375,900 --hide-scrollbars "file:///..._预览.html"`
- 若 vision_analyze 报 `unknown variant image_url`（deepseek 系辅助端点只收 text），是模型限制不是图片问题 → 用浏览器 DOM 检查兜底:
  `JSON.stringify({docW: document.documentElement.scrollWidth, winW: window.innerWidth, overflow: scrollWidth>innerWidth, sections: querySelectorAll('section').length, leafSpans: querySelectorAll('span[leaf]').length})`
  确认无横向溢出 + 组件齐全，把截图路径交给用户自己看。

## 编码与响应式（用户实测踩坑，必须做）

- **片段中文乱码**: 干净正文无 `<meta charset>`，用户工具按 GBK 解析会乱码（用户报过）。交付前两个产物都加 UTF-8 BOM，BOM 不影响微信粘贴。
- **响应式验收**: 片段无 viewport（合规不能加），真机打开按 980px 缩放小字（用户报过）。正确入口是预览页（有 viewport + 375/768/1280 切换按钮）。交付时明确告知: 看效果用 `_预览.html`，片段只用于粘贴。
- **目录卡不可点**: 公众号禁 JS，目录纯展示属正常。预览外壳可加 gzhInitToc（章节名文本匹配 + 平滑滚动 + toast），正文保持零 JS。

## 其它实测结论

- component_lint.py 在仓库根跑: 9/11 库干净 ERROR×0（2 WARN 是主题库特征虚线框，属预期）。
- 校验脚本对违规 HTML（style/div/class）能确定性拦截并精确报位置；成品判定"完全合规"才交付。
- 署名区默认 `{{作者名}}` 占位，用户没给署名就保留占位并提示替换，不写死。
