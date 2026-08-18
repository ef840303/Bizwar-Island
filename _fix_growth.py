"""成長平衡修正:營收成長率降速、員工自然成長封頂、上市段市值波動降溫。"""
import re

path = 'index.html'
src = open(path).read()

changes = 0

# 1) runOps 營收成長:能力項係數砍半、景氣波動降、clamp 收窄
old1 = "let grow=0.05*S.sectorGrowth+(S.stats.sales*0.008+S.stats.tech*0.007+S.stats.vision*0.005)*(1+st*0.12);"
new1 = "let grow=0.05*S.sectorGrowth+(S.stats.sales*0.004+S.stats.tech*0.0035+S.stats.vision*0.0025)*(1+st*0.12);"
if old1 in src:
    src = src.replace(old1, new1); changes += 1
else:
    print('MISS 1:', old1[:60])

old2 = "grow+=(R()-0.5)*0.16; if(R()<0.035)grow-=0.3+R()*0.25;"
new2 = "grow+=(R()-0.5)*0.08; if(R()<0.035)grow-=0.3+R()*0.25;"
if old2 in src:
    src = src.replace(old2, new2); changes += 1
else:
    print('MISS 2:', old2[:60])

old3 = "grow=clamp(grow,-0.5,0.5);"
new3 = "grow=clamp(grow,-0.15,0.25);"
if old3 in src:
    src = src.replace(old3, new3); changes += 1
else:
    print('MISS 3:', old3[:60])

# 2) 上市段市值波動降溫
old4 = "else {let r2=0.1+(S.profitLast>0?S.stats.mgmt*0.006:0)+(R()-0.5)*0.4;if(R()<0.03)r2=-0.2-R()*0.2;"
new4 = "else {let r2=0.05+(S.profitLast>0?S.stats.mgmt*0.004:0)+(R()-0.5)*0.2;if(R()<0.03)r2=-0.15-R()*0.1;"
if old4 in src:
    src = src.replace(old4, new4); changes += 1
else:
    print('MISS 4:', old4[:60])

# 3) 員工自然成長:封頂 stageCap,月化成長率
old5 = "if(S.staffCount>0){S.staffCount=Math.max(1,Math.round(S.staffCount*(1+0.02+st*0.02+(S.stats.mgmt*0.002-0.008)+(R()-0.5)*0.04)));}"
new5 = "if(S.staffCount>0){const capNow=staffCap||[3,20,60,200,600,1500,4000,12000,25000][Math.min(S.stageIdx,8)]||25000;let gr=0.005+st*0.005+(S.stats.mgmt*0.0008-0.004)+(R()-0.5)*0.01;let ns=Math.round(S.staffCount*(1+gr));S.staffCount=Math.max(1,Math.min(ns,capNow));}"
if old5 in src:
    src = src.replace(old5, new5); changes += 1
else:
    print('MISS 5:', old5[:60])

# 4) 缺口擴編 hrate 降
old6 = "let hires=Math.max(0,Math.round(need*0.08));"
new6 = "let hires=Math.max(0,Math.round(need*0.05));"
if old6 in src:
    src = src.replace(old6, new6); changes += 1
else:
    print('MISS 6:', old6[:60])

open(path, 'w').write(src)
print(f'applied {changes}/6 changes')
