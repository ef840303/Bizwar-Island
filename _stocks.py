import re
# 股市系統完整植入
p = 'index.html'
s = open(p, encoding='utf-8').read()

# ============ 1. newState 加欄位 ============
a1 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,'
b1 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,\n    stockPrice:0, enemyStake:0, stockHist:[],'
assert a1 in s
s = s.replace(a1, b1)

# ============ 2. runFinance 內上市後啟動股價 + 每月 runStock 呼叫點 ============
# 2a. 在 runFinance 上市段之後初始化股價(若尚未初始化)
a2 = "  else {let r2=0.1+(S.profitLast>0?S.stats.mgmt*0.006:0)+(R()-0.5)*0.4;if(R()<0.03)r2=-0.2-R()*0.2;S.mcap=Math.max(1e6,Math.round(S.mcap*(1+r2)));}"
b2 = """  else {let r2=0.1+(S.profitLast>0?S.stats.mgmt*0.006:0)+(R()-0.5)*0.4;if(R()<0.03)r2=-0.2-R()*0.2;S.mcap=Math.max(1e6,Math.round(S.mcap*(1+r2)));
    // 股價=市值÷固定股本,每月更新
    const shares=S.staffCount*5000+500000;
    S.stockPrice=Math.round(S.mcap/shares);S.stockHist.push(S.stockPrice);
    if(S.stockHist.length>360)S.stockHist=S.stockHist.slice(-360);
    // 上市後每月檢核敵意收購建倉(掠奪者逐步吃貨)
    if(S.flags.listed&&R()<0.05+S.stageIdx*0.01){const bites=[1,2,2,3,3,4];S.enemyStake=Math.min(60,S.enemyStake+bites[Math.round(R()*5)]*0.6);
      if(S.enemyStake>=25&&!S.flags.raiderWarn){S.flags.raiderWarn=true;mile(S,"🔍",`盤面上出現異樣的大買盤——有掠奪者正在悄悄收集你的股票（敵方持股 ${Math.round(S.enemyStake*10)/10}%）……`);}
      if(S.enemyStake>=50&&!S.flags.raiderWin){S.flags.raiderWin=true;S.ending={t:"控制權易主",key:"raider",icon:"🦅"};S.alive=false;logLine(S.age,"🦅 掠奪者持股超過半數,股東會表決把你趕出董事會——"+S.name+"落入他人手中。",[],"death");}}
  }"""
assert a2 in s
s = s.replace(a2, b2)

# ============ 3. ACTIONS ipo 行動升級:成功即 listed=true + 觸發上市慶典 ============
a3 = '{id:"ipo",icon:"🔔",t:"啟動 IPO 計畫",cond:S=>S.year>=3&&S.stageIdx>=5&&S.money>1e7,act:S=>{let ok=chance(S,0.35+sk("finance")*0.05);if(ok){return{log:"IPO 過會成功！公司敲鐘上市，融資與品牌力一飛沖天。",d:[...inc(S,{vision:5})]};}S.flags.ipoFailed=true;return{log:"上市聆訊被打回，券商建議再練一年。",d:[...money(S,-3000000),...inc(S,{happy:-4,finance:2})]};}},'
b3 = '{id:"ipo",icon:"🔔",t:"啟動 IPO 計畫",cond:S=>S.year>=3&&S.stageIdx>=5&&!S.flags.listed&&S.money>1e7,act:S=>{let ok=chance(S,0.35+sk("finance")*0.05);if(ok){S.flags.listed=true;S.stageIdx=6;S.stage=S.stageKeys[6];S.money+=1e8;const shares=S.staffCount*5000+500000;S.stockPrice=Math.round(S.mcap/shares);return{log:`🔔 IPO 過會成功！「${S.name}」正式敲鐘上市，募得 1 億元資金，股價起步 ${fmtMoney(S.stockPrice)} 元。`,d:[...inc(S,{vision:5,street:3})]};}S.flags.ipoFailed=true;return{log:"上市聆訊被打回，券商建議再練一年。",d:[...money(S,-3000000),...inc(S,{happy:-4,finance:2})]};}},'
assert a3 in s
s = s.replace(a3, b3)

# ============ 4. 新增股市行動 buyback/reissue/acquireRival ============
a4 = '  {id:"pr",icon:"🎙️",t:"公關止血",'
b4 = """  {id:"buyback",icon:"🛡️",t:"股票回購護盤",cond:S=>S.flags.listed&&S.money>5e6&&S.enemyStake>0,act:S=>{let amt=Math.min(S.money*0.25,5e7);S.money-=amt;const shares=S.staffCount*5000+500000;S.enemyStake=Math.max(0,S.enemyStake-amt/Math.max(1,S.stockPrice)/shares*100*1.5);S.mcap=Math.max(1e6,Math.round(S.mcap*1.05));return{log:`斥資 ${fmtMoney(amt)} 回購自家股票,股價撐起來了,掠奪者持股降至 ${Math.round(S.enemyStake*10)/10}%。`,d:[...inc(S,{street:2,finance:2})]};}},
  {id:"reissue",icon:"📜",t:"現金增發",cond:S=>S.flags.listed,act:S=>{let ok=chance(S,0.6+sk("finance")*0.04);if(ok){let amt=Math.round(S.mcap*0.08+1e6);S.money+=amt;S.equity=Math.max(20,S.equity-4);return{log:`現金增發募得 ${fmtMoney(amt)}，現金流滿血復活，但股權又被攤薄。`,d:[...inc(S,{finance:2,happy:-2})]};}return{log:"增發認購不足，市場對你的股票沒信心。",d:[...inc(S,{happy:-4,finance:1})]};}},
  {id:"raiderEvade",icon:"🕊️",t:"引入白衣騎士",cond:S=>S.flags.listed&&S.enemyStake>=10&&S.flags.cofounder===undefined,act:S=>{let ok=chance(S,0.4+sk("nego")*0.05+sk("street")*0.04);if(ok){S.enemyStake=Math.max(0,S.enemyStake-15);S.flags.whiteKnight=true;return{log:"白衣騎士進場接盤掠奪者的籌碼,敵意收購解除——代價是讓出一部分股權。",d:inc(S,{nego:3,street:2})};}return{log:"談判破裂,掠奪者繼續吃貨。",d:inc(S,{happy:-4,nego:1})};}},
  {id:"pr",icon:"🎙️",t:"公關止血","""
