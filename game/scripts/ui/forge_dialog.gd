class_name ForgeDialog
extends Control
## 《發條之心》天宮鐵匠鍛造彈窗 (ForgeDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，主要按鈕做立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 連接既有鍛造系統與連敗保底進度 (3 格保底)。
## 7. 零 emoji、零系統字型符號。
## 8. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換)。

signal closed()
signal workshop_requested()
signal dismantle_requested()
signal power_stat_requested()
signal shop_requested()
signal go_shop()
signal inventory_requested()
signal go_inventory()
signal skill_requested()
signal go_skill()
signal wardrobe_requested()
signal go_wardrobe()
signal vault_requested()
signal go_vault()
signal title_wall_requested()
signal go_title_wall()
signal swap_weapon_requested(slot_idx: int)
signal weapon_swapped(slot_idx: int, uid: String)

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CoreSystem = preload("res://scripts/systems/core_system.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_PINK  := Color("#FFF0F4")  ## 珊瑚粉柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）
const COLOR_CARD_MUTED := Color("#EFEBE0")  ## 壓暗奶油底
const COLOR_BORDER_MUTED := Color("#D2CCC0")  ## 壓暗淡邊框
const COLOR_TEXT_DIM   := Color("#888294")  ## 壓暗提示文字
const COLOR_TEXT_MUTED := Color("#6B6680")  ## 次要輔助文字

var _dialog_card: PanelContainer
var _title_lbl: Label
var _weapon_label: Label
var _quality_label: Label
var _atk_label: Label
var _gold_label: Label
var _cost_label: Label
var _rate_label: Label
var _slots_label: Label
var _affix_label: Label

var _slot_chips: Array[Button] = []
var _active_slot_idx: int = 0

var _pity_title_label: Label
var _pity_sub_label: Label
var _pity_bars: Array[ProgressBar] = []

var _msg_label: Label
var _btn_forge: Button
var _btn_auto_forge: Button
var _btn_auto_calibrate: Button
var _btn_unequip_all: Button
var _core_title_lbl: Label
var _iron_scrap_capsule: PanelContainer
var _scrap_label: Label
var _btn_go_dismantle: Button
var _btn_go_workshop: Button
var _btn_go_power_stat: Button
var _btn_go_shop: Button
var _btn_go_inventory: Button
var _btn_go_skill: Button
var _btn_go_wardrobe: Button
var _btn_go_vault: Button
var _btn_go_title_wall: Button
var _act_scroll: ScrollContainer
var _btn_close: Button
var _btn_swap_weapon: Button
var _weapon_swap_dialog: Control = null
var _power_label: Label
var _cached_font: Font = null
var _last_calibrate_state: Dictionary = {}
var _current_toast: Label = null
var last_toast_text: String = ""


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)
		var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_signal("inventory_changed"):
			if not inv.inventory_changed.is_connected(_refresh_iron_scrap_display):
				inv.inventory_changed.connect(_refresh_iron_scrap_display)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)
		var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_signal("inventory_changed") and inv.inventory_changed.is_connected(_refresh_iron_scrap_display):
			inv.inventory_changed.disconnect(_refresh_iron_scrap_display)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	_refresh_display()
	_refresh_all_forge_core_slots()
	_update_calibrate_message()


func _update_calibrate_message() -> void:
	if not is_instance_valid(_msg_label) or _last_calibrate_state.is_empty():
		return
	var sname: String = _t(str(_last_calibrate_state.get("slot_name", "")))
	var tip_key: String = str(_last_calibrate_state.get("tip_key", ""))
	var default_tip: String = str(_last_calibrate_state.get("tip", ""))
	var tip: String = default_tip
	if not tip_key.is_empty():
		var trans := _t(tip_key)
		if trans != tip_key:
			tip = trans
		else:
			tip = _t(default_tip)
	else:
		tip = _t(default_tip)
	var raw_tnm: String = str(_last_calibrate_state.get("tier_name", "白"))
	var tnm: String = _t(raw_tnm)
	var rem: int = int(_last_calibrate_state.get("rem", 0))
	_msg_label.text = _t("【%s】%s · 目前色階：%s階（剩餘 %d 次）") % [sname, tip, tnm, rem]
	if bool(_last_calibrate_state.get("ok", false)):
		_msg_label.add_theme_color_override("font_color", COLOR_MINT)
	else:
		_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)


func _get_equip_sys() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	return null


func _update_ui_texts() -> void:
	if _title_lbl and is_instance_valid(_title_lbl):
		_title_lbl.text = _t("天宮鐵匠 · 裝備鍛造")
	if _core_title_lbl and is_instance_valid(_core_title_lbl):
		_core_title_lbl.text = _t("機芯五槽部位")
	if _btn_auto_forge and is_instance_valid(_btn_auto_forge):
		_btn_auto_forge.text = _t("一鍵鍛造")
	if _btn_auto_calibrate and is_instance_valid(_btn_auto_calibrate):
		_btn_auto_calibrate.text = _t("一鍵校準")
	if _btn_unequip_all and is_instance_valid(_btn_unequip_all):
		_btn_unequip_all.text = _t("一鍵卸下")
	if _btn_go_dismantle and is_instance_valid(_btn_go_dismantle):
		_btn_go_dismantle.text = _t("前往拆解")
	if _btn_go_workshop and is_instance_valid(_btn_go_workshop):
		_btn_go_workshop.text = _t("前往工坊")
	if _btn_go_power_stat and is_instance_valid(_btn_go_power_stat):
		var btn_txt := _t("forge.btn_go_power_stat")
		if btn_txt == "forge.btn_go_power_stat" or btn_txt.is_empty():
			btn_txt = _t("前往戰力")
		_btn_go_power_stat.text = btn_txt
	if _btn_go_shop and is_instance_valid(_btn_go_shop):
		var shop_btn_txt := _t("forge.btn_go_shop")
		if shop_btn_txt == "forge.btn_go_shop" or shop_btn_txt.is_empty():
			shop_btn_txt = _t("前往商城")
		_btn_go_shop.text = shop_btn_txt
	if _btn_go_inventory and is_instance_valid(_btn_go_inventory):
		var inv_btn_txt := _t("forge.btn_go_inventory")
		if inv_btn_txt == "forge.btn_go_inventory" or inv_btn_txt.is_empty():
			inv_btn_txt = _t("前往背包")
		_btn_go_inventory.text = inv_btn_txt
	if _btn_go_skill and is_instance_valid(_btn_go_skill):
		var skill_btn_txt := _t("forge.btn_go_skill")
		if skill_btn_txt == "forge.btn_go_skill" or skill_btn_txt.is_empty():
			skill_btn_txt = _t("前往心法")
		_btn_go_skill.text = skill_btn_txt
	if _btn_go_wardrobe and is_instance_valid(_btn_go_wardrobe):
		var wardrobe_btn_txt := _t("forge.btn_go_wardrobe")
		if wardrobe_btn_txt == "forge.btn_go_wardrobe" or wardrobe_btn_txt.is_empty():
			wardrobe_btn_txt = _t("前往衣櫥")
		_btn_go_wardrobe.text = wardrobe_btn_txt
	if _btn_go_vault and is_instance_valid(_btn_go_vault):
		var vault_btn_txt := _t("forge.btn_go_vault")
		if vault_btn_txt == "forge.btn_go_vault" or vault_btn_txt.is_empty():
			vault_btn_txt = _t("前往儲能庫")
		_btn_go_vault.text = vault_btn_txt
	if _btn_go_title_wall and is_instance_valid(_btn_go_title_wall):
		var title_wall_btn_txt := _t("forge.btn_go_title_wall")
		if title_wall_btn_txt == "forge.btn_go_title_wall" or title_wall_btn_txt.is_empty():
			title_wall_btn_txt = _t("前往稱號")
		_btn_go_title_wall.text = title_wall_btn_txt
	if _btn_close and is_instance_valid(_btn_close):
		_btn_close.text = _t("離開鐵匠鋪")
	if _btn_swap_weapon and is_instance_valid(_btn_swap_weapon):
		_btn_swap_weapon.text = _t("更換裝備")
	_refresh_slot_chips()
	_refresh_iron_scrap_display()


func _ready() -> void:
	name = "ForgeDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_connect_loc_signal()
	_ensure_initial_state()
	_build_ui()
	_update_ui_texts()
	_refresh_display()
	_refresh_all_forge_core_slots()


func _ensure_initial_state() -> void:
	if not GameState.has_flag("c1_forged"):
		GameState.set_flag("c1_forged", true)
	var es := _get_equip_sys()
	if es and es.has_method("active_loadout_index"):
		_active_slot_idx = clampi(int(es.call("active_loadout_index")), 0, 2)
	elif "weapon_loadout_active" in GameState:
		_active_slot_idx = clampi(int(GameState.weapon_loadout_active), 0, 2)
	else:
		_active_slot_idx = 0

	var inst := _current_weapon_inst()
	if not inst.is_empty():
		var r: Dictionary = inst.get("rolled", {})
		GameState.weapon_atk = int(r.get("atk", GameState.weapon_atk))
		GameState.weapon_tier = maxi(GameState.weapon_tier, int(inst.get("tier", 1)))
		GameState.weapon_name = str(inst.get("name", GameState.weapon_name))
	else:
		if GameState.weapon_tier < 1:
			GameState.weapon_tier = 1
		if GameState.weapon_atk <= 0:
			GameState.weapon_atk = 6
		if GameState.weapon_name.is_empty():
			GameState.weapon_name = "微末之刃"


func _current_weapon_inst() -> Dictionary:
	var es := _get_equip_sys()
	if es:
		if es.has_method("loadout_uid") and es.has_method("weapon_inst"):
			var uid: String = str(es.call("loadout_uid", _active_slot_idx))
			if not uid.is_empty():
				var inst: Dictionary = es.call("weapon_inst", uid)
				if not inst.is_empty():
					return inst
		elif es.has_method("active_weapon_inst") and _active_slot_idx == 0:
			var inst: Dictionary = es.call("active_weapon_inst")
			if not inst.is_empty():
				return inst

	# Fallback: GameState
	if "weapon_loadout" in GameState and GameState.weapon_loadout != null and _active_slot_idx < GameState.weapon_loadout.size():
		var wuid := str(GameState.weapon_loadout[_active_slot_idx])
		if wuid != "" and GameState.equip_worn != null and GameState.equip_worn.has(wuid):
			return GameState.equip_worn[wuid]

	if _active_slot_idx == 0:
		var wuid := str(GameState.equip_slots.get("weapon", "")) if GameState.equip_slots != null else ""
		if wuid != "" and GameState.equip_worn != null and GameState.equip_worn.has(wuid):
			return GameState.equip_worn[wuid]
	return {}


func _current_weapon_atk() -> int:
	var inst := _current_weapon_inst()
	if not inst.is_empty():
		var r: Dictionary = inst.get("rolled", {})
		return int(r.get("atk", 0))
	if _active_slot_idx == 0:
		return GameState.weapon_atk
	return 0


