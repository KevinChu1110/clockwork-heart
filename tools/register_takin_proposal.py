#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

TAKIN_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_takin_bronze_cast_default",
        "name": "青古銅鑄鐵重裝底盤",
        "tier": "common",
        "race": "takin"
    },
    "head_unit": {
        "id": "head_takin_brass_twisted_horn_cowl",
        "name": "黃銅反曲扭角重盔",
        "tier": "common",
        "race": "takin"
    },
    "winding_key": {
        "id": "key_takin_tri_leaf_zen_brass",
        "name": "三葉天元雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_takin_zen_pioneer_heavy_robe",
        "name": "天元拓荒道袍重肩甲",
        "tier": "common",
        "race": "takin"
    },
    "optic_core": {
        "id": "face_takin_emerald_quartz_visors",
        "name": "翡翠石英耐震雙目鏡",
        "tier": "common",
        "race": "takin"
    },
    "weapon": {
        "id": "weapon_takin_zen_bamboo_cleaving_axe",
        "name": "天元破竹開山巨斧",
        "tier": "common",
        "weapon_type": "axe"
    },
    "back_curio": {
        "id": "curio_takin_dual_bamboo_oil_flasks",
        "name": "雙聯竹露油壺減震閥",
        "tier": "common",
        "race": "takin"
    }
}

TAKIN_RACE_SPEC = {
    "race_id": "takin",
    "aliases": [
        "bamboo_cleaving_takin",
        "zen_takin",
        "clockwork_takin",
        "golden_takin",
        "mountain_takin"
    ],
    "name_zh": "破竹羚牛",
    "name_en": "The Bamboo-Cleaving Takin",
    "class_archetype": "戰士 (Viking)",
    "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
    "lore_anchor": "駐守於竹影道場·天元竹林「青石武鬥古道場·演武坪」，穿行於「發條天元竹海」與「飛瀑木簧水碓」之間，仰望「凌雲青竹懸索天梯·道場總站」與「晨曦天軌 9 號演武道場月台」，巡檢「古老重型零件輸送翻斗軌道·竹林終端站」與「翠竹彈力阻尼編織網」，在「山門竹煙茶舍」飲用清香竹露潤滑油保養軸承，結伴圓空師傅、煮茶偶阿茶與木人小師弟木木，庇護陶瓷熊貓武僧、木雕竹葉青蛇與演武木人童子；通體覆蓋沖壓青古銅鑄鐵合金底盤與象牙白瓷護腹板、雙聯鍛造黃銅反曲扭角重盔、翡翠石英耐震雙目鏡、天元拓荒道袍重肩甲、雙聯竹露油壺減震閥、三葉天元雕花黃銅發條鑰匙，右手單持專屬天元破竹開山巨斧，以2.2頭身矮萌厚重體態、扎實青石蹄踏步、霸體蓄力開山重劈見長的天元竹林守護戰士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1920s-1950s 經典古典發條鐵皮重獸偶與東方機巧榫卯自動偶)",
        "posture": "2.2 頭身矮萌重裝身軀微側30度穩重扎馬站姿，雙蹄穩踏地面，右手單持雙刃戰斧斜立於身側，左臂曲於胸前呈厚重防禦架勢，背後三葉發條鑰匙隨竹林秒針每3.0秒鐘鳴一格勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 560
    },
    "mechanical_features": {
        "horns": "雙聯鍛造高光黃銅反曲扭角，角尖微向上翹，刻有同心圓加強肋線，隨步伐微幅震動",
        "face": "沖壓青鋼防塵面甲，雙頰鑲嵌光滑黃銅咬合齒輪，半球形高透耐震翡翠石英雙目鏡",
        "torso_and_limbs": "青古銅鑄鐵合金厚重底盤，胸腹鑲嵌溫潤象牙白生漆陶瓷板，四肢為球形轉向鉸鏈配防滑青石蹄",
        "venting": "背部左右雙聯耐壓玻璃竹露油壺，中央連通微型水碓氣動排氣減震閥門",
        "key": "三葉天元祥雲雕花黃銅發條鑰匙，中心飾有珊瑚粉防震鉚釘"
    },
    "color_palette": {
        "primary": "#FFFDF8 (奶油白陶瓷生漆胸腹板與道袍)",
        "secondary": "#4ED86A (多巴胺薄荷綠板件烤漆邊與翡翠石英目鏡)",
        "accent_gold": "#FFD028 (天元金黃雙扭角、發條鑰匙與戰斧雕花)",
        "accent_orange": "#FFA010 (落日暖橘道袍防磨滾邊)",
        "dark_bronze": "#3A4454 (青古銅鑄鐵厚重板件底盤)",
        "accent_pink": "#FF5E8A (珊瑚粉防震鉚釘與油壺浮標)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "default_items": {
        "chassis": "chassis_takin_bronze_cast_default",
        "head_unit": "head_takin_brass_twisted_horn_cowl",
        "optic_core": "face_takin_emerald_quartz_visors",
        "costume": "costume_takin_zen_pioneer_heavy_robe",
        "back_curio": "curio_takin_dual_bamboo_oil_flasks",
        "winding_key": "key_takin_tri_leaf_zen_brass",
        "weapon": "weapon_takin_zen_bamboo_cleaving_axe"
    }
}

if __name__ == "__main__":
    print("Takin specification template ready.")
