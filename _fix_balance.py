# 修復腳本(2026-08-18):
# 1. 人名語意統一:S.name=公司名(S.founder=創辦人姓名),隨機命名補公司名庫
# 2. 營收不爆炸:人均營收上限 + 成長率上限下修
# 3. 員工成長加快
# 4. payroll 微調 + mcap 平滑

import io, re, sys

path = "index.html"
src = open(path, encoding="utf-8").read()

# ---------- 1. 人名語意修正 ----------
# 1a. HTML 標籤:輸入框語意保持(nameInput=創辦人,founderInput=公司)不動,
#     但 btnBorn 內把 setup.name 與 setup.founder 交換存成「語意正確」版本
old_click = """$("btnBorn").onclick=()=>{
  applySeed(readSeed());
  let nm=($("nameInput").value||"").trim().slice(0,8);
  if(!nm)nm=randomName("男");
  let fd=($("founderInput").value||"").trim().slice(0,8);
  if(!fd)fd=randomName("男");
  setup.name=nm;setup.founder=fd;setup.sex=null;setup.region=null;"""
new_click = """$("btnBorn").onclick=()=>{
  applySeed(readSeed());
  let founderNm=($("nameInput").value||"").trim().slice(0,8);
  if(!founderNm)founderNm=randomName("男");
  let compNm=($("founderInput").value||"").trim().slice(0,8);
  if(!compNm)compNm=randomCompanyName(founderNm);
  setup.name=compNm;setup.founder=founderNm;setup.sex=null;setup.region=null;"""
assert old_click in src, "btnBorn block not found"
src = src.replace(old_click, new_click)

# 1b. 新增隨機公司名函式
old_rng = "function randomName(sex){return SURNAMES[Math.floor(Math.random()*SURNAMES.length)]+(sex===\"女\"?GIVEN_F:GIVEN_M)[Math.floor(Math.random()*12)];}"
new_rng = old_rng + """
const CO_PREFIX=["天龍","星耀","雲頂","華碩","鑫茂","遠騰","錦豐","瀚海","鼎瑞","宏旭","嘉禾","兆邦","旭日","飛揚","瑞德","康寧","博遠","聯創"];
const CO_SUFFIX=["科技","創客","實業","股份","國際","資訊","生技","電商","餐飲","控股"];
function randomCompanyName(seed){return (CO_PREFIX[Math.floor(Math.random()*CO_PREFIX.length)]+(Math.random()<0.5?seed.slice(0,1):""))+CO_SUFFIX[Math.floor(Math.random()*CO_SUFFIX.length)];}"""
assert old_rng in src, "randomName not found"
src = src.replace(old_rng, new_rng)

# 1c. 渲染位置:birthLine / logLine 開場 / idLabel / gradeSub / PNG sub / endCard / checkDeath 理由
fixes = [
 # birthLine:公司（創辦人：OOO）
 ('```${S.name}（創辦人：${S.founder}）· ${S.origin.nm} · ${S.sector.tag||""} · ${S.hq.nm} · ${S.cap.nm}```',
  '```${S.name} · ${S.sector.tag||""} · ${S.hq.nm} ``` 與 ````（創辦人：${S.founder}）· ${S.origin.nm} · ${S.cap.nm}```` 分開'),
]
# 用行級替換較穩,逐筆處理:
pairs = [
 # birthLine(籌備期回顧第一行)
 ('`${S.name}（創辦人：${S.founder}）· ${S.origin.nm} · ${S.sector.tag||""} · ${S.hq.nm} · ${S.cap.nm}`',
  '`${S.name}（創辦人：${S.founder}）· ${S.sector.tag||""} · ${S.hq.nm} · ${S.origin.nm} · ${S.cap.nm}`'),
 # 開場【】logLine(1100)
 ('`【${S.name} · 創辦人 ${S.founder} · ${S.origin.nm} · ${S.sector.tag||""} · ${S.hq.nm} · ${S.cap.nm}】`',
  '`${S.name} · ${S.sector.tag||""} · ${S.hq.nm}`'),
]
for a, b in pairs:
    assert a in src, f"NOT FOUND: {a[:40]}"
    src = src.replace(a, b)

# 開場 logLine 需改為三行:公司 + 創辦人 + 志向(原先志向行保留)
# 現在開場變成只顯示公司行,需補創辦人與天賦兩行 → 在志向行前後加
old_log_line = """logLine(-1,`${S.name} · ${S.sector.tag||""} · ${S.hq.nm}`,[]);
  logLine(-1,`創辦人天賦：${S.talent.nm}`,[],"big");
  logLine(-1,`企業志向：${gg.icon} ${gg.nm}`,[],"mile");"""