func _sync_state_from_weapon() -> void:
	var inst := _current_weapon_inst()
	if not inst.is_empty():
		var r: Dictionary = inst.get("rolled", {})
		GameState.weapon_atk = int(r.get("atk", GameState.weapon_atk))
		GameState.weapon_tier = int(inst.get("tier", GameState.weapon_tier))
		GameState.weapon_name = str(inst.get("name", GameState.weapon_name))


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	var scrim_btn := Button.new()
	scrim_btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_btn.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_btn.add_theme_stylebox_override("normal", esb)
	scrim_btn.add_theme_stylebox_override("hover", esb)
	scrim_btn.add_theme_stylebox_override("pressed", esb)
	scrim_btn.pressed.connect(_on_close)
	scrim.add_child(scrim_btn)

	# 2. 置中卡片 (寬 750px，符合 review.md 第 28 條 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "ForgeCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 520)
	# 奶油米白底 + 深藍紫立體邊框 + 22px 大圓角
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 10)
	margin.add_child(v)

	# 標題列 + 頂部戰力展示 + 右上「✕」關閉按鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("天宮鐵匠 · 裝備鍛造")
	_title_lbl.add_theme_font_size_override("font_size", 22)
	_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_title_lbl.add_theme_font_override("font", _cached_font)
	_title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(_title_lbl)

	# 頂部戰力展示 (TopPowerLabel)
	_power_label = Label.new()
	_power_label.name = "TopPowerLabel"
	_power_label.text = ""
	_power_label.add_theme_font_size_override("font_size", 18)
	_power_label.add_theme_color_override("font_color", COLOR_TEXT_GOLD)  ## 亮底用壓明度金（#9A6B00，對奶油底 4.6:1）
	_power_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_power_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_power_label.add_theme_font_override("font", _cached_font)
	head.add_child(_power_label)

	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 亮橘色粗分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# 三欄武器槽位切換 Chip / 頁籤 (槽位 1 / 槽位 2 / 槽位 3)
	var chip_row := HBoxContainer.new()
	chip_row.name = "WeaponSlotChipRow"
	chip_row.alignment = BoxContainer.ALIGNMENT_CENTER
	chip_row.add_theme_constant_override("separation", 10)
	v.add_child(chip_row)

	_slot_chips.clear()
	for i in range(3):
		var chip := Button.new()
		chip.name = "WeaponSlotChip_%d" % i
		chip.custom_minimum_size = Vector2(0, 46)
		chip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var slot_idx := i
		chip.pressed.connect(func(): _on_slot_chip_pressed(slot_idx))
		chip_row.add_child(chip)
		_slot_chips.append(chip)

	# 武器當前數值面板 (亮金黃溫暖卡片底)
	var status_panel := PanelContainer.new()
	status_panel.name = "StatusPanel"
	status_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 20))
	v.add_child(status_panel)

	var s_margin := MarginContainer.new()
	s_margin.add_theme_constant_override("margin_left", 16)
	s_margin.add_theme_constant_override("margin_right", 16)
	s_margin.add_theme_constant_override("margin_top", 10)
	s_margin.add_theme_constant_override("margin_bottom", 10)
	status_panel.add_child(s_margin)

	var sv := VBoxContainer.new()
	sv.add_theme_constant_override("separation", 5)
	s_margin.add_child(sv)

	var weapon_head := HBoxContainer.new()
	weapon_head.name = "WeaponStatusHead"
	weapon_head.add_theme_constant_override("separation", 10)
	sv.add_child(weapon_head)

	_weapon_label = Label.new()
	_weapon_label.name = "WeaponLabel"
	_weapon_label.text = ""
	_weapon_label.add_theme_font_size_override("font_size", 18)
	_weapon_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_weapon_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_weapon_label.add_theme_constant_override("outline_size", 2)
	_weapon_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_weapon_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if _cached_font:
		_weapon_label.add_theme_font_override("font", _cached_font)
	weapon_head.add_child(_weapon_label)

	# ── 更換裝備立體果凍按鈕 (BtnSwapWeapon，高>=48px，熱區>=48px，圓角18px，天藍果凍厚底，深藍紫描邊2px，零Emoji) ──
	_btn_swap_weapon = Button.new()
	_btn_swap_weapon.name = "BtnSwapWeapon"
	_btn_swap_weapon.text = _t("更換裝備")
	_btn_swap_weapon.custom_minimum_size = Vector2(110, 48)
	_btn_swap_weapon.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_btn_swap_weapon.add_theme_font_size_override("font_size", 16)
	_btn_swap_weapon.add_theme_color_override("font_color", Color.WHITE)
	_btn_swap_weapon.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_swap_weapon.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_btn_swap_weapon.add_theme_font_override("font", _cached_font)
	_btn_swap_weapon.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18, 2))
	_btn_swap_weapon.add_theme_stylebox_override("hover", _create_button_style(Color("#5DBBFF"), COLOR_BORDER, 5, 18, 2))
	_btn_swap_weapon.add_theme_stylebox_override("pressed", _create_button_style(Color("#268AE6"), COLOR_BORDER, 2, 18, 2))
	_btn_swap_weapon.add_theme_stylebox_override("disabled", _create_button_style(Color("#CAD9E8"), COLOR_BORDER, 2, 18, 2))
	_btn_swap_weapon.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_swap_weapon.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_swap_weapon.pressed.connect(_on_swap_weapon_pressed)
	weapon_head.add_child(_btn_swap_weapon)

	var stats_grid := GridContainer.new()
	stats_grid.columns = 2
	stats_grid.add_theme_constant_override("h_separation", 24)
	stats_grid.add_theme_constant_override("v_separation", 4)
	sv.add_child(stats_grid)

	_atk_label = _create_info_label(stats_grid, "")
	_atk_label.name = "AtkLabel"
	_quality_label = _create_info_label(stats_grid, "")
	_quality_label.name = "QualityLabel"
	_cost_label = _create_info_label(stats_grid, "")
	_cost_label.name = "CostLabel"
	_rate_label = _create_info_label(stats_grid, "")
	_rate_label.name = "RateLabel"
	_gold_label = _create_info_label(stats_grid, "")
	_gold_label.name = "GoldLabel"
	_slots_label = _create_info_label(stats_grid, "")
	_slots_label.name = "SlotsLabel"
	_slots_label.add_theme_color_override("font_color", COLOR_SKY)

	_affix_label = Label.new()
	_affix_label.name = "AffixLabel"
	_affix_label.text = ""
	_affix_label.add_theme_font_size_override("font_size", 14)
	_affix_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_affix_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_affix_label.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_affix_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_affix_label)

	# 機芯五槽部位槽位列 (亮金黃柔和卡片底)
	var core_panel := PanelContainer.new()
	core_panel.name = "ForgeCoreSlotsPanel"
	core_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 18))
	v.add_child(core_panel)

	var cm := MarginContainer.new()
	cm.add_theme_constant_override("margin_left", 14)
	cm.add_theme_constant_override("margin_right", 14)
	cm.add_theme_constant_override("margin_top", 8)
	cm.add_theme_constant_override("margin_bottom", 8)
	core_panel.add_child(cm)

	var cv := VBoxContainer.new()
	cv.add_theme_constant_override("separation", 6)
	cm.add_child(cv)

	var core_head := HBoxContainer.new()
	core_head.name = "ForgeCoreSlotsHead"
	core_head.add_theme_constant_override("separation", 8)
	cv.add_child(core_head)

	_core_title_lbl = Label.new()
	_core_title_lbl.name = "ForgeCoreSlotsTitle"
	_core_title_lbl.text = _t("機芯五槽部位")
	_core_title_lbl.add_theme_font_size_override("font_size", 16)
	_core_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_core_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_core_title_lbl.add_theme_constant_override("outline_size", 2)
	_core_title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_core_title_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if _cached_font:
		_core_title_lbl.add_theme_font_override("font", _cached_font)
	core_head.add_child(_core_title_lbl)

	# ── 鐵屑持有進度膠囊 (IronScrapCapsule 與 _scrap_label) ──
	_iron_scrap_capsule = PanelContainer.new()
	_iron_scrap_capsule.name = "IronScrapCapsule"
	_iron_scrap_capsule.custom_minimum_size = Vector2(0, 48)
	_iron_scrap_capsule.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_iron_scrap_capsule.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	core_head.add_child(_iron_scrap_capsule)

	var scm := MarginContainer.new()
	scm.add_theme_constant_override("margin_left", 12)
	scm.add_theme_constant_override("margin_right", 12)
	scm.add_theme_constant_override("margin_top", 4)
	scm.add_theme_constant_override("margin_bottom", 6)
	_iron_scrap_capsule.add_child(scm)

	_scrap_label = Label.new()
	_scrap_label.name = "IronScrapLabel"
	_scrap_label.text = ""
	_scrap_label.add_theme_font_size_override("font_size", 16)
	_scrap_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_scrap_label.add_theme_color_override("font_outline_color", Color.WHITE)
	_scrap_label.add_theme_constant_override("outline_size", 2)
	_scrap_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_scrap_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if _cached_font:
		_scrap_label.add_theme_font_override("font", _cached_font)
	scm.add_child(_scrap_label)

	# ── 前往拆解立體果凍按鈕 (BtnGoDismantle，高>=48px，熱區>=48px，圓角18px，薄荷綠果凍厚底，零Emoji) ──
	_btn_go_dismantle = Button.new()
	_btn_go_dismantle.name = "BtnGoDismantle"
	_btn_go_dismantle.text = _t("前往拆解")
	_btn_go_dismantle.custom_minimum_size = Vector2(110, 48)
	_btn_go_dismantle.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_btn_go_dismantle.add_theme_font_size_override("font_size", 16)
	_btn_go_dismantle.add_theme_color_override("font_color", Color.WHITE)
	_btn_go_dismantle.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_dismantle.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_btn_go_dismantle.add_theme_font_override("font", _cached_font)
	_btn_go_dismantle.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18, 2))
	_btn_go_dismantle.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18, 2))
	_btn_go_dismantle.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18, 2))
	_btn_go_dismantle.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 2, 18, 2))
	_btn_go_dismantle.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_dismantle.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_dismantle.pressed.connect(_on_go_dismantle_pressed)
	core_head.add_child(_btn_go_dismantle)

	# 一鍵校準果凍厚底按鈕 (BtnAutoCalibrateCore，高>=48px，金黃果凍厚底，零Emoji)
	_btn_auto_calibrate = Button.new()
	_btn_auto_calibrate.name = "BtnAutoCalibrateCore"
	_btn_auto_calibrate.text = _t("一鍵校準")
	_btn_auto_calibrate.custom_minimum_size = Vector2(110, 48)
	_btn_auto_calibrate.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_btn_auto_calibrate.add_theme_font_size_override("font_size", 16)
	_btn_auto_calibrate.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_auto_calibrate.add_theme_color_override("font_outline_color", Color.WHITE)
	_btn_auto_calibrate.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_btn_auto_calibrate.add_theme_font_override("font", _cached_font)
	_btn_auto_calibrate.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_auto_calibrate.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_auto_calibrate.add_theme_stylebox_override("pressed", _create_button_style(Color("#E6B800"), COLOR_BORDER, 2, 18, 2))
	_btn_auto_calibrate.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 2, 18, 2))
	_btn_auto_calibrate.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_auto_calibrate.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_auto_calibrate.pressed.connect(_on_auto_calibrate_pressed)
	core_head.add_child(_btn_auto_calibrate)

	# 一鍵卸下全部機芯果凍按鈕 (BtnUnequipAllCores，高度 46px，珊瑚粉 #FF5E8A，深藍紫描邊 #1F1A3A，底邊 5px，圓角 16px，與一鍵校準按鈕成對並列)
	_btn_unequip_all = Button.new()
	_btn_unequip_all.name = "BtnUnequipAllCores"
	_btn_unequip_all.text = _t("一鍵卸下")
	_btn_unequip_all.custom_minimum_size = Vector2(105, 46)
	_btn_unequip_all.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_btn_unequip_all.add_theme_font_size_override("font_size", 15)
	_btn_unequip_all.add_theme_color_override("font_color", Color.WHITE)
	_btn_unequip_all.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_unequip_all.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_btn_unequip_all.add_theme_font_override("font", _cached_font)
	_btn_unequip_all.add_theme_stylebox_override("normal", _create_button_style(COLOR_PINK, COLOR_BORDER, 5, 16, 2))
	_btn_unequip_all.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7096"), COLOR_BORDER, 5, 16, 2))
	_btn_unequip_all.add_theme_stylebox_override("pressed", _create_button_style(Color("#E04E78"), COLOR_BORDER, 2, 16, 2))
	_btn_unequip_all.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 2, 16, 2))
	_btn_unequip_all.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_unequip_all.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_unequip_all.pressed.connect(_on_unequip_all_cores_pressed)
	core_head.add_child(_btn_unequip_all)

	_refresh_iron_scrap_display()

	var core_row := HBoxContainer.new()
	core_row.name = "ForgeCoreSlotsRow"
	core_row.alignment = BoxContainer.ALIGNMENT_CENTER
	core_row.add_theme_constant_override("separation", 10)
	cv.add_child(core_row)

	for def in SpriteDB.CORE_SLOT_DEFS:
		core_row.add_child(_create_forge_core_slot(def))

	# 既有連敗保底進度條區塊 (珊瑚粉卡片底)
	var pity_panel := PanelContainer.new()
	pity_panel.name = "PityContainer"
	pity_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_PINK, COLOR_BORDER, 2, 4, 20))
	v.add_child(pity_panel)

	var pm := MarginContainer.new()
	pm.add_theme_constant_override("margin_left", 16)
	pm.add_theme_constant_override("margin_right", 16)
	pm.add_theme_constant_override("margin_top", 10)
	pm.add_theme_constant_override("margin_bottom", 10)
	pity_panel.add_child(pm)

	var pv := VBoxContainer.new()
	pv.add_theme_constant_override("separation", 6)
	pm.add_child(pv)

	_pity_title_label = Label.new()
	_pity_title_label.name = "PityTitleLabel"
	_pity_title_label.text = ""
	_pity_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_title_label.add_theme_font_size_override("font_size", 17)
	_pity_title_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
	_pity_title_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_pity_title_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_pity_title_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_title_label)

	var bar_row := HBoxContainer.new()
	bar_row.name = "PityBarRow"
	bar_row.alignment = BoxContainer.ALIGNMENT_CENTER
	bar_row.add_theme_constant_override("separation", 10)
	pv.add_child(bar_row)

	_pity_bars.clear()
	for i in range(3):
		var seg := ProgressBar.new()
		seg.min_value = 0
		seg.max_value = 1
		seg.value = 0.0
		seg.custom_minimum_size = Vector2(160, 22)
		seg.show_percentage = false
		var fill_color: Color = COLOR_ORANGE if i < 2 else COLOR_PINK
		_style_dopamine_progress(seg, fill_color, Color("#FFFDF8"))
		bar_row.add_child(seg)
		_pity_bars.append(seg)

	_pity_sub_label = Label.new()
	_pity_sub_label.name = "PitySubLabel"
	_pity_sub_label.text = ""
	_pity_sub_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_sub_label.add_theme_font_size_override("font_size", 16)
	_pity_sub_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_pity_sub_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_pity_sub_label.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_pity_sub_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_sub_label)

	# 訊息回饋
	_msg_label = Label.new()
	_msg_label.name = "MsgLabel"
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 16)
	_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_msg_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_msg_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 動作按鈕列 (按鈕高 >= 50，支援橫向捲動)
	_act_scroll = ScrollContainer.new()
	_act_scroll.name = "ActionScroll"
	_act_scroll.custom_minimum_size = Vector2(710, 60)
	_act_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	_act_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	v.add_child(_act_scroll)

	var act_row := HBoxContainer.new()
	act_row.name = "act_row"
	act_row.add_theme_constant_override("separation", 6)
	act_row.alignment = BoxContainer.ALIGNMENT_CENTER
	_act_scroll.add_child(act_row)

	# 主要按鈕：強化升階 (薄荷綠立體果凍厚底 6px)
	_btn_forge = Button.new()
	_btn_forge.name = "BtnForge"
	_btn_forge.text = ""
	_btn_forge.custom_minimum_size = Vector2(130, 50)
	_btn_forge.add_theme_font_size_override("font_size", 16)
	_btn_forge.add_theme_color_override("font_color", Color.WHITE)
	_btn_forge.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_forge.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_btn_forge.add_theme_font_override("font", _cached_font)
	_btn_forge.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 20, 2))
	_btn_forge.add_theme_stylebox_override("hover", _create_button_style(Color("#68E882"), COLOR_BORDER, 6, 20, 2))
	_btn_forge.add_theme_stylebox_override("pressed", _create_button_style(Color("#3BBF55"), COLOR_BORDER, 2, 20, 2))
	_btn_forge.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 3, 20, 2))
	_btn_forge.pressed.connect(_on_forge_pressed)
	act_row.add_child(_btn_forge)

	# 新增『一鍵鍛造』按鈕 BtnAutoForge（熱區 >= 48px，果凍厚底 5px，薄荷綠配色）
	_btn_auto_forge = Button.new()
	_btn_auto_forge.name = "BtnAutoForge"
	_btn_auto_forge.text = _t("一鍵鍛造")
	_btn_auto_forge.custom_minimum_size = Vector2(105, 50)
	_btn_auto_forge.add_theme_font_size_override("font_size", 16)
	_btn_auto_forge.add_theme_color_override("font_color", Color.WHITE)
	_btn_auto_forge.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_auto_forge.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_btn_auto_forge.add_theme_font_override("font", _cached_font)
	_btn_auto_forge.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 20, 2))
	_btn_auto_forge.add_theme_stylebox_override("hover", _create_button_style(Color("#68E882"), COLOR_BORDER, 5, 20, 2))
	_btn_auto_forge.add_theme_stylebox_override("pressed", _create_button_style(Color("#3BBF55"), COLOR_BORDER, 2, 20, 2))
	_btn_auto_forge.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 3, 20, 2))
	_btn_auto_forge.pressed.connect(_on_auto_forge_pressed)
	act_row.add_child(_btn_auto_forge)

	# 快捷按鈕：前往工坊 (暖橘立體厚底 5px)
	_btn_go_workshop = Button.new()
	_btn_go_workshop.name = "BtnGoWorkshop"
	_btn_go_workshop.text = _t("前往工坊")
	_btn_go_workshop.custom_minimum_size = Vector2(105, 50)
	_btn_go_workshop.add_theme_font_size_override("font_size", 16)
	_btn_go_workshop.add_theme_color_override("font_color", Color.WHITE)
	_btn_go_workshop.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_workshop.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_btn_go_workshop.add_theme_font_override("font", _cached_font)
	_btn_go_workshop.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 20, 2))
	_btn_go_workshop.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB338"), COLOR_BORDER, 5, 20, 2))
	_btn_go_workshop.add_theme_stylebox_override("pressed", _create_button_style(Color("#E08B00"), COLOR_BORDER, 2, 20, 2))
	_btn_go_workshop.pressed.connect(_on_go_workshop_pressed)
	act_row.add_child(_btn_go_workshop)

	# 快捷按鈕：前往戰力 (金黃立體厚底 5px, 140x50, 規格 140x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_power_stat = Button.new()
	_btn_go_power_stat.name = "BtnGoPowerStat"
	var pstat_txt := _t("forge.btn_go_power_stat")
	if pstat_txt == "forge.btn_go_power_stat" or pstat_txt.is_empty():
		pstat_txt = _t("前往戰力")
	_btn_go_power_stat.text = pstat_txt
	_btn_go_power_stat.custom_minimum_size = Vector2(140, 50)
	_btn_go_power_stat.add_theme_font_size_override("font_size", 16)
	_btn_go_power_stat.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_power_stat.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_power_stat.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_power_stat.add_theme_font_override("font", _cached_font)
	_btn_go_power_stat.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_go_power_stat.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_go_power_stat.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
	_btn_go_power_stat.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_power_stat.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_power_stat.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_power_stat.pressed.connect(_on_go_power_stat_pressed)
	act_row.add_child(_btn_go_power_stat)

	# 快捷按鈕：前往商城 (暖橘立體厚底 5px, 115x50, 規格 115x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_shop = Button.new()
	_btn_go_shop.name = "BtnGoShop"
	var shop_btn_txt := _t("forge.btn_go_shop")
	if shop_btn_txt == "forge.btn_go_shop" or shop_btn_txt.is_empty():
		shop_btn_txt = _t("前往商城")
	_btn_go_shop.text = shop_btn_txt
	_btn_go_shop.custom_minimum_size = Vector2(115, 50)
	_btn_go_shop.add_theme_font_size_override("font_size", 16)
	_btn_go_shop.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_shop.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_shop.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_shop.add_theme_font_override("font", _cached_font)
	_btn_go_shop.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 18, 2))
	_btn_go_shop.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB338"), COLOR_BORDER, 5, 18, 2))
	_btn_go_shop.add_theme_stylebox_override("pressed", _create_button_style(Color("#E08B00"), COLOR_BORDER, 2, 18, 2))
	_btn_go_shop.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_shop.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_shop.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_shop.pressed.connect(_on_go_shop_pressed)
	act_row.add_child(_btn_go_shop)

	# 快捷按鈕：前往背包 (天藍立體厚底 5px, 115x50, 規格 115x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_inventory = Button.new()
	_btn_go_inventory.name = "BtnGoInventory"
	var inv_btn_txt := _t("forge.btn_go_inventory")
	if inv_btn_txt == "forge.btn_go_inventory" or inv_btn_txt.is_empty():
		inv_btn_txt = _t("前往背包")
	_btn_go_inventory.text = inv_btn_txt
	_btn_go_inventory.custom_minimum_size = Vector2(115, 50)
	_btn_go_inventory.add_theme_font_size_override("font_size", 16)
	_btn_go_inventory.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_inventory.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_inventory.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_inventory.add_theme_font_override("font", _cached_font)
	_btn_go_inventory.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18, 2))
	_btn_go_inventory.add_theme_stylebox_override("hover", _create_button_style(Color("#5CB4FF"), COLOR_BORDER, 5, 18, 2))
	_btn_go_inventory.add_theme_stylebox_override("pressed", _create_button_style(Color("#2085E5"), COLOR_BORDER, 2, 18, 2))
	_btn_go_inventory.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_inventory.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_inventory.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_inventory.pressed.connect(_on_go_inventory_pressed)
	act_row.add_child(_btn_go_inventory)

	# 快捷按鈕：前往心法 (天藍立體厚底 5px, 140x50 >= 140x48, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_skill = Button.new()
	_btn_go_skill.name = "BtnGoSkill"
	var skill_btn_txt := _t("forge.btn_go_skill")
	if skill_btn_txt == "forge.btn_go_skill" or skill_btn_txt.is_empty():
		skill_btn_txt = _t("前往心法")
	_btn_go_skill.text = skill_btn_txt
	_btn_go_skill.custom_minimum_size = Vector2(140, 50)
	_btn_go_skill.add_theme_font_size_override("font_size", 16)
	_btn_go_skill.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_skill.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_skill.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_skill.add_theme_font_override("font", _cached_font)
	_btn_go_skill.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18, 2))
	_btn_go_skill.add_theme_stylebox_override("hover", _create_button_style(Color("#5CB4FF"), COLOR_BORDER, 5, 18, 2))
	_btn_go_skill.add_theme_stylebox_override("pressed", _create_button_style(Color("#2085E5"), COLOR_BORDER, 2, 18, 2))
	_btn_go_skill.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_skill.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_skill.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_skill.pressed.connect(_on_go_skill_pressed)
	act_row.add_child(_btn_go_skill)

	# 快捷按鈕：前往衣櫥 (金黃立體厚底 5px, 140x50 >= 115x50, 規格 140x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_wardrobe = Button.new()
	_btn_go_wardrobe.name = "BtnGoWardrobe"
	var wardrobe_btn_txt := _t("forge.btn_go_wardrobe")
	if wardrobe_btn_txt == "forge.btn_go_wardrobe" or wardrobe_btn_txt.is_empty():
		wardrobe_btn_txt = _t("前往衣櫥")
	_btn_go_wardrobe.text = wardrobe_btn_txt
	_btn_go_wardrobe.custom_minimum_size = Vector2(140, 50)
	_btn_go_wardrobe.add_theme_font_size_override("font_size", 16)
	_btn_go_wardrobe.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_wardrobe.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_wardrobe.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_wardrobe.add_theme_font_override("font", _cached_font)
	_btn_go_wardrobe.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_go_wardrobe.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_go_wardrobe.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
	_btn_go_wardrobe.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_wardrobe.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_wardrobe.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_wardrobe.pressed.connect(_on_go_wardrobe_pressed)
	act_row.add_child(_btn_go_wardrobe)

	# 快捷按鈕：前往儲能庫 (金黃立體厚底 5px, 140x50 >= 115x50, 規格 140x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_vault = Button.new()
	_btn_go_vault.name = "BtnGoVault"
	var vault_btn_txt := _t("forge.btn_go_vault")
	if vault_btn_txt == "forge.btn_go_vault" or vault_btn_txt.is_empty():
		vault_btn_txt = _t("前往儲能庫")
	_btn_go_vault.text = vault_btn_txt
	_btn_go_vault.custom_minimum_size = Vector2(140, 50)
	_btn_go_vault.add_theme_font_size_override("font_size", 16)
	_btn_go_vault.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_vault.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_vault.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_vault.add_theme_font_override("font", _cached_font)
	_btn_go_vault.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_go_vault.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_go_vault.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
	_btn_go_vault.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_vault.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_vault.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_vault.pressed.connect(_on_go_vault_pressed)
	act_row.add_child(_btn_go_vault)

	# 快捷按鈕：前往稱號 (金黃立體厚底 5px, 140x50 >= 115x50, 規格 140x50, 圓角 18px, 文字深藍紫, 零系統 Emoji)
	_btn_go_title_wall = Button.new()
	_btn_go_title_wall.name = "BtnGoTitleWall"
	var title_wall_btn_txt := _t("forge.btn_go_title_wall")
	if title_wall_btn_txt == "forge.btn_go_title_wall" or title_wall_btn_txt.is_empty():
		title_wall_btn_txt = _t("前往稱號")
	_btn_go_title_wall.text = title_wall_btn_txt
	_btn_go_title_wall.custom_minimum_size = Vector2(140, 50)
	_btn_go_title_wall.add_theme_font_size_override("font_size", 16)
	_btn_go_title_wall.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_go_title_wall.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_go_title_wall.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_go_title_wall.add_theme_font_override("font", _cached_font)
	_btn_go_title_wall.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_go_title_wall.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_go_title_wall.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
	_btn_go_title_wall.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEBE0"), COLOR_BORDER_MUTED, 3, 18, 2))
	_btn_go_title_wall.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_btn_go_title_wall.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_go_title_wall.pressed.connect(_on_go_title_wall_pressed)
	act_row.add_child(_btn_go_title_wall)

	# 次要按鈕：離開鐵匠鋪 (金黃立體厚底 5px)
	_btn_close = Button.new()
	_btn_close.name = "BtnCloseForge"
	_btn_close.text = _t("離開鐵匠鋪")
	_btn_close.custom_minimum_size = Vector2(105, 50)
	_btn_close.add_theme_font_size_override("font_size", 16)
	_btn_close.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_close.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_close.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_close.add_theme_font_override("font", _cached_font)
	_btn_close.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20, 2))
	_btn_close.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 20, 2))
	_btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
	_btn_close.pressed.connect(_on_close)
	act_row.add_child(_btn_close)


