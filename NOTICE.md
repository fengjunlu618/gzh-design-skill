# NOTICE

## 派生说明

本仓库是 [isjiamu/gzh-design-skill](https://github.com/isjiamu/gzh-design-skill)
（甲木 × 摸鱼小李，AGPL-3.0）的派生/增强版，保留原作者全部历史提交与
`LICENSE`（GNU Affero General Public License v3.0）。

## 本地增强（相对上游 main 分支）

1. **预览页视口切换** — `assets/preview-template.html`
   预览外壳新增设备视口切换工具栏（自适应 / 📱375 / 💻768 / 🖥1280），
   用于验收公众号排版在不同宽度下的响应式表现；手机窄屏自动收起提示文字。
2. **半角标点批量修复脚本** — `scripts/fix_halfwidth_punct.py`
   把正文文本节点的半角 `, : ? !` 与 ASCII 直引号批量转为中文全角/弯引号，
   对应 `validate_gzh_html.py` 最高频的 WARNING 返工点（代码块/行内代码自动跳过）。
3. **SKILL.md 工作流更新** — 输出步骤补充视口切换说明；实测验证的合规校验结论。
4. **本机使用笔记** — `docs/local-usage.md`（2026-08 实测排版闭环记录）。

## 合规

- 保留上游 `LICENSE`（AGPL-3.0），未做任何修改。
- 按 AGPL-3.0 要求，派生修改以本 NOTICE 声明；如您分发/修改本仓库，
  请同样保留 LICENSE 与本 NOTICE。

修改时间：2026-08-10
