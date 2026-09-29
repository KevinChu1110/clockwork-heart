#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

LEMUR_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_lemur_orbit_polymer_default",
        "name": "星穹輕量聚合物高機動底盤",
        "tier": "common",
        "race": "lemur"
    },
    "head_unit": {
        "id": "head_lemur_orbit_radar_cowl",
        "name": "星軌冷光雷達耳罩面甲",
        "tier": "common",
        "race": "lemur"
    },
    "winding_key": {
        "id": "key_lemur_tri_ring_orbit_brass",
        "name": "三環軌道星環黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_lemur_astro_stealth_harness",
        "name": "宇航匿蹤輕量安全吊帶胸甲",
        "tier": "common",
        "race": "lemur"
    },
    "optic_core": {
        "id": "face_lemur_amber_pulsar_visors",
        "name": "琥珀脈衝星穹雙目鏡",
        "tier": "common",
        "race": "lemur"
    },
    "weapon": {
        "id": "weapon_lemur_orbital_pulse_daggers",
        "name": "星軌脈衝雙鋒短匕",
        "tier": "common",
        "weapon_type": "dagger"
    },
    "back_curio": {
        "id": "curio_lemur_neon_ring_fiber_tail",
        "name": "多節霓光光纖星環天線尾",
        "tier": "common",
        "race": "lemur"
    }
}

LEMUR_RACE_SPEC = {
    "race_id": "lemur",
    "aliases": [
        "star_ring_lemur",
        "orbit_lemur",
        "ringtail_lemur",
        "clockwork_lemur",
        "pulse_lemur"
    ],
    "name_zh": "星環狐猴",
    "name_en": "The Star-Ring Lemur",
    "class_archetype": "忍者 (Ninja)",
    "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
    "lore_anchor": "穿行於星穹軌道·外星基地「高光懸空螢光軌道」、「太陽能帆板與微型排氣天線」與「太空拼裝維修船塢」，巡檢「聚合物太空艙模組」、「失重慣性磁力捕捉網」與「高真空抗靜電除塵室」，駐守「高壓地熱升空彈射井·軌道受壓對接艙」與「垂直磁浮天軌·星穹軌道月台」，在太空船塢更換特種全氟聚醚耐低溫潤滑油，結伴螺栓隊長、萊卡波波與光纖婆婆，庇護組裝式宇航機器人、太空發條小狗與螢光軌道維護偶；通體覆蓋高抗衝擊工程聚合物塑料底盤與象牙白防滑襯板、星軌冷光雷達耳罩面甲、琥珀脈衝星穹雙目鏡、宇航匿蹤輕量安全吊帶胸甲、多節霓光光纖星環天線尾、三環軌道星環黃銅發條鑰匙，雙持專屬星軌脈衝雙鋒短匕，以2.2頭身輕巧機動體態、掌底矽膠吸附踏步、失重微氣反推向量折返與近戰雙刃死角背刺見長的星穹軌道匿蹤忍者",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1960s-1980s 太空時代發條翻滾玩偶與科幻組裝微縮偶)",
        "posture": "2.2 頭身矮萌輕巧身軀微屈膝靈動站姿，雙腳矽膠吸盤穩踏地面，右手反握主鋒匕橫於胸前，左手副匕微屈護胸，身後光纖星環長尾優雅高翹，背後三環發條鑰匙隨星穹秒針每3.0秒鐘鳴一格勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "ears": "半透明高透聚碳酸酯冷光雷達耳罩，邊緣流動薄荷綠光纖微光，耳根嵌黃銅微型轉軸",
        "eyes": "雙聯球形高透聚碳酸酯太空泡罩目鏡，深藍紫金屬眼圈，浮現落日暖橘脈衝雷達刻線",
        "tail": "七節同軸深空消光黑曜與薄荷綠冷光光纖星環天線尾，末端安裝金黃微型全向天線球",
        "torso_and_limbs": "象牙白高強度工程聚合物塑料外殼，關節為自潤滑尼龍球鉸，雙手掌底與足底嵌導電矽膠吸附墊",
        "key": "三環軌道同心嵌套星環黃銅發條鑰匙，中心飾有多巴胺珊瑚粉防塵鉚釘"
    },
    "color_palette": {
        "primary": "#FFFDF8 (象牙白高抗衝擊聚合物板件)",
        "secondary": "#38A0FF (多巴胺天藍宇航吊帶胸甲與短匕刃身)",
        "accent_mint": "#4ED86A (薄荷綠冷光光纖尾環與雷達飾圈)",
        "accent_gold": "#FFD028 (金黃星環發條鑰匙與天線姿態球)",
        "accent_orange": "#FFA010 (落日暖橘琥珀目鏡與反光警示條)",
        "accent_pink": "#FF5E8A (珊瑚粉防塵鉚釘與減震密封膠圈)",
        "dark_polymer": "#1A243B (深空消光星夜藍黑聚合物尾環)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "default_items": {
        "chassis": "chassis_lemur_orbit_polymer_default",
        "head_unit": "head_lemur_orbit_radar_cowl",
        "optic_core": "face_lemur_amber_pulsar_visors",
        "costume": "costume_lemur_astro_stealth_harness",
        "back_curio": "curio_lemur_neon_ring_fiber_tail",
        "winding_key": "key_lemur_tri_ring_orbit_brass",
        "weapon": "weapon_lemur_orbital_pulse_daggers"
    }
}

if __name__ == "__main__":
    print("Star-Ring Lemur (Race 64) proposal template ready.")