func _create_info_label(parent: Container, text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 16)
	l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	l.add_theme_color_override("font_outline_color", COLOR_BORDER)
	l.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		l.add_theme_font_override("font", _cached_font)
	parent.add_child(l)
	return l


func _create_forge_core_slot(def: Dictionary) -> Control:
	var slot_id := str(def.get("id", ""))
	var slot_name := _t(str(def.get("name", "")))
	var slot_desc := _t(str(def.get("desc", "")))

	var card := PanelContainer.new()
	card.name = "SlotCard_" + slot_id
	card.custom_minimum_size = Vector2(132, 0)
	card.add_theme_stylebox_override("panel", _create_panel_style(Color("#FFFDF8"), COLOR_BORDER, 2, 3, 14))

	var vcol := VBoxContainer.new()
	vcol.alignment = BoxContainer.ALIGNMENT_CENTER
	vcol.add_theme_constant_override("separation", 3)
	card.add_child(vcol)

	# 上半部點選選取區域（含 SlotButton）
	var top_area := PanelContainer.new()
	top_area.custom_minimum_size = Vector2(124, 52)
	var top_sb := StyleBoxEmpty.new()
	top_area.add_theme_stylebox_override("panel", top_sb)
	vcol.add_child(top_area)

	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 6)
	row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top_area.add_child(row)

	var icon := TextureRect.new()
	icon.name = "SlotIcon"
	icon.custom_minimum_size = Vector2(38, 38)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var t: Texture2D = SpriteDB.core_slot_icon(slot_id)
	if t:
		icon.texture = t
	row.add_child(icon)

	var part := CoreSystem.get_equipped_part(slot_id)
	var tier_id: String = str(part.get("tier", "white"))
	var tier_name: String = str(part.get("tier_name", "白"))
	var tier_color: Color = CoreSystem.get_tier_color(tier_id) if not part.is_empty() else Color(0.72, 0.62, 0.82, 0.5)
	var count: int = int(part.get("calibration_count", 0))
	var max_cnt: int = int(part.get("max_calibrations", 7))
	var remains: int = maxi(0, max_cnt - count) if not part.is_empty() else 0
	icon.modulate = tier_color

	var col := VBoxContainer.new()
	col.alignment = BoxContainer.ALIGNMENT_CENTER
	col.add_theme_constant_override("separation", 1)
	col.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(col)

	var name_lbl := Label.new()
	name_lbl.name = "SlotName"
	name_lbl.text = slot_name
	name_lbl.add_theme_font_size_override("font_size", 12)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	name_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	name_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	col.add_child(name_lbl)

	var tier_lbl := Label.new()
	tier_lbl.name = "TierLabel"
	tier_lbl.text = _t(tier_name + "階") if not part.is_empty() else _t("未裝備")
	tier_lbl.add_theme_font_size_override("font_size", 11)
	tier_lbl.add_theme_color_override("font_color", tier_color if (not part.is_empty() and tier_id != "white") else COLOR_TEXT_DARK)
	tier_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	tier_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		tier_lbl.add_theme_font_override("font", _cached_font)
	col.add_child(tier_lbl)

	var count_lbl := Label.new()
	count_lbl.name = "CountLabel"
	count_lbl.text = _t("剩餘 %d 次") % remains if not part.is_empty() else ""
	count_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	count_lbl.add_theme_font_size_override("font_size", 10)
	count_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	count_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	count_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		count_lbl.add_theme_font_override("font", _cached_font)
	vcol.add_child(count_lbl)

	var desc_lbl := Label.new()
	desc_lbl.name = "SlotDesc"
	desc_lbl.text = slot_desc
	desc_lbl.visible = false
	card.add_child(desc_lbl)

	# 點選檢視按鈕（熱區 >= 48px）
	var btn := Button.new()
	btn.name = "SlotButton"
	btn.flat = true
	btn.custom_minimum_size = Vector2(124, 52)
	btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	btn.tooltip_text = "%s\n%s" % [slot_name, slot_desc]
	top_area.add_child(btn)

	# 單次拇指校準按鈕（尺寸 118x48，熱區 >= 48px）
	var btn_cal := Button.new()
	btn_cal.name = "BtnCalibrate"
	btn_cal.custom_minimum_size = Vector2(118, 48)
	btn_cal.text = _t("校準") if remains > 0 else _t("已達上限")
	if part.is_empty():
		btn_cal.text = _t("未裝備")
	btn_cal.disabled = (remains <= 0 or part.is_empty())
	btn_cal.add_theme_font_size_override("font_size", 13)
	btn_cal.add_theme_color_override("font_color", Color.WHITE)
	btn_cal.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_cal.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		btn_cal.add_theme_font_override("font", _cached_font)
	btn_cal.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 4, 14, 2))
	btn_cal.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB74D"), COLOR_BORDER, 4, 14, 2))
	btn_cal.add_theme_stylebox_override("pressed", _create_button_style(Color("#F57C00"), COLOR_BORDER, 2, 14, 2))
	btn_cal.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 2, 14, 2))
	vcol.add_child(btn_cal)

	# 卸下果凍厚底按鈕（高 >= 50px、熱區 >= 48px，零系統 emoji，空槽不出現）
	var btn_unequip := Button.new()
	btn_unequip.name = "BtnUnequip"
	btn_unequip.custom_minimum_size = Vector2(118, 50)
	btn_unequip.text = _t("卸下")
	btn_unequip.add_theme_font_size_override("font_size", 13)
	btn_unequip.add_theme_color_override("font_color", Color.WHITE)
	btn_unequip.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_unequip.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		btn_unequip.add_theme_font_override("font", _cached_font)
	btn_unequip.add_theme_stylebox_override("normal", _create_button_style(Color("#FF5E8A"), COLOR_BORDER, 5, 14, 2))
	btn_unequip.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7096"), COLOR_BORDER, 5, 14, 2))
	btn_unequip.add_theme_stylebox_override("pressed", _create_button_style(Color("#E04E78"), COLOR_BORDER, 2, 14, 2))
	btn_unequip.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 2, 14, 2))
	btn_unequip.pressed.connect(func():
		AudioManager.play_ui()
		CoreSystem.unequip_part(slot_id)
		_refresh_all_forge_core_slots()
		_refresh_display()
	)
	if not part.is_empty():
		vcol.add_child(btn_unequip)

	var update_forge_card_ui = func():
		var p = CoreSystem.get_equipped_part(slot_id)
		var tid: String = str(p.get("tier", "white"))
		var tnm: String = str(p.get("tier_name", "白"))
		var tc: Color = CoreSystem.get_tier_color(tid) if not p.is_empty() else Color(0.72, 0.62, 0.82, 0.5)
		var cnt: int = int(p.get("calibration_count", 0))
		var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - cnt) if not p.is_empty() else 0
		var scrap: int = CoreSystem.get_player_scrap()
		var cost: int = CoreSystem.get_calibration_scrap_cost()
		var has_scrap: bool = (scrap >= cost)

		name_lbl.text = _t(str(def.get("name", "")))
		btn.tooltip_text = "%s\n%s" % [_t(str(def.get("name", ""))), _t(str(def.get("desc", "")))]
		icon.modulate = tc
		tier_lbl.text = _t(tnm + "階") if not p.is_empty() else _t("未裝備")
		tier_lbl.add_theme_color_override("font_color", tc if (not p.is_empty() and tid != "white") else COLOR_TEXT_DARK)
		count_lbl.text = _t("剩餘 %d 次") % rem if not p.is_empty() else ""

		var can_cal := (not p.is_empty() and rem > 0 and has_scrap)
		btn_cal.disabled = not can_cal
		if p.is_empty():
			btn_cal.text = _t("未裝備")
		elif rem <= 0:
			btn_cal.text = _t("已達上限")
		elif not has_scrap:
			btn_cal.text = _t("鐵屑不足")
		else:
			btn_cal.text = _t("校準")

		var bu: Button = card.find_child("BtnUnequip", true, false) as Button
		if not p.is_empty():
			if bu == null:
				vcol.add_child(btn_unequip)
				bu = btn_unequip
			bu.visible = true
			bu.text = _t("卸下")
		else:
			if bu != null:
				bu.visible = false

		return {"tier_name": tnm, "remains": rem, "part": p, "has_scrap": has_scrap}

	card.set_meta("update_ui", update_forge_card_ui)
	update_forge_card_ui.call()

	btn_cal.pressed.connect(func():
		AudioManager.play_ui()
		var p_check = CoreSystem.get_equipped_part(slot_id)
		if p_check.is_empty():
			return
		var res: Dictionary = CoreSystem.calibrate_player_part(slot_id)
		_refresh_all_forge_core_slots()
		_refresh_display()
		var p = CoreSystem.get_equipped_part(slot_id)
		var tnm: String = str(p.get("tier_name", "白"))
		var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
		var tip: String = str(res.get("message", ""))
		var tip_k: String = str(res.get("message_key", ""))
		_last_calibrate_state = {
			"slot_name": str(def.get("name", "")),
			"tip": tip,
			"tip_key": tip_k,
			"tier_name": tnm,
			"rem": rem,
			"ok": bool(res.get("ok", false))
		}
		_update_calibrate_message()
	)

	btn.pressed.connect(func():
		AudioManager.play_ui()
		var p = CoreSystem.get_equipped_part(slot_id)
		var sname: String = _t(str(def.get("name", "")))
		var sdesc: String = _t(str(def.get("desc", "")))
		if p.is_empty():
			if is_instance_valid(_msg_label):
				_msg_label.text = _t("【%s】未裝備機芯") % sname
				_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
			return
		var tnm: String = _t(str(p.get("tier_name", "白")))
		var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
		var scrap: int = CoreSystem.get_player_scrap()
		var cost: int = CoreSystem.get_calibration_scrap_cost()
		if is_instance_valid(_msg_label):
			if rem <= 0:
				_msg_label.text = _t("【%s】%s（已達最大校準次數上限 7 次）") % [sname, sdesc]
			elif scrap < cost:
				_msg_label.text = _t("【%s】%s · 鐵屑不足（持有 %d/%d）· 剩餘校準 %d 次") % [sname, sdesc, scrap, cost, rem]
			else:
				_msg_label.text = _t("【%s】%s（目前色階：%s階 · 每次消耗 %d 鐵屑 · 剩餘校準 %d 次）") % [sname, sdesc, tnm, cost, rem]
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	)

	return card


