#!/usr/bin/env python3
"""第二輪閉包修正。
第一輪只改了 eff 內的 let 宣告(let ok= → S._ok=),但 eff 函式內後面的
ok/moon 引用(if(ok)、ok?、:ok?、S._scandalOk=ok、S._tmp=moon、if(moon))還在。
修正:逐行處理 eff:S=>{ 開頭的選項行,把宣告後的孤立 ok/moon 引用全部換掉。
限制在同一行處理;對於 ok?1.3:1.02 這類三元已用 ok 的也換。
確認只碰 EV 選項行(grep 'eff:S=>'),不碰 ACTIONS(act:S=>)。
"""
import re

path = 'index.html'
lines = open(path, encoding='utf-8').read().split('\n')
out = []
for i, line in enumerate(lines):
    if 'eff:S=>' in line and ('_ok=' in line or '_moon=' in line or 'ok?' in line):
        # 若此行仍有 eff:S=>{let ok= 或 let moon=(第一輪漏掉的)先處理宣告
        line = line.replace('eff:S=>{let ok=', 'eff:S=>{S._ok=')
        line = line.replace('eff:S=>{let moon=', 'eff:S=>{S._moon=')
        # 宣告後的孤立引用:先處理 moon(避免 ok 換後 moon 仍殘留),再處理 ok
        line = re.sub(r'\bS\._tmp=moon\b', 'S._tmp=S._moon', line)
        line = re.sub(r'if\(moon\)', 'if(S._moon)', line)
        line = re.sub(r'\bmoon\b', 'S._moon', line)
        line = line.replace('S._scandalOk=ok', 'S._scandalOk=S._ok')
        line = re.sub(r'if\(ok\)', 'if(S._ok)', line)
        line = re.sub(r'if\(!ok\)', 'if(!S._ok)', line)
        line = re.sub(r'\bok\b\?', 'S._ok?', line)
        line = re.sub(r':\bok\b', ':S._ok', line)
        line = re.sub(r'\bok\b\)', 'S._ok)', line)
        # 檢查殘留(排除註解與字串中的 ok 詞如 ok?)——字串內若有「ok?」可能誤換,
        # 但字串是中文或英文句子很少含孤立 ok;保留原樣印出供檢查
        rem = re.findall(r'(?<!_)(?<!S\.)\bok\b', line.replace('eff:S=>{S._ok=', '').replace('eff:S=>{S._moon=', ''))
        if rem:
            print(f'LINE {i+1} 殘留 ok: {rem}')
    out.append(line)
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print('done')
