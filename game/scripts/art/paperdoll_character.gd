class_name PaperdollCharacter
extends Node2D
## 《發條之心》紙娃娃可見角色渲染節點 (PaperdollCharacter)
## 依據 docs/design/paperdoll_slots.json 規格書 3.1 節標準：
## 1. 128x128 模組切片畫布，以 root_anchor (64, 120) 為雙足接地中心點。
## 2. 呼叫 PaperdollRenderer 取得 7 大槽位依 layer_z_index (5~40) 排序之貼圖清單。
## 3. 多層 Sprite2D 疊合渲染，缺圖安全 fallback（不拋出例外、隱藏該層）。

signal character_rendered(race: String, slot_selections: Dictionary)

const CANVAS_DEFAULT_WIDTH := 128
const CANVAS_DEFAULT_HEIGHT := 128
const ROOT_ANCHOR_DEFAULT := Vector2(64, 120)

@export var race: String = "rabbit":
	set(val):
		race = val
		if auto_render and is_inside_tree():
			render_character()

@export var slot_selections: Dictionary = {}:
	set(val):
		slot_selections = val
		if auto_render and is_inside_tree():
			render_character()

@export var root_anchor: Vector2 = ROOT_ANCHOR_DEFAULT:
	set(val):
		root_anchor = val
		_update_layers_alignment()

@export var apply_root_anchor: bool = true:
	set(val):
		apply_root_anchor = val
		_update_layers_alignment()

@export var auto_render: bool = true

## 圖層容器節點
var _layers_container: Node2D = null
## 槽位節點快取：{slot_id: Sprite2D}
var _slot_sprites: Dictionary = {}
## 最後一次成功渲染的槽位資料快照
var _last_rendered_entries: Array[Dictionary] = []


func _ready() -> void:
	_ensure_layers_container()
	if auto_render:
		render_character()


## 確保圖層父容器節點存在
func _ensure_layers_container() -> void:
	if _layers_container == null:
		var found = get_node_or_null("Layers")
		if found is Node2D:
			_layers_container = found
		else:
			_layers_container = Node2D.new()
			_layers_container.name = "Layers"
			add_child(_layers_container)


## 取得特定槽位的 Sprite2D 節點
func get_slot_sprite(slot_id: String) -> Sprite2D:
	return _slot_sprites.get(slot_id, null)


## 取得所有槽位 Sprite2D 節點字典 {slot_id: Sprite2D}
func get_all_slot_sprites() -> Dictionary:
	return _slot_sprites.duplicate()


## 取得最後一次渲染的槽位結構詳細資料
func get_rendered_entries() -> Array[Dictionary]:
	return _last_rendered_entries


## 執行紙娃娃圖層渲染與裝配
func render_character(new_race: String = "", new_selections: Dictionary = {}) -> void:
	_ensure_layers_container()

	if new_race != "":
		race = new_race
	if not new_selections.is_empty():
		slot_selections = new_selections

	# 自 PaperdollRenderer 取得已按 z_index 排序之 7 大槽位完整資料
	var entries := PaperdollRenderer.get_sorted_slot_entries(race, slot_selections)
	_last_rendered_entries = entries

	for entry in entries:
		var sid: String = str(entry.get("slot_id", ""))
		var z_idx: int = int(entry.get("layer_z_index", 0))
		var tex: Texture2D = entry.get("texture", null)

		var sprite: Sprite2D = _get_or_create_slot_sprite(sid)
		sprite.z_index = z_idx
		sprite.texture = tex

		# 缺圖 fallback：貼圖為 null 時隱藏該圖層，確保畫面不異常且絕不崩潰
		if tex == null:
			sprite.visible = false
		else:
			sprite.visible = true

	_update_layers_alignment()
	character_rendered.emit(race, slot_selections)


## 取得或建立單一槽位的 Sprite2D 節點
func _get_or_create_slot_sprite(slot_id: String) -> Sprite2D:
	if _slot_sprites.has(slot_id):
		var existing: Sprite2D = _slot_sprites[slot_id]
		if is_instance_valid(existing):
			return existing

	var node_name := "Slot_" + slot_id
	var found = _layers_container.get_node_or_null(node_name)
	var sprite: Sprite2D = null

	if found is Sprite2D:
		sprite = found
	else:
		sprite = Sprite2D.new()
		sprite.name = node_name
		_layers_container.add_child(sprite)

	sprite.centered = false
	_slot_sprites[slot_id] = sprite
	return sprite


## 更新所有圖層的畫布偏移對齊
## 規格書 3.1 節：128x128 畫布，root_anchor 為 (64, 120)
## 當 apply_root_anchor 為 true 時，將 (0, 0) 作為角色雙足接地點，偏移 (-64, -120)
func _update_layers_alignment() -> void:
	var offset_pos := -root_anchor if apply_root_anchor else Vector2.ZERO
	for sid in _slot_sprites.keys():
		var sprite: Sprite2D = _slot_sprites[sid]
		if is_instance_valid(sprite):
			sprite.position = offset_pos


## 更新單一槽位選擇並重新渲染
func set_slot_item(slot_id: String, item_id: String) -> void:
	slot_selections[slot_id] = item_id
	render_character()


## 生成 128x128 RGBA8 記憶體合成 Image（依 z_index 順序疊合所有有效圖層）
## 可用於 headless 測試驗證、UI 頭像快取或儲存截圖驗證
func get_composite_image() -> Image:
	var base_img := Image.create(CANVAS_DEFAULT_WIDTH, CANVAS_DEFAULT_HEIGHT, false, Image.FORMAT_RGBA8)
	base_img.fill(Color(0, 0, 0, 0)) # 全透明背景

	# 依照 z_index 順序疊加各槽位貼圖
	for entry in _last_rendered_entries:
		var tex: Texture2D = entry.get("texture", null)
		if tex == null:
			continue

		var layer_img: Image = tex.get_image()
		if layer_img == null or layer_img.is_empty():
			continue

		# 確保顏色格式為 RGBA8 避免混合失真
		if layer_img.get_format() != Image.FORMAT_RGBA8:
			layer_img.convert(Image.FORMAT_RGBA8)

		var src_rect := Rect2i(0, 0, layer_img.get_width(), layer_img.get_height())
		base_img.blend_rect(layer_img, src_rect, Vector2i.ZERO)

	return base_img


## 將當前紙娃娃合成圖儲存為 PNG 檔案
func save_composite_png(output_path: String) -> Error:
	var img := get_composite_image()
	if img == null or img.is_empty():
		return ERR_CANT_CREATE

	# 檢查並建立目標目錄
	var dir_path := output_path.get_base_dir()
	if dir_path != "" and not DirAccess.dir_exists_absolute(dir_path):
		DirAccess.make_dir_recursive_absolute(dir_path)

	return img.save_png(output_path)