func _refresh_iron_scrap_display() -> void:
	if not _scrap_label or not is_instance_valid(_scrap_label):
		return
	var scrap: int = int(GameState.iron_scrap) if "iron_scrap" in GameState else CoreSystem.get_player_scrap()
	var cost: int = CoreSystem.get_calibration_scrap_cost()
	_scrap_label.text = _t("鐵屑：%d（每次消耗 %d）") % [scrap, cost]
	var is_insufficient: bool = (scrap < cost)
	if is_insufficient:
		if _iron_scrap_capsule and is_instance_valid(_iron_scrap_capsule):
			_iron_scrap_capsule.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_PINK, COLOR_PINK, 2, 4, 18))
		_scrap_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
		if _btn_go_dismantle and is_instance_valid(_btn_go_dismantle):
			_btn_go_dismantle.visible = true
	else:
		if _iron_scrap_capsule and is_instance_valid(_iron_scrap_capsule):
			_iron_scrap_capsule.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
		_scrap_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		if _btn_go_dismantle and is_instance_valid(_btn_go_dismantle):
			_btn_go_dismantle.visible = false


func _refresh_all_forge_core_slots() -> void:
	_refresh_iron_scrap_display()
	var core_row = find_child("ForgeCoreSlotsRow", true, false)
	if core_row:
		for card in core_row.get_children():
			if card is Control and card.has_meta("update_ui"):
				var fn = card.get_meta("update_ui")
				if fn is Callable:
					fn.call()


