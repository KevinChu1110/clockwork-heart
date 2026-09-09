class_name PaperdollSelectDemo
extends Control
## 《發條之心》紙娃娃五族選角與即時換裝技術驗證面板 (PaperdollSelectDemo)
## 依據規格書 docs/design/paperdoll_slots.json 與手遊人體工學介面規範：
## 1. 橫向 5 大動物族縮圖按鈕（128x128 實體切片縮圖，按鈕熱區 180x108 >= 50px）。
## 2. 中央舞台顯示選取族系之 PaperdollCharacter 節點（7 大槽位疊合渲染）。
## 3. 部件槽即時換裝控制（外裝服飾 costume、機體塗裝 chassis 左右切換）。
## 4. 全程使用開源粉圓體 (OpenHuninn)，嚴禁系統 Emoji，多巴胺鮮亮高飽和配色。

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 規格書 (res://data/tables/paperdoll_slots.json) 官方部件名稱快取
static var _spec_variant_names: Dictionary = {}

static func _load_spec_names() -> void:
	if not _spec_variant_names.is_empty():
		return
	const SPEC_PATH := "res://data/tables/paperdoll_slots.json"
	if FileAccess.file_exists(SPEC_PATH):
		var file := FileAccess.open(SPEC_PATH, FileAccess.READ)
		if file != null:
			var json_str := file.get_as_text()
			var json = JSON.parse_string(json_str)
			if json is Dictionary and json.has("slots_architecture"):
				var slots: Array = json["slots_architecture"].get("slots", [])
				for slot in slots:
					var variants: Array = slot.get("sample_variants", [])
					for v in variants:
						var vid: String = str(v.get("id", ""))
						var vname: String = str(v.get("name", ""))
						if not vid.is_empty() and not vname.is_empty():
							_spec_variant_names[vid] = vname

static func get_variant_spec_name(id: String, fallback: String = "") -> String:
	_load_spec_names()
	if id == "none":
		return "無外裝 (裸機素體)"
	if _spec_variant_names.has(id):
		return str(_spec_variant_names[id])
	return fallback if not fallback.is_empty() else id

## 五大種族詳細設定與可用部件變體表
const RACES_DATA: Dictionary = {
	"rabbit": {
		"id": "rabbit",
		"name_zh": "兔 (小白)",
		"name_en": "Whitey",
		"archetype": "劍士 (knight)",
		"thumb": "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_rabbit_composite.png",
		"desc": "發條之心的守護象徵，身形輕巧，搭載高響應晨曦核心與剛性長耳。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "經典紅藍胡桃鉗金屬禮服與黃銅肩章"},
			{"id": "costume_steam_artisan", "name_zh": "蒸氣工匠吊帶工作裝", "desc": "耐磨工匠鍛鐵胸板與工具掛扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白精密機械軀體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "溫潤微光象牙白高光琺瑯塗層"},
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "古典黃銅金屬原色重拋光鏡面"}
		]
	},
	"fox": {
		"id": "fox",
		"name_zh": "狐",
		"name_en": "Fox",
		"archetype": "法師 (mage)",
		"thumb": "res://assets/sprites/player/paperdoll/fox/proof_paperdoll_fox_composite.png",
		"desc": "掌握星軌共鳴的靈動玩具法師，具備金屬雷達耳與分節發條尾。",
		"costumes": [
			{"id": "costume_astral_cape", "name_zh": "星紋見習占星斗篷", "desc": "深藍琺瑯釉面與星芒金屬扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現曜橙靈動狐型素體"}
		],
		"chassis": [
			{"id": "paint_fox_orange", "name_zh": "靈狐曜橙烤漆", "desc": "高飽和鮮明暖橘琺瑯烤漆"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "低調優雅素體象牙白烤漆"}
		]
	},
	"lion": {
		"id": "lion",
		"name_zh": "獅",
		"name_en": "Lion",
		"archetype": "騎士 (knight)",
		"thumb": "res://assets/sprites/player/paperdoll/lion/proof_paperdoll_lion_composite.png",
		"desc": "恪守騎士榮譽的黃銅機甲獅，配備金色板件鬃毛與折疊尾翼。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "典禮侍衛金屬胸甲與禮服分件"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現全黃銅厚重鍛造素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "皇家黃金尊貴拋光金屬外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "皇家象牙白紀念版典雅塗裝"}
		]
	},
	"boar": {
		"id": "boar",
		"name_zh": "野豬",
		"name_en": "Boar",
		"archetype": "戰士 (viking)",
		"thumb": "res://assets/sprites/player/paperdoll/boar/proof_paperdoll_boar_composite.png",
		"desc": "熔爐鐵匠鋪的重型開拓者，金屬鉚釘獠牙與強韌彈簧衝擊核心。",
		"costumes": [
			{"id": "costume_viking_harness", "name_zh": "粗獷鍛爐護胸皮帶", "desc": "鉚釘加固厚重鍛鐵戰士胸甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現剛硬生鐵鍛造衝擊素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "耐磨耐高溫黃銅金屬強化外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白抗衝擊塗裝"}
		]
	},
	"macaque": {
		"id": "macaque",
		"name_zh": "猴",
		"name_en": "Macaque",
		"archetype": "未定案",
		"thumb": "res://assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png",
		"desc": "敏捷靈活的彈簧行者，同軸金屬耳與伸縮爪刃，機巧多變。",
		"costumes": [
			{"id": "costume_dawn_monk_tunic", "name_zh": "晨曦行者武道短褂", "desc": "輕量合金武道短褂分件"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現極簡彈簧骨架素體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "高韌性象牙白減震琺瑯"}
		]
	}
}