assert a4 in s
s = s.replace(a4, b4)

# ============ 5. EV 新事件:股市崩盤 stockCrash + 掠奪者敲門 predatorBid ============
# 找 EV 陣列中一個 minor 事件之後插入(用 born 事件之後的 anchor)
a5 = '{id:"born",min:0,max:0,w:999,eff:S=>{'
# 在 born 事件結尾的 '}},' 後插入兩個新事件
ev_new = """{id:"stockCrash",min:3,max:8,w:4,cond:S=>S.flags.listed&&S.year>=3&&S.equity>20,choice:true,q:"📉 股市劇烈回檔！你的股票單月暴跌，散戶哀鴻遍野。要怎麼應對？",
 options:[
  {t:"📢 公開說明會穩定信心",hint:"花錢但不流血",eff:S=>{S.mcap=Math.round(S.mcap*0.9);return{log:"召開說明會釋放利多，跌勢趨緩，市值縮水但人氣回流。",d:[...money(S,-3e6),...inc(S,{street:3,happy:2})]};}},
  {t:"🛡️ 大筆回購護盤",hint:"花大錢護住股價",eff:S=>{let amt=Math.min(S.money*0.3,8e7);S.money-=amt;S.mcap=Math.round(S.mcap*0.95);return{log:`斥資 ${fmtMoney(amt)} 護盤，股價止跌回穩，現金流被吸掉一大口。`,d:inc(S,{street:4})};}},
  {t:"🧘 躺平不動",hint:"讓市場自己修復",eff:S=>{S.mcap=Math.round(S.mcap*0.82);S.stockPrice=Math.round(S.mcap/(S.staffCount*5000+500000));return{log:"跌深自然有人接，但市值蒸發了 18%，輿論酸你無作為。",d:[...inc(S,{happy:-6})]};}},
]},
{id:"predatorBid",min:4,max:9,w:3,cond:S=>S.flags.listed&&S.enemyStake>=8,choice:true,q:"🦅 掠奪者舉牌了！公開宣布要收購你的公司，散戶開始拋售。",
 options:[
  {t:"⚔️ 反擊：增購自家股權",hint:"把敵方持股壓回去",eff:S=>{let amt=Math.min(S.money*0.35,1e8);S.money-=amt;const shares=S.staffCount*5000+500000;S.enemyStake=Math.max(0,S.enemyStake-amt/Math.max(1,S.stockPrice)/shares*100*1.8);return{log:`反收購大作戰！斥資 ${fmtMoney(amt)} 拉高敵方吃貨成本,對方持股降至 ${Math.round(S.enemyStake*10)/10}%。`,d:inc(S,{street:4,nego:2})};}},
  {t:"🕊️ 談判:賣一部分給對方",hint:"化敵為友,分一杯羹",eff:S=>{S.money+=S.mcap*0.12;S.equity=Math.max(20,S.equity-10);S.flags.neutralized=true;return{log:"簽下和解協議,掠奪者轉為策略股東——你拿到一筆和解金,但交出了部分主導權。",d:[...inc(S,{nego:4,happy:-2})]};}},
  {t:"🏰 毒丸防禦",hint:"兩敗俱傷的嚇阻",eff:S=>{S.flags.poisonPill=true;S.enemyStake=Math.max(0,S.enemyStake-5);S.mcap=Math.round(S.mcap*0.92);return{log:"祭出毒丸條款,掠奪者吃貨成本暴增被迫收手——你的股價也跌了一大截。",d:[...inc(S,{street:3,happy:-4})]};}},
]},
"""
i = s.find(a5)
assert i >= 0
# born 事件是陣列第一筆,插入到 born 之前
s = s[:i] + ev_new + s[i:]

# ============ 6. HUD 股價顯示:在 mcap 附近加 stock chip ============
# 找 moneyLabel 渲染段,加 stockLabel
a6 = '$("moneyLabel")'
if '$("stockLabel")' not in s:
    pass
# 先看 moneyLabel 寫入的程式碼
m = re.search(r'\$\("moneyLabel"\)\s*=\s*[^\n]+\n', s)
print('moneyLabel render:', m.group(0) if m else 'NOT FOUND')
mcapHist_push = re.search(r'S\.mcapHist\.push\(([^)]*)\);', s)
print('mcapHist push:', mcapHist_push.group(0) if mcapHist_push else 'none')

open(p, 'w', encoding='utf-8').write(s)
print('stocks part2 OK')