func get_slot_chips() -> Array[Button]:
	return _slot_chips


func get_active_slot_index() -> int:
	return _active_slot_idx


func get_active_weapon_inst() -> Dictionary:
	return _current_weapon_inst()


## 設定或自動選中特定裝備/武器為鍛造目標
func select_target_equipment(target: Variant) -> void:
	if target == null:
		return
	var es := _get_equip_sys()
	var target_str := str(target).strip_edges()
	var target_uid := ""
	var target_id := ""
	if target is String:
		target_uid = target_str
		target_id = target_str
	elif target is Dictionary:
		target_uid = str(target.get("uid", target.get("id", ""))).strip_edges()
		target_id = str(target.get("id", target.get("base_id", target_uid))).strip_edges()
		target_str = target_uid if not target_uid.is_empty() else target_id

	# 1. 檢查是否已在武器槽位 0, 1, 2 中
	for i in range(3):
		var uid := ""
		if es and es.has_method("loadout_uid"):
			uid = str(es.call("loadout_uid", i))
		elif "weapon_loadout" in GameState and GameState.weapon_loadout != null and i < GameState.weapon_loadout.size():
			uid = str(GameState.weapon_loadout[i])
		if not uid.is_empty():
			if uid == target_uid or uid == target_id:
				_on_slot_chip_pressed(i)
				return
			var inst: Dictionary = {}
			if es and es.has_method("weapon_inst"):
				inst = es.call("weapon_inst", uid)
			elif GameState.equip_worn != null and GameState.equip_worn.has(uid):
				inst = GameState.equip_worn[uid]
			if not inst.is_empty():
				if str(inst.get("uid", "")) == target_uid or str(inst.get("base_id", "")) == target_id or str(inst.get("id", "")) == target_id:
					_on_slot_chip_pressed(i)
					return

	# 2. 若未裝備在槽位中，檢查裝備庫 (equip_bag / find_any) 並自動裝入當前作用槽位
	if es and es.has_method("equip_weapon_to_loadout"):
		var bag_inst: Dictionary = {}
		if es.has_method("find_bag"):
			bag_inst = es.call("find_bag", target_uid)
		if bag_inst.is_empty() and es.has_method("find_any"):
			bag_inst = es.call("find_any", target_uid)
		if bag_inst.is_empty() and "equip_bag" in GameState and GameState.equip_bag is Array:
			for e in GameState.equip_bag:
				if e is Dictionary and (str(e.get("uid", "")) == target_uid or str(e.get("base_id", "")) == target_id or str(e.get("id", "")) == target_id):
					bag_inst = e
					break
		if not bag_inst.is_empty():
			var real_uid := str(bag_inst.get("uid", target_uid))
			es.call("equip_weapon_to_loadout", real_uid, _active_slot_idx)
			_sync_state_from_weapon()
			_refresh_display()
			_refresh_slot_chips()
			return

	# 3. 若為純字典或裝備定義，同步至當前鍛造目標
	if target is Dictionary:
		var r: Dictionary = target.get("rolled", {})
		GameState.weapon_atk = int(r.get("atk", target.get("atk", GameState.weapon_atk)))
		GameState.weapon_tier = int(target.get("tier", GameState.weapon_tier))
		GameState.weapon_name = str(target.get("name", GameState.weapon_name))
	elif not target_id.is_empty():
		GameState.weapon_name = target_id
	_refresh_display()
	_refresh_slot_chips()


func get_quality_label() -> Label:
	return _quality_label


func get_affix_label() -> Label:
	return _affix_label


func _get_quality_color(q: String) -> Color:
	match q:
		"common": return Color("#8E8A9F")
		"uncommon": return Color("#2E9E4A")
		"rare": return Color("#2575FC")
		"epic": return Color("#9B51E0")
		_: return Color("#8E8A9F")


func _style_chip_btn(btn: Button, bg: Color, text_col: Color, font_sz: int, bottom_px: int = 4, radius: int = 14, border_col: Color = COLOR_BORDER) -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border_col
	sb.set_border_width_all(2)
	sb.border_width_bottom = bottom_px
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	if bottom_px > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = bg.lightened(0.08)

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.bg_color = bg.darkened(0.08)
	sb_p.border_width_bottom = 2

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("disabled", sb)
	btn.add_theme_color_override("font_color", text_col)
	btn.add_theme_color_override("font_hover_color", text_col)
	btn.add_theme_color_override("font_pressed_color", text_col)
	btn.add_theme_color_override("font_disabled_color", text_col)
	btn.add_theme_font_size_override("font_size", font_sz)
	if _cached_font:
		btn.add_theme_font_override("font", _cached_font)


