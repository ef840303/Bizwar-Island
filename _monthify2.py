# 月制語意修正:所有「以年為單位」的判定改用 S.year;S.age 保留為月總數(曲線/里程)
p = 'index.html'
s = open(p, encoding='utf-8').read()

# --- pickEvent 內 min/max 與冷卻:改用年語意 ---
s = s.replace('if(S.age<e.min||S.age>e.max)return false;', 'if(S.year<e.min||S.year>e.max)return false;')
s = s.replace('if(last!==undefined&&S.age-last<6)ww*=0.04;', 'if(last!==undefined&&S.year-last<6)ww*=0.04;')
s = s.replace('} else if(last!==undefined&&S.age-last<4)ww*=0.1;', '} else if(last!==undefined&&S.year-last<4)ww*=0.1;')
s = s.replace('S.evLast[chosen.id]=S.age;S.evCount[chosen.id]=(S.evCount[chosen.id]||0)+1;',
              'S.evLast[chosen.id]=S.year;S.evCount[chosen.id]=(S.evCount[chosen.id]||0)+1;')

# --- EV 事件:cond 中 S.age 時間語意改 S.year(逐筆精修) ---
reps = [
    ('cond:S=>S.age>=4,', 'cond:S=>S.year>=4,'),
    ('cond:S=>S.stageIdx>=6&&S.age>=20,', 'cond:S=>S.stageIdx>=6&&S.year>=20,'),
    ('cond:S=>S.age>=15&&S.stageIdx>=4,', 'cond:S=>S.year>=15&&S.stageIdx>=4,'),
    ('min:6,max:24', 'min:6,max:24'),  # 已是年,不動
]
for a, b in reps:
    if a != b:
        assert a in s, 'MISSING: ' + a
        s = s.replace(a, b)

# --- EV 事件中其他 S.age 時間判定(在事件內部的) → 用 grep 確認後精修 ---
more = {
    # schedule/at 到期判定以年計(stepMonth 已改),不需動
    # runOps 內年齡保護
    'if(S.age===0)return;': None,  # 處理見下(批量)
}
# runOps/runFinance/ongoingCorp 的 S.age===0 保護與年齡判定改月語意
s = s.replace('if(S.age===0)return;\n  // 籌備期自動招募', 'if(S.age<12)return;\n  // 籌備期自動招募')
# 找出所有 S.age===0 return(保護籌備期)→ 籌備期現在是前 12 個月
import re
n = s.count('if(S.age===0)return;')
s = s.replace('if(S.age===0)return;', 'if(S.age<12)return;')
print('S.age===0 return 替換次數:', n)

# --- runOps 內年度週期判定改月週期 ---
s = s.replace('if(S.flags.lobby&&S.age%2===0)grow+=0.05;', 'if(S.flags.lobby&&S.age%24===0)grow+=0.05;')
s = s.replace('if(S.stats.faith>20&&S.age%3===0&&S.money<0)S.money+=Math.round(S.revenue*0.02);',
              'if(S.stats.faith>20&&S.age%36===0&&S.money<0)S.money+=Math.round(S.revenue*0.02);')

# --- ongoingCorp 競爭對手生成:每年判定(原 S.age>=2) ---
s = s.replace('if(S.age>=2&&S.rivals.length<(S.stageIdx>=6?3:1)&&R()<0.12+S.stageIdx*0.03){',
              'if(S.year>=2&&S.rivals.length<(S.stageIdx>=6?3:1)&&R()<0.12+S.stageIdx*0.03){')

# --- tryPromoteStage 年齡門檻(年) ---
s = s.replace("if(S.age<({種子輪:1,天使輪:2,\"A 輪\":3,\"B 輪\":4,\"C 輪\":5,上市:6,控股:8}[nx]||99))return;",
              "if(S.year<({種子輪:1,天使輪:2,\"A 輪\":3,\"B 輪\":4,\"C 輪\":5,上市:6,控股:8}[nx]||99))return;")

# --- DICE_MILE 年齡里程碑改年 ---
s = s.replace('{id:"a10",cond:S=>S.age>=10,n:1,t:"十年老店,閱歷淬煉"}', '{id:"a10",cond:S=>S.year>=10,n:1,t:"十年老店,閱歷淬煉"}')
s = s.replace('{id:"a20",cond:S=>S.age>=20,n:1,t:"廿年深耕,穩如磐石"}', '{id:"a20",cond:S=>S.year>=20,n:1,t:"廿年深耕,穩如磐石"}')
s = s.replace('{id:"a30",cond:S=>S.age>=30,n:1,t:"三十年基業,傳承在望"}', '{id:"a30",cond:S=>S.year>=30,n:1,t:"三十年基業,傳承在望"}')

