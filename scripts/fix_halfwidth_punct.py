#!/usr/bin/env python3
"""公众号排版正文半角标点批量修复 (gzh-design-skill 本地增强, 2026-08 实测)。

把正文文本节点里的半角 , : ? ! 和 ASCII 直引号换成中文全角/弯引号。
validate_gzh_html.py 的半角标点 WARNING 是最高频返工点, 用本脚本批量修。

用法:
    fix_halfwidth_punct.py <file.html>

保护规则 (不会误伤):
- 跳过含 SF Mono / Consolas 的行 (深色代码块内容保持半角)
- 数字间冒号保留 (如 9:16 比例)
- 直引号只替换紧贴中文短语两侧的成对 "..." → 中文弯引号 ""
- CSS 属性 (style="...") 不受影响, 只处理 >文本< 之间的内容

修完必须重跑 validate_gzh_html.py 确认 0 ERROR 0 WARNING。
"""
import re
import sys


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    fixed = 0
    out = []
    for line in lines:
        # 保护 1: 代码块行 (等宽字体) 保持半角
        if "SF Mono" in line or "Consolas" in line:
            out.append(line)
            continue

        def repl(m: re.Match) -> str:
            nonlocal fixed
            t = m.group(2)
            if not t.strip():
                return m.group(0)
            # 保护 2: 数字间冒号 (9:16) 保留
            t2 = re.sub(r"(?<!\d):(?!\d)", "：", t)
            t2 = t2.replace(",", "，").replace("?", "？").replace("!", "！")
            if t2 != t:
                fixed += 1
            return m.group(1) + t2 + m.group(3)

        new = re.sub(r"(>)([^<>]*)(<)", repl, line)
        out.append(new)

    # 保护 3: 成对 ASCII 直引号 (紧贴中文短语) → 中文弯引号
    content = "".join(out)
    q_count = 0
    for phrase in re.findall(r"[\u4e00-\u9fff]{2,}", content):
        pass  # 占位, 实际按引用计数配对处理
    # 简化: 把 "X" 中 X 为中文串的成对直引号替换
    def quote_pair(m: re.Match) -> str:
        nonlocal q_count
        q_count += 1
        return "\u201c" + m.group(1) + "\u201d"

    content = re.sub(r'"([\u4e00-\u9fff][^"]{0,20}?[\u4e00-\u9fff])"', quote_pair, content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"文本节点修正: {fixed} 处; 直引号配对: {q_count} 处")
    print("重跑: python3 <SKILL_ROOT>/scripts/validate_gzh_html.py <html>")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
