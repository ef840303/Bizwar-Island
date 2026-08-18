#!/usr/bin/env python3
"""v1.3.0 新增霸業志向:
- 財團巨頭(股價翻 10 倍,靠股市封頂)
- 員工王國(萬人集團、幸福企業)
- 研發大國(技術滿級、研發轉化)
- 財報聖手(年年獲利、現金流健康)
- 政商紅人(政商點數滿級、立委關係)
- 江湖傳奇(手腕滿級、江湖事跡)
grid 2x3 -> 3x4 需支援,改用 c3(3 欄)並讓 12 個志向排成 4 列
"""
import re

path = 'index.html'
src = open(path).read()

# 1) 擴充 GOALS 陣列:在 tycoon 志向後插入 6 個新志向
anchor = '  {id:"tycoon",icon:"👑",nm:"梟雄霸業",desc:"併購、壟斷、股權攻防——手段黑白不重要,規模才重要",prog:S=>clamp01((S.flags.mergerKing?0.35:0)+(S.mktShare>=0.5?0.35:0)+(S.flags.hostile?0.3:0)+(S.flags.darkline?0.2:0))},'
new_goals = anchor + """
  {id:"mogul",icon:"🏦",nm:"財團巨頭",desc:"股價就是你的名片——從 IPO 起封頂 10 倍,站在資本市場之巔",prog:S=>{const h=S.stockHist||[];const ip=S.ipoPrice||0;return clamp01((h.length?Math.max(...h)/Math.max(1,ip):0)/10);}},
  {id:"happycorp",icon:"🌈",nm:"員工王國",desc:"千人以上的幸福企業——規模與士氣雙豐收,人人搶著進的公司",prog:S=>clamp01(((S.peak.staff||0)/1000*0.5)+((S.peak.happy||0)/100*0.3)+(S.flags.corner?0.2:0))},
  {id:"techking",icon:"⚗️",nm:"研發大國",desc:"技術封神、專利護城河——把新創做到靠產品統治市場",prog:S=>clamp01((Math.max(S.peak.tech||0)/100*0.55)+((S.flags.koiHit||0)+0)+(S.peak.tech>=90?0.25:0)+((S.flags.listed||S.stageIdx>=6)?0.2:0))},
  {id:"cashking",icon:"💴",nm:"財報聖手",desc:"穩如定存——連年獲利、現金流從不燒錢,用紀律贏得市場",prog:S=>clamp01(((S.profitHist||[]).length/12*0.6)+(((S.peak.mcap||0)>=1e8)?0.2:0)+(S.flags.survived?0.2:0))},
  {id:"powerbroker",icon:"🏯",nm:"政商紅人",desc:"白手套與紅頂商人——政商點數拉滿,關說招標樣樣通",prog:S=>clamp01((Math.max(S.peak.politics||0)/100*0.5)+(S.flags.lobby?0.3:0)+(S.flags.govSubsidy?0.2:0))},
  {id:"streetking",icon:"🌘",nm:"江湖傳奇",desc:"白道黑道都是朋友——手腕封神,江湖傳頌你的名號",prog:S=>clamp01((Math.max(S.peak.street||0)/100*0.5)+(S.flags.darkline?0.25:0)+(S.flags.reformed?0.25:0))},"""
assert anchor in src, 'anchor not found'
src = src.replace(anchor, new_goals, 1)

# 2) goalGrid 由 c2 改 c3(12 個志向 3 欄 x 4 列)
assert '<div class="grid c2" id="goalGrid"></div>' in src
src = src.replace('<div class="grid c2" id="goalGrid"></div>', '<div class="grid c3" id="goalGrid"></div>', 1)

# 3) peak 記錄股價峰值:在 peak 更新段補 stock
old_peak = "S.peak.revenue=Math.max(S.peak.revenue||0,S.revenue);"
new_peak = "S.peak.revenue=Math.max(S.peak.revenue||0,S.revenue);S.peak.stock=Math.max(S.peak.stock||0,S.stockPrice||0);"
if old_peak in src and 'S.peak.stock' not in src:
    src = src.replace(old_peak, new_peak)

open(path, 'w').write(src)
print('OK: added 6 goals, grid c3, peak.stock')
