#!/usr/bin/env python3
import json
import subprocess

parry_translations = {
    "zh_TW": {
        "發條格擋": "發條格擋",
        "巨偶蓄力中… %.1f 秒後可格擋": "巨偶蓄力中… %.1f 秒後可格擋",
        "蓄力必殺": "蓄力必殺",
        "現在按 J 或點發條格擋！": "現在按 J 或點發條格擋！",
        "現在點發條格擋！": "現在點發條格擋！"
    },
    "zh_CN": {
        "發條格擋": "发条格挡",
        "巨偶蓄力中… %.1f 秒後可格擋": "巨偶蓄力中… %.1f 秒后可格挡",
        "蓄力必殺": "蓄力必杀",
        "現在按 J 或點發條格擋！": "现在按 J 或点发条格挡！",
        "現在點發條格擋！": "现在点发条格挡！"
    },
    "en": {
        "發條格擋": "Windup Parry",
        "巨偶蓄力中… %.1f 秒後可格擋": "Colossus charging… parryable in %.1f s",
        "蓄力必殺": "Charged Strike",
        "現在按 J 或點發條格擋！": "Press J or tap Windup Parry now!",
        "現在點發條格擋！": "Tap Windup Parry now!"
    },
    "ja": {
        "發條格擋": "ぜんまいパリィ",
        "巨偶蓄力中… %.1f 秒後可格擋": "巨偶が力を溜めている… %.1f 秒後にパリィ可能",
        "蓄力必殺": "チャージ必殺",
        "現在按 J 或點發條格擋！": "今すぐ J かぜんまいパリィをタップ！",
        "現在點發條格擋！": "今すぐぜんまいパリィをタップ！"
    },
    "ko": {
        "發條格擋": "태엽 패링",
        "巨偶蓄力中… %.1f 秒後可格擋": "거상 기 모으는 중… %.1f 초 뒤 패링 가능",
        "蓄力必殺": "차지 필살기",
        "現在按 J 或點發條格擋！": "지금 J 또는 태엽 패링을 탭하세요!",
        "現在點發條格擋！": "지금 태엽 패링을 탭하세요!"
    },
    "es": {
        "發條格擋": "Parada de Cuerda",
        "巨偶蓄力中… %.1f 秒後可格擋": "Coloso cargando… se podrá parar en %.1f s",
        "蓄力必殺": "Golpe Cargado",
        "現在按 J 或點發條格擋！": "¡Pulsa J o toca Parada de Cuerda ahora!",
        "現在點發條格擋！": "¡Toca Parada de Cuerda ahora!"
    }
}

conflicted_files = [
    "game/data/i18n/content/en/ui.json",
    "game/data/i18n/content/es/ui.json",
    "game/data/i18n/content/ja/ui.json",
    "game/data/i18n/content/ko/ui.json",
    "game/data/i18n/content/zh_CN/ui.json",
    "game/data/i18n/content/zh_TW/ui.json",
    "game/data/i18n/en.json",
    "game/data/i18n/es.json",
    "game/data/i18n/ja.json",
    "game/data/i18n/ko.json",
    "game/data/i18n/zh_CN.json",
    "game/data/i18n/zh_TW.json"
]

for fpath in conflicted_files:
    subprocess.run(["git", "checkout", "--ours", fpath], check=True)

for loc, kv in parry_translations.items():
    for fpath in [f"game/data/i18n/content/{loc}/ui.json", f"game/data/i18n/{loc}.json"]:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in kv.items():
            data[k] = v
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Applied parry translations to {fpath}")

for fpath in conflicted_files:
    subprocess.run(["git", "add", fpath], check=True)

print("All i18n conflicts resolved and staged.")
