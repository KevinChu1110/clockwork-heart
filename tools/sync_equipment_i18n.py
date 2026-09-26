import json
import os

# 44 bases from equipment.json + existing keys (微末之刃, 鏽劍, 銹劍, 空手)
EQUIPMENT_TRANSLATIONS = {
    # ── 1. 既有三項（不得重做，嚴格維持既有譯名）──
    "鏽劍": {
        "zh_TW": "鏽劍",
        "zh_CN": "锈剑",
        "en": "Rusty Sword",
        "ja": "錆びた剣",
        "ko": "녹슨 검",
        "es": "Espada oxidada"
    },
    "銹劍": {
        "zh_TW": "銹劍",
        "zh_CN": "锈剑",
        "en": "Rusty Sword",
        "ja": "錆びた剣",
        "ko": "녹슨 검",
        "es": "Espada oxidada"
    },
    "微末之刃": {
        "zh_TW": "微末之刃",
        "zh_CN": "微末之刃",
        "en": "Meager Edge",
        "ja": "微末の刃",
        "ko": "미말의 칼날",
        "es": "Filo Ínfimo"
    },
    "空手": {
        "zh_TW": "空手",
        "zh_CN": "空手",
        "en": "Bare hands",
        "ja": "素手",
        "ko": "맨손",
        "es": "Manos vacías"
    },

    # ── 2. 武器類（缺譯補齊）──
    "騎士軍刀": {
        "zh_TW": "騎士軍刀",
        "zh_CN": "骑士军刀",
        "en": "Knight's Saber",
        "ja": "騎士の軍刀",
        "ko": "기사의 군도",
        "es": "Sable de caballero"
    },
    "疾風刃": {
        "zh_TW": "疾風刃",
        "zh_CN": "疾风刃",
        "en": "Gale Edge",
        "ja": "疾風の刃",
        "ko": "질풍의 칼날",
        "es": "Filo del vendaval"
    },
    "晨光長劍": {
        "zh_TW": "晨光長劍",
        "zh_CN": "晨光长剑",
        "en": "Dawn Blade",
        "ja": "暁光の長剣",
        "ko": "여명의 장검",
        "es": "Espada del alba"
    },
    "蘆風短弓": {
        "zh_TW": "蘆風短弓",
        "zh_CN": "芦风短弓",
        "en": "Reed Shortbow",
        "ja": "芦風の短弓",
        "ko": "갈대바람 단궁",
        "es": "Arco corto de caña"
    },
    "鷹眼長弓": {
        "zh_TW": "鷹眼長弓",
        "zh_CN": "鹰眼长弓",
        "en": "Hawkeye Longbow",
        "ja": "鷹目の長弓",
        "ko": "매의 눈 장궁",
        "es": "Arco largo de halcón"
    },
    "星屑短杖": {
        "zh_TW": "星屑短杖",
        "zh_CN": "星屑短杖",
        "en": "Stardust Wand",
        "ja": "星屑の短杖",
        "ko": "별빛가루 단봉",
        "es": "Vara de polvo estelar"
    },
    "星牙短匕": {
        "zh_TW": "星牙短匕",
        "zh_CN": "星牙短匕",
        "en": "Starfang Dagger",
        "ja": "星牙の短剣",
        "ko": "별송곳니 단도",
        "es": "Daga colmillo estelar"
    },
    "星雲細針": {
        "zh_TW": "星雲細針",
        "zh_CN": "星云细针",
        "en": "Nebula Needle",
        "ja": "星雲の細針",
        "ko": "성운의 바늘",
        "es": "Aguja de nébula"
    },
    "溢地獵爪": {
        "zh_TW": "溢地獵爪",
        "zh_CN": "溢地猎爪",
        "en": "Earthbound Talon",
        "ja": "溢地の猟爪",
        "ko": "일지의 사냥발톱",
        "es": "Garra de caza terrenal"
    },
    "虛空羽鋒": {
        "zh_TW": "虛空羽鋒",
        "zh_CN": "虚空羽锋",
        "en": "Void Quillblade",
        "ja": "虚空の羽鋒",
        "ko": "허공의 깃날",
        "es": "Pluma del vacío"
    },
    "練拳綁帶": {
        "zh_TW": "練拳綁帶",
        "zh_CN": "练拳绑带",
        "en": "Training Wraps",
        "ja": "鍛錬の拳帯",
        "ko": "수련용 붕대",
        "es": "Vendas de entrenamiento"
    },
    "鐵節拳套": {
        "zh_TW": "鐵節拳套",
        "zh_CN": "铁节拳套",
        "en": "Iron Knuckles",
        "ja": "鉄節ナックル",
        "ko": "무쇠 너클",
        "es": "Puños de hierro"
    },
    "缺刃手斧": {
        "zh_TW": "缺刃手斧",
        "zh_CN": "缺刃手斧",
        "en": "Notched Hatchet",
        "ja": "刃こぼれの手斧",
        "ko": "이 빠진 손도끼",
        "es": "Hacha mellada"
    },
    "裂山巨斧": {
        "zh_TW": "裂山巨斧",
        "zh_CN": "裂山巨斧",
        "en": "Mountain Splitter",
        "ja": "裂山の大斧",
        "ko": "열산의 거대도끼",
        "es": "Gran hacha hendemontes"
    },
    "砧心小鎚": {
        "zh_TW": "砧心小鎚",
        "zh_CN": "砧心小锤",
        "en": "Anvil Heart Mallet",
        "ja": "砧心の小槌",
        "ko": "모루심 작은망치",
        "es": "Martillo de yunque"
    },
    "鐵骨重棒": {
        "zh_TW": "鐵骨重棒",
        "zh_CN": "铁骨重棒",
        "en": "Ironbone Club",
        "ja": "鉄骨の重棍",
        "ko": "철골 중곤",
        "es": "Maza de hueso de hierro"
    },
    "壁壘厚刃": {
        "zh_TW": "壁壘厚刃",
        "zh_CN": "壁垒厚刃",
        "en": "Bastion Cleaver",
        "ja": "城壁の厚刃",
        "ko": "보루의 후인",
        "es": "Filo del bastión"
    },
    "錨心戰斧": {
        "zh_TW": "錨心戰斧",
        "zh_CN": "锚心战斧",
        "en": "Anchor Battleaxe",
        "ja": "錨心の戦斧",
        "ko": "닻심 전투도끼",
        "es": "Hacha de guerra de ancla"
    },
    "灰木長槍": {
        "zh_TW": "灰木長槍",
        "zh_CN": "灰木长枪",
        "en": "Ashwood Spear",
        "ja": "灰木の長槍",
        "ko": "물푸레 창",
        "es": "Lanza de fresno"
    },
    "騎士長矛": {
        "zh_TW": "騎士長矛",
        "zh_CN": "骑士长矛",
        "en": "Knight's Pike",
        "ja": "騎士の長矛",
        "ko": "기사의 장창",
        "es": "Pica de caballero"
    },
    "燧發火銃": {
        "zh_TW": "燧發火銃",
        "zh_CN": "燧发火铳",
        "en": "Flintlock Musket",
        "ja": "火打石の銃",
        "ko": "플린트락 총",
        "es": "Mosquete de chispa"
    },
    "黑火長銃": {
        "zh_TW": "黑火長銃",
        "zh_CN": "黑火长銃",
        "en": "Blackpowder Rifle",
        "ja": "黒色火薬の長銃",
        "ko": "흑색화약 소총",
        "es": "Rifle de pólvora negra"
    },
    "霧隱手鏢": {
        "zh_TW": "霧隱手鏢",
        "zh_CN": "雾隐手镖",
        "en": "Mist Darts",
        "ja": "霧隠れの手裏剣",
        "ko": "안개 표창",
        "es": "Dardos de niebla"
    },
    "影環飛刃": {
        "zh_TW": "影環飛刃",
        "zh_CN": "影环飞刃",
        "en": "Shadow Chakram",
        "ja": "影輪の飛刃",
        "ko": "그림자 고리날",
        "es": "Chakram sombrío"
    },
    "碎晶聚能": {
        "zh_TW": "碎晶聚能",
        "zh_CN": "碎晶聚能",
        "en": "Shard Focus",
        "ja": "砕晶の集束器",
        "ko": "수정 파편 집속기",
        "es": "Foco de esquirlas"
    },
    "棱鏡權杖": {
        "zh_TW": "棱鏡權杖",
        "zh_CN": "棱镜权杖",
        "en": "Prism Scepter",
        "ja": "プリズムの笏",
        "ko": "프리즘 홀",
        "es": "Cetro de prisma"
    },

    # ── 3. 防具類（缺譯補齊）──
    "灰燼甲片": {
        "zh_TW": "灰燼甲片",
        "zh_CN": "灰烬甲片",
        "en": "Ash Scale Mail",
        "ja": "灰のスケイルメイル",
        "ko": "잿빛 비늘갑옷",
        "es": "Malla de ceniza"
    },
    "騎士殘甲": {
        "zh_TW": "騎士殘甲",
        "zh_CN": "骑士残甲",
        "en": "Knight's Scrap Plate",
        "ja": "騎士の残甲",
        "ko": "기사의 잔갑옷",
        "es": "Placa de caballero"
    },
    "北境獸甲": {
        "zh_TW": "北境獸甲",
        "zh_CN": "北境兽甲",
        "en": "Northbound Beast Hide",
        "ja": "北境の獣甲",
        "ko": "북방 야수갑옷",
        "es": "Coraza de bestia del norte"
    },
    "霧隱夜衣": {
        "zh_TW": "霧隱夜衣",
        "zh_CN": "雾隐夜衣",
        "en": "Mist Shadow Garb",
        "ja": "霧隠れの夜装",
        "ko": "안개 닌자복",
        "es": "Ropaje nocturno de niebla"
    },
    "道場練衣": {
        "zh_TW": "道場練衣",
        "zh_CN": "道场练衣",
        "en": "Dojo Gi",
        "ja": "道場の道着",
        "ko": "도장 수련복",
        "es": "Gi de entrenamiento"
    },
    "星紗披風": {
        "zh_TW": "星紗披風",
        "zh_CN": "星纱披风",
        "en": "Starveil Cloak",
        "ja": "星紗のマント",
        "ko": "별빛 베일 망토",
        "es": "Capa de velo estelar"
    },
    "遊俠鉚甲": {
        "zh_TW": "遊俠鉚甲",
        "zh_CN": "游侠铆甲",
        "en": "Ranger Studded Leather",
        "ja": "レンジャーの鋲革鎧",
        "ko": "방랑자 징박힌 가죽갑옷",
        "es": "Cuero tachonado de montaraz"
    },

    # ── 4. 飾品類（缺譯補齊）──
    "星屑墜": {
        "zh_TW": "星屑墜",
        "zh_CN": "星屑坠",
        "en": "Stardust Pendant",
        "ja": "星屑のペンダント",
        "ko": "별빛가루 펜던트",
        "es": "Colgante de polvo estelar"
    },
    "橡心符": {
        "zh_TW": "橡心符",
        "zh_CN": "橡心符",
        "en": "Oakheart Charm",
        "ja": "オークハートの護符",
        "ko": "참나무 심장 부적",
        "es": "Amuleto de corazón de roble"
    },
    "鋒勢指環": {
        "zh_TW": "鋒勢指環",
        "zh_CN": "锋势指环",
        "en": "Bladestance Ring",
        "ja": "鋭刃の指輪",
        "ko": "검세의 반지",
        "es": "Anillo de filo"
    },
    "霧晶耳環": {
        "zh_TW": "霧晶耳環",
        "zh_CN": "雾晶耳环",
        "en": "Mist Crystal Earring",
        "ja": "霧晶のピアス",
        "ko": "안개수정 귀걸이",
        "es": "Pendiente de cristal de niebla"
    },
    "潮貝手環": {
        "zh_TW": "潮貝手環",
        "zh_CN": "潮贝手环",
        "en": "Tide Shell Bangle",
        "ja": "潮貝の腕輪",
        "ko": "조개 팔찌",
        "es": "Brazalete de concha marina"
    },
    "疤焰護符": {
        "zh_TW": "疤焰護符",
        "zh_CN": "疤焰护符",
        "en": "Scarfire Amulet",
        "ja": "傷痕の炎護符",
        "ko": "흉터불꽃 호신부",
        "es": "Amuleto de fuego cicatrizante"
    },
    "騎士腰帶": {
        "zh_TW": "騎士腰帶",
        "zh_CN": "骑士腰带",
        "en": "Knight's Belt",
        "ja": "騎士のベルト",
        "ko": "기사의 벨트",
        "es": "Cinturón de caballero"
    },
    "狼牙戒指": {
        "zh_TW": "狼牙戒指",
        "zh_CN": "狼牙戒指",
        "en": "Wolf Fang Ring",
        "ja": "狼牙の指輪",
        "ko": "늑대송곳니 반지",
        "es": "Anillo de colmillo de lobo"
    },
    "翠玉項鍊": {
        "zh_TW": "翠玉項鍊",
        "zh_CN": "翠玉项链",
        "en": "Jade Necklace",
        "ja": "翠玉のネックレス",
        "ko": "비취 목걸이",
        "es": "Collar de jade"
    }
}

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