func _on_slot_chip_pressed(slot_idx: int) -> void:
	if AudioManager.has_method("play_ui"):
		AudioManager.play_ui()
	var es := _get_equip_sys()
	var req_lv := 10 if slot_idx == 1 else 16
	if es and es.has_method("loadout_unlock_level"):
		req_lv = int(es.call("loadout_unlock_level", slot_idx))

	var unlocked := true
	if es and es.has_method("loadout_slot_unlocked"):
		unlocked = bool(es.call("loadout_slot_unlocked", slot_idx))
	elif GameState.level < req_lv:
		unlocked = (slot_idx == 0)

	if not unlocked:
		if is_instance_valid(_msg_label):
			_msg_label.text = _t("武器欄 %d 需達到 Lv%d 解鎖") % [slot_idx + 1, req_lv]
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
		return

	if es and es.has_method("switch_weapon_loadout"):
		var res: Dictionary = es.call("switch_weapon_loadout", slot_idx)
		if not bool(res.get("ok", false)):
			var uid: String = str(es.call("loadout_uid", slot_idx)) if es.has_method("loadout_uid") else ""
			if uid.is_empty():
				_active_slot_idx = slot_idx
				if "weapon_loadout_active" in GameState:
					GameState.weapon_loadout_active = slot_idx
				if is_instance_valid(_msg_label):
					_msg_label.text = _t("武器欄 %d 尚未裝備武器") % [slot_idx + 1]
					_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
				_refresh_display()
				return
			else:
				if is_instance_valid(_msg_label):
					_msg_label.text = str(res.get("msg", _t("無法切換該槽位武器")))
					_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
				return
	else:
		_active_slot_idx = slot_idx
		if "weapon_loadout_active" in GameState:
			GameState.weapon_loadout_active = slot_idx
		if "weapon_loadout" in GameState and slot_idx < GameState.weapon_loadout.size():
			var uid := str(GameState.weapon_loadout[slot_idx])
			if uid.is_empty():
				if is_instance_valid(_msg_label):
					_msg_label.text = _t("武器欄 %d 尚未裝備武器") % [slot_idx + 1]
					_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
				_refresh_display()
				return
			if GameState.equip_slots != null:
				GameState.equip_slots["weapon"] = uid

	_active_slot_idx = slot_idx
	_sync_state_from_weapon()
	if is_instance_valid(_msg_label):
		var inst := _current_weapon_inst()
		var wname := _t(str(inst.get("name", GameState.weapon_name)))
		_msg_label.text = _t("已切換至武器槽位 %d：【%s】") % [slot_idx + 1, wname]
		_msg_label.add_theme_color_override("font_color", COLOR_MINT)
	_refresh_display()


func _refresh_slot_chips() -> void:
	var es := _get_equip_sys()
	for i in range(_slot_chips.size()):
		var chip: Button = _slot_chips[i]
		var unlocked := true
		var req_lv := 10 if i == 1 else 16
		if es and es.has_method("loadout_slot_unlocked"):
			unlocked = bool(es.call("loadout_slot_unlocked", i))
			if es.has_method("loadout_unlock_level"):
				req_lv = int(es.call("loadout_unlock_level", i))
		elif GameState.level < req_lv:
			unlocked = (i == 0)

		if not unlocked:
			chip.text = _t("槽位 %d（需 Lv%d）") % [i + 1, req_lv]
			_style_chip_btn(chip, COLOR_CARD_MUTED, COLOR_TEXT_DIM, 13, 2, 14, COLOR_BORDER_MUTED)
			continue

		var uid := ""
		if es and es.has_method("loadout_uid"):
			uid = str(es.call("loadout_uid", i))
		elif "weapon_loadout" in GameState and GameState.weapon_loadout != null and i < GameState.weapon_loadout.size():
			uid = str(GameState.weapon_loadout[i])

		var wname := ""
		var wtier := 1
		if not uid.is_empty():
			var inst: Dictionary = {}
			if es and es.has_method("weapon_inst"):
				inst = es.call("weapon_inst", uid)
			if inst.is_empty() and GameState.equip_worn != null and GameState.equip_worn.has(uid):
				inst = GameState.equip_worn[uid]
			if not inst.is_empty():
				wname = _t(str(inst.get("name", "武器")))
				wtier = int(inst.get("tier", 1))

		var text_str := ""
		if wname.is_empty():
			text_str = _t("槽位 %d · 空槽") % [i + 1]
		else:
			text_str = _t("槽位 %d · %s") % [i + 1, "%s (T%d)" % [wname, wtier]]

		chip.text = text_str
		if i == _active_slot_idx:
			_style_chip_btn(chip, COLOR_ORANGE, COLOR_TEXT_DARK, 14, 5, 14)
		else:
			_style_chip_btn(chip, COLOR_CARD_WARM, COLOR_TEXT_DARK, 13, 3, 14)


func _format_affixes(inst: Dictionary) -> String:
	var affixes: Array[String] = []
	var r: Dictionary = inst.get("rolled", {})
	if r.has("crit") and float(r["crit"]) > 0.0:
		affixes.append(_t("暴擊 +%.1f%%") % float(r["crit"]))
	if r.has("crit_dmg") and float(r["crit_dmg"]) > 0.0:
		affixes.append(_t("暴傷 +%.1f%%") % float(r["crit_dmg"]))
	if r.has("def") and int(r["def"]) > 0:
		affixes.append(_t("防禦 +%d") % int(r["def"]))
	if r.has("hp") and int(r["hp"]) > 0:
		affixes.append(_t("生命 +%d") % int(r["hp"]))
	if r.has("speed") and int(r["speed"]) > 0:
		affixes.append(_t("速度 +%d") % int(r["speed"]))
	if r.has("penetration") and int(r["penetration"]) > 0:
		affixes.append(_t("穿透 +%d") % int(r["penetration"]))
	if inst.has("affixes") and inst["affixes"] is Array:
		for af in inst["affixes"]:
			if af is Dictionary:
				var af_name := _t(str(af.get("name", "")))
				var af_val: Variant = af.get("value", 0)
				if not af_name.is_empty():
					affixes.append("%s +%s" % [af_name, str(af_val)])
			elif af is String and not str(af).is_empty():
				affixes.append(_t(str(af)))

	if affixes.is_empty():
		return _t("副詞條：暫無")
	return _t("副詞條：%s") % " · ".join(affixes)


func _refresh_display() -> void:
	if not is_instance_valid(_weapon_label) or not is_instance_valid(_btn_forge):
		return

	if is_instance_valid(_power_label):
		_power_label.text = _t("戰力 %d") % GameState.power_score()

	_refresh_slot_chips()

	var inst := _current_weapon_inst()
	var is_empty_slot := inst.is_empty() and (_active_slot_idx > 0 or GameState.weapon_name.is_empty())

	if is_empty_slot:
		_weapon_label.text = _t("當前裝備：空槽（尚未裝備武器）")
		if is_instance_valid(_quality_label):
			_quality_label.text = _t("品質色階：未裝備")
			_quality_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_atk_label.text = _t("武器攻擊：+0")
		_gold_label.text = _t("持有金幣：%d") % GameState.gold
		_cost_label.text = _t("升階花費：—")
		_rate_label.text = _t("基礎成功率：—")
		if is_instance_valid(_affix_label):
			_affix_label.text = _t("副詞條：無")
		_slots_label.text = _t("魂槽開放：—")
		_btn_forge.text = _t("當前槽位無武器可鍛造")
		_btn_forge.disabled = true
		if is_instance_valid(_btn_auto_forge):
			_btn_auto_forge.disabled = true
		for seg in _pity_bars:
			seg.value = 0.0
		_pity_title_label.text = _t("當前槽位未裝備武器")
		_pity_sub_label.text = _t("請至背包或兵器架裝備武器後再進行鍛造")
		return

	var cur_tier := int(inst.get("tier", GameState.weapon_tier))
	var at_max := cur_tier >= ForgeSystem.FORGE_MAX_TIER
	var wname := _t(str(inst.get("name", GameState.weapon_name)))
	_weapon_label.text = _t("當前裝備：%s（第 %d 階）") % [wname, cur_tier]
	_atk_label.text = _t("武器攻擊：+%d") % _current_weapon_atk()
	_gold_label.text = _t("持有金幣：%d") % GameState.gold

	if is_instance_valid(_quality_label):
		var q_key := str(inst.get("quality", "common"))
		var q_label := _t(str(inst.get("quality_label", "凡品")))
		_quality_label.text = _t("品質色階：%s") % q_label
		_quality_label.add_theme_color_override("font_color", _get_quality_color(q_key))

	var cost := ForgeSystem.forge_cost()
	if at_max:
		_cost_label.text = _t("升階花費：已達上限")
		_rate_label.text = _t("成功率：已封頂")
		_btn_forge.text = _t("鍛造已封頂")
		_btn_forge.disabled = true
		if is_instance_valid(_btn_auto_forge):
			_btn_auto_forge.disabled = true
	else:
		_cost_label.text = _t("升階花費：%d 金幣") % cost
		var rate_pct := int(ForgeSystem.forge_rate_base() * 100.0)
		_rate_label.text = _t("基礎成功率：%d%%") % rate_pct
		_btn_forge.text = _t("強化升階（消耗 %d 金幣）") % cost
		_btn_forge.disabled = false
		if is_instance_valid(_btn_auto_forge):
			_btn_auto_forge.disabled = false

	if is_instance_valid(_affix_label):
		_affix_label.text = _format_affixes(inst)

	# 魂槽狀態
	var slots := SoulSystem.slot_count()
	var next_slot := 0
	for need in SoulSystem.SLOT_TIERS:
		if cur_tier < need:
			next_slot = need
			break
	if next_slot > 0:
		_slots_label.text = _t("魂槽開放：%d/%d 槽（下一槽需器階 %d）") % [slots, SoulSystem.SLOT_TIERS.size(), next_slot]
	else:
		_slots_label.text = _t("魂槽開放：%d/%d 槽（已全數開放）") % [slots, SoulSystem.SLOT_TIERS.size()]

	# 保底進度條
	var streak: int = clampi(GameState.forge_fail_streak, 0, 3)
	if at_max:
		_pity_title_label.text = _t("器階已達上限 · 鍛造已封頂")
		_pity_sub_label.text = _t("所有階級均已鍛造完成")
	elif streak < 3:
		_pity_title_label.text = _t("鍛造連敗保底 %d/3 · 滿 3 格釘釘摔錘必成功") % streak
		if streak == 2:
			_pity_sub_label.text = _t("再失敗 1 次將觸發第 3 格摔錘保底")
		elif streak == 1:
			_pity_sub_label.text = _t("升階失敗累積 1 格 · 升階成功清空進度")
		else:
			_pity_sub_label.text = _t("累積 3 次升階失敗將啟動必成功保底機制")
	else:
		_pity_title_label.text = _t("保底已滿 3/3 · 本次升階釘釘摔錘必成功！")
		_pity_sub_label.text = _t("保底已觸發 · 釘釘發脾氣必定升階")

	for i in range(_pity_bars.size()):
		_pity_bars[i].value = 1.0 if streak > i else 0.0


func _on_forge_pressed() -> void:
	var res: Dictionary = ForgeSystem.try_forge()
	match str(res.get("code", "")):
		"tier_max":
			_msg_label.text = _t("器階已達上限，無法再進行鍛造！")
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		"no_gold":
			var cost: int = int(res.get("cost", ForgeSystem.forge_cost()))
			_msg_label.text = _t("金幣不足！升階需要 %d 金幣。") % cost
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
		"success":
			var scrap_tip := _t("（消耗鐵屑穩火）") if bool(res.get("used_scrap", false)) else ""
			_msg_label.text = _t("鍛造成功！升階至第 %d 階，攻擊力上升！%s") % [GameState.weapon_tier, scrap_tip]
			_msg_label.add_theme_color_override("font_color", COLOR_MINT)
			var es := _get_equip_sys()
			if es == null:
				var inst := _current_weapon_inst()
				if not inst.is_empty() and inst.has("uid"):
					var uid: String = str(inst["uid"])
					if GameState.equip_worn != null and GameState.equip_worn.has(uid):
						var w: Dictionary = GameState.equip_worn[uid]
						w["tier"] = GameState.weapon_tier
						if not w.has("rolled"):
							w["rolled"] = {}
						w["rolled"]["atk"] = GameState.weapon_atk
		"pity_break":
			_msg_label.text = _t("鍛造失敗！釘釘摔錘了，吃塊消氣餅回復體力！")
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
		"failed":
			var streak: int = int(res.get("fail_streak", GameState.forge_fail_streak))
			_msg_label.text = _t("鍛造失敗！累積 1 格保底進度（目前 %d/3 格）。") % streak
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
	_refresh_display()


