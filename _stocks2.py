# 股市 HUD + 結算欄 + mcapHist 滑窗 + 新狀態欄位
p = 'index.html'
s = open(p, encoding='utf-8').read()

# 1. HUD: assetSub 加股價與敵方持股
a1 = "const asub=$(\"assetSub\");if(asub){const parts=[];parts.push(`估值 ${fmtMoney(S.mcap).replace(\"NT$\",\"\")}`);if(S.equity<100)parts.push(`持股 ${S.equity}%`);parts.push(`營收 ${fmtMoney(S.revenue).replace(\"NT$\",\"\")}`);asub.textContent=parts.join(\"・\");}"
b1 = "const asub=$(\"assetSub\");if(asub){const parts=[];parts.push(`估值 ${fmtMoney(S.mcap).replace(\"NT$\",\"\")}`);if(S.flags.listed)parts.push(`股價 ${fmtMoney(S.stockPrice||0).replace(\"NT$\",\"\")}${S.enemyStake>0?` ⚠️敵方 ${Math.round(S.enemyStake*10)/10}%`:\"\"}`);if(S.equity<100)parts.push(`持股 ${S.equity}%`);parts.push(`營收 ${fmtMoney(S.revenue).replace(\"NT$\",\"\")}`);asub.textContent=parts.join(\"・\");}"
assert a1 in s
s = s.replace(a1, b1)

# 2. mcapHist 滑窗(防爆炸)
s = s.replace('S.mcapHist.push(S.mcap);', 'S.mcapHist.push(S.mcap);if(S.mcapHist.length>600)S.mcapHist=S.mcapHist.slice(-600);')

# 3. 結算畫面:peakStage 後加股市欄(找 gradeSub 後的 end card 欄位列)
a3 = '<div class="s"><span>經營年數</span><b>${S.year} 年</b></div>'
b3 = '<div class="s"><span>經營年數</span><b>${S.year} 年</b></div>' + ('' if '${S.flags.listed?"🔔 上市公司 · 最終股價 "+fmtMoney(S.stockPrice||0).replace("NT$",""):""}' == '' else '')
# 改用明確插入
s = s.replace(a3, a3 + '\n    <div class="s"><span>股市紀錄</span><b>${S.flags.listed?("🔔 上市公司,股價 "+fmtMoney(S.stockPrice||0).replace("NT$","")+" · 敵方持股 "+Math.round(S.enemyStake*10)/10+"%"):"未上市"}</b></div>')

# 4. newState 欄位補強
a4 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,'
b4 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,\n    stockPrice:0, enemyStake:0, stockHist:[],'
if 'stockPrice:0' not in s:
    s = s.replace(a4, b4)

# 5. 分享 PNG 加股市資訊
a5 = 'peakMoney:p.mcap||0, finalMoney:nwFinal,'
b5 = 'peakMoney:p.mcap||0, finalMoney:nwFinal, listed:S.flags.listed, stockPrice:S.stockPrice||0, enemyStake:S.enemyStake||0,'
if 'listed:S.flags.listed' not in s:
    s = s.replace(a5, b5)

open(p, 'w', encoding='utf-8').write(s)
print('stocks2 OK')
