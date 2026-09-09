extends Control
## 《發條之心》紙娃娃可見角色多族切換 dev 測試與預覽場景 (Dev Only)
## 負責展示 PaperdollCharacter 節點在不同種族（rabbit, lion, fox, boar, macaque）下的切換效果，
## 驗證 7 大槽位疊合、缺圖安全 fallback 與無損合成圖輸出。

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

@onready var character: PaperdollCharacter = $Stage/PaperdollCharacter as PaperdollCharacter
@onready var info_label: Label = $Panel/ScrollContainer/VBox/InfoLabel
@onready var slots_list: VBoxContainer = $Panel/ScrollContainer/VBox/SlotsList
@onready var race_option_button: OptionButton = $Panel/ScrollContainer/VBox/RaceOptionButton
@onready var quick_buttons_container: HBoxContainer = $Panel/ScrollContainer/VBox/QuickButtonsContainer

const DEFAULT_PROOF_DIR := "res://assets/sprites/player/paperdoll"

var _race_list: Array[Dictionary] = []
var _current_race_id: String = "rabbit"
var _is_initialized: bool = false


func _ready() -> void:
	ensure_initialized()
	# 儲存預設兔族驗證截圖
	save_current_proof()
	# 檢查是否需要截取 Viewport（僅在有完整渲染後端時執行）
	call_deferred("_check_viewport_capture")


func ensure_initialized() -> void:
	if _is_initialized:
		return
	_ensure_nodes()
	_init_races_ui()
	_bind_quick_buttons()

	if character != null:
		if not character.character_rendered.is_connected(_on_character_rendered):
			character.character_rendered.connect(_on_character_rendered)
		switch_to_race("rabbit")
	_is_initialized = true


func _ensure_nodes() -> void:
	if character == null:
		character = get_node_or_null("Stage/PaperdollCharacter") as PaperdollCharacter
	if info_label == null:
		info_label = get_node_or_null("Panel/ScrollContainer/VBox/InfoLabel") as Label
	if slots_list == null:
		slots_list = get_node_or_null("Panel/ScrollContainer/VBox/SlotsList") as VBoxContainer
	if race_option_button == null:
		race_option_button = get_node_or_null("Panel/ScrollContainer/VBox/RaceOptionButton") as OptionButton
	if quick_buttons_container == null:
		quick_buttons_container = get_node_or_null("Panel/ScrollContainer/VBox/QuickButtonsContainer") as HBoxContainer


func _init_races_ui() -> void:
	_ensure_nodes()
	if race_option_button == null:
		return

	race_option_button.clear()
	_race_list = PaperdollRenderer.get_races()
	if _race_list.is_empty():
		_race_list = [
			{"race_id": "rabbit", "name_zh": "白金兔", "name_en": "Clockwork Rabbit"},
			{"race_id": "lion", "name_zh": "烈鬃獅", "name_en": "Gilded Lion"},
			{"race_id": "fox", "name_zh": "靈尾狐", "name_en": "Astral Fox"},
			{"race_id": "boar", "name_zh": "鋼牙豕", "name_en": "Forge Boar"},
			{"race_id": "macaque", "name_zh": "靈爪猴", "name_en": "Spring Macaque"}
		]

	for i in range(_race_list.size()):
		var r: Dictionary = _race_list[i]
		var rid: String = str(r.get("race_id", ""))
		var n_zh: String = str(r.get("name_zh", ""))
		var has_assets: bool = PaperdollRenderer.has_race_assets(rid)
		var status_str := "已就緒" if has_assets else "待素材/Fallback"
		var label_text := "%s (%s) [%s]" % [n_zh, rid, status_str]
		race_option_button.add_item(label_text, i)

	if not race_option_button.item_selected.is_connected(_on_race_option_selected):
		race_option_button.item_selected.connect(_on_race_option_selected)


func _bind_quick_buttons() -> void:
	_ensure_nodes()
	if quick_buttons_container == null:
		return

	var button_map: Dictionary = {
		"BtnRabbit": "rabbit",
		"BtnLion": "lion",
		"BtnFox": "fox",
		"BtnBoar": "boar",
		"BtnMacaque": "macaque"
	}

	for btn_name in button_map.keys():
		var btn = quick_buttons_container.get_node_or_null(btn_name)
		if btn is Button:
			var target_race: String = button_map[btn_name]
			btn.pressed.connect(func(): switch_to_race(target_race))


