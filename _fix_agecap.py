import re

p = 'index.html'
s = open(p, encoding='utf-8').read()

old = ("if(S.age>=60&&!die){die=true;reason=S.stageIdx>=8?(\"功成身退，\"+S.name+\"走完輝煌一生，交棒給下一代。\"):"
       "(S.age>=55?\"創辦人安詳退休，\"+S.name+\"的故事告一段落。\":\"創辦人行使交棒條款，\"+S.name+\"就此走入歷史。\");}")

assert s.count(old) == 1, s.count(old)

new = ("if(!die&&S.age>=100){die=true;reason=\"歲月不饒人，\"+S.name+\"的創辦人在高齡安詳離世，企業走入歷史。\";}\n"
       + old)

s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)
print('OK, age>=100 cap inserted')
