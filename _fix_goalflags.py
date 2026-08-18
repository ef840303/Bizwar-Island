#!/usr/bin/env python3
"""修正志向 prog 的 flag 引用:
- techking: koiHit(錦鯉求籤 flag)是誤植,改用專利事件觸發的 flags.newPatent
- 需在專利事件處設定 flags.newPatent=true
"""
path = 'index.html'
src = open(path).read()

# 1. techking 志向改用 newPatent
old = '(Math.max(S.peak.tech||0)/100*0.55)+((S.flags.koiHit||0)+0)+(S.peak.tech>=90?0.25:0)'
new = '(Math.max(S.peak.tech||0)/100*0.55)+((S.flags.newPatent||0)*0.15)+(S.peak.tech>=90?0.25:0)'
assert old in src, 'techking old pattern not found'
src = src.replace(old, new)

# 2. 專利事件(984 行附近 "關鍵專利核准")設定 flags.newPatent
old2 = 'if(chance(S,0.5)){S.mcap=Math.round((S.mcap||S.revenue*3)*1.2);mile(S,"📜","關鍵專利核准!護城河加寬。");}'
new2 = 'if(chance(S,0.5)){S.mcap=Math.round((S.mcap||S.revenue*3)*1.2);S.flags.newPatent=true;mile(S,"📜","關鍵專利核准!護城河加寬。");}'
assert old2 in src, 'patent event pattern not found'
src = src.replace(old2, new2)

open(path, 'w').write(src)
print('goal flags fixed')