def update_json_file(file_path, new_entries):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
    
    changed = False
    for k, v in new_entries.items():
        if data.get(k) != v:
            data[k] = v
            changed = True
            
    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  Updated: {file_path} (+{len(new_entries)} entries)")
    else:
        print(f"  Unchanged: {file_path}")

def main():
    print(f"Syncing {len(EQUIPMENT_TRANSLATIONS)} equipment entries across 6 locales...")
    
    # 1. Update game/data/i18n/content/{locale}/weapon.json
    for loc in LOCALES:
        p_weapon = f"game/data/i18n/content/{loc}/weapon.json"
        loc_entries = {k: trans[loc] for k, trans in EQUIPMENT_TRANSLATIONS.items()}
        update_json_file(p_weapon, loc_entries)

    # 2. Update game/data/i18n/content/{locale}/ui.json
    for loc in LOCALES:
        p_ui = f"game/data/i18n/content/{loc}/ui.json"
        loc_entries = {k: trans[loc] for k, trans in EQUIPMENT_TRANSLATIONS.items()}
        update_json_file(p_ui, loc_entries)

    # 3. Update game/data/i18n/{locale}.json
    for loc in LOCALES:
        p_root = f"game/data/i18n/{loc}.json"
        loc_entries = {k: trans[loc] for k, trans in EQUIPMENT_TRANSLATIONS.items()}
        update_json_file(p_root, loc_entries)

    print("Sync complete.")

if __name__ == "__main__":
    main()
