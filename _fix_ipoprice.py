#!/usr/bin/env python3
"""IPO 成功時記錄 S.ipoPrice,供財團巨頭志向(mogul)計算股價倍數。"""
path = 'index.html'
src = open(path).read()

old = 'S.stockPrice=Math.round(S.mcap/shares);'
new = 'S.stockPrice=Math.round(S.mcap/shares);S.ipoPrice=S.ipoPrice||S.stockPrice;'
assert old in src, 'anchor not found'
# 只在 IPO 行動那行補(該行前後為 IPO 行動),先確認出現次數
cnt = src.count(old)
print('occurrences of anchor:', cnt)
# 全部替換安全(peak.stock 那段也補了同樣片段,但 ipoPrice|| 冪等)
src = src.replace(old, new)
open(path, 'w').write(src)
print('OK: ipoPrice recorded')
