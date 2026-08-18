path = '/home/ubuntu/bizwar/index.html'
src = open(path, encoding='utf-8').read()

old_block = '''  // 缺口型自然擴編:營收超出團隊容量時才補人,受階段上限約束
  const staffCap=[3,20,60,200,600,1500,4000,12000,40000][Math.min(S.stageIdx,8)]||40000;
  if(S.staffCount<staffCap){
    const need=S.revenue/perCap-S.staffCount*1.15;
    if(need>0&&S.profitLast>0){
      let hires=Math.max(0,Math.round(need*0.4));
      hires=Math.min(hires,staffCap-S.staffCount);
      if(hires>0)S.staffCount+=hires;
    }
  }'''

new_block = '''  // 缺口型自然擴編:營收超出團隊容量時才補人,受階段上限約束,逐月追趕
  const staffCap=[3,20,60,200,600,1500,4000,12000,25000][Math.min(S.stageIdx,8)]||25000;
  if(S.staffCount<staffCap){
    const need=S.revenue/perCap-S.staffCount*1.15;
    if(need>0&&S.profitLast>0){
      let hires=Math.max(0,Math.round(need*0.08));
      hires=Math.min(hires,Math.round(S.staffCount*0.15)+3,staffCap-S.staffCount);
      if(hires>0)S.staffCount+=hires;
    }
  } else if(S.staffCount>staffCap*1.5&&!S.flags.merger){
    // 明顯臃腫:每月自然精簡 5%
    let cut=Math.max(1,Math.round(S.staffCount*0.05));
    S.staffCount=Math.max(Math.round(staffCap*1.3),S.staffCount-cut);
  }'''

assert old_block in src, 'old block not found'
src = src.replace(old_block, new_block, 1)
open(path, 'w', encoding='utf-8').write(src)
print('staff growth v3 applied')
