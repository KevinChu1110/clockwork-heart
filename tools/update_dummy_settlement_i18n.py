#!/usr/bin/env python3
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TRANSLATIONS = {
    "zh_TW": {
        "木人試招數據卡": "木人試招數據卡",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "武術館「招」軸訓練回饋 · 能量消耗 0",
        "本次總傷害": "本次總傷害",
        "招式命中累積": "招式命中累積",
        "點": "點",
        "試招耗時": "試招耗時",
        "戰鬥歷程秒數": "戰鬥歷程秒數",
        "秒": "秒",
        "秒傷 (DPS)": "秒傷 (DPS)",
        "每秒平均輸出": "每秒平均輸出",
        "點 / 秒": "點 / 秒",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。",
        "完成試招": "完成試招",
    },
    "zh_CN": {
        "木人試招數據卡": "木人试招数据卡",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "武术馆「招」轴训练反馈 · 能量消耗 0",
        "本次總傷害": "本次总伤害",
        "招式命中累積": "招式命中累积",
        "點": "点",
        "試招耗時": "试招耗时",
        "戰鬥歷程秒數": "战斗历程秒数",
        "秒": "秒",
        "秒傷 (DPS)": "秒伤 (DPS)",
        "每秒平均輸出": "每秒平均输出",
        "點 / 秒": "点 / 秒",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "木人桩为不消耗能量的自由试招训练。可在武术馆兵器架调配各色兵刃，体会不同招式的出招前摇与段数节奏。",
        "完成試招": "完成试招",
    },
    "en": {
        "木人試招數據卡": "Dummy Trial Report",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "Martial Hall Skill Training Feedback · Energy Cost: 0",
        "本次總傷害": "Total Damage",
        "招式命中累積": "Cumulative Hits",
        "點": "pts",
        "試招耗時": "Trial Duration",
        "戰鬥歷程秒數": "Combat Duration (s)",
        "秒": "s",
        "秒傷 (DPS)": "DPS",
        "每秒平均輸出": "Avg Damage / Second",
        "點 / 秒": "pts / s",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "Training dummy practice consumes no energy. Switch weapons at the Martial Hall rack to feel the wind-up and combo rhythm of each style.",
        "完成試招": "Finish Trial",
    },
    "ja": {
        "木人試招數據卡": "木人試技データカード",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "武術館「技」訓練フィードバック · エネルギー消費 0",
        "本次總傷害": "総ダメージ",
        "招式命中累積": "技命中累積",
        "點": "pt",
        "試招耗時": "試技時間",
        "戰鬥歷程秒數": "戦闘時間（秒）",
        "秒": "秒",
        "秒傷 (DPS)": "秒間ダメージ (DPS)",
        "每秒平均輸出": "毎秒平均ダメージ",
        "點 / 秒": "pt / 秒",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "木人での試技はエネルギーを消費しない自由訓練です。武術館の武器架で多彩な武器を試し、技の発生や連撃のリズムを掴みましょう。",
        "完成試招": "試技を終了",
    },
    "ko": {
        "木人試招數據卡": "목인 연습 데이터 카드",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "무술관 「기술」 훈련 피드백 · 에너지 소모 0",
        "本次總傷害": "총 피해량",
        "招式命中累積": "기술 적중 누적",
        "點": "점",
        "試招耗時": "연습 시간",
        "戰鬥歷程秒數": "전투 시간(초)",
        "秒": "초",
        "秒傷 (DPS)": "초당 피해량 (DPS)",
        "每秒平均輸出": "초당 평균 공격력",
        "點 / 秒": "점 / 초",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "목인 연습은 에너지를 소모하지 않는 자유 훈련입니다. 무술관 무기 거치대에서 다양한 무기를 골라 기술의 선딜레이와 연타 리듬을 익혀보세요.",
        "完成試招": "연습 완료",
    },
    "es": {
        "木人試招數據卡": "Ficha de prueba con muñeco",
        "武術館「招」軸訓練回饋 · 能量消耗 0": "Entrenamiento en sala marcial · Coste de energía 0",
        "本次總傷害": "Daño total",
        "招式命中累積": "Impactos acumulados",
        "點": "pts",
        "試招耗時": "Tiempo de prueba",
        "戰鬥歷程秒數": "Duración en segundos",
        "秒": "s",
        "秒傷 (DPS)": "DPS",
        "每秒平均輸出": "Daño medio / segundo",
        "點 / 秒": "pts / s",
        "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。": "La práctica con el muñeco no consume energía. Elige armas en el armero de la sala marcial para dominar los tiempos y el ritmo de cada técnica.",
        "完成試招": "Finalizar prueba",
    },
}

def update_json_file(file_path: Path, new_entries: dict):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for k, v in new_entries.items():
        if k not in data or data[k] != v:
            data[k] = v
            added += 1

    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {file_path.relative_to(REPO_ROOT)}: {added} entries added/updated")

def main():
    for loc, entries in TRANSLATIONS.items():
        # 1. 更新 data/i18n/content/<loc>/ui.json
        ui_json = REPO_ROOT / "game" / "data" / "i18n" / "content" / loc / "ui.json"
        update_json_file(ui_json, entries)

        # 2. 更新 data/i18n/<loc>.json
        loc_json = REPO_ROOT / "game" / "data" / "i18n" / f"{loc}.json"
        update_json_file(loc_json, entries)

if __name__ == "__main__":
    main()