# --- ACTIONS 內 S.age 時間判定(逐筆) ---
s = s.replace('cond:S=>S.age>=1,act:S=>{return{log:"全面緊縮', 'cond:S=>S.year>=1,act:S=>{return{log:"全面緊縮')

# --- checkDeath 高齡/退休判定:歲改年 ---
s = s.replace('if(!die&&S.age>=100){', 'if(!die&&S.year>=8){')
s = s.replace('if(S.age>=60&&!die){die=true;reason=S.stageIdx>=8?("功成身退，"+S.name+"走完輝煌一生，交棒給下一代。"):(S.age>=55?"創辦人安詳退休，"+S.name+"的故事告一段落。":"創辦人行使交棒條款，"+S.name+"就此走入歷史。");}',
              'if(!die&&S.year>=6){die=true;reason=S.stageIdx>=8?("功成身退，"+S.name+"走完輝煌一生，交棒給下一代。"):(S.year>=5?"創辦人安詳退休，"+S.name+"的故事告一段落。":"創辦人行使交棒條款，"+S.name+"就此走入歷史。");}')
assert 'S.age>=60&&!die' not in s

# --- 結算/分享文案:經營年數改 S.year ---
s = s.replace('if(S.age>=40)a.push("🕯️ 長壽企業");else if(S.age<15)a.push("💀 英年早逝");',
              'if(S.year>=40)a.push("🕯️ 長壽企業");else if(S.year<15)a.push("💀 英年早逝");')
s = s.replace('let raw=S.age*1.5+avgHappy', 'let raw=S.year*1.5+avgHappy')
s = s.replace('`經營 ${S.age} 年 · 🌱${S.seed}`;', '`經營 ${S.year} 年 · 🌱${S.seed}`;')
s = s.replace('<div class="s"><span>經營年數</span><b>${S.age} 年</b></div>', '<div class="s"><span>經營年數</span><b>${S.year} 年</b></div>')
s = s.replace('sub:`${S.name} · 創辦人 ${S.founder} · ${S.sector.tag||""} · ${S.hq.nm} · 經營 ${S.age} 年 · 🌱${S.seed}`,',
              'sub:`${S.name} · 創辦人 ${S.founder} · ${S.sector.tag||""} · ${S.hq.nm} · 經營 ${S.year} 年 · 🌱${S.seed}`,')
s = s.replace('age:S.age, peakMoney:p.mcap||0, finalMoney:nwFinal,', 'age:S.year, peakMoney:p.mcap||0, finalMoney:nwFinal,')
s = s.replace('<div class="q">${S.name} 的故事走到了終點，經營 ${S.age} 年。</div>', '<div class="q">${S.name} 的故事走到了終點，經營 ${S.year} 年。</div>')

# --- presentChoice/特訓文案「歲」改「年月」 ---
s = s.replace('<div class="q">${S.age}歲 · ${q}</div>', '<div class="q">第 ${S.year} 年 ${S.month} 月 · ${q}</div>')
s = s.replace('<div class="q">${S.age} 歲・把骰子投入專長', '<div class="q">第 ${S.year} 年 ${S.month} 月・把骰子投入專長')
s = s.replace('<div class="q">${S.age}歲・你想主動做什麼？</div>', '<div class="q">第 ${S.year} 年 ${S.month} 月・你想主動做什麼？</div>')

# --- doubleGrow late age 判定 ---
s = s.replace('if(ev.grow&&S.flags.late&&S.age>=40)deltas=doubleGrow(S,deltas);',
              'if(ev.grow&&S.flags.late&&S.year>=40)deltas=doubleGrow(S,deltas);')

# --- generateChildhood S.age=0 保留(初始化) ---
# --- applyEvent logLine age 參數:傳 S.age 時改為傳年(月)格式;看 applyEvent ---
s = s.replace("if(txt!==undefined&&ev.id!==\"born\")logLine(S.age,txt,deltas,ev.kind===\"minor\"?\"minor\":\"\");",
              "if(txt!==undefined&&ev.id!==\"born\")logLine(S.age,txt,deltas,ev.kind===\"minor\"?\"minor\":\"\");")  # logLine 已處理年/月

# --- 死亡原因收尾 logLine(S.age...) 在 checkDeath:logLine 用 age=月總數,已被 logLine 轉換為年第N年,OK ---

open(p, 'w', encoding='utf-8').write(s)
print('monthify part2 OK')