func _on_race_option_selected(index: int) -> void:
	if index >= 0 and index < _race_list.size():
		var selected_race_id := str(_race_list[index].get("race_id", "rabbit"))
		switch_to_race(selected_race_id)


## 切換渲染種族（公開方法）
func switch_to_race(race_id: String) -> void:
	_ensure_nodes()
	_current_race_id = race_id.to_lower().strip_edges()
	if character != null:
		character.render_character(_current_race_id)

	# 同步下拉選單選取項
	if race_option_button != null:
		for i in range(_race_list.size()):
			if str(_race_list[i].get("race_id", "")).to_lower() == _current_race_id:
				race_option_button.selected = i
				break

	_refresh_ui_info()


func get_current_race() -> String:
	return _current_race_id


func _on_character_rendered(_race: String, _selections: Dictionary) -> void:
	_refresh_ui_info()


func _refresh_ui_info() -> void:
	_ensure_nodes()
	if character == null or info_label == null or slots_list == null:
		return

	var entries: Array[Dictionary] = character.get_rendered_entries()
	var loaded_count := 0
	for child in slots_list.get_children():
		child.queue_free()

	for entry in entries:
		var sid: String = str(entry.get("slot_id", ""))
		var z_idx: int = int(entry.get("layer_z_index", 0))
		var is_loaded: bool = bool(entry.get("is_loaded", false))
		var name_zh: String = str(entry.get("name_zh", ""))

		if is_loaded:
			loaded_count += 1

		var row := Label.new()
		row.text = "• [Z:%2d] %-12s: %s (%s)" % [
			z_idx,
			sid,
			name_zh,
			"已載入" if is_loaded else "無貼圖/隱藏 (Fallback)"
		]
		if is_loaded:
			row.modulate = Color(0.12, 0.55, 0.25) # 綠色
		else:
			row.modulate = Color(0.65, 0.45, 0.2) # 柔和警示灰橘
		slots_list.add_child(row)

	var race_def := PaperdollRenderer.get_race_def(_current_race_id)
	var race_name_zh: String = str(race_def.get("name_zh", _current_race_id))
	var race_name_en: String = str(race_def.get("name_en", ""))
	var archetype: String = str(race_def.get("class_archetype", ""))

	var status_summary: String = ""
	if loaded_count == entries.size():
		status_summary = "全部 7 槽位模組切片皆已就緒並正常渲染。"
	elif loaded_count > 0:
		status_summary = "部分槽位已載入，其餘槽位自動安全隱藏。"
	else:
		status_summary = "該族系尚未提供專屬切片，已觸發安全 Fallback（所有槽位隱藏不崩潰）。"

	info_label.text = "【當前預覽種族】%s (%s) - %s\n種族 ID: %s | 槽位載入數: %d/%d\n畫布: 128x128 | 雙足錨點 (64, 120)\n狀態說明: %s" % [
		race_name_zh,
		race_name_en,
		archetype,
		_current_race_id,
		loaded_count,
		entries.size(),
		status_summary
	]


## 儲存當前種族的無損合成圖
func save_current_proof(output_path: String = "") -> Error:
	_ensure_nodes()
	if character == null:
		return ERR_UNCONFIGURED

	var path := output_path
	if path == "":
		if _current_race_id == "rabbit":
			path = "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_composite.png"
		else:
			path = "%s/%s/proof_paperdoll_scene_composite_%s.png" % [DEFAULT_PROOF_DIR, _current_race_id, _current_race_id]

	var global_path := ProjectSettings.globalize_path(path)
	var err := character.save_composite_png(global_path)
	if err == OK:
		print("[DevPaperdollPreview] 成功儲存 %s 合成圖至：%s" % [_current_race_id, global_path])
	else:
		push_warning("[DevPaperdollPreview] 儲存合成圖失敗：%d" % err)
	return err


func _check_viewport_capture() -> void:
	if DisplayServer.get_name() == "headless":
		return

	await get_tree().process_frame
	await get_tree().process_frame

	var vp := get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var global_vp_path := ProjectSettings.globalize_path("res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_viewport.png")
				var err := img.save_png(global_vp_path)
				if err == OK:
					print("[DevPaperdollPreview] 成功儲存 Viewport 畫面截圖至：%s" % global_vp_path)