const RACE_KEYS: Array[String] = ["rabbit", "fox", "lion", "boar", "macaque"]

## 節點引用
@onready var character: PaperdollCharacter = $CenterStage/CharacterContainer/PaperdollCharacter as PaperdollCharacter
@onready var race_buttons_container: HBoxContainer = $TopRaceBar/ButtonsHBox as HBoxContainer

@onready var hero_title_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroTitleLabel as Label
@onready var hero_archetype_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroArchetypeLabel as Label
@onready var hero_desc_label: Label = $CenterStage/DescPanel/HeroDescLabel as Label

@onready var costume_name_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeNameLabel as Label
@onready var costume_desc_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeDescLabel as Label
@onready var btn_costume_prev: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumePrev as Button
@onready var btn_costume_next: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumeNext as Button

@onready var chassis_name_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisNameLabel as Label
@onready var chassis_desc_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisDescLabel as Label
@onready var btn_chassis_prev: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisPrev as Button
@onready var btn_chassis_next: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisNext as Button

@onready var weapon_name_label: Label = $RightControlPanel/Margin/VBox/WeaponControl/WeaponDisplay/WeaponNameLabel as Label

@onready var slot_summary_label: Label = $RightControlPanel/Margin/VBox/StatusCard/SlotSummaryLabel as Label
@onready var btn_reset_default: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnResetDefault as Button
@onready var btn_capture_proof: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnCaptureProof as Button

## 執行期狀態
var _current_race_id: String = "rabbit"
var _costume_index: int = 0
var _chassis_index: int = 0
var _race_buttons: Dictionary = {}


func _ready() -> void:
	_init_race_buttons()
	_bind_controls()
	select_race("rabbit")


## 初始化橫向種族選擇按鈕
func _init_race_buttons() -> void:
	for rid in RACE_KEYS:
		var btn_path := "TopRaceBar/ButtonsHBox/BtnRace_" + rid
		var btn: Button = get_node_or_null(btn_path) as Button
		if btn != null:
			_race_buttons[rid] = btn
			btn.pressed.connect(func(): select_race(rid))


## 綁定控制按鈕
func _bind_controls() -> void:
	if btn_costume_prev != null:
		btn_costume_prev.pressed.connect(_on_costume_prev_pressed)
	if btn_costume_next != null:
		btn_costume_next.pressed.connect(_on_costume_next_pressed)
	if btn_chassis_prev != null:
		btn_chassis_prev.pressed.connect(_on_chassis_prev_pressed)
	if btn_chassis_next != null:
		btn_chassis_next.pressed.connect(_on_chassis_next_pressed)
	if btn_reset_default != null:
		btn_reset_default.pressed.connect(reset_to_default)
	if btn_capture_proof != null:
		btn_capture_proof.pressed.connect(func(): save_proof_screenshot())


## 選取指定種族
func select_race(race_id: String) -> void:
	if not RACES_DATA.has(race_id):
		race_id = "rabbit"
	_current_race_id = race_id
	_costume_index = 0
	_chassis_index = 0

	_update_race_buttons_visual()
	_apply_current_selections()


## 左右切換外裝
func _on_costume_prev_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index - 1 + costumes.size()) % costumes.size()
	_apply_current_selections()


func _on_costume_next_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index + 1) % costumes.size()
	_apply_current_selections()


## 左右切換塗裝
func _on_chassis_prev_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index - 1 + chassis_list.size()) % chassis_list.size()
	_apply_current_selections()


func _on_chassis_next_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index + 1) % chassis_list.size()
	_apply_current_selections()


## 重設為當前種族預設裝備
func reset_to_default() -> void:
	_costume_index = 0
	_chassis_index = 0
	_apply_current_selections()


