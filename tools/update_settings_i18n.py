#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    "音量調節與聲效開關": {
        "zh_TW": "音量調節與聲效開關",
        "zh_CN": "音量调节与声效开关",
        "en": "Volume & Sound Effects",
        "ja": "音量調整と効果音設定",
        "ko": "볼륨 조절 및 사운드 설정",
        "es": "Ajuste de volumen y sonido",
    },
    "背景音樂 (BGM)": {
        "zh_TW": "背景音樂 (BGM)",
        "zh_CN": "背景音乐 (BGM)",
        "en": "Music (BGM)",
        "ja": "背景音楽 (BGM)",
        "ko": "배경음악 (BGM)",
        "es": "Música (BGM)",
    },
    "戰鬥音效 (SFX)": {
        "zh_TW": "戰鬥音效 (SFX)",
        "zh_CN": "战斗音效 (SFX)",
        "en": "Sound Effects (SFX)",
        "ja": "効果音 (SFX)",
        "ko": "전투 효과음 (SFX)",
        "es": "Efectos de sonido (SFX)",
    },
    "顯示模式與渲染設定": {
        "zh_TW": "顯示模式與渲染設定",
        "zh_CN": "显示模式与渲染设置",
        "en": "Display & Rendering",
        "ja": "表示モードと描画設定",
        "ko": "화면 모드 및 렌더링 설정",
        "es": "Modo de pantalla y renderizado",
    },
    "全螢幕沉浸模式": {
        "zh_TW": "全螢幕沉浸模式",
        "zh_CN": "全屏幕沉浸模式",
        "en": "Fullscreen Immersive Mode",
        "ja": "全画面没入モード",
        "ko": "전체 화면 몰입 모드",
        "es": "Modo inmersivo pantalla completa",
    },
    "切換顯示模式": {
        "zh_TW": "切換顯示模式",
        "zh_CN": "切换显示模式",
        "en": "Switch Display Mode",
        "ja": "表示モード切替",
        "ko": "화면 모드 전환",
        "es": "Cambiar modo de pantalla",
    },
    "已切換顯示模式！": {
        "zh_TW": "已切換顯示模式！",
        "zh_CN": "已切换显示模式！",
        "en": "Display mode switched!",
        "ja": "表示モードを切り替えました！",
        "ko": "화면 모드가 전환되었습니다!",
        "es": "¡Modo de pantalla cambiado!",
    },
    "雲端與本機存檔備份": {
        "zh_TW": "雲端與本機存檔備份",
        "zh_CN": "云端与本机存档备份",
        "en": "Cloud & Local Save Backup",
        "ja": "クラウド・ローカルセーブ",
        "ko": "클라우드 및 로컬 세이브 백업",
        "es": "Copia de seguridad local y nube",
    },
    "匯出存檔備份檔 (JSON)": {
        "zh_TW": "匯出存檔備份檔 (JSON)",
        "zh_CN": "导出存档备份文件 (JSON)",
        "en": "Export Save Backup (JSON)",
        "ja": "セーブデータを書き出す (JSON)",
        "ko": "세이브 백업 내보내기 (JSON)",
        "es": "Exportar partida guardada (JSON)",
    },
    "從外部備份還原存檔": {
        "zh_TW": "從外部備份還原存檔",
        "zh_CN": "从外部备份还原存档",
        "en": "Restore Save from Backup",
        "ja": "外部バックアップから復元",
        "ko": "외부 백업에서 세이브 복원",
        "es": "Restaurar desde copia",
    },
    "存檔備份已成功匯出至本機！": {
        "zh_TW": "存檔備份已成功匯出至本機！",
        "zh_CN": "存档备份已成功导出至本机！",
        "en": "Save backup successfully exported locally!",
        "ja": "セーブデータをローカルに書き出しました！",
        "ko": "세이브 백업을 로컬에 성공적으로 내보냈습니다!",
        "es": "¡Copia de seguridad exportada localmente!",
    },
    "請選擇要還原的備份存檔...": {
        "zh_TW": "請選擇要還原的備份存檔...",
        "zh_CN": "请选择要还原的备份存档...",
        "en": "Please select backup save to restore...",
        "ja": "復元するバックアップを選択してください...",
        "ko": "복원할 백업 세이브를 선택하세요...",
        "es": "Seleccione la copia para restaurar...",
    },
}

# 1. 更新 game/data/i18n/content/<loc>/ui.json
content_dir = 'game/data/i18n/content'
for loc in locales:
    p = os.path.join(content_dir, loc, 'ui.json')
    if not os.path.exists(p):
        print(f"[content/ui.json] Missing {p}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    before_len = len(d)
    for k, v in data_map.items():
        d[k] = v[loc]
    after_len = len(d)
    print(f'[content/ui.json] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

# 2. 同步更新 game/data/i18n/<loc>.json（滿足 Loc.t 根層查找）
root_i18n_dir = 'game/data/i18n'
for loc in locales:
    p = os.path.join(root_i18n_dir, f'{loc}.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        before_len = len(d)
        for k, v in data_map.items():
            d[k] = v[loc]
        after_len = len(d)
        print(f'[root i18n] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')

print("Update completed successfully!")
