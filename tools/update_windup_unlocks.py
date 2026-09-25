import json
import os

UNLOCK_ENTRIES = {
    "釘釘把風箱蓋上，沒說謝謝。爐火重新咬住鐵。他丟來一塊碎齒輪：「別弄丟。」": {
        "zh_TW": "釘釘把風箱蓋上，沒說謝謝。爐火重新咬住鐵。他丟來一塊碎齒輪：「別弄丟。」",
        "zh_CN": "钉钉把风箱盖上，没说谢谢。炉火重新咬住铁。他丢来一块碎齿轮：「别弄丢。」",
        "en": "Ding closed the bellows without a thank you. The flames bit into iron again. Tossing a shattered gear, he said: 'Don't lose it.'",
        "ja": "釘釘は礼も言わずにふいごの蓋を閉めた。炉の火が再び鉄を捉える。彼は欠けた歯車を放り投げた：「失くすなよ。」",
        "ko": "딩딩은 고맙다는 말도 없이 풀무 덮개를 닫았다. 화로의 불길이 다시 쇠를 집어삼킨다. 그가 부서진 톱니바퀴 하나를 던져주었다: \"잃어버리지 마라.\"",
        "es": "Ding cerró el fuelle sin dar las gracias. El fuego volvió a morder el hierro. Lanzó un engranaje roto: «No lo pierdas».",
    },
    "灰鼬哼一聲，把門推開半掌。腳步聲從石板上傳回來。他沒看你。": {
        "zh_TW": "灰鼬哼一聲，把門推開半掌。腳步聲從石板上傳回來。他沒看你。",
        "zh_CN": "灰鼬哼一声，把门推开半掌。脚步声从石板上传回来。他没看你。",
        "en": "Gray Weasel snorted, pushing the gate open a hand's breadth. Footsteps echoed from the cobblestones. He didn't look at you.",
        "ja": "灰イタチは鼻を鳴らし、門を半掌ほど押し開けた。敷石から足音が響いてくる。彼はあなたを見ようとしなかった。",
        "ko": "회색족제비는 콧방귀를 뀌며 성문을 반 뼘쯤 밀어 열었다. 돌판 위로 발소리가 메아리쳤다. 그는 당신을 쳐다보지도 않았다.",
        "es": "Comadreja Gris resopló, empujando la puerta medio palmo. Los pasos resonaron en los adoquines. No te miró.",
    },
    "木劍又開始小小地晃。小芽把劍舉過頭頂：「我以後要當騎士！比獅子還大！」": {
        "zh_TW": "木劍又開始小小地晃。小芽把劍舉過頭頂：「我以後要當騎士！比獅子還大！」",
        "zh_CN": "木剑又开始小小地晃。小芽把剑举过头顶：「我以后要当骑士！比狮子还大！」",
        "en": "The wooden sword began to swing gently again. Sprout raised it high above her head: 'I'll become a knight one day! Greater than a lion!'",
        "ja": "木剣が再び小さく揺れ始めた。芽は剣を頭上高く掲げた：「いつか騎士になるんだ！ライオンより大きくなるぞ！」",
        "ko": "목검이 다시 작게 흔들리기 시작했다. 새싹은 검을 머리 위로 번쩍 치켜들었다: \"나 나중에 기사가 될 거야! 사자보다 더 큰 기사!\"",
        "es": "La espada de madera volvió a mecerse suavemente. Brote la alzó sobre su cabeza: «¡Algún día seré caballero! ¡Más grande que un león!».",
    },
    "盤重新咬合，發出極輕的齒聲。星讀合上眼：「它記得路。我們只是幫它醒。」": {
        "zh_TW": "盤重新咬合，發出極輕的齒聲。星讀合上眼：「它記得路。我們只是幫它醒。」",
        "zh_CN": "盘重新咬合，发出极轻的齿声。星读合上眼：「它记得路。我们只是帮它醒。」",
        "en": "The astrolabe re-engaged with a faint click. Starreader closed her eyes: 'It remembers the way. We merely help it wake.'",
        "ja": "盤は再び噛み合い、かすかな歯車の音を立てた。星読は目を閉じた：「星盤は道を知っている。我らはただ目覚めを手伝うだけ。」",
        "ko": "성반이 다시 맞물리며 아주 가냘픈 톱니 소리를 냈다. 별읽기가 눈을 감았다: \"길을 기억하고 있구나. 우리는 그저 깨워주었을 뿐이다.\"",
        "es": "El astrolabio volvió a engranar con un suave chasquido. Lector de Estrellas cerró los ojos: «Recuerda el camino. Solo lo ayudamos a despertar».",
    },
    "石獅那隻完好的眼沒有眨。台座卻輕輕震了一下，像有人在裡面吸了一口氣。": {
        "zh_TW": "石獅那隻完好的眼沒有眨。台座卻輕輕震了一下，像有人在裡面吸了一口氣。",
        "zh_CN": "石狮那只完好的眼没有眨。台座却轻轻震了一下，像有人在里面吸了一口气。",
        "en": "The stone lion's intact eye never blinked. Yet the pedestal trembled slightly, as if someone inside had taken a deep breath.",
        "ja": "石獅子の無事な目は瞬きしなかった。だが台座がかすかに震え、まるで何者かが内で深く息を吸い込んだかのようだった。",
        "ko": "돌사자의 온전한 눈은 깜빡이지 않았다. 하지만 받침대가 은은하게 떨렸다, 마치 누군가 그 안에서 숨을 들이쉰 것처럼.",
        "es": "El ojo sano del león de piedra no parpadeó. Sin embargo, el pedestal tembló levemente, como si alguien adentro hubiera tomado aliento.",
    },
    "發條咬回去時，白狐耳尖動了一下。香灰掉下一點。它仍閉眼。": {
        "zh_TW": "發條咬回去時，白狐耳尖動了一下。香灰掉下一點。它仍閉眼。",
        "zh_CN": "发条咬回去时，白狐耳尖动了一下。香灰掉下一点。它仍闭眼。",
        "en": "As the spring clicked into place, the tip of the white fox's ear twitched. A trace of incense ash fell. Its eyes remained closed.",
        "ja": "ゼンマイが再び噛み合った瞬間、白狐の耳先がかすかに動いた。線香の灰が少し落ちる。像は依然として目を閉じたままだ。",
        "ko": "태엽이 다시 맞물릴 때, 백여우의 귓등이 살짝 떨렸다. 향의 재가 조금 떨어져 내렸다. 여전히 눈은 감은 채였다.",
        "es": "Al encajar el resorte, la punta de la oreja del zorro blanco se movió. Cayó una pizca de ceniza. Sus ojos siguieron cerrados.",
    }
}

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
BASE_DIR = "/opt/side/bravesoul-game/game/data/i18n/content"

for loc in LOCALES:
    path = os.path.join(BASE_DIR, loc, "ui.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    updated = 0
    for key, trans in UNLOCK_ENTRIES.items():
        val = trans[loc]
        if key not in data:
            data[key] = val
            added += 1
        elif data[key] != val:
            data[key] = val
            updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"[{loc}] ui.json 追加 unlock 句子完成: 新增 {added} 條, 更新 {updated} 條, 總條目: {len(data)}")
