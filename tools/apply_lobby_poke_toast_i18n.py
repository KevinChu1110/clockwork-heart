#!/usr/bin/env python3
import json
import os
import sys

TRANSLATIONS = {
    "zh_TW": {
        "看我的旋風斬～喝！": "看我的旋風斬～喝！",
        "背後的發條上得剛剛好，出發吧！": "背後的發條上得剛剛好，出發吧！",
        "聽見神殿齒輪的轉動聲了嗎？": "聽見神殿齒輪的轉動聲了嗎？",
        "神殿的以太核心正在共鳴……": "神殿的以太核心正在共鳴……",
        "隨時準備好去挑戰大首領！": "隨時準備好去挑戰大首領！",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "聚魂完畢！獲得了戰魂碎片與戰魂經驗！"
    },
    "zh_CN": {
        "看我的旋風斬～喝！": "看我的旋风斩～喝！",
        "背後的發條上得剛剛好，出發吧！": "背后的发条上得刚刚好，出发吧！",
        "聽見神殿齒輪的轉動聲了嗎？": "听见神殿齿轮的转动声了吗？",
        "神殿的以太核心正在共鳴……": "神殿的以太核心正在共鸣……",
        "隨時準備好去挑戰大首領！": "随时准备好去挑战大首领！",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "聚魂完毕！获得了战魂碎片与战魂经验！"
    },
    "en": {
        "看我的旋風斬～喝！": "Take my Whirlwind Slash—Hah!",
        "背後的發條上得剛剛好，出發吧！": "The wind-up key on my back is wound just right, let's go!",
        "聽見神殿齒輪的轉動聲了嗎？": "Can you hear the temple gears turning?",
        "神殿的以太核心正在共鳴……": "The temple's ether core is resonating...",
        "隨時準備好去挑戰大首領！": "Always ready to challenge the Grand Boss!",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "Soul gathering complete! Received Soul Shards and Soul EXP!"
    },
    "ja": {
        "看我的旋風斬～喝！": "我が旋風斬を見よ～ハッ！",
        "背後的發條上得剛剛好，出發吧！": "背中のゼンマイはバッチリ巻けた、出発だ！",
        "聽見神殿齒輪的轉動聲了嗎？": "神殿の歯車が回る音が聞こえるかい？",
        "神殿的以太核心正在共鳴……": "神殿のエーテルコアが共鳴している……",
        "隨時準備好去挑戰大首領！": "大ボスに挑む準備はいつでも万全だ！",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "聚魂完了！戦魂の欠片と戦魂経験を獲得！"
    },
    "ko": {
        "看我的旋風斬～喝！": "내 회오리 베기를 받아라~ 핫!",
        "背後的發條上得剛剛好，出發吧！": "등 뒤의 태엽이 딱 맞게 감겼어, 출발하자!",
        "聽見神殿齒輪的轉動聲了嗎？": "신전 톱니바퀴가 돌아가는 소리가 들리나요?",
        "神殿的以太核心正在共鳴……": "신전의 에테르 코어가 공명하고 있어……",
        "隨時準備好去挑戰大首領！": "언제든 대보스에게 도전할 준비 완료!",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "전혼 집중 완료! 전혼 조각과 전혼 경험치를 획득했습니다!"
    },
    "es": {
        "看我的旋風斬～喝！": "¡Mira mi Corte Torbellino... Ja!",
        "背後的發條上得剛剛好，出發吧！": "¡La cuerda de mi espalda está perfecta, en marcha!",
        "聽見神殿齒輪的轉動聲了嗎？": "¿Oyes el girar de los engranajes del templo?",
        "神殿的以太核心正在共鳴……": "El núcleo de éter del templo está resonando...",
        "隨時準備好去挑戰大首領！": "¡Siempre listos para desafiar al Gran Jefe!",
        "聚魂完畢！獲得了戰魂碎片與戰魂經驗！": "¡Reunión de almas completada! ¡Obtuviste fragmentos de alma y EXP de alma!"
    }
}

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    base_dir = os.path.join(root, "game", "data", "i18n")

    for lang, terms in TRANSLATIONS.items():
        # 1. Update content/<lang>/ui.json
        ui_path = os.path.join(base_dir, "content", lang, "ui.json")
        if os.path.exists(ui_path):
            with open(ui_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in terms.items():
                data[k] = v
            with open(ui_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {ui_path}")

        # 2. Update <lang>.json
        lang_path = os.path.join(base_dir, f"{lang}.json")
        if os.path.exists(lang_path):
            with open(lang_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in terms.items():
                data[k] = v
            with open(lang_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {lang_path}")

if __name__ == "__main__":
    main()
