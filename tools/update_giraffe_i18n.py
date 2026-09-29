#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "鐘塔長頸鹿": "鐘塔長頸鹿",
        "長頸鹿": "長頸鹿",
        "鐘樓天弦複合機關弓": "鐘樓天弦複合機關弓",
        "三環鏤空八音音筒發條鑰匙": "三環鏤空八音音筒發條鑰匙",
        "微型黃銅鐘擺重錘連桿短尾": "微型黃銅鐘擺重錘連桿短尾",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "沖壓馬口鐵胡桃拼花矮萌底盤",
        "三節黃銅伸縮潛望觀測兜帽": "三節黃銅伸縮潛望觀測兜帽",
        "晨曦禮賓防風呢絨斗篷披肩": "晨曦禮賓防風呢絨斗篷披肩",
        "雙聯潛望測距石英凸透鏡": "雙聯潛望測距石英凸透鏡",
    },
    "zh_CN": {
        "鐘塔長頸鹿": "钟塔长颈鹿",
        "長頸鹿": "长颈鹿",
        "鐘樓天弦複合機關弓": "钟楼天弦复合机关弓",
        "三環鏤空八音音筒發條鑰匙": "三环镂空八音音筒发条钥匙",
        "微型黃銅鐘擺重錘連桿短尾": "微型黄铜钟摆重锤连杆短尾",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "冲压马口铁胡桃拼花矮萌底盘",
        "三節黃銅伸縮潛望觀測兜帽": "三节黄铜伸缩潜望观测兜帽",
        "晨曦禮賓防風呢絨斗篷披肩": "晨曦礼宾防风呢绒斗篷披肩",
        "雙聯潛望測距石英凸透鏡": "双联潜望测距石英凸透镜",
    },
    "en": {
        "鐘塔長頸鹿": "The Belfry Giraffe",
        "長頸鹿": "Giraffe",
        "鐘樓天弦複合機關弓": "Belfry Celestial-String Composite Bow",
        "三環鏤空八音音筒發條鑰匙": "Three-Ring Carillon Brass Winding Key",
        "微型黃銅鐘擺重錘連桿短尾": "Pendulum Bob Brass Link Tail",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "Stamped Tinplate Walnut Giraffe Chassis",
        "三節黃銅伸縮潛望觀測兜帽": "Telescoping Periscope Observation Cowl",
        "晨曦禮賓防風呢絨斗篷披肩": "Dawn Herald Woolen Cape",
        "雙聯潛望測距石英凸透鏡": "Dual Periscope Quartz Lenses",
    },
    "ja": {
        "鐘塔長頸鹿": "鐘塔の麒麟 (ショウタウのキリン)",
        "長頸鹿": "キリン",
        "鐘樓天弦複合機關弓": "鐘楼天弦複合機関弓",
        "三環鏤空八音音筒發條鑰匙": "三連透かしオルゴールぜんまい鍵",
        "微型黃銅鐘擺重錘連桿短尾": "黄銅振り子ロッド短尾",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "プレス加工ブリキ胡桃細工矮萌素体",
        "三節黃銅伸縮潛望觀測兜帽": "三段黄銅伸縮潜望観測頭巾",
        "晨曦禮賓防風呢絨斗篷披肩": "晨曦礼賓防風ラシャケープ",
        "雙聯潛望測距石英凸透鏡": "連装潜望測距石英凸レンズ",
    },
    "ko": {
        "鐘塔長頸鹿": "종탑 기린",
        "長頸鹿": "기린",
        "鐘樓天弦複合機關弓": "종루 천현 복합 기관활",
        "三環鏤空八音音筒發條鑰匙": "3단 투각 오르골 태엽 열쇠",
        "微型黃銅鐘擺重錘連桿短尾": "초소형 황동 시계추 링크 꼬리",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "스탬핑 양철 호두 상감 소체 하판",
        "三節黃銅伸縮潛望觀測兜帽": "3단 황동 신축 잠망경 관측 두건",
        "晨曦禮賓防風呢絨斗篷披肩": "새벽 의전 방풍 모직 케이프",
        "雙聯潛望測距石英凸透鏡": "2연장 잠망 측거 석영 볼록렌즈",
    },
    "es": {
        "鐘塔長頸鹿": "La Jirafa del Campanario",
        "長頸鹿": "Jirafa",
        "鐘樓天弦複合機關弓": "Arco Mecánico Celestial del Campanario",
        "三環鏤空八音音筒發條鑰匙": "Llave de Cuerda Calada de Latón con Carillón",
        "微型黃銅鐘擺重錘連桿短尾": "Cola de Péndulo con Varilla de Latón",
        "沖壓馬口鐵胡桃拼花矮萌底盤": "Chasis de Jirafa de Hojalata y Nogal",
        "三節黃銅伸縮潛望觀測兜帽": "Capucha de Observación Periscópica Telescópica",
        "晨曦禮賓防風呢絨斗篷披肩": "Capa de Paño de Gala del Alba",
        "雙聯潛望測距石英凸透鏡": "Lentes Biconvexas de Cuarzo Periscópicas",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"File not found: {ui_path}")
        continue
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v in entries.items():
        if k not in data:
            data[k] = v
            added += 1
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {loc}/ui.json，新增 {added} 條目")
