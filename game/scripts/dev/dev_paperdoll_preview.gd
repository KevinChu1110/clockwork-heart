extends Control
## 《發條之心》紙娃娃可見角色 dev 測試與預覽場景
## 負責在 2D 畫布上展示 PaperdollCharacter 節點與 7 大槽位疊合效果，
## 並提供截圖存證與即時切換展示功能。

const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

@onready var character: PaperdollCharacter = $Stage/PaperdollCharacter as PaperdollCharacter
@onready var info_label: Label = $Panel/VBox/InfoLabel
@onready var slots_list: VBoxContainer = $Panel/VBox/SlotsList

const SCREENSHOT_COMPOSITE_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_composite.png"
const SCREENSHOT_VIEWPORT_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_viewport.png"


func _ready() -> void:
	if character != null:
		character.character_rendered.connect(_on_character_rendered)
		character.render_character("rabbit")
		_refresh_ui_info()

		# 自動產生驗證截圖（無損合成圖，headless 與 GUI 模式皆原生支援）
		var global_composite_path := ProjectSettings.globalize_path(SCREENSHOT_COMPOSITE_PATH)
		var err: Error = character.save_composite_png(global_composite_path)
		if err == OK:
			print("[DevPaperdollPreview] 成功儲存 128x128 合成圖至：%s" % global_composite_path)
		else:
			push_warning("[DevPaperdollPreview] 儲存合成圖失敗：錯誤碼 %d" % err)

	# 檢查是否需要截取 Viewport（僅在有完整渲染後端時執行）
	call_deferred("_check_viewport_capture")


func _on_character_rendered(_race: String, _selections: Dictionary) -> void:
	_refresh_ui_info()


func _refresh_ui_info() -> void:
	if character == null or info_label == null:
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
			"已載入" if is_loaded else "無貼圖/隱藏"
		]
		if is_loaded:
			row.modulate = Color(0.12, 0.55, 0.25) # 成功青綠色
		else:
			row.modulate = Color(0.6, 0.6, 0.6)
		slots_list.add_child(row)

	info_label.text = "【發條之心】紙娃娃 7 槽位疊合實時渲染\n種族: %s | 槽位載入數: %d/%d\n畫布: 128x128 | 雙足錨點 (64, 120)" % [
		character.race,
		loaded_count,
		entries.size()
	]


func _check_viewport_capture() -> void:
	# 在無頭 (headless) 模式下，渲染伺服器為 dummy，不支援 Viewport 貼圖抓取
	if DisplayServer.get_name() == "headless":
		return

	# 延遲兩幀等待渲染管線完成畫面繪製
	await get_tree().process_frame
	await get_tree().process_frame

	var vp := get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var global_vp_path := ProjectSettings.globalize_path(SCREENSHOT_VIEWPORT_PATH)
				var err: Error = img.save_png(global_vp_path)
				if err == OK:
					print("[DevPaperdollPreview] 成功儲存 Viewport 畫面截圖至：%s" % global_vp_path)
