# 月制改造:stepYear -> stepMonth;年度結算每年年末跑;籌備期 12 個月
p = 'index.html'
s = open(p, encoding='utf-8').read()

# ---------- 1. newState:加 month ----------
s = s.replace('age:0, alive:true, paused:false, year:0,', 'age:0, alive:true, paused:false, year:0, month:1,')

# ---------- 2. renderGame:年齡標籤改「第 N 年 M 月」 ----------
s = s.replace('$("ageLabel").textContent=S.age;',
              '$("ageLabel").textContent=S.year+" 年 "+S.month+" 月";')

# ---------- 3. logLine:歲 -> 年月 ----------
s = s.replace("const yr=year>=0?`<span class=\"yr\">${year}歲</span>`:`<span class=\"yr\">◆</span>`;",
              "const y=Math.floor(year/12),m=year%12+1;const yr=year>=0?`<span class=\"yr\">第 ${y} 年 ${m} 月</span>`:`<span class=\"yr\">◆</span>`;")

# ---------- 4. 主循環重寫 stepYear -> stepMonth ----------
old_main = '''function stepYear(){
  if(!S.alive)return;
  S.age++;
  S.actedThisYear=false;
  const s=S.stats;
  S.happySum+=s.happy;S.happyCount++;S.happyHist.push({x:S.age,y:s.happy});S.moneyHist.push({x:S.age,y:netWorth(S)});
  // 營運循環:營收、毛利、固定成本、市占
  runOps(S);
  // 財務循環:估值、稀釋、階段晉升
  runFinance(S);
  // 每年持續效果:競爭對手、人才流失
  ongoingCorp(S);
  // 企業稅(依毛利率與營收)
  if(S.revenue>0&&S.profitLast>0){
    let rate=S.profitLast/S.revenue>0.3?0.28:0.2;
    let tax=Math.round(S.profitLast*rate);
    if(tax){S.money-=tax;S.ledger=(S.ledger||{});S.ledger.op-=tax;}
  }
  // 利息支出(負債時)
  if(S.money<0){S.money-=Math.round(Math.abs(S.money)*0.08);S.stats.happy=clamp(S.stats.happy-2,0,100);}
  // 快樂回歸:現金流為正、獲利時快樂回升
  s.happy+=(S.profitLast>=0?58:40-s.happy)*0.05;
  // 階段越高、健康折舊(創辦人過勞)
  if(S.age%4===0&&S.stageIdx>=3)s.street=clamp(s.street-1,0,100);
  if(s.happy<35)s.street=clamp(s.street-1,0,100);
  if(s.happy>70)s.street=clamp(s.street+1,0,100);
  // 里程碑:身價/週年/條件骰子
  checkWealthMile(S); checkAgeMile(S); checkDiceMile(S);
  // 死亡條件:破產/健康/高齡(見 checkDeath)
  // 多段式劇情鏈:到期的後續事件優先觸發
  if(S.pending&&S.pending.length){
    let idx=S.pending.findIndex(p=>p.at<=S.age);
    while(idx>=0){
      const p=S.pending.splice(idx,1)[0];const cev=EV.find(e=>e.id===p.ev);
      if(cev&&(!cev.cond||cev.cond(S))){
        if(cev.choice){presentChoice(cev);clampStats();renderGame();return;}
        applyEvent(cev);afterMain();return;
      }
      idx=S.pending.findIndex(p=>p.at<=S.age);
    }
  }
  // 特訓骰子:每 3 年 2 顆 + 里程碑獎勵骰
  if(S.dice.length===0){
    const normalDue=(S.age>=2&&S.age<=36&&S.age-S.lastAlloc>=3);
    const n=(normalDue?2:0)+(S.bonusDice||0);
    if(n>0){
      S.bonusDice=0;
      if(normalDue)S.lastAlloc=S.age;
      S.dice=[];for(let i=0;i<n;i++)S.dice.push(1+rnd(3));
      presentSkillAlloc();clampStats();renderGame();return;
    }
  }
  // 主事件
  const ev=pickEvent("main");
  if(ev){
    if(ev.choice){presentChoice(ev);clampStats();renderGame();return;}
    applyEvent(ev);
  }
  afterMain();
}'''

