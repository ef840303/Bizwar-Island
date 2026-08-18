path = '/home/ubuntu/bizwar/index.html'
src = open(path, encoding='utf-8').read()

# 1. 月利息 0.6% -> 0.3%(避免與年末 8% 雙重計息)
assert 'S.money-=Math.round(Math.abs(S.money)*0.006)' in src, 'monthly interest not found'
src = src.replace('S.money-=Math.round(Math.abs(S.money)*0.006)', 'S.money-=Math.round(Math.abs(S.money)*0.003)', 1)

# 2. 年末利息 8% -> 5%
assert 'S.money-=Math.round(Math.abs(S.money)*0.08)' in src, 'yearly interest not found'
src = src.replace('S.money-=Math.round(Math.abs(S.money)*0.08)', 'S.money-=Math.round(Math.abs(S.money)*0.05)', 1)

# 3. 破產閾值放寬:money<=-5000萬且 mcap<500萬 -> 現金<=-1億 且 淨值(含市值)低於 1000 萬才破產
old = "if(!die&&S.money<=-50000000&&S.mcap<5000000){die=true;reason=\"現金流徹底斷裂，銀行斷頭、資方袖手旁觀——\"+S.name+\"宣布破產倒閉。\";}"
new = "if(!die&&S.money<=-100000000&&netWorth(S)<10000000){die=true;reason=\"現金流徹底斷裂，銀行斷頭、資方袖手旁觀——\"+S.name+\"宣布破產倒閉。\";}"
assert old in src, 'bankrupt threshold not found'
src = src.replace(old, new, 1)

open(path, 'w', encoding='utf-8').write(src)
print('bankrupt mechanics fixed')
