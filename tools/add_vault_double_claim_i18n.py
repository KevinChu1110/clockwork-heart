import json
import os

repo = "/opt/side/bravesoul-game"
keys = {
    "zh_TW": {
        "vault.btn_double_claim": "雙倍領取",
        "vault.ad_removed_double": "已去廣告尊享雙倍",
    },
    "zh_CN": {
        "vault.btn_double_claim": "双倍领取",
        "vault.ad_removed_double": "已去广告尊享双倍",
    },
    "en": {
        "vault.btn_double_claim": "Double Claim",
        "vault.ad_removed_double": "No-Ads Privilege: Double Rewards Granted",
    },
    "ja": {
        "vault.btn_double_claim": "2倍受取",
        "vault.ad_removed_double": "広告削除特権：2倍受取完了",
    },
    "ko": {
        "vault.btn_double_claim": "2배 수령",
        "vault.ad_removed_double": "광고 제거 혜택: 2배 수령 완료",
    },
    "es": {
        "vault.btn_double_claim": "Reclamo Doble",
        "vault.ad_removed_double": "Sin anuncios: Recompensa doble reclamada",
    },
}

for loc, kv in keys.items():
    p1 = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p1)

    p2 = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p2)
