import json

with open('docs/design/paperdoll_slots.json') as f1, open('game/data/tables/paperdoll_slots.json') as f2:
    d1 = json.load(f1)
    d2 = json.load(f2)

print('slots_architecture equal:', d1['slots_architecture'] == d2['slots_architecture'])
print('full doc equal:', d1 == d2)