new_main = '''function stepMonth(){
  if(!S.alive)return;
  S.age++;S.year=Math.floor(S.age/12);S.month=S.age%12+1;
  const s=S.stats;
  const isYearEnd=(S.month===1); // 每年 1 月是新一年的開始,結算放在 12 月
  // 每月進度:士氣歷史、淨值歷史(每年存一筆,平滑曲線)
  if(S.month===1){S.happyHist.push({x:S.year,y:s.happy});S.moneyHist.push({x:S.year,y:netWorth(S)});}
  // 營運循環(月版):營收、毛利、固定成本、市占
  runOps(S);
  // 每月營運開支與利息(月版,年度利息/稅在年末結算)
  if(S.money<0){S.money-=Math.round(Math.abs(S.money)*0.006);if(S.month===1)s.happy=clamp(s.happy-1,0,100);}
  // 快樂微調
  s.happy+=(S.profitLast>=0?0.6:0.3-s.happy*0.005);
  // 籌備期(第 1 年,12 個月)
  const prep=(S.stageIdx===0&&S.year===0);
  if(prep){
    // 籌備期每月投骰 1 顆,讓玩家有成長手感
    if(S.month===12){logLine(S.age,"📦 一年籌備期滿,公司正式掛牌營運!",[],"mile");S.stageIdx=1;S.stage=S.stageKeys[1];S.flags.hired=true;S.staffCount=3;}
    if(S.dice.length===0&&S.month<=11){
      S.dice=[1+rnd(3)];
      presentSkillAlloc();clampStats();renderGame();return;
    }
  }
  // 財務循環:估值、稀釋、階段晉升
  runFinance(S);
  // 競爭對手
  ongoingCorp(S);
  // 股市:上市公司每月更新股價與敵方持股(見 runStock)
  if(S.flags.listed)runStock(S);
  // 每年 12 月年末結算(年度回顧)
  if(!prep&&S.month===12){
    S.actedThisYear=false;
    // 企業稅
    if(S.revenue>0&&S.profitLast>0){
      let rate=S.profitLast/S.revenue>0.3?0.28:0.2;
      let tax=Math.round(S.profitLast*rate);
      if(tax){S.money-=tax;S.ledger=(S.ledger||{});S.ledger.op-=tax;}
    }
    // 年度利息
    if(S.money<0){S.money-=Math.round(Math.abs(S.money)*0.08);s.happy=clamp(s.happy-2,0,100);}
    // 快樂回歸
    s.happy+=(S.profitLast>=0?58:40-s.happy)*0.05;
    // 健康折舊
    if(S.year%4===0&&S.stageIdx>=3)s.street=clamp(s.street-1,0,100);
    if(s.happy<35)s.street=clamp(s.street-1,0,100);
    if(s.happy>70)s.street=clamp(s.street+1,0,100);
    // 里程碑
    checkWealthMile(S); checkAgeMile(S); checkDiceMile(S);
    // 年度回顧
    mile(S,"🗓️",`第 ${S.year} 年總結:營收 ${fmtMoney(S.revenue).replace("NT$","")},團隊 ${S.staffCount} 人,${S.money>=0?"現金流健康":"負債經營中"}`);
  }
  // 死亡條件:破產/健康/高齡(見 checkDeath)
  // 多段式劇情鏈:到期的後續事件優先觸發(以年為單位到期)
  if(S.pending&&S.pending.length){
    let idx=S.pending.findIndex(p=>p.at<=S.year+1);
    while(idx>=0){
      const p=S.pending.splice(idx,1)[0];const cev=EV.find(e=>e.id===p.ev);
      if(cev&&(!cev.cond||cev.cond(S))){
        if(cev.choice){presentChoice(cev);clampStats();renderGame();return;}
        applyEvent(cev);afterMonth();return;
      }
      idx=S.pending.findIndex(p=>p.at<=S.year+1);
    }
  }
  // 特訓骰子:每年 2 顆(非籌備期)+ 里程碑獎勵骰
  if(S.dice.length===0&&!prep){
    const normalDue=(S.year>=2&&S.year<=36&&S.year-S.lastAlloc>=3);
    const n=(normalDue?2:0)+(S.bonusDice||0);
    if(n>0){
      S.bonusDice=0;
      if(normalDue)S.lastAlloc=S.year;
      S.dice=[];for(let i=0;i<n;i++)S.dice.push(1+rnd(3));
      presentSkillAlloc();clampStats();renderGame();return;
    }
  }
  // 主事件
  const ev=pickEvent("main");
  if(ev){
    if(ev.choice){presentChoice(ev);clampStats();renderGame();return;}
    applyEvent(ev);
  }
  afterMonth();
}'''
assert old_main in s, 'old_main not found'
s = s.replace(old_main, new_main, 1)

# ---------- 5. afterMain -> afterMonth;小事件機率降(月頻率高) ----------
s = s.replace('function afterMain(){\n  if(!S.alive){clampStats();renderGame();checkDeath();return;}\n  // 小事件 0~2\n  let n=(R()<0.6?1:0)+(R()<0.28?1:0);\n  for(let i=0;i<n;i++){const m=pickEvent("minor");if(m)applyEvent(m);}\n  clampStats();renderGame();checkDeath();\n}',
'''function afterMonth(){
  if(!S.alive){clampStats();renderGame();checkDeath();return;}
  // 每月小事件 0~1(年結算月較多)
  let n=(R()<(S.month===12?0.65:0.5)?1:0);
  for(let i=0;i<n;i++){const m=pickEvent("minor");if(m)applyEvent(m);}
  clampStats();renderGame();checkDeath();
}''')
assert s.count('function afterMonth()') == 1

# ---------- 6. 事件綁定:stepYear -> stepMonth ----------
s = s.replace('$("btnNext").onclick=()=>{if(!S.paused&&S.alive)stepYear();};',
              '$("btnNext").onclick=()=>{if(!S.paused&&S.alive)stepMonth();};')

# ---------- 7. 主動行動文案:每年一次不變 ----------
s = s.replace('S.paused=true;$("btnNext").disabled=true;$("btnAct").disabled=true;',
              'S.paused=true;$("btnNext").disabled=true;$("btnAct").disabled=true;')

# ---------- 8. checkDeath 內 logLine 的 age 已是 year 語意(保持) ----------
# ---------- 9. renderSetup/其他 UI 中 age 顯示:renderGame jobLabel 已是年營收,不變 ----------

open(p, 'w', encoding='utf-8').write(s)
print('monthify part1 OK')
