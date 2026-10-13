import json
import os

repo_dir = "/opt/side/bravesoul-game"

data_by_lang = {
    "zh_TW": {
        "vault.bubble_accumulated": "已累積 %dh / %dh",
        "vault.bubble_claim_ready": "可領取",
        "vault.bubble_full": "已滿 8h · 可領取",
    },
    "zh_CN": {
        "vault.bubble_accumulated": "已累积 %dh / %dh",
        "vault.bubble_claim_ready": "可领取",
        "vault.bubble_full": "已满 8h · 可领取",
    },
    "en": {
        "vault.bubble_accumulated": "Stored %dh / %dh",
        "vault.bubble_claim_ready": "Claim",
        "vault.bubble_full": "Full 8h · Claim",
    },
    "ja": {
        "vault.bubble_accumulated": "蓄積 %dh / %dh",
        "vault.bubble_claim_ready": "受取可能",
        "vault.bubble_full": "満充電 8h · 受取可能",
    },
    "ko": {
        "vault.bubble_accumulated": "누적 %dh / %dh",
        "vault.bubble_claim_ready": "수령 가능",
        "vault.bubble_full": "완전 충전 8h · 수령 가능",
    },
    "es": {
        "vault.bubble_accumulated": "Acumulado %dh / %dh",
        "vault.bubble_claim_ready": "Reclamar",
        "vault.bubble_full": "Lleno 8h · Reclamar",
    },
}

for lang, items in data_by_lang.items():
    p1 = os.path.join(repo_dir, f"game/data/i18n/{lang}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
        for k, v in items.items():
            d1[k] = v
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
        print(f"Updated {p1}")

    p2 = os.path.join(repo_dir, f"game/data/i18n/content/{lang}/ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        for k, v in items.items():
            d2[k] = v
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
        print(f"Updated {p2}")