## 套用並重新渲染紙娃娃
func _apply_current_selections() -> void:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}

	var selections: Dictionary = {}
	if cur_costume.has("id"):
		selections["costume"] = cur_costume["id"]
	if cur_chassis.has("id"):
		selections["chassis"] = cur_chassis["id"]

	# 驅動紙娃娃節點渲染
	if character != null:
		character.render_character(_current_race_id, selections)

	# 更新 UI 顯示文字與標記
	_update_info_ui(data, cur_costume, cur_chassis)


## 更新 UI 資訊
func _update_info_ui(race_data: Dictionary, cur_costume: Dictionary, cur_chassis: Dictionary) -> void:
	var name_zh: String = str(race_data.get("name_zh", ""))
	var name_en: String = str(race_data.get("name_en", ""))
	var archetype: String = str(race_data.get("archetype", ""))
	var desc: String = str(race_data.get("desc", ""))

	if hero_title_label != null:
		hero_title_label.text = "%s (%s)" % [name_zh, name_en]
	if hero_archetype_label != null:
		if archetype == "未定案":
			hero_archetype_label.text = "【未定案】"
		elif archetype.is_empty():
			hero_archetype_label.text = ""
		else:
			hero_archetype_label.text = "【%s】" % archetype
	if hero_desc_label != null:
		hero_desc_label.text = desc

	# 外裝顯示
	if costume_name_label != null:
		var c_id := str(cur_costume.get("id", "none"))
		var c_name := get_variant_spec_name(c_id, str(cur_costume.get("name_zh", "未裝備")))
		costume_name_label.text = "%s [%s]" % [c_name, c_id]
	if costume_desc_label != null:
		costume_desc_label.text = str(cur_costume.get("desc", "標準外觀"))

	# 塗裝顯示
	if chassis_name_label != null:
		var ch_id := str(cur_chassis.get("id", "paint_ivory_stock"))
		var ch_name := get_variant_spec_name(ch_id, str(cur_chassis.get("name_zh", "原廠塗裝")))
		chassis_name_label.text = "%s [%s]" % [ch_name, ch_id]
	if chassis_desc_label != null:
		chassis_desc_label.text = str(cur_chassis.get("desc", "外殼拋光烤漆"))

	# 武器顯示
	if weapon_name_label != null:
		var default_wpn := str(PaperdollRenderer._get_default_variant_id(_current_race_id, "weapon"))
		var wpn_name := get_variant_spec_name(default_wpn, default_wpn)
		weapon_name_label.text = "%s (%s)" % [wpn_name, default_wpn]

	# 槽位總結
	if slot_summary_label != null and character != null:
		var entries := character.get_rendered_entries()
		var loaded_count := 0
		for e in entries:
			if bool(e.get("is_loaded", false)):
				loaded_count += 1
		slot_summary_label.text = "7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)" % [entries.size(), loaded_count, entries.size()]


## 更新按鈕選取高亮樣式
func _update_race_buttons_visual() -> void:
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		var is_selected: bool = (rid == _current_race_id)
		var check_lbl = btn.get_node_or_null("Margin/VBox/CheckLabel")
		if check_lbl is Label:
			check_lbl.text = "✓ 已選" if is_selected else ""
			check_lbl.modulate = Color(0.98, 0.65, 0.1) if is_selected else Color(1, 1, 1, 0)

		# 邊框高亮反饋
		if is_selected:
			btn.modulate = Color(1.0, 0.98, 0.9)
		else:
			btn.modulate = Color(0.9, 0.9, 0.94)


## 取得當前種族
func get_current_race() -> String:
	return _current_race_id


## 取得當前選取的部件組合
func get_current_selections() -> Dictionary:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])
	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}
	return {
		"race": _current_race_id,
		"costume": cur_costume.get("id", ""),
		"chassis": cur_chassis.get("id", "")
	}


## 儲存驗證截圖
func save_proof_screenshot(target_path: String = "") -> String:
	var path := target_path
	if path == "":
		path = "res://../screenshots/proof_paperdoll_select_demo.png"

	var global_path := ProjectSettings.globalize_path(path)
	var dir_path := global_path.get_base_dir()
	if not DirAccess.dir_exists_absolute(dir_path):
		DirAccess.make_dir_recursive_absolute(dir_path)

	# 透過 Viewport 截取 1280x720 完整高畫質畫面
	var vp := get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var err := img.save_png(global_path)
				if err == OK:
					print("[PaperdollSelectDemo] 成功儲存 Viewport 畫面截圖至：%s" % global_path)
					return global_path

	# Fallback: 若在無頭純合成模式，儲存中心角色合成圖
	if character != null:
		var char_path := global_path.replace(".png", "_character.png")
		character.save_composite_png(char_path)
		print("[PaperdollSelectDemo] 儲存角色合成圖備用截圖至：%s" % char_path)
		return char_path

	return ""
