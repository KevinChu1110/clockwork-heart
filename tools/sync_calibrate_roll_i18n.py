import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "CALIBRATE_JUMP_2": "極限跳兩階！發條大幅進階",
        "極限跳兩階！發條大幅進階": "極限跳兩階！發條大幅進階",
        "CALIBRATE_JUMP_1": "跳一階成功！發條突破進階",
        "跳一階成功！發條突破進階": "跳一階成功！發條突破進階",
        "CALIBRATE_PITY_JUMP": "第七次保底啟動！突破跳階成功",
        "第七次保底啟動！突破跳階成功": "第七次保底啟動！突破跳階成功",
        "CALIBRATE_MAINTAIN": "校準微調完成，維持同階",
        "校準微調完成，維持同階": "校準微調完成，維持同階",
        "CALIBRATE_RED_MAX": "已達極限紅階，微調維持頂階",
        "已達極限紅階，微調維持頂階": "已達極限紅階，微調維持頂階",
        "CALIBRATE_FAIL": "校準未達標，安全彈簧保護不碎裝",
        "校準未達標，安全彈簧保護不碎裝": "校準未達標，安全彈簧保護不碎裝",
    },
    "zh_CN": {
        "CALIBRATE_JUMP_2": "极限跳两阶！发条大幅进阶",
        "極限跳兩階！發條大幅進階": "极限跳两阶！发条大幅进阶",
        "CALIBRATE_JUMP_1": "跳一阶成功！发条突破进阶",
        "跳一階成功！發條突破進階": "跳一阶成功！发条突破进阶",
        "CALIBRATE_PITY_JUMP": "第七次保底启动！突破跳阶成功",
        "第七次保底啟動！突破跳階成功": "第七次保底启动！突破跳阶成功",
        "CALIBRATE_MAINTAIN": "校准微调完成，维持同阶",
        "校準微調完成，維持同階": "校准微调完成，维持同阶",
        "CALIBRATE_RED_MAX": "已达极限红阶，微调维持顶阶",
        "已達極限紅階，微調維持頂階": "已达极限红阶，微调维持顶阶",
        "CALIBRATE_FAIL": "校准未达标，安全弹簧保护不碎装",
        "校準未達標，安全彈簧保護不碎裝": "校准未达标，安全弹簧保护不碎装",
    },
    "en": {
        "CALIBRATE_JUMP_2": "Massive leap +2 tiers! Clockwork greatly advanced",
        "極限跳兩階！發條大幅進階": "Massive leap +2 tiers! Clockwork greatly advanced",
        "CALIBRATE_JUMP_1": "Success +1 tier! Clockwork breakthrough",
        "跳一階成功！發條突破進階": "Success +1 tier! Clockwork breakthrough",
        "CALIBRATE_PITY_JUMP": "7th pity triggered! Guaranteed tier leap",
        "第七次保底啟動！突破跳階成功": "7th pity triggered! Guaranteed tier leap",
        "CALIBRATE_MAINTAIN": "Calibrated: fine-tuned, maintained tier",
        "校準微調完成，維持同階": "Calibrated: fine-tuned, maintained tier",
        "CALIBRATE_RED_MAX": "At Red tier cap: fine-tuned, maintained peak",
        "已達極限紅階，微調維持頂階": "At Red tier cap: fine-tuned, maintained peak",
        "CALIBRATE_FAIL": "Calibration failed: safety spring protects gear",
        "校準未達標，安全彈簧保護不碎裝": "Calibration failed: safety spring protects gear",
    },
    "ja": {
        "CALIBRATE_JUMP_2": "限界突破！2段階一気にランクアップ！",
        "極限跳兩階！發條大幅進階": "限界突破！2段階一気にランクアップ！",
        "CALIBRATE_JUMP_1": "校正成功！1段階ランクアップ！",
        "跳一階成功！發條突破進階": "校正成功！1段階ランクアップ！",
        "CALIBRATE_PITY_JUMP": "7回目天井発動！確定ランクアップ！",
        "第七次保底啟動！突破跳階成功": "7回目天井発動！確定ランクアップ！",
        "CALIBRATE_MAINTAIN": "校正完了：微調整、同ランクを維持",
        "校準微調完成，維持同階": "校正完了：微調整、同ランクを維持",
        "CALIBRATE_RED_MAX": "極限の赤ランク到達中：微調整で最高位を維持",
        "已達極限紅階，微調維持頂階": "極限の赤ランク到達中：微調整で最高位を維持",
        "CALIBRATE_FAIL": "校正未達：安全バネが作動、破損なし",
        "校準未達標，安全彈簧保護不碎裝": "校正未達：安全バネが作動、破損なし",
    },
    "ko": {
        "CALIBRATE_JUMP_2": "한계 돌파! 2단계 연속 도약 성공!",
        "極限跳兩階！發條大幅進階": "한계 돌파! 2단계 연속 도약 성공!",
        "CALIBRATE_JUMP_1": "교정 성공! 1단계 도약 완료!",
        "跳一階成功！發條突破進階": "교정 성공! 1단계 도약 완료!",
        "CALIBRATE_PITY_JUMP": "7회 천장 발동! 확정 단계 도약!",
        "第七次保底啟動！突破跳階成功": "7회 천장 발動! 확정 단계 도약!",
        "CALIBRATE_MAINTAIN": "교정 완료: 미세 조정, 동일 단계 유지",
        "校準微調完成，維持同階": "교정 완료: 미세 조정, 동일 단계 유지",
        "CALIBRATE_RED_MAX": "극한의 붉은 등급 도달: 최고 단계 유지",
        "已達極限紅階，微調維持頂階": "극한의 붉은 등급 도달: 최고 단계 유지",
        "CALIBRATE_FAIL": "교정 미달: 안전 스프링 작동, 장비 보존",
        "校準未達標，安全彈簧保護不碎裝": "교정 미달: 안전 스프링 작동, 장비 보존",
    },
    "es": {
        "CALIBRATE_JUMP_2": "¡Salto masivo de 2 niveles! Gran avance",
        "極限跳兩階！發條大幅進階": "¡Salto masivo de 2 niveles! Gran avance",
        "CALIBRATE_JUMP_1": "¡Éxito +1 nivel! Mecanismo mejorado",
        "跳一階成功！發條突破進階": "¡Éxito +1 nivel! Mecanismo mejorado",
        "CALIBRATE_PITY_JUMP": "¡Garantía en intento 7 activada! Salto asegurado",
        "第七次保底啟動！突破跳階成功": "¡Garantía en intento 7 activada! Salto asegurado",
        "CALIBRATE_MAINTAIN": "Calibrado: ajuste fino, mismo nivel",
        "校準微調完成，維持同階": "Calibrado: ajuste fino, mismo nivel",
        "CALIBRATE_RED_MAX": "Nivel Rojo máximo: ajuste fino, mantiene cima",
        "已達極限紅階，微調維持頂階": "Nivel Rojo máximo: ajuste fino, mantiene cima",
        "CALIBRATE_FAIL": "Calibración no alcanzada: resorte de seguridad protege",
        "校準未達標，安全彈簧保護不碎裝": "Calibración no alcanzada: resorte de seguridad protege",
    },
}

def sync_locales():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "game", "data", "i18n", "content")
    root_i18n_dir = os.path.join(base_dir, "game", "data", "i18n")

    for loc, trans in TRANSLATIONS.items():
        # 1. Update content/<loc>/ui.json
        ui_path = os.path.join(content_dir, loc, "ui.json")
        if os.path.exists(ui_path):
            with open(ui_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in trans.items():
                data[k] = v
            with open(ui_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Updated {ui_path}")
        else:
            print(f"[WARN] Not found: {ui_path}")

        # 2. Update root <loc>.json
        root_path = os.path.join(root_i18n_dir, f"{loc}.json")
        if os.path.exists(root_path):
            with open(root_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in trans.items():
                data[k] = v
            with open(root_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Updated {root_path}")
        else:
            print(f"[WARN] Not found: {root_path}")

if __name__ == "__main__":
    sync_locales()