assert old_log_line in src
src = src.replace(old_log_line, """logLine(-1,`${S.name} · ${S.sector.tag||""} · ${S.hq.nm}`,[]);
  logLine(-1,`創辦人：${S.founder} · ${S.origin.nm} · ${S.cap.nm}`,[],"big");
  logLine(-1,`天賦：${S.talent.nm}`,[],"minor");
  logLine(-1,`企業志向：${gg.icon} ${gg.nm}`,[],"mile");""")

# endGame gradeSub / PNG sub:改為「公司 · 創辦人 · 領域 · 總部」
for old in [
 "`${S.name} · 創辦人 ${S.founder} · ${S.origin.nm} · ${S.hq.nm} · ${S.stage||\"已退場\"} · 經營 ${S.age} 年 · 🌱${S.seed}`",
 "`${S.name} · 創辦人 ${S.founder} · ${S.origin.nm} · ${S.hq.nm} · 經營 ${S.age} 年 · 🌱${S.seed}`",
]:
    if old in src:
        src = src.replace(old, "`${S.name} · 創辦人 ${S.founder} · ${S.sector.tag||\"\"} · ${S.hq.nm} · 經營 ${S.age} 年 · 🌱${S.seed}`")

# endCard 文案
old_card = '`${S.name} 的故事走到了終點，經營 ${S.age} 年。`'
if old_card in src:
    src = src.replace(old_card, '`${S.name} 的企業走到了終點，經營 ${S.age} 年。`')

# ---------- 2. 營收平衡 ----------
# grow 上限 0.8→0.5,並加入人均營收上限制約
old_grow = """  let grow=0.05*S.sectorGrowth+(S.stats.sales*0.008+S.stats.tech*0.007+S.stats.vision*0.005)*(1+st*0.12);"""
new_grow = """  // 人均營收上限:團隊規模決定營收天花板(避免 3 人做百億)
  let perCap=2e6*(1+st*0.9)+(S.stats.sales*4e4)+(S.stats.tech*3e4);
  if(S.staffCount>0&&S.revenue>S.staffCount*perCap)grow=Math.min(grow,(S.staffCount*perCap/Math.max(1,S.revenue))-1);
  let grow=0.05*S.sectorGrowth+(S.stats.sales*0.008+S.stats.tech*0.007+S.stats.vision*0.005)*(1+st*0.12);"""
assert old_grow in src
src = src.replace(old_grow, new_grow)

old_clamp = "  grow=clamp(grow,-0.5,0.8);"
new_clamp = "  grow=clamp(grow,-0.5,0.5);"
assert old_clamp in src
src = src.replace(old_clamp, new_clamp)

# ---------- 3. 員工成長加快 ----------
old_staff = "  if(S.staffCount>0){S.staffCount=Math.max(1,Math.round(S.staffCount*(1+(S.stats.mgmt*0.0015-0.005)+(R()-0.5)*0.06)));}"
new_staff = "  if(S.staffCount>0){S.staffCount=Math.max(1,Math.round(S.staffCount*(1+0.02+st*0.02+(S.stats.mgmt*0.002-0.008)+(R()-0.5)*0.04)));}"
assert old_staff in src
src = src.replace(old_staff, new_staff)

# ---------- 4. payroll 微調(每人年薪 80萬→100萬) ----------
src = src.replace("Math.round(8e5)", "Math.round(1e6)")

# ---------- 5. mcap 平滑:未上市估值年化漲幅 cap ±60% ----------
old_mcap = "  if(S.stageIdx<6){S.mcap=Math.round(rev*mult[st]*(1+(R()-0.5)*0.3));}"
new_mcap = "  if(S.stageIdx<6){let m=Math.round(rev*mult[st]*(1+(R()-0.5)*0.3));if(S.mcap>1e6)m=Math.round(S.mcap*clamp(1+(m-S.mcap)/Math.max(1,S.mcap),0.4,1.6));S.mcap=Math.max(1e4,m);}"
assert old_mcap in src
src = src.replace(old_mcap, new_mcap)

# ---------- 6. generateChildhood 初始營收基數下修 ----------
old_init_rev = "  S.revenue=Math.round(S.money*(0.5+R()*1.5));"
new_init_rev = "  S.revenue=Math.round(Math.max(3e5,S.money*(0.2+R()*0.4)));"
assert old_init_rev in src
src = src.replace(old_init_rev, new_init_rev)

open(path, "w", encoding="utf-8").write(src)
print("ALL_PATCHES_APPLIED")
