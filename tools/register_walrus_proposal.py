#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

WALRUS_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_walrus_icebreaker_alloy_default",
        "name": "深淵耐壓鍍鈦合金底盤",
        "tier": "common",
        "race": "walrus"
    },
    "head_unit": {
        "id": "head_walrus_tungsten_tusk_cowl",
        "name": "雙聯鎢鋼破冰長牙面罩",
        "tier": "common",
        "race": "walrus"
    },
    "winding_key": {
        "id": "key_walrus_anchor_handwheel_brass",
        "name": "雙葉海錨輪轂黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_walrus_abyssal_peacoat_cuirass",
        "name": "深淵領航雙排扣水手胸甲",
        "tier": "common",
        "race": "walrus"
    },
    "optic_core": {
        "id": "face_walrus_quartz_dome_eyes",
        "name": "雙聯耐壓石英泡罩目鏡",
        "tier": "common",
        "race": "walrus"
    },
    "weapon": {
        "id": "weapon_walrus_abyssal_icebreaker_cutlass",
        "name": "深淵破冰海軍短闊劍",
        "tier": "common",
        "weapon_type": "sword"
    },
    "back_curio": {
        "id": "curio_walrus_dual_ballast_tanks",
        "name": "雙聯減壓壓載氣箱與防鏽油壺",
        "tier": "common",
        "race": "walrus"
    }
}

WALRUS_RACE_SPEC = {
    "race_id": "walrus",
    "aliases": [
        "icebreaker_walrus",
        "deepsea_walrus",
        "clockwork_walrus",
        "trench_walrus",
        "abyssal_walrus"
    ],
    "name_zh": "破冰海象",
    "name_en": "The Icebreaker Walrus",
    "class_archetype": "騎士 (Knight)",
    "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
    "lore_anchor": "駐守於琉璃汪洋·發條海淵「海淵地表與馬賽克步道」，穿行於「發條珊瑚群」與「水下發條宮殿與氧氣泡罩」之間，仰望「深淵排污豎井管道·耐壓吊籠」與「晨曦天軌 5 號深海浮標月台」，巡檢「深海熱液湧泉管道」與「環域水幕磁阻防護波」，在「海底防鏽超聲油壓艙」保養氣密艙體，結伴舵手巴克、信差碧浪，庇護發條熱帶魚、橡皮小黃鴨船長與發條海馬信差；通體覆蓋沖壓耐壓鍍鈦合金底盤與象牙白瓷腹板、雙聯冷軋鎢鋼破冰鑿長牙面罩、耐壓深海石英泡罩目鏡、深淵領航雙排扣水手胸甲、雙聯減壓壓載氣箱與防鏽油壺、雙葉海錨輪轂黃銅發條鑰匙，右手單持專屬深淵破冰海軍短闊劍，以2.2頭身矮萌圓滾體態、厚實腳蹼踏步、深海水壓阻尼格擋與破冰重刃下劈破陣見長的深海守護騎士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1920s-1950s 歐洲古典發條鐵皮海象偶與維多利亞深潛鐘自動偶)",
        "posture": "2.2 頭身矮萌身軀微側30度穩重海床站姿，雙蹼穩踏地面，右手單持短闊劍斜立於胸前，雙聯鎢鋼長牙微張，背後海錨發條鑰匙隨海淵秒針每3~4秒划動一格勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 560
    },
    "mechanical_features": {
        "head_and_neck": "深潛鐘圓弧造型耐壓面罩配雙聯冷軋鎢鋼破冰鑿長牙（#FFD028 / #38A0FF），口鼻排列八聯柔性黃銅聲納探針天線鬚，兩腮鑲嵌溫潤象牙白瓷板（#FFFDF8）",
        "ears": "無外耳，以兩側微型耐壓氣閥與旋轉螺栓替代，隨洋流微波調節艙體內外氣壓平衡",
        "torso_and_limbs": "沖壓厚鑄耐壓鍍鈦合金板件與鎢鋼骨架外殼，胸腹鑲嵌象牙白瓷護板，前鰭短粗圓潤配耐磨橡膠防滑抓握墊，後鰭為流線型金屬游動舵板",
        "tail": "扇形金屬導流板小短尾，配合減壓排氣提供流體航行配重平衡",
        "weapon_system": "右手單持專屬「深淵破冰海軍短闊劍（Abyssal Icebreaker Cutlass）」，厚背鋸齒排水槽配半球形雕花黃銅海軍護手，底層掛載 equipment.json 既有 clockwork_sword (tier 1)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白彩釉白瓷高光，腹部護板與面罩高光)",
        "primary": "#38A0FF (主色多巴胺天藍，水手胸甲主色、金屬腳蹼塗裝、短闊劍護手水流槽)",
        "secondary": "#FFD028 (次色多巴胺金黃，鎢鋼破冰鑿鍍金刻線、黃銅海錨鈕扣、銅絲聲納探針鬚、發條鑰匙)",
        "accent": "#FFA010 (點綴色多巴胺落日暖橘，水手翻領滾邊、氣壓表指針、壓載氣箱裝飾條)",
        "detail": "#4ED86A (細節色多巴胺薄荷淺綠，石英泡罩目鏡微光、磷光排氣微泡特效)",
        "metal": "#FF5E8A (金屬色多巴胺珊瑚粉，發條鑰匙中心鉚釘、防鏽油壺密封圈)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_walrus.png (品牌形象立牌)",
                "web/media/hero/char_walrus.png (官網英雄展示立繪)",
                "docs/art/icebreaker_walrus_concept.png (概念立繪)",
                "game/assets/sprites/player/walrus_idle.png (64x64 待機)",
                "game/assets/sprites/player/walrus_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/walrus_idle.png (隊伍待機)",
                "web/media/hero/walrus_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/walrus_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/walrus_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/walrus_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/walrus_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/walrus_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/walrus_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/walrus/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/walrus.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/walrus_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/icebreaker_walrus.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/walrus/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_walrus.png (560x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/icebreaker_walrus_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_walrus.png (560x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/walrus_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/walrus_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/walrus_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/walrus_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/walrus_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/walrus_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/walrus_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/walrus/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/walrus.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/icebreaker_walrus.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/walrus/{slot_id}/{item_id}.png [待產出]"
    }
}

if __name__ == "__main__":
    print("Walrus proposal registered specification ready.")
