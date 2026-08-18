# 股市系統完整植入(基於月制後的檔案)
import re
p = 'index.html'
s = open(p, encoding='utf-8').read()

# 1. newState 加欄位
a1 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,'
b1 = '    money:0, mcap:0, revenue:0, equity:100, stage:"籌備期", stageIdx:0, stageKeys:stageKeys,\n    stockPrice:0, enemyStake:0, stockHist:[],'
assert a1 in s and 'stockPrice:0' not in s
s = s.replace(a1, b1)

# 2. runFinance 上市段後加股價更新+敵意收購檢核
a2 = "  else {let r2=0.1+(S.profitLast>0?S.stats.mgmt*0.006:0)+(R()-0.5)*0.4;if(R()<0.03)r2=-0.2-R()*0.2;S.mcap=Math.max(1e6,Math.round(S.mcap*(1+r2)));}"
b2 = """  else {let r2=0.1+(S.profitLast>0?S.stats.mgmt*0.006:0)+(R()-0.5)*0.4;if(R()<0.03)r2=-0.2-R()*0.2;S.mcap=Math.max(1e6,Math.round(S.mcap*(1+r2)));
    // 股價=市值÷固定股本,每月更新
    const shares=S.staffCount*5000+500000;
    S.stockPrice=Math.round(S.mcap/shares);S.stockHist.push(S.stockPrice);
    if(S.stockHist.length>360)S.stockHist=S.stockHist.slice(-360);
    // 上市後每月檢核掠奪者建倉
    if(S.flags.listed&&R()<0.05+S.stageIdx*0.01){const bites=[1,2,2,3,3,4];S.enemyStake=Math.min(60,S.enemyStake+bites[Math.round(R()*5)]*0.6);
      if(S.enemyStake>=25&&!S.flags.raiderWarn){S.flags.raiderWarn=true;mile(S,"🔍",`盤面上出現異樣的大買盤——有掠奪者正在悄悄收集你的股票（敵方持股 ${Math.round(S.enemyStake*10)/10}%）……`);}
      if(S.enemyStake>=50&&!S.flags.raiderWin){S.flags.raiderWin=true;S.ending={t:"控制權易主",key:"raider",icon:"🦅"};S.alive=false;logLine(S.age,"🦅 掠奪者持股超過半數,股東會表決把你趕出董事會——"+S.name+"落入他人手中。",[],"death");}}
  }"""
assert a2 in s
s = s.replace(a2, b2)

# 3. ipo 行動升級(S.age>=3 是月制前語意? ACTIONS 內 S.age>=3 需改 S.year——月制腳本只改部分,此處補)
a3 = '{id:"ipo",icon:"🔔",t:"啟動 IPO 計畫",cond:S=>S.age>=3&&S.stageIdx>=5&&S.money>1e7,act:S=>{let ok=chance(S,0.35+sk("finance")*0.05);if(ok){return{log:"IPO 過會成功！公司敲鐘上市，融資與品牌力一飛沖天。",d:[...inc(S,{vision:5})]};}S.flags.ipoFailed=true;return{log:"上市聆訊被打回，券商建議再練一年。",d:[...money(S,-3000000),...inc(S,{happy:-4,finance:2})]};}},'
b3 = '{id:"ipo",icon:"🔔",t:"啟動 IPO 計畫",cond:S=>S.year>=3&&S.stageIdx>=5&&!S.flags.listed&&S.money>1e7,act:S=>{let ok=chance(S,0.35+sk("finance")*0.05);if(ok){S.flags.listed=true;S.stageIdx=6;S.stage=S.stageKeys[6];S.money+=1e8;const shares=S.staffCount*5000+500000;S.stockPrice=Math.round(S.mcap/shares);return{log:`🔔 IPO 過會成功！「${S.name}」正式敲鐘上市，募得 1 億元資金，股價起步 ${fmtMoney(S.stockPrice)} 元。`,d:[...inc(S,{vision:5,street:3})]};}S.flags.ipoFailed=true;return{log:"上市聆訊被打回，券商建議再練一年。",d:[...money(S,-3000000),...inc(S,{happy:-4,finance:2})]};}},'
assert a3 in s
s = s.replace(a3, b3)

