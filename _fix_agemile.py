#!/usr/bin/env python3
"""修正週年里程碑月制 bug:
1. checkAgeMile 用 S.age(月總數)與年數閾值比較 → 改為 S.year(年數)
2. longRun 成就 c:S=>S.age>=30 也是年制殘留 → 改 S.year>=30
"""
path = 'index.html'
src = open(path).read()

# 1. checkAgeMile 判定改年數
old1 = 'for(const [a,icon,t] of AGE_MILE){ if(!S.ageMile[a]&&S.age>=a){S.ageMile[a]=1;mile(S,icon,t);} }'
new1 = 'for(const [a,icon,t] of AGE_MILE){ if(!S.ageMile[a]&&S.year>=a){S.ageMile[a]=1;mile(S,icon,t);} }'
assert old1 in src, 'checkAgeMile pattern not found'
src = src.replace(old1, new1)

# 2. longRun 成就閾值改年數
old2 = '{id:"longRun",icon:"⏳",nm:"三十年老店",c:S=>S.age>=30}'
new2 = '{id:"longRun",icon:"⏳",nm:"三十年老店",c:S=>S.year>=30}'
assert old2 in src, 'longRun pattern not found'
src = src.replace(old2, new2)

open(path, 'w').write(src)
print('age milestone fixed')
