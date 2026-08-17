p = 'index.html'
s = open(p, encoding='utf-8').read()

old = """  const gm=S.sectorGm, st=S.stageIdx;
  let rev=S.revenue||0;
  // 成長引擎：能力×階段×領域成長率
  // 人均營收上限:團隊規模決定營收天花板(避免 3 人做百億)
  let perCap=2e6*(1+st*0.9)+(S.stats.sales*4e4)+(S.stats.tech*3e4);
  if(S.staffCount>0&&S.revenue>S.staffCount*perCap)grow=Math.min(grow,(S.staffCount*perCap/Math.max(1,S.revenue))-1);
  let grow=0.05*S.sectorGrowth+(S.stats.sales*0.008+S.stats.tech*0.007+S.stats.vision*0.005)*(1+st*0.12);
  // 領域景氣波動
  grow+=(R()-0.5)*0.16; if(R()<0.035)grow-=0.3+R()*0.25;
  if(S.flags.scandal)grow-=0.15;
  if(S.flags.lobby&&S.age%2===0)grow+=0.05;
  grow=clamp(grow,-0.5,0.5);
  S.revenue=Math.max(0,Math.round(rev*(1+grow)));
  S.profitLast=Math.round(S.revenue*gm)-(S.staffCount*Math.round(1e6))*(1+Math.max(0,(st-2)*0.05));
  // 人才成本:階段越高,每人成本越高
  let payroll=S.staffCount*Math.round(1e6)*(1+Math.max(0,(st-2)*0.05));
  // 固定費用(租金、設備、雜支)
  let fixed=Math.round(S.revenue*0.12+1e5*(1+st*0.5));"""

new = """  const gm=S.sectorGm, st=S.stageIdx;
  let rev=S.revenue||0;
  // 成長引擎：能力×階段×領域成長率
  let grow=0.05*S.sectorGrowth+(S.stats.sales*0.008+S.stats.tech*0.007+S.stats.vision*0.005)*(1+st*0.12);
  // 領域景氣波動
  grow+=(R()-0.5)*0.16; if(R()<0.035)grow-=0.3+R()*0.25;
  if(S.flags.scandal)grow-=0.15;
  if(S.flags.lobby&&S.age%2===0)grow+=0.05;
  // 人均營收上限:團隊規模決定營收天花板(避免 3 人做百億),超標時漸進收斂
  const perCap=2e6*(1+st*0.9)+(S.stats.sales*4e4)+(S.stats.tech*3e4);
  const cap=S.staffCount>0?S.staffCount*perCap:perCap*3;
  if(rev>cap*1.2)grow=Math.min(grow,-0.12);      // 嚴重超標先止血
  else if(rev>cap)grow=Math.min(grow,(cap/rev-1)*0.5); // 輕微超標漸進收斂
  grow=clamp(grow,-0.5,0.5);
  S.revenue=Math.max(0,Math.round(rev*(1+grow)));
  // 人才成本:早期每人成本較低,避免虧損滾雪球
  let costPer=(st>=5?2.2e6:(st>=3?1.6e6:1e6));
  let payroll=Math.round(S.staffCount*costPer);
  S.profitLast=Math.round(S.revenue*gm)-payroll;
  // 固定費用(租金、設備、雜支)
  let fixed=Math.round(S.revenue*0.10+1e5*(1+st*0.4));"""

assert s.count(old) == 1, ('old count = %d' % s.count(old))
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)
print('runOps rewritten OK')
