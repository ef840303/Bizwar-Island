#!/usr/bin/env python3
"""修正 ipoCraze 的 let moon 作用域 bug:res arrow 抓不到 eff 內的區域變數 moon。
改法:用 S._tmp 暫存 chance 結果,讓 res 引用 S._tmp(與 945 行 templeVisit 相同手法)。"""
path = 'index.html'
src = open(path, encoding='utf-8').read()

old = ("eff:S=>{let moon=chance(S,0.5+S.stats.finance*0.005);if(moon){S.mcap=Math.round((S.mcap||S.revenue*10)*1.6);"
       "S.money+=12e6;return inc(S,{finance:3,happy:6});}S.flags.scandal=true;return inc(S,{finance:1,happy:-6});},"
       "res:S=>moon?\"市場瘋狂,你募資抽到好籤!\":\"熱錢反噬,被媒體點名『炒作』。\"")
new = ("eff:S=>{let moon=chance(S,0.5+S.stats.finance*0.005);S._tmp=moon;if(moon){S.mcap=Math.round((S.mcap||S.revenue*10)*1.6);"
       "S.money+=12e6;return inc(S,{finance:3,happy:6});}S.flags.scandal=true;return inc(S,{finance:1,happy:-6});},"
       "res:S=>(S._tmp!==undefined?S._tmp:moon)?\"市場瘋狂,你募資抽到好籤!\":\"熱錢反噬,被媒體點名『炒作』。\"")

cnt = src.count(old)
assert cnt == 1, f"pattern count={cnt}"
src = src.replace(old, new, 1)
open(path, 'w', encoding='utf-8').write(src)
print('moon fix done')