# 4. 新股市行動(插 pr 前)
a4 = '  {id:"pr",icon:"🎙️",t:"公關止血",'
b4 = """  {id:"buyback",icon:"🛡️",t:"股票回購護盤",cond:S=>S.flags.listed&&S.money>5e6&&S.enemyStake>0,act:S=>{let amt=Math.min(S.money*0.25,5e7);S.money-=amt;const shares=S.staffCount*5000+500000;S.enemyStake=Math.max(0,S.enemyStake-amt/Math.max(1,S.stockPrice)/shares*100*1.5);S.mcap=Math.max(1e6,Math.round(S.mcap*1.05));return{log:`斥資 ${fmtMoney(amt)} 回購自家股票,股價撐起來了,掠奪者持股降至 ${Math.round(S.enemyStake*10)/10}%。`,d:[...inc(S,{street:2,finance:2})]};}},
  {id:"reissue",icon:"📜",t:"現金增發",cond:S=>S.flags.listed,act:S=>{let ok=chance(S,0.6+sk("finance")*0.04);if(ok){let amt=Math.round(S.mcap*0.08+1e6);S.money+=amt;S.equity=Math.max(20,S.equity-4);return{log:`現金增發募得 ${fmtMoney(amt)}，現金流滿血復活，但股權又被攤薄。`,d:[...inc(S,{finance:2,happy:-2})]};}return{log:"增發認購不足，市場對你的股票沒信心。",d:[...inc(S,{happy:-4,finance:1})]};}},
  {id:"raiderEvade",icon:"🕊️",t:"引入白衣騎士",cond:S=>S.flags.listed&&S.enemyStake>=10,act:S=>{let ok=chance(S,0.4+sk("nego")*0.05+sk("street")*0.04);if(ok){S.enemyStake=Math.max(0,S.enemyStake-15);S.flags.whiteKnight=true;return{log:"白衣騎士進場接盤掠奪者的籌碼,敵意收購解除——代價是讓出一部分股權。",d:inc(S,{nego:3,street:2})};}return{log:"談判破裂,掠奪者繼續吃貨。",d:inc(S,{happy:-4,nego:1})};}},
  {id:"pr",icon:"🎙️",t:"公關止血","""
assert a4 in s
s = s.replace(a4, b4)

# 5. EV 新事件 stockCrash + predatorBid(插在 born 前)
a5 = '{id:"born",min:0,max:0,w:999,eff:S=>{'
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
assert a5 in s
s = s.replace(a5, ev_new + a5)

# 6. HUD 股價顯示
a6 = "const asub=$(\"assetSub\");if(asub){const parts=[];parts.push(`估值 ${fmtMoney(S.mcap).replace(\"NT$\",\"\")}`);if(S.equity<100)parts.push(`持股 ${S.equity}%`);parts.push(`營收 ${fmtMoney(S.revenue).replace(\"NT$\",\"\")}`);asub.textContent=parts.join(\"・\");}"
b6 = "const asub=$(\"assetSub\");if(asub){const parts=[];parts.push(`估值 ${fmtMoney(S.mcap).replace(\"NT$\",\"\")}`);if(S.flags.listed)parts.push(`股價 ${fmtMoney(S.stockPrice||0).replace(\"NT$\",\"\")}${S.enemyStake>0?` ⚠️敵方 ${Math.round(S.enemyStake*10)/10}%`:\"\"}`);if(S.equity<100)parts.push(`持股 ${S.equity}%`);parts.push(`營收 ${fmtMoney(S.revenue).replace(\"NT$\",\"\")}`);asub.textContent=parts.join(\"・\");}"
if 'stockLabel' not in s:
    assert a6 in s, 'asub anchor missing: ' + a6[:60]
    s = s.replace(a6, b6)

# 7. mcapHist 滑窗
s = s.replace('S.mcapHist.push(S.mcap);', 'S.mcapHist.push(S.mcap);if(S.mcapHist.length>600)S.mcapHist=S.mcapHist.slice(-600);')

# 8. 結算畫面股市欄
a8 = '<div class="s"><span>經營年數</span><b>${S.year} 年</b></div>'
b8 = '<div class="s"><span>經營年數</span><b>${S.year} 年</b></div>\n    <div class="s"><span>股市紀錄</span><b>${S.flags.listed?("🔔 上市公司,股價 "+fmtMoney(S.stockPrice||0).replace("NT$","")+" · 敵方持股 "+Math.round(S.enemyStake*10)/10+"%"):"未上市"}</b></div>'
if '股市紀錄' not in s:
    assert a8 in s
    s = s.replace(a8, b8)

# 9. 分享 PNG 欄位
a9 = 'peakMoney:p.mcap||0, finalMoney:nwFinal,'
b9 = 'peakMoney:p.mcap||0, finalMoney:nwFinal, listed:S.flags.listed, stockPrice:S.stockPrice||0, enemyStake:S.enemyStake||0,'
if 'listed:S.flags.listed' not in s:
    assert a9 in s
    s = s.replace(a9, b9)

# 10. endLabel 加 raider 結局映射(找 endMap 定義)
if '"raider"' not in s:
    m = re.search(r'(const endMap=\{[^}]+\})', s)
    if m:
        old = m.group(1)
        new = old[:-1] + ',raider:{t:"控制權易主,企業淪為獵物",icon:"🦅"}}'
        s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('stocks3 ALL OK')