func _on_auto_forge_pressed() -> void:
	if AudioManager.has_method("play_ui"):
		AudioManager.play_ui()
	var res: Dictionary = ForgeSystem.auto_forge(10)
	var es := _get_equip_sys()
	if es == null:
		var inst := _current_weapon_inst()
		if not inst.is_empty() and inst.has("uid"):
			var uid: String = str(inst["uid"])
			if GameState.equip_worn != null and GameState.equip_worn.has(uid):
				var w: Dictionary = GameState.equip_worn[uid]
				w["tier"] = GameState.weapon_tier
				if not w.has("rolled"):
					w["rolled"] = {}
				w["rolled"]["atk"] = GameState.weapon_atk

	var tries: int = int(res.get("tries", 0))
	var success_count: int = int(res.get("success_count", 0))
	var atk_gain: int = int(res.get("atk_gain", 0))
	var spent_gold: int = int(res.get("spent_gold", 0))
	var spent_scrap: int = int(res.get("spent_scrap", 0))
	var stop_reason: String = str(res.get("stop_reason", ""))
	var code: String = str(res.get("code", ""))

	if tries == 0:
		match code:
			"tier_max":
				_msg_label.text = _t("器階已達上限，無法再進行鍛造！")
				_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
			"no_gold":
				_msg_label.text = _t("金幣不足！無法進行一鍵鍛造。")
				_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
			"no_scrap":
				_msg_label.text = _t("鐵屑不足！一鍵鍛造需要鐵屑穩火。")
				_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
			_:
				_msg_label.text = _t("目前條件無法進行一鍵鍛造。")
				_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	else:
		if success_count > 0:
			_msg_label.text = _t("一鍵鍛造完成！成功 %d 次（嘗試 %d 次）· 攻擊力 +%d · 消耗 %d 金幣、%d 鐵屑") % [success_count, tries, atk_gain, spent_gold, spent_scrap]
			_msg_label.add_theme_color_override("font_color", COLOR_MINT)
		else:
			_msg_label.text = _t("一鍵鍛造結束：嘗試 %d 次全數失敗 · 消耗 %d 金幣、%d 鐵屑") % [tries, spent_gold, spent_scrap]
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)

	_refresh_display()


func get_auto_forge_button() -> Button:
	return _btn_auto_forge


func get_auto_calibrate_button() -> Button:
	return _btn_auto_calibrate


func get_unequip_all_cores_button() -> Button:
	return _btn_unequip_all


func get_unequip_all_button() -> Button:
	return _btn_unequip_all


func get_current_toast() -> Label:
	return _current_toast


func auto_calibrate_cores() -> Dictionary:
	# 1. 檢查鐵屑是否充足 (GameState.iron_scrap 與 CoreSystem.has_enough_scrap_to_calibrate)
	var scrap: int = int(GameState.iron_scrap) if "iron_scrap" in GameState else CoreSystem.get_player_scrap()
	var cost: int = CoreSystem.get_calibration_scrap_cost()
	if scrap < cost or not CoreSystem.has_enough_scrap_to_calibrate():
		var err_msg := _t("鐵屑不足！無法進行一鍵校準。")
		if is_instance_valid(_msg_label):
			_msg_label.text = err_msg
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_PINK)
		_show_toast(err_msg)
		return {
			"ok": false,
			"code": "no_scrap",
			"message": err_msg,
			"total_calibrated": 0,
			"power_gain": 0,
			"spent_scrap": 0
		}

	# 2. 檢查已裝備機芯部件是否可校準
	var slot_defs: Array = SpriteDB.CORE_SLOT_DEFS
	var has_equipped := false
	var has_eligible := false
	for def in slot_defs:
		var slot_id: String = str(def.get("id", ""))
		var norm: String = CoreSystem.normalize_slot_id(slot_id)
		var p: Dictionary = CoreSystem.get_equipped_part(norm)
		if not p.is_empty():
			has_equipped = true
			var cnt: int = int(p.get("calibration_count", 0))
			var max_c: int = int(p.get("max_calibrations", CoreSystem.MAX_CALIBRATIONS))
			var cur_score: int = int(p.get("score", 0))
			var tier_info := CoreSystem.get_tier_by_score(cur_score)
			var tid: String = str(tier_info.get("id", p.get("tier", "white")))
			if cnt < max_c and tid != CoreSystem.TIER_RED and CoreSystem.can_calibrate(p):
				has_eligible = true
				break

	if not has_equipped:
		var no_eq_msg := _t("未裝備任何可校準的機芯部位！")
		if is_instance_valid(_msg_label):
			_msg_label.text = no_eq_msg
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_show_toast(no_eq_msg)
		return {
			"ok": false,
			"code": "no_equipped",
			"message": no_eq_msg,
			"total_calibrated": 0,
			"power_gain": 0,
			"spent_scrap": 0
		}

	if not has_eligible:
		var maxed_msg := _t("所有部位均已達上限或已滿色階！")
		if is_instance_valid(_msg_label):
			_msg_label.text = maxed_msg
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_show_toast(maxed_msg)
		return {
			"ok": false,
			"code": "all_maxed",
			"message": maxed_msg,
			"total_calibrated": 0,
			"power_gain": 0,
			"spent_scrap": 0
		}

	# 3. 依順序循環對已裝備機芯執行 CoreSystem.calibrate_player_part()，直到鐵屑不足或所有部位校準次數耗盡
	var initial_power := GameState.power_score()
	var total_calibrated: int = 0
	var total_spent_scrap: int = 0
	var any_in_round := true

	while any_in_round:
		any_in_round = false
		for def in slot_defs:
			if not CoreSystem.has_enough_scrap_to_calibrate():
				break
			var slot_id: String = str(def.get("id", ""))
			var norm: String = CoreSystem.normalize_slot_id(slot_id)
			var part: Dictionary = CoreSystem.get_equipped_part(norm)
			if part.is_empty():
				continue
			if not CoreSystem.can_calibrate(part):
				continue
			var cnt: int = int(part.get("calibration_count", 0))
			var max_c: int = int(part.get("max_calibrations", CoreSystem.MAX_CALIBRATIONS))
			if cnt >= max_c:
				continue
			var cur_score: int = int(part.get("score", 0))
			var tier_info := CoreSystem.get_tier_by_score(cur_score)
			var tid: String = str(tier_info.get("id", part.get("tier", "white")))
			if tid == CoreSystem.TIER_RED:
				continue

			var res: Dictionary = CoreSystem.calibrate_player_part(norm)
			if not bool(res.get("rejected", false)):
				total_calibrated += 1
				total_spent_scrap += int(res.get("used_scrap", CoreSystem.get_calibration_scrap_cost()))
				any_in_round = true
			else:
				if not CoreSystem.has_enough_scrap_to_calibrate():
					break
		if not CoreSystem.has_enough_scrap_to_calibrate():
			break

	_last_calibrate_state.clear()

	# 4. 即時更新五槽色階、屬性數值、頂部戰力與飄字提示 (Toast)
	_refresh_all_forge_core_slots()
	_refresh_display()

	var final_power := GameState.power_score()
	var power_gain := final_power - initial_power

	var feedback_msg := ""
	if total_calibrated > 0:
		if power_gain > 0:
			feedback_msg = _t("一鍵校準完成！共校準 %d 次 · 戰力提升 +%d · 消耗 %d 鐵屑") % [total_calibrated, power_gain, total_spent_scrap]
		else:
			feedback_msg = _t("一鍵校準完成！共校準 %d 次 · 消耗 %d 鐵屑") % [total_calibrated, total_spent_scrap]
		if is_instance_valid(_msg_label):
			_msg_label.text = feedback_msg
			_msg_label.add_theme_color_override("font_color", COLOR_GOLD if power_gain > 0 else COLOR_TEXT_DARK)
		_show_toast(feedback_msg)
	else:
		feedback_msg = _t("所有部位均已達上限或已滿色階！")
		if is_instance_valid(_msg_label):
			_msg_label.text = feedback_msg
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_show_toast(feedback_msg)

	return {
		"ok": total_calibrated > 0,
		"total_calibrated": total_calibrated,
		"power_gain": power_gain,
		"spent_scrap": total_spent_scrap,
		"remaining_scrap": CoreSystem.get_player_scrap(),
		"message": feedback_msg
	}


func _on_auto_calibrate_pressed() -> void:
	if AudioManager.has_method("play_ui"):
		AudioManager.play_ui()
	auto_calibrate_cores()


func _on_unequip_all_cores_pressed() -> void:
	if AudioManager.has_method("play_ui"):
		AudioManager.play_ui()
	unequip_all_cores()


func unequip_all_cores() -> Dictionary:
	var slot_defs: Array = SpriteDB.CORE_SLOT_DEFS
	var equipped_slots: Array = []
	for def in slot_defs:
		var slot_id: String = str(def.get("id", ""))
		var norm: String = CoreSystem.normalize_slot_id(slot_id)
		var p: Dictionary = CoreSystem.get_equipped_part(norm)
		if not p.is_empty():
			equipped_slots.append(norm)

	if equipped_slots.is_empty():
		var no_eq_msg := _t("未裝備任何機芯")
		if is_instance_valid(_msg_label):
			_msg_label.text = no_eq_msg
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_show_toast(no_eq_msg)
		return {
			"ok": false,
			"code": "no_equipped",
			"message": no_eq_msg,
			"unequipped_count": 0
		}

	var unequipped_count: int = 0
	for norm in equipped_slots:
		var old: Dictionary = CoreSystem.unequip_part(norm)
		if not old.is_empty():
			unequipped_count += 1

	_last_calibrate_state.clear()
	_refresh_all_forge_core_slots()
	_refresh_display()

	var success_msg := _t("已卸下所有機芯")
	if is_instance_valid(_msg_label):
		_msg_label.text = success_msg
		_msg_label.add_theme_color_override("font_color", COLOR_GOLD)
	_show_toast(success_msg)

	return {
		"ok": true,
		"code": "success",
		"message": success_msg,
		"unequipped_count": unequipped_count
	}


