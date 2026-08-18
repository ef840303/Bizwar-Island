#!/usr/bin/env python3
"""EV 選項 eff/res 模式閉包 bug 修正。
eff:S=>{let ok=chance(...);...},res:S=>ok?...
res 回呼看不到 eff 的區域變數 ok/moon → ReferenceError。
修正:
 - eff 內 `let ok=` → `S._ok=`;`let moon=` → `S._moon=`
 - res 內引用 ok/moon → S._ok/S._moon(含 893 行 (S._tmp!==undefined?S._tmp:moon) 與 898 行 (S._scandalOk!==undefined?S._scandalOk:ok))
只改 EV 選項字面量模式;ACTIONS/ongoingCorp 用 return {log,d} 不受影響。
"""
import re

path = 'index.html'
src = open(path, encoding='utf-8').read()

# 1) 選項 eff 內的宣告(let 只在物件字面量選項裡出現;ACTIONS 的 let ok 在同一函式,但改存 S._ok 也不錯——
#    為安全只換選項段:eff:S=>{let ok= 與 eff:S=>{let moon=)
src = re.sub(r'eff:S=>\{let ok=', 'eff:S=>{S._ok=', src)
src = re.sub(r'eff:S=>\{let moon=', 'eff:S=>{S._moon=', src)

# 2) res 內引用
src = src.replace('(S._tmp!==undefined?S._tmp:moon)', 'S._tmp')
src = src.replace('(S._scandalOk!==undefined?S._scandalOk:ok)', 'S._ok')
src = src.replace('res:S=>ok?', 'res:S=>S._ok?')
src = src.replace('res:S=>ok?"', 'res:S=>S._ok?"')

# 3) 驗證:還有無 res 內孤立 ok/moon 引用
leftovers = re.findall(r'res:S=>[^,}]*\b(?:ok|moon)\b[^,}]*', src)
print('res 內 ok/moon 殘留:', len(leftovers))
for l in leftovers[:20]:
    print(' ', l)

open(path, 'w', encoding='utf-8').write(src)
print('closure fix applied')
