path = '/home/ubuntu/bizwar/index.html'
src = open(path, encoding='utf-8').read()

anchor = "function fmtMoney(n){const neg=n<0;let v=Math.abs(n);let s;if(v>=1e8)s=(v/1e8).toFixed(v>=1e9?0:2).replace(/\\.?0+$/,'')+\"億\";else if(v>=1e4)s=Math.round(v/1e4).toLocaleString()+\"萬\";else s=Math.round(v).toLocaleString();return (neg?\"負\":\"\")+\"NT$\"+s;}"
add = "\nfunction fmtDelta(n){return fmtMoney(n);}"
assert anchor in src, 'anchor not found'
assert 'function fmtDelta' not in src, 'already exists'
src = src.replace(anchor, anchor + add, 1)
open(path, 'w', encoding='utf-8').write(src)
print('fmtDelta added')
