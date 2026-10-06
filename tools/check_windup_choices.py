import json

CASES = [
    {"id": "ding", "npc": "釘釘", "title": "釘釘的風箱停了", "desc": "鐵匠鋪風箱發條鬆了一夜。釘釘蹲在爐邊，錘提得動、風卻沒有。", "prompt": "釘釘：別站門口看。發條在爐左側，順時針兩圈。弄斷了你賠。", "choices": [{"id": "a", "label": "順時針兩圈"}, {"id": "b", "label": "先擦淨再轉"}], "unlock": "釘釘把風箱蓋上，沒說謝謝。爐火重新咬住鐵。他丟來一塊碎齒輪：「別弄丟。」"},
    {"id": "weasel", "npc": "灰鼬", "title": "灰鼬的門栓鬆了", "desc": "城門栓發條一夜走完。灰鼬靠牆，不讓人進出，也不自己彎腰。", "prompt": "灰鼬：門栓在腳邊。上緊。別指望有人抱你。", "choices": [{"id": "a", "label": "蹲下去上緊門栓"}, {"id": "b", "label": "問他要不要一起轉"}], "unlock": "灰鼬哼一聲，把門推開半掌。腳步聲從石板上傳回來。他沒看你。"},
    {"id": "sprout", "npc": "小芽", "title": "小芽的木劍轉不動", "desc": "小芽蹲在旗下，木劍發條卡死。她轉了三次，第三次咬嘴唇。", "prompt": "小芽：它昨天還會自己晃！你幫我看好不好？輕輕的。", "choices": [{"id": "a", "label": "輕輕轉回原位"}, {"id": "b", "label": "讓她扶著、你轉"}], "unlock": "木劍又開始小小地晃。小芽把劍舉過頭頂：「我以後要當騎士！比獅子還大！」"},
    {"id": "starread", "npc": "星讀", "title": "星讀的觀星盤停一格", "desc": "聚魂殿觀星盤昨夜停了一格。星讀手指停在空位上，沒有責備盤。", "prompt": "星讀：缺的那格在東側。轉回去就好。別急著問為什麼停。", "choices": [{"id": "a", "label": "把東側那格轉回去"}, {"id": "b", "label": "先聽她數一圈再轉"}], "unlock": "盤重新咬合，發出極輕的齒聲。星讀合上眼：「它記得路。我們只是幫它醒。」"},
    {"id": "lion_remnant", "npc": "獅子殘件", "title": "石獅像掉出發條", "desc": "石獅缺了一眼。另一眼望向內殿。眼窩裡一截發條掉在台座上。", "prompt": "發條還溫。塞回去，順著齒紋轉半圈。石獅不說話。", "choices": [{"id": "a", "label": "把發條塞回眼窩"}, {"id": "b", "label": "先對齊齒再轉半圈"}], "unlock": "石獅那隻完好的眼沒有眨。台座卻輕輕震了一下，像有人在裡面吸了一口氣。"},
    {"id": "fox_remnant", "npc": "狐狸殘件", "title": "白狐像耳後卡住", "desc": "白狐像閉著眼。香灰未冷。耳後一截發條卡在半途，轉不動也退不回。", "prompt": "卡住的是耳後那截。逆時針退一齒，再順回去。", "choices": [{"id": "a", "label": "逆時針退一齒再上"}, {"id": "b", "label": "上香後再轉"}], "unlock": "發條咬回去時，白狐耳尖動了一下。香灰掉下一點。它仍閉眼。"}
]

for lc in ["en", "ja"]:
    path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/ui.json"
    data = json.load(open(path, encoding="utf-8"))
    for c in CASES:
        for ch in c["choices"]:
            lbl = ch["label"]
            print(f"[{lc}] {lbl} -> {data.get(lbl, 'MISSING')}")
