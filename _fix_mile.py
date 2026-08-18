"""milestones 顯示修正:age 為月總數,結算畫面改為「N 年 M 月」格式。"""
path = 'index.html'
src = open(path).read()
changes = 0

# 結算畫面渲染 milestones 的模板(只有一處)
old = '<div class="ta">${m.age} 年</div>'
new = '<div class="ta">${Math.floor(m.age/12)} 年 ${m.age%12} 月</div>'
if old in src:
    src = src.replace(old, new); changes += 1
else:
    print('MISS milestone template:', old)

open(path, 'w').write(src)
print(f'applied {changes}/1 changes')
