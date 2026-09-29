#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

MARMOT_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_marmot_quarry_tinplate_default",
        "name": "碎石耐磨馬口鐵底盤",
        "tier": "common",
        "race": "marmot"
    },
    "head_unit": {
        "id": "head_marmot_alloy_chisel_visor",
        "name": "雙聯合金鑿齒護目面罩",
        "tier": "common",
        "race": "marmot"
    },
    "winding_key": {
        "id": "key_marmot_dual_pawl_brass",
        "name": "雙向棘爪減速黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_marmot_scavenger_canvas_harness",
        "name": "舊庫拾荒加固帆布工裝胸甲",
        "tier": "common",
        "race": "marmot"
    },
    "optic_core": {
        "id": "face_marmot_amber_dust_goggles",
        "name": "雙聯琥珀防塵石英風鏡",
        "tier": "common",
        "race": "marmot"
    },
    "weapon": {
        "id": "weapon_marmot_eccentric_piston_fists",
        "name": "廢土偏心衝壓機關拳套",
        "tier": "common",
        "weapon_type": "fist"
    },
    "back_curio": {
        "id": "curio_marmot_pneumatic_sand_tail",
        "name": "減震氣動平衡排砂尾",
        "tier": "common",
        "race": "marmot"
    }
}

MARMOT_RACE_SPEC = {
    "race_id": "marmot",
    "aliases": [
        "rockbreaker_marmot",
        "quarry_marmot",
        "piston_marmot",
        "clockwork_marmot",
        "dune_groundhog"
    ],
    "name_zh": "碎石旱獺",
    "name_en": "The Rockbreaker Marmot",
    "class_archetype": "武術家 (Monk)",
    "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
    "lore_anchor": "穿行於荒漠齒輪塚·遺忘舊庫「巨型零件殘骸沙丘」、「零件分揀斜坡裂谷」與「拾荒拼裝聚落·齒輪營地」，巡檢「舊庫重型吊裝龍門架」、「大齒輪懸索天梯·舊庫總站」與「高溫蒸氣除鏽清洗槽」，駐守「冷卻熔渣重力傾卸滑道·舊庫受料口」與「軌道廢棄排障滑道·舊庫分揀倉」，在齒輪營地熬製塗抹高黏度抗氧化除鏽潤滑脂，結伴補丁爺爺、鏽刃阿席與鈴鐺嘟嘟，庇護拾荒拼裝布偶、生鏽發條浪人與發條除鏽工兵偶；通體覆蓋沖壓耐磨馬口鐵底盤與奶油米白隔震襯板、雙聯合金鑿齒護目面罩、雙聯琥珀防塵石英風鏡、舊庫拾荒加固帆布工裝胸甲、減震氣動平衡排砂尾、雙向棘爪減速黃銅發條鑰匙，雙手佩戴專屬廢土偏心衝壓機關拳套，以2.2頭身矮萌扎實身軀、足底黃銅鉚釘扎根步法、偏心連桿高頻活塞衝程與貼身近戰寸勁連打破勢見長的荒原破障武術家",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 昭和發條鐵皮拳擊偶與敲打地鼠自動機)",
        "posture": "2.2 頭身矮萌結實身軀扎馬步抱樁微屈膝，雙足黃銅抓地鉚釘穩踏地面，雙拳佩戴偏心衝壓拳套一前一後微動抱架於胸前，短尾平置地面輔助支撐，背後雙向棘爪發條鑰匙隨舊庫秒針每2.5~3.5秒金屬摩擦聲『喀——嚓！』勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 540
    },
    "mechanical_features": {
        "ears": "小巧半球形黃銅受音碗耳罩，邊緣飾以微型散熱通風孔，耳根嵌鉚釘固定座",
        "eyes": "雙聯大尺寸琥珀防塵石英風鏡，深藍紫金屬密封圈，浮現落日暖橘同心圓測距刻度與發光指針",
        "teeth": "下顎突出雙聯冷軋沖壓黃銅開山鑿齒，厚度6mm，專門鑿碎卡死齒輪之硬質鏽斑與沉積石塊",
        "tail": "圓柱形短促生鐵馬口鐵排砂尾，內置氣動減震氣缸與旋風排砂濾網，末端飾薄荷綠指示環",
        "torso_and_limbs": "生鐵青灰耐磨馬口鐵沖壓外殼，冷軋鎢鋼自潤滑球鉸關節，雙足底各嵌三枚黃銅圓頭抓地鉚釘",
        "key": "雙向棘爪減速重型黃銅發條鑰匙，外緣帶齒輪棘齒，中心飾有多巴胺珊瑚粉防震鉚釘"
    },
    "color_palette": {
        "primary": "#5A6E7F (生鐵青灰沖壓耐磨馬口鐵板件)",
        "secondary": "#FFFDF8 (奶油米白腹部抗衝擊隔震襯板與面罩高光)",
        "accent_orange": "#FFA010 (多巴胺落日暖橘衝壓活塞筒身與胸甲警示斜紋)",
        "accent_gold": "#FFD028 (多巴胺天元金黃雙向棘爪發條鑰匙與開山鑿齒)",
        "accent_mint": "#4ED86A (多巴胺薄荷綠氣動壓力表與排砂尾指示環)",
        "accent_blue": "#38A0FF (多巴胺天藍胸甲金屬快拆卡扣與護腕消震墊)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與減震膠圈)",
        "canvas_tan": "#D49B4B (舊庫拾荒斑駁耐磨粗帆布工裝胸甲底色)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "default_items": {
        "chassis": "chassis_marmot_quarry_tinplate_default",
        "head_unit": "head_marmot_alloy_chisel_visor",
        "optic_core": "face_marmot_amber_dust_goggles",
        "costume": "costume_marmot_scavenger_canvas_harness",
        "back_curio": "curio_marmot_pneumatic_sand_tail",
        "winding_key": "key_marmot_dual_pawl_brass",
        "weapon": "weapon_marmot_eccentric_piston_fists"
    }
}

if __name__ == "__main__":
    print("Rockbreaker Marmot (Race 65) proposal template ready.")
