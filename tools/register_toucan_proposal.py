#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

TOUCAN_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_toucan_canopy_alloy_default",
        "name": "林冠輕量化合金素體底盤",
        "tier": "common",
        "race": "toucan"
    },
    "head_unit": {
        "id": "head_toucan_prism_bill_brass_cowl",
        "name": "彩晶折光巨嘴面罩",
        "tier": "common",
        "race": "toucan"
    },
    "winding_key": {
        "id": "key_toucan_canopy_rotor_brass",
        "name": "三葉林冠旋翼黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_toucan_vine_scout_harness",
        "name": "蔓谷探險巡林獵裝",
        "tier": "common",
        "race": "toucan"
    },
    "optic_core": {
        "id": "face_toucan_emerald_quartz_monocle",
        "name": "翡翠石英瞄準目鏡",
        "tier": "common",
        "race": "toucan"
    },
    "weapon": {
        "id": "weapon_toucan_canopy_prism_arquebus",
        "name": "林冠聚能氣動銃",
        "tier": "common",
        "weapon_type": "gun"
    },
    "back_curio": {
        "id": "curio_toucan_segmented_copper_rudder_tail",
        "name": "多節沖壓銅片導航尾翼",
        "tier": "common",
        "race": "toucan"
    }
}

TOUCAN_RACE_SPEC = {
    "race_id": "toucan",
    "aliases": [
        "prism_bill_toucan",
        "canopy_toucan",
        "clockwork_toucan",
        "emerald_toucan",
        "prism_toucan"
    ],
    "name_zh": "彩喙巨嘴鳥",
    "name_en": "The Prism-Bill Toucan",
    "class_archetype": "遊俠 (Ranger)",
    "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
    "lore_anchor": "駐守於翡翠深林·發條蔓谷「機械巨木」樹冠頂部觀測平台，穿行於「發條藤蔓」與「樹屋聚落」各樹冠平台，沐浴「丁達爾發條晨曦光斑」，仰望「高架重軌引橋·巨輪城站」與「赤焰索道懸橋」，巡檢「蔓谷天梯引道·深林站」與「晨曦天軌 3 號月台」，依託「防護金屬藤蔓彈力網」與「樹脂發光菌菇」，在「樹汁導流泵」前保養氣缸，結伴守林哨兵·風耳、靈尾工藝師·小鈴，庇護守林發條小鹿、發條松鼠信差與林木守護木偶；通體覆蓋沖壓雕花薄銅板合金底盤與象牙白瓷喉胸板、多層沖壓鏤空黃銅彩晶巨嘴面罩、翡翠石英瞄準目鏡、蔓谷探險巡林獵裝、折扇式沖壓薄銅板導航尾羽、三葉林冠旋翼黃銅發條鑰匙，右手單持專屬林冠聚能氣動銃，以2.2頭身矮萌微胖體態、粗壯黃銅三叉爪扣枝、林冠光學測距與遠距定點一響定生死見長的深林高空遊俠",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1910s-1930s 歐洲古典發條鐵皮鳥偶與維多利亞光學測候偶)",
        "posture": "2.2 頭身矮萌身軀微側30度高枝站姿，雙爪穩固扣握踏板，右手單持氣動火銃斜指前上方，左手托握護木，彩晶巨嘴前傾測距，背後三葉發條鑰匙隨深林秒針每3~4秒跳拍一格勻速自轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "沖壓薄銅板圓形頭盔配彩晶巨喙面罩（#FFD028 / #FFA010 / #4ED86A / #38A0FF），前額挺立沖壓薄銅板羽冠，兩腮鑲嵌溫潤象牙白瓷板（#FFFDF8），眼眶處鏤空透光",
        "ears": "無外耳，以頭頂三片分層沖壓薄銅板羽冠替代，隨林間微風與氣壓波動微幅彈動",
        "torso_and_limbs": "沖壓雕花薄銅板與輕量化合金骨架外殼，胸腹鑲嵌象牙白瓷喉胸襯板，雙足為粗壯精工黃銅三叉球窩鳥爪配耐磨橡膠防滑抓握墊",
        "tail": "折扇式沖壓薄銅板導航尾羽（#FFD028 / #38A0FF），三聯折扇式沖壓薄銅片以微型發條鉸鏈相連，提供跳躍氣動制動",
        "weapon_system": "右手單持專屬「林冠聚能氣動銃（Canopy Prism Pneumatic Arquebus）」，雕花長管配花瓣形洩壓制退器與側置轉輪發條供彈盤，底層掛載 equipment.json 既有 flint_gun (tier 1)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白彩釉白瓷高光，喉胸襯板與腹部高光)",
        "primary": "#FFD028 (主色多巴胺金黃，彩晶巨喙基底、三葉旋翼鑰匙、黃銅三叉鳥爪與銃身雕花)",
        "secondary": "#4ED86A (次色多巴胺薄荷淺綠，巡林工裝獵裝主色、頭頂羽冠、翡翠石英目鏡)",
        "accent": "#FFA010 (點綴色多巴胺落日暖橘，巨喙漸層中段、工裝防風滾邊、瞄準鏡十字光紋)",
        "detail": "#38A0FF (細節色多巴胺天藍，巨喙尖端彩釉、導航尾羽裝飾飾條、洩壓蒸氣微光)",
        "metal": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心鉚釘與彈匣包縫線標記)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_toucan.png (品牌形象立牌)",
                "web/media/hero/char_toucan.png (官網英雄展示立繪)",
                "docs/art/prism_bill_toucan_concept.png (概念立繪)",
                "game/assets/sprites/player/toucan_idle.png (64x64 待機)",
                "game/assets/sprites/player/toucan_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/toucan_idle.png (隊伍待機)",
                "web/media/hero/toucan_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/toucan_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/toucan_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/toucan_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/toucan_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/toucan_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/toucan_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/toucan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/toucan.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/toucan_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/prism_bill_toucan.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/toucan/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_toucan.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/prism_bill_toucan_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_toucan.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/toucan_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/toucan_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/toucan_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/toucan_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/toucan_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/toucan_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/toucan_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/toucan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/toucan.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/prism_bill_toucan.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/toucan/{slot_id}/{item_id}.png [待產出]"
    }
}

if __name__ == "__main__":
    print("Toucan proposal registered specification ready.")
