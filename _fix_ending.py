"""結局補漏:checkDeath 退休/老死路徑設 S.ending;endMap 補 raider。"""
path = 'index.html'
src = open(path).read()
changes = 0

# 1) 60 歲退休路徑設 ending
old1 = 'if(!die&&S.year>=60){die=true;reason=S.stageIdx>=8?("功成身退，"+S.name+"走完輝煌一生，交棒給下一代。"):(S.year>=5?"創辦人安詳退休，"+S.name+"的故事告一段落。":"創辦人行使交棒條款，"+S.name+"就此走入歷史。");}'
new1 = 'if(!die&&S.year>=60){die=true;S.ending={t:"功成身退",key:"retire",icon:"🌅"};reason=S.stageIdx>=8?("功成身退，"+S.name+"走完輝煌一生，交棒給下一代。"):(S.year>=5?"創辦人安詳退休，"+S.name+"的故事告一段落。":"創辦人行使交棒條款，"+S.name+"就此走入歷史。");}'
if old1 in src:
    src = src.replace(old1, new1); changes += 1
else:
    print('MISS 1:', old1[:60])

# 2) 80 歲老死路徑設 ending
old2 = 'if(!die&&S.year>=80){die=true;reason="歲月不饒人，"+S.name+"的創辦人享嵩壽而逝，企業傳奇落幕。";}'
new2 = 'if(!die&&S.year>=80){die=true;S.ending={t:"嵩壽落幕",key:"retire",icon:"🌅"};reason="歲月不饒人，"+S.name+"的創辦人享嵩壽而逝，企業傳奇落幕。";}'
if old2 in src:
    src = src.replace(old2, new2); changes += 1
else:
    print('MISS 2:', old2[:60])

# 3) endMap 補 raider
old3 = 'const endMap={"jail":{icon:"⛓️",t:"涉黑入獄、鐵窗收場"},"bankrupt":{icon:"📉",t:"破產退場、黯然離席"},"exit":{icon:"🤝",t:"併購套現、功成身退"},"legacy":{icon:"🏛️",t:"基業傳承、世代延續"},"retire":{icon:"🌅",t:"功成身退、自由人生"}};'
new3 = 'const endMap={"jail":{icon:"⛓️",t:"涉黑入獄、鐵窗收場"},"bankrupt":{icon:"📉",t:"破產退場、黯然離席"},"exit":{icon:"🤝",t:"併購套現、功成身退"},"legacy":{icon:"🏛️",t:"基業傳承、世代延續"},"retire":{icon:"🌅",t:"功成身退、自由人生"},"raider":{icon:"🦅",t:"控制權易主、黯然離席"}};'
if old3 in src:
    src = src.replace(old3, new3); changes += 1
else:
    print('MISS 3:', old3[:60])

open(path, 'w').write(src)
print(f'applied {changes}/3 changes')
