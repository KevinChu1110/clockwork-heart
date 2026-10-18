class_name MaplePaperdollShowcase
extends Control
## 《發條之心》楓之谷 Character.wz 骨骼錨點與部件分層掛載展示場景
## 1. 展示發條白兔單一待機方向錨點拼裝
## 2. 部件自由置換（塗裝、外裝、眼睛、武器、發條鑰匙）
## 3. 具備即時呼吸待機動態（Body 呼吸帶動全身錨點子節點聯動、發條鑰匙自轉、眼睛自然眨眼）
## 4. 動態 Z-Order 調整
## 5. 錨點視覺化 Debug 檢視（neck/navel/hand/brow/back_key）

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")

@onready var doll_container: Node2D = $DollContainer
@onready var paperdoll: Node2D = $DollContainer/MaplePaperdoll
@onready var anchor_debug_overlay: Control = $AnchorDebugOverlay
@onready var lbl_info: Label = $UI/PanelInfo/VBox/LblInfo

var show_anchor_debug: bool = true


func _ready() -> void:
	if paperdoll == null:
		var doll_inst = MaplePaperdollClass.new()
		doll_inst.name = "MaplePaperdoll"
		if doll_container != null:
			doll_container.add_child(doll_inst)
		else:
			add_child(doll_inst)
		paperdoll = doll_inst

	if paperdoll != null:
		paperdoll.position = Vector2(0, 0)
		paperdoll.breathing_enabled = true
	_update_info_label()


func _process(_delta: float) -> void:
	if show_anchor_debug and anchor_debug_overlay != null:
		anchor_debug_overlay.queue_redraw()


## 切換塗裝
func select_chassis(chassis_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_body(chassis_id)
		_update_info_label()


## 切換外裝
func select_costume(costume_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_costume(costume_id)
		_update_info_label()


## 切換眼睛
func select_eyes(eyes_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_eyes(eyes_id)
		_update_info_label()


## 切換武器
func select_weapon(weapon_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_weapon(weapon_id)
		_update_info_label()


## 切換發條鑰匙
func select_winding_key(key_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_winding_key(key_id)
		_update_info_label()


## 切換武器前後 Z-Order (前持 z=40 vs 背持 z=4)
func toggle_weapon_z_order() -> void:
	if paperdoll != null:
		var cur_z: int = int(paperdoll.get_part_z_index("weapon"))
		var new_z: int = 4 if cur_z == 40 else 40
		paperdoll.set_part_z_index("weapon", new_z)
		_update_info_label()


## 切換發條鑰匙前後 Z-Order (後背 z=5 vs 胸前/立體透視 z=15)
func toggle_key_z_order() -> void:
	if paperdoll != null:
		var cur_z: int = int(paperdoll.get_part_z_index("winding_key"))
		var new_z: int = 15 if cur_z == 5 else 5
		paperdoll.set_part_z_index("winding_key", new_z)
		_update_info_label()


## 切換呼吸待機動態開關
func toggle_breathing() -> void:
	if paperdoll != null:
		paperdoll.breathing_enabled = not paperdoll.breathing_enabled
		_update_info_label()


## 切換錨點視覺化覆蓋層
func toggle_anchor_debug() -> void:
	show_anchor_debug = not show_anchor_debug
	if anchor_debug_overlay != null:
		anchor_debug_overlay.visible = show_anchor_debug


func _update_info_label() -> void:
	if lbl_info == null or paperdoll == null:
		return
	var loadout: Dictionary = paperdoll.get_current_loadout()
	var z_order: Dictionary = paperdoll.get_layer_order()
	var txt: String = "【發條白兔 · 楓之谷錨點部件掛載展示】\n"
	txt += "• 塗裝素體: %s (Z: %d)\n" % [loadout.get("body", ""), z_order.get("body", 0)]
	txt += "• 頭部耳朵: %s (Z: %d)\n" % [loadout.get("head_unit", ""), z_order.get("head_unit", 0)]
	txt += "• 面部光學: %s (Z: %d)\n" % [loadout.get("eyes", ""), z_order.get("eyes", 0)]
	txt += "• 玩具外裝: %s (Z: %d)\n" % [loadout.get("costume", ""), z_order.get("costume", 0)]
	txt += "• 手持武器: %s (Z: %d)\n" % [loadout.get("weapon", ""), z_order.get("weapon", 0)]
	txt += "• 發條鑰匙: %s (Z: %d)\n" % [loadout.get("winding_key", ""), z_order.get("winding_key", 0)]
	txt += "• 呼吸動態: %s" % ["啟用中 (Active)" if paperdoll.breathing_enabled else "暫停 (Paused)"]
	lbl_info.text = txt