func _show_toast(msg: String) -> void:
	last_toast_text = msg
	if _current_toast and is_instance_valid(_current_toast):
		_current_toast.queue_free()
		_current_toast = null
	var toast := Label.new()
	toast.name = "ForgeToast"
	_current_toast = toast
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	var toast_w := clampi(int(msg.length() * 12) + 60, 360, 720)
	toast.offset_left = -int(toast_w / 2)
	toast.offset_right = int(toast_w / 2)
	toast.offset_top = 80
	toast.offset_bottom = 128

	var tsb := StyleBoxFlat.new()
	tsb.bg_color = Color(0.12, 0.10, 0.23, 0.95)
	tsb.border_color = COLOR_GOLD
	tsb.set_border_width_all(2)
	tsb.border_width_bottom = 4
	tsb.set_corner_radius_all(14)
	tsb.content_margin_left = 20
	tsb.content_margin_right = 20
	tsb.content_margin_top = 8
	tsb.content_margin_bottom = 10
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", Color("#FFFDF8"))
	toast.add_theme_color_override("font_outline_color", COLOR_BORDER)
	toast.add_theme_constant_override("outline_size", 2)
	toast.add_theme_font_size_override("font_size", 16)
	toast.z_index = 100
	if _cached_font:
		toast.add_theme_font_override("font", _cached_font)
	add_child(toast)

	var tw := create_tween()
	if tw:
		tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
		tw.tween_interval(1.5)
		tw.tween_property(toast, "modulate:a", 0.0, 0.4)
		tw.tween_callback(toast.queue_free)


func get_top_power_label() -> Label:
	return _power_label


func get_msg_label() -> Label:
	return _msg_label


func get_go_workshop_button() -> Button:
	return _btn_go_workshop


func get_iron_scrap_capsule() -> PanelContainer:
	return _iron_scrap_capsule


func get_scrap_label() -> Label:
	return _scrap_label


func get_btn_go_dismantle() -> Button:
	return _btn_go_dismantle


func _on_go_dismantle_pressed() -> void:
	dismantle_requested.emit()
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_maple_inventory"):
			ml.call("open_maple_inventory", "core")
	var p := get_parent()
	if p and p.has_method("open_maple_inventory"):
		p.call("open_maple_inventory", "core")
	if not is_queued_for_deletion():
		_on_close()


func _on_go_workshop_pressed() -> void:
	workshop_requested.emit()
	if not is_queued_for_deletion():
		_on_close()


func get_go_power_stat_button() -> Button:
	return _btn_go_power_stat


func _on_go_power_stat_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	power_stat_requested.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_power_stat_dialog"):
			if power_stat_requested.get_connections().is_empty():
				ml.call("open_power_stat_dialog")
	var p := get_parent()
	if p and p.has_method("open_power_stat_dialog"):
		if power_stat_requested.get_connections().is_empty():
			p.call("open_power_stat_dialog")
	if not is_queued_for_deletion():
		_on_close()


func get_go_shop_button() -> Button:
	return _btn_go_shop


func _on_go_shop_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	shop_requested.emit()
	go_shop.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_shop"):
			if shop_requested.get_connections().is_empty() and go_shop.get_connections().is_empty():
				ml.call("open_shop")
	var p := get_parent()
	if p and p.has_method("open_shop"):
		if shop_requested.get_connections().is_empty() and go_shop.get_connections().is_empty():
			p.call("open_shop")
	if not is_queued_for_deletion():
		_on_close()


func get_go_inventory_button() -> Button:
	return _btn_go_inventory


func _on_go_inventory_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	closed.emit()
	inventory_requested.emit()
	go_inventory.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_maple_inventory"):
			if inventory_requested.get_connections().is_empty() and go_inventory.get_connections().is_empty():
				ml.call("open_maple_inventory")
	var p := get_parent()
	if p and p.has_method("open_maple_inventory"):
		if inventory_requested.get_connections().is_empty() and go_inventory.get_connections().is_empty():
			p.call("open_maple_inventory")
	if not is_queued_for_deletion():
		_on_close()


func get_go_skill_button() -> Button:
	return _btn_go_skill


func _on_go_skill_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	closed.emit()
	skill_requested.emit()
	go_skill.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_skill_dialog"):
			if skill_requested.get_connections().is_empty() and go_skill.get_connections().is_empty():
				ml.call("open_skill_dialog")
	var p := get_parent()
	if p and p.has_method("open_skill_dialog"):
		if skill_requested.get_connections().is_empty() and go_skill.get_connections().is_empty():
			p.call("open_skill_dialog")
	if not is_queued_for_deletion():
		_on_close()


func get_go_wardrobe_button() -> Button:
	return _btn_go_wardrobe


func get_go_vault_button() -> Button:
	return _btn_go_vault


func get_go_title_wall_button() -> Button:
	return _btn_go_title_wall


func get_action_scroll() -> ScrollContainer:
	return _act_scroll


func _on_go_title_wall_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	closed.emit()
	title_wall_requested.emit()
	go_title_wall.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_title_wall_dialog"):
			if title_wall_requested.get_connections().is_empty() and go_title_wall.get_connections().is_empty():
				ml.call("open_title_wall_dialog")
	var p := get_parent()
	if p and p.has_method("open_title_wall_dialog"):
		if title_wall_requested.get_connections().is_empty() and go_title_wall.get_connections().is_empty():
			p.call("open_title_wall_dialog")
	if not is_queued_for_deletion():
		_on_close()


func _on_go_vault_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	closed.emit()
	vault_requested.emit()
	go_vault.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_clockwork_vault"):
			if vault_requested.get_connections().is_empty() and go_vault.get_connections().is_empty():
				ml.call("open_clockwork_vault")
	var p := get_parent()
	if p and p.has_method("open_clockwork_vault"):
		if vault_requested.get_connections().is_empty() and go_vault.get_connections().is_empty():
			p.call("open_clockwork_vault")
	if not is_queued_for_deletion():
		_on_close()


func _on_go_wardrobe_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	closed.emit()
	wardrobe_requested.emit()
	go_wardrobe.emit()
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var root_node := (loop as SceneTree).root
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml and ml.has_method("open_wardrobe"):
			if wardrobe_requested.get_connections().is_empty() and go_wardrobe.get_connections().is_empty():
				ml.call("open_wardrobe")
	var p := get_parent()
	if p and p.has_method("open_wardrobe"):
		if wardrobe_requested.get_connections().is_empty() and go_wardrobe.get_connections().is_empty():
			p.call("open_wardrobe")
	if not is_queued_for_deletion():
		_on_close()


func _on_close() -> void:
	closed.emit()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	sb.shadow_size = 10
	sb.shadow_offset = Vector2(0, 5)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.35)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb


func _style_dopamine_progress(bar: ProgressBar, fill: Color, bg: Color = Color("#FFFDF8")) -> void:
	var bg_s := StyleBoxFlat.new()
	bg_s.bg_color = bg
	bg_s.border_color = COLOR_BORDER
	bg_s.set_border_width_all(2)
	bg_s.border_width_bottom = 4
	bg_s.set_corner_radius_all(12)

	var fill_s := StyleBoxFlat.new()
	fill_s.bg_color = fill
	fill_s.border_color = COLOR_BORDER
	fill_s.set_border_width_all(1)
	fill_s.border_width_bottom = 2
	fill_s.set_corner_radius_all(10)

	bar.add_theme_stylebox_override("background", bg_s)
	bar.add_theme_stylebox_override("fill", fill_s)
	bar.show_percentage = false


func get_swap_weapon_button() -> Button:
	return _btn_swap_weapon


func get_weapon_swap_dialog() -> Control:
	return _weapon_swap_dialog


func _on_swap_weapon_pressed() -> void:
	swap_weapon_requested.emit(_active_slot_idx)
	open_weapon_swap_dialog(_active_slot_idx)


func open_weapon_swap_dialog(slot_idx: int = -1) -> Control:
	var target_slot := slot_idx if slot_idx >= 0 else _active_slot_idx
	var existing := get_node_or_null("WeaponSwapDialog")
	if existing != null and not existing.is_queued_for_deletion():
		return existing
	var DlgClass: GDScript = load("res://scripts/ui/weapon_swap_dialog.gd")
	if DlgClass == null:
		push_error("無法載入 WeaponSwapDialog")
		return null
	var dlg: Control = DlgClass.new(target_slot) as Control
	dlg.name = "WeaponSwapDialog"
	dlg.z_index = 85
	dlg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if dlg.has_method("setup"):
		dlg.call("setup", target_slot)

	_weapon_swap_dialog = dlg
	dlg.tree_exited.connect(func():
		_weapon_swap_dialog = null
	)

	if dlg.has_signal("weapon_swapped"):
		dlg.weapon_swapped.connect(_on_weapon_swapped_from_dialog)
	if dlg.has_signal("slot_unequipped"):
		dlg.slot_unequipped.connect(_on_slot_unequipped_from_dialog)
	if dlg.has_signal("inventory_requested"):
		dlg.inventory_requested.connect(func():
			if is_instance_valid(_weapon_swap_dialog) and not _weapon_swap_dialog.is_queued_for_deletion():
				_weapon_swap_dialog.queue_free()
				_weapon_swap_dialog = null
			_on_go_inventory_pressed()
		)

	add_child(dlg)
	return dlg


func _on_weapon_swapped_from_dialog(slot_idx: int, uid: String) -> void:
	if is_instance_valid(_weapon_swap_dialog) and not _weapon_swap_dialog.is_queued_for_deletion():
		_weapon_swap_dialog.queue_free()
		_weapon_swap_dialog = null
	_active_slot_idx = clampi(slot_idx, 0, 2)
	var es := _get_equip_sys()
	if es and es.has_method("equip_weapon_to_loadout") and not uid.is_empty():
		var cur_uid: String = str(es.call("loadout_uid", _active_slot_idx)) if es.has_method("loadout_uid") else ""
		if cur_uid != uid:
			es.call("equip_weapon_to_loadout", uid, _active_slot_idx)
	if "weapon_loadout" in GameState and GameState.weapon_loadout != null:
		if _active_slot_idx < GameState.weapon_loadout.size():
			GameState.weapon_loadout[_active_slot_idx] = uid
	if "weapon_loadout_active" in GameState:
		GameState.weapon_loadout_active = _active_slot_idx
	if GameState.equip_slots != null and not uid.is_empty() and _active_slot_idx == 0:
		GameState.equip_slots["weapon"] = uid
	_sync_state_from_weapon()
	_refresh_display()
	_refresh_all_forge_core_slots()
	weapon_swapped.emit(slot_idx, uid)
	if is_instance_valid(_msg_label):
		var inst := _current_weapon_inst()
		var wname := _t(str(inst.get("name", GameState.weapon_name)))
		_msg_label.text = _t("已成功更換槽位 %d 裝備：【%s】") % [slot_idx + 1, wname]
		_msg_label.add_theme_color_override("font_color", COLOR_MINT)



func _on_slot_unequipped_from_dialog(slot_idx: int) -> void:
	if is_instance_valid(_weapon_swap_dialog) and not _weapon_swap_dialog.is_queued_for_deletion():
		_weapon_swap_dialog.queue_free()
		_weapon_swap_dialog = null
	_active_slot_idx = clampi(slot_idx, 0, 2)
	if "weapon_loadout_active" in GameState:
		GameState.weapon_loadout_active = _active_slot_idx
	_sync_state_from_weapon()
	_refresh_display()
	_refresh_all_forge_core_slots()
	if is_instance_valid(_msg_label):
		_msg_label.text = _t("武器欄 %d 尚未裝備武器") % [slot_idx + 1]
		_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)

