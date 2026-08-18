path = '/home/ubuntu/bizwar/index.html'
src = open(path, encoding='utf-8').read()

# --- 1. 從 ongoingCorp 移除錯誤位置的擴編塊 ---
bad_block = '''  // 獲利年的自然擴編:規模越大本月可新增越多(受階段上限約束)
  const staffCap=[3,20,60,200,600,1500,4000,12000,40000][Math.min(S.stageIdx,8)]||40000;
  if(S.profitLast>0&&S.staffCount<staffCap){
    let hires=Math.max(0,Math.round((S.revenue/perCap-0.75)*0.35)+Math.round(S.profitLast/(perCap*2)));
    hires=Math.min(hires,staffCap-S.staffCount);
    if(hires>0)S.staffCount+=hires;
  }
'''
assert bad_block in src, 'bad block not found'
src = src.replace(bad_block, '', 1)

# --- 2. 插入到 runOps 內 perCap 定義之後(市占段之前) ---
anchor = '  // 市占(行銷+談判驅動,有天花板)'
assert anchor in src, 'anchor not found'
grow_block = '''  // 獲利年的自然擴編:規模越大本月可新增越多(受階段上限約束)
  const staffCap=[3,20,60,200,600,1500,4000,12000,40000][Math.min(S.stageIdx,8)]||40000;
  if(S.profitLast>0&&S.staffCount<staffCap){
    let hires=Math.max(0,Math.round((S.revenue/perCap-0.75)*0.35)+Math.round(S.profitLast/(perCap*2)));
    hires=Math.min(hires,staffCap-S.staffCount);
    if(hires>0)S.staffCount+=hires;
  }
'''
assert bad_block not in src, 'block already present'
src = src.replace(anchor, grow_block + anchor, 1)
open(path, 'w', encoding='utf-8').write(src)
print('staff grow moved into runOps after perCap')
