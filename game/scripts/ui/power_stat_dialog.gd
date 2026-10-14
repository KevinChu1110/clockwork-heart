class_name PowerStatDialog
extends Control
## 《發條之心》大廳頂部戰力屬性總覽彈窗 (PowerStatDialog)
## 依多巴胺鮮亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗規格：寬 720px，黑曜石底色＋多巴胺卡片底，圓角 18px。
## 2. 右上「✕」關閉按鈕尺寸 50x50px，底部按鈕 140x48px（熱區 >= 48px，果凍厚底 5px）。
## 3. 全螢幕半透明遮罩 (Scrim)，點擊遮罩關閉。
## 4. 整合展示：綜合戰力總覽（成長拆解）、基礎六維屬性、三欄武器裝備貢獻、寶石孔位加成與招式心法加成。
## 5. 零系統 Emoji，使用粉圓體 (Open Huninn)。
## 6. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換刷新)。

signal closed()
signal equip_requested()
signal workshop_requested()
signal skill_requested()
signal soul_requested()
signal calibrate_requested()
signal forge_requested()
signal title_wall_requested()
signal inventory_requested()
signal colossus_requested()
signal go_dummy_practice()
signal vault_requested()
signal windup_daily_requested()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var soul_res := ContentLoc.text("soul", s)
	if soul_res != s:
		return soul_res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD         := Color("#FFD028")  ## 金黃
const COLOR_ORANGE       := Color("#FFA010")  ## 暖橘
const COLOR_MINT         := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY          := Color("#38A0FF")  ## 天藍
const COLOR_PINK         := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER       := Color("#1F1A3A")  ## 深藍紫描邊

## ── 底色規範 ──
const COLOR_OBSIDIAN     := Color("#141118")  ## 黑曜石底色
const COLOR_BG_CARD      := Color("#1E1A26")  ## 暗卡片深底
const COLOR_CARD_WARM    := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD    := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_SKY     := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_MINT    := Color("#EAF9EE")  ## 柔和薄荷卡片底
const COLOR_CARD_MUTED   := Color("#EFEBE0")  ## 壓暗奶油底
const COLOR_BORDER_MUTED := Color("#D2CCC0")  ## 壓暗淡邊框

## ── 文字顏色 ──
const COLOR_TEXT_DARK    := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD    := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE  := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MUTED   := Color("#6B6680")  ## 次要輔助文字
const COLOR_TEXT_LIGHT   := Color("#FFFDF8")  ## 奶油白高亮文字
const COLOR_TEXT_DIM     := Color("#888294")  ## 壓暗提示文字

const DIALOG_WIDTH  := 720
const DIALOG_HEIGHT := 560
const CORNER_RADIUS := 18

var _scrim: ColorRect
var _dialog_card: PanelContainer
var _title_lbl: Label
var _sub_title_lbl: Label
var _close_x_btn: Button
var _btn_go_equip: Button
var _btn_go_workshop: Button
var _btn_go_skill: Button
var _btn_go_soul: Button
var _btn_go_calibrate: Button
var _btn_go_forge: Button
var _btn_go_title_wall: Button
var _btn_go_inventory: Button
var _btn_go_colossus: Button
var _btn_go_dummy_practice: Button
var _btn_go_vault: Button
var _btn_go_windup_daily: Button
var _bottom_close_btn: Button
var _scroll_box: ScrollContainer
var _content_vbox: VBoxContainer

var _cached_font: Font = null
var _built: bool = false


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and not loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.connect(_on_locale_changed)
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_signal("equipped_title_changed") and not gs.equipped_title_changed.is_connected(_on_equipped_title_changed):
			gs.equipped_title_changed.connect(_on_equipped_title_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_signal("equipped_title_changed") and gs.equipped_title_changed.is_connected(_on_equipped_title_changed):
			gs.equipped_title_changed.disconnect(_on_equipped_title_changed)


func _on_equipped_title_changed(_new_title: String = "") -> void:
	refresh()


func _on_locale_changed(_new_locale: String = "") -> void:
	refresh()


func _ready() -> void:
	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_ui()
	refresh()


func _build_ui() -> void:
	if _built:
		return
	_built = true
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP

	# 1. 全螢幕半透明遮罩 (Scrim)
	_scrim = ColorRect.new()
	_scrim.name = "ModalScrim"
	_scrim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_scrim.color = Color(0.10, 0.08, 0.14, 0.78)
	_scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	_scrim.gui_input.connect(func(ev: InputEvent):
		if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
			_on_close_pressed()
	)
	add_child(_scrim)

	# 2. 置中黑曜石底色彈窗卡片 (720 x 520)
	var card := PanelContainer.new()
	card.name = "DialogCard"
	card.custom_minimum_size = Vector2(DIALOG_WIDTH, DIALOG_HEIGHT)
	card.set_anchors_preset(Control.PRESET_CENTER)
	card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	card.grow_vertical = Control.GROW_DIRECTION_BOTH
	card.mouse_filter = Control.MOUSE_FILTER_STOP

	var card_sb := StyleBoxFlat.new()
	card_sb.bg_color = COLOR_OBSIDIAN
	card_sb.border_color = Color("#836D38")
	card_sb.set_border_width_all(2)
	card_sb.border_width_bottom = 5
	card_sb.set_corner_radius_all(CORNER_RADIUS)
	card_sb.content_margin_left = 18
	card_sb.content_margin_right = 18
	card_sb.content_margin_top = 14
	card_sb.content_margin_bottom = 14
	card_sb.shadow_color = Color(0.06, 0.04, 0.10, 0.45)
	card_sb.shadow_size = 10
	card_sb.shadow_offset = Vector2(0, 4)
	card.add_theme_stylebox_override("panel", card_sb)
	add_child(card)
	_dialog_card = card

	var root_v := VBoxContainer.new()
	root_v.name = "RootVBox"
	root_v.add_theme_constant_override("separation", 10)
	root_v.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.add_child(root_v)

	# 3. 頂部列（標題 + 副標 + 右上✕）
	var top_h := HBoxContainer.new()
	top_h.name = "TopBar"
	top_h.add_theme_constant_override("separation", 8)
	root_v.add_child(top_h)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.add_theme_constant_override("separation", 2)
	top_h.add_child(title_box)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("戰力屬性總覽")
	_apply_font(_title_lbl, 20, COLOR_TEXT_LIGHT, true)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 3)
	title_box.add_child(_title_lbl)

	_sub_title_lbl = Label.new()
	_sub_title_lbl.name = "SubTitleLabel"
	_sub_title_lbl.text = _t("角色核心數值與裝備流派加成詳情")
	_apply_font(_sub_title_lbl, 13, Color("#C8B99D"))
	title_box.add_child(_sub_title_lbl)

	_close_x_btn = Button.new()
	_close_x_btn.name = "BtnCloseX"
	_close_x_btn.text = "✕"
	_close_x_btn.custom_minimum_size = Vector2(50, 50)
	_style_jelly_btn(_close_x_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 18, 5, 18)
	_close_x_btn.pressed.connect(_on_close_pressed)
	top_h.add_child(_close_x_btn)

	# 4. 可滾動內容容器 (ScrollContainer)
	_scroll_box = ScrollContainer.new()
	_scroll_box.name = "ScrollBox"
	_scroll_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_scroll_box.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root_v.add_child(_scroll_box)

	_content_vbox = VBoxContainer.new()
	_content_vbox.name = "ContentVBox"
	_content_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_content_vbox.add_theme_constant_override("separation", 10)
	_scroll_box.add_child(_content_vbox)

	# 5. 底部按鈕列（並列『前往整頓』與『確定』雙按鈕）
	var bottom_h := HBoxContainer.new()
	bottom_h.name = "BottomBar"
	bottom_h.alignment = BoxContainer.ALIGNMENT_CENTER
	bottom_h.add_theme_constant_override("separation", 16)
	root_v.add_child(bottom_h)

	# 前往整頓快捷按鈕（天藍果凍質感，140x48px，熱區>=48px，果凍底 5px）
	_btn_go_equip = Button.new()
	_btn_go_equip.name = "BtnGoEquip"
	_btn_go_equip.text = _t("前往整頓")
	_btn_go_equip.custom_minimum_size = Vector2(140, 48)
	_style_jelly_btn(_btn_go_equip, COLOR_SKY, COLOR_TEXT_LIGHT, 16, 5, 16)
	_btn_go_equip.pressed.connect(_on_go_equip_pressed)
	bottom_h.add_child(_btn_go_equip)

	# 前往背包快捷按鈕（薄荷綠果凍質感，140x48px，熱區>=48px，果凍底 5px）
	_btn_go_inventory = Button.new()
	_btn_go_inventory.name = "BtnGoInventory"
	var inv_txt := _t("power_stat.btn_go_inventory")
	if inv_txt == "power_stat.btn_go_inventory" or inv_txt.is_empty():
		inv_txt = _t("前往背包")
	_btn_go_inventory.text = inv_txt
	_btn_go_inventory.custom_minimum_size = Vector2(140, 48)
	_style_jelly_btn(_btn_go_inventory, COLOR_MINT, COLOR_TEXT_DARK, 16, 5, 16)
	_btn_go_inventory.pressed.connect(_on_go_inventory_pressed)
	bottom_h.add_child(_btn_go_inventory)

	# 確定/關閉按鈕（溫暖米黃卡片底果凍按鈕，140x48px，熱區>=48px，果凍底 5px）
	_bottom_close_btn = Button.new()
	_bottom_close_btn.name = "BtnBottomClose"
	_bottom_close_btn.text = _t("確定")
	_bottom_close_btn.custom_minimum_size = Vector2(140, 48)
	_style_jelly_btn(_bottom_close_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 16, 5, 16)
	_bottom_close_btn.pressed.connect(_on_close_pressed)
	bottom_h.add_child(_bottom_close_btn)


## 重新讀取數值並渲染內容
func refresh() -> void:
	if not _built:
		return

	var gs := _gs()
	var eq := _eq()
	var gem := _gem()
	var sk := _sk()
	var soul_sys := _soul()

	# 更新頂部文字
	if _title_lbl:
		_title_lbl.text = _t("戰力屬性總覽")
	if _sub_title_lbl:
		var p_name := str(gs.player_name) if gs and "player_name" in gs else "勇者"
		var p_lv := int(gs.level) if gs and "level" in gs else 1
		var p_path := str(gs.call("path_display")) if gs and gs.has_method("path_display") else ""
		_sub_title_lbl.text = "%s · Lv.%d%s" % [p_name, p_lv, (" · " + p_path) if not p_path.is_empty() else ""]
	if _btn_go_equip:
		_btn_go_equip.text = _t("前往整頓")
	if _btn_go_workshop:
		_btn_go_workshop.text = _t("前往工坊")
	if _btn_go_skill:
		_btn_go_skill.text = _t("前往心法")
	if _btn_go_soul:
		_btn_go_soul.text = _t("前往聚魂")
	if _btn_go_calibrate:
		_btn_go_calibrate.text = _t("前往校準")
	if _btn_go_forge:
		_btn_go_forge.text = _t("前往鍛造")
	if _btn_go_title_wall:
		_btn_go_title_wall.text = _t("power_stat.btn_go_title_wall")
	if _btn_go_inventory:
		var inv_txt := _t("power_stat.btn_go_inventory")
		if inv_txt == "power_stat.btn_go_inventory" or inv_txt.is_empty():
			inv_txt = _t("前往背包")
		_btn_go_inventory.text = inv_txt
	if _btn_go_colossus:
		_btn_go_colossus.text = _t("power_stat.btn_go_colossus")
	if _btn_go_dummy_practice:
		var dummy_btn_txt := _t("power_stat.btn_go_dummy_practice")
		if dummy_btn_txt == "power_stat.btn_go_dummy_practice" or dummy_btn_txt.is_empty():
			dummy_btn_txt = _t("前往試招")
		_btn_go_dummy_practice.text = dummy_btn_txt
	if _btn_go_vault:
		var vault_btn_txt := _t("power_stat.btn_go_vault")
		if vault_btn_txt == "power_stat.btn_go_vault" or vault_btn_txt.is_empty():
			vault_btn_txt = _t("前往儲能")
		_btn_go_vault.text = vault_btn_txt
	if _bottom_close_btn:
		_bottom_close_btn.text = _t("確定")

	# 清空內容區
	for child in _content_vbox.get_children():
		_content_vbox.remove_child(child)
		child.queue_free()

	# 1. 綜合戰力總覽卡片
	_content_vbox.add_child(_build_power_overview_card(gs, soul_sys))

	# 2. 基礎六維屬性卡片
	_content_vbox.add_child(_build_six_stats_card(gs))

	# 3. 三欄武器裝備貢獻卡片
	_content_vbox.add_child(_build_weapon_loadout_card(gs, eq))

	# 4. 寶石孔位與招式心法加成卡片（雙欄）
	_content_vbox.add_child(_build_gem_and_skill_card(gs, gem, sk))

	# 5. 戰魂共鳴卡片（第四大戰力支柱）
	_content_vbox.add_child(_build_soul_resonance_card(gs, soul_sys))

	# 6. 機芯部件卡片（五大槽位與前往校準）
	var cs := _core_sys()
	_content_vbox.add_child(_build_core_parts_card(gs, cs))

	# 7. 佩戴稱號展示卡片（當前稱號膠囊與前往稱號牆）
	_content_vbox.add_child(_build_title_card(gs))

	# 8. 停擺巨偶挑戰進度卡片（今日次數與前往挑戰）
	_content_vbox.add_child(_build_colossus_card(gs))

	# 9. 木人樁試招紀錄卡片（歷史最佳 DPS、最高單擊與前往試招）
	_content_vbox.add_child(_build_dummy_trial_card(gs))

	# 10. 發條儲能庫放置收益卡片（累積放置能量值、上限與產能效率，前往儲能）
	_content_vbox.add_child(_build_vault_card(gs))

	# 11. 冒險委託每日上發條進度卡片（今日完成進度、領取膠囊與前往委託）
	_content_vbox.add_child(_build_windup_daily_card(gs))


## 綜合戰力總覽卡片
func _build_power_overview_card(gs: Node, soul_sys: Node = null) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "PowerOverviewCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 16)
	m.add_child(h)

	# 左側大號戰力徽章
	var pow_box := PanelContainer.new()
	pow_box.name = "PowerBadge"
	pow_box.custom_minimum_size = Vector2(140, 72)
	pow_box.add_theme_stylebox_override("panel", _create_card_style(COLOR_OBSIDIAN, Color("#D4AF37"), 2, 3, 12))
	var pv := VBoxContainer.new()
	pv.alignment = BoxContainer.ALIGNMENT_CENTER
	pv.add_theme_constant_override("separation", 2)
	pow_box.add_child(pv)

	var p_title := Label.new()
	p_title.text = _t("綜合戰力")
	p_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(p_title, 12, Color("#E5C158"))
	pv.add_child(p_title)

	var total_pow: int = int(gs.call("power_score")) if gs and gs.has_method("power_score") else 0
	var p_val := Label.new()
	p_val.name = "TotalPowerValue"
	p_val.text = str(total_pow)
	p_val.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(p_val, 26, COLOR_GOLD, true)
	p_val.add_theme_color_override("font_outline_color", COLOR_BORDER)
	p_val.add_theme_constant_override("outline_size", 3)
	pv.add_child(p_val)
	h.add_child(pow_box)

	# 右側戰力拆解說明
	var v_breakdown := VBoxContainer.new()
	v_breakdown.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v_breakdown.alignment = BoxContainer.ALIGNMENT_CENTER
	v_breakdown.add_theme_constant_override("separation", 4)
	h.add_child(v_breakdown)

	var b_title := Label.new()
	b_title.text = _t("戰力成長拆解")
	_apply_font(b_title, 13, COLOR_TEXT_DARK, true)
	v_breakdown.add_child(b_title)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 2)
	v_breakdown.add_child(grid)

	var lv: int = int(gs.level) if gs and "level" in gs else 1
	var w_tier: int = int(gs.weapon_tier) if gs and "weapon_tier" in gs else 1
	var e_atk: int = int(gs.call("effective_atk")) if gs and gs.has_method("effective_atk") else 0
	var e_def: int = int(gs.call("effective_def")) if gs and gs.has_method("effective_def") else 0
	var e_crit: float = float(gs.call("effective_crit")) if gs and gs.has_method("effective_crit") else 0.0
	var has_path: bool = (str(gs.path_style) != "") if gs and "path_style" in gs else false

	var s_bonus: Dictionary = soul_sys.call("total_equipped_bonus") if soul_sys and soul_sys.has_method("total_equipped_bonus") else {}
	var s_pow: int = int(s_bonus.get("atk", 0)) + int(s_bonus.get("def", 0)) + int(int(s_bonus.get("hp", 0)) / 4.0)

	var c_bonus: Dictionary = {}
	var CsClass = load("res://scripts/systems/core_system.gd")
	if CsClass != null and gs and "core_slots" in gs and not gs.core_slots.is_empty():
		c_bonus = CsClass.get_total_bonuses(gs.core_slots)
	elif CsClass != null and CsClass.has_method("total_core_bonuses"):
		c_bonus = CsClass.total_core_bonuses()
	var c_atk := int(c_bonus.get("atk", 0))
	var c_def := int(c_bonus.get("def", 0))
	var c_hp := int(c_bonus.get("hp", 0))
	var c_crit := float(c_bonus.get("crit", 0.0))
	var c_pow: int = c_atk + c_def + int(c_hp / 4.0) + int(c_crit / 2.0)

	_add_breakdown_item(grid, _t("等級成長"), "+%d" % (lv * 3))
	_add_breakdown_item(grid, _t("武器階數"), "+%d" % (w_tier * 4))
	_add_breakdown_item(grid, _t("攻防加成"), "+%d" % (e_atk + e_def))
	_add_breakdown_item(grid, _t("暴擊折算"), "+%d" % int(e_crit / 2.0))
	_add_breakdown_item(grid, _t("流派心法"), "+%d" % (2 if has_path else 0))
	_add_breakdown_item(grid, _t("戰魂共鳴"), "+%d" % s_pow)
	_add_breakdown_item(grid, _t("機芯部件"), "+%d" % c_pow)

	return card


func _add_breakdown_item(parent: Container, label_text: String, val_text: String) -> void:
	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 4)
	var l := Label.new()
	l.text = label_text + ":"
	_apply_font(l, 12, COLOR_TEXT_MUTED)
	h.add_child(l)
	var v := Label.new()
	v.text = val_text
	_apply_font(v, 12, COLOR_TEXT_ORANGE, true)
	h.add_child(v)
	parent.add_child(h)


## 基礎六維屬性卡片
func _build_six_stats_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "SixStatsCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_SKY, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	var t := Label.new()
	t.text = _t("基礎六維屬性")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	v.add_child(t)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 8)
	v.add_child(grid)

	var cur_hp: int = int(gs.call("effective_max_hp")) if gs and gs.has_method("effective_max_hp") else 100
	var base_hp: int = int(gs.max_hp) if gs and "max_hp" in gs else 100

	var cur_atk: int = int(gs.call("effective_atk")) if gs and gs.has_method("effective_atk") else 10
	var base_atk: int = int(gs.atk) if gs and "atk" in gs else 10

	var cur_def: int = int(gs.call("effective_def")) if gs and gs.has_method("effective_def") else 5
	var base_def: int = int(gs.def_stat) if gs and "def_stat" in gs else 5

	var cur_crit: float = float(gs.call("effective_crit")) if gs and gs.has_method("effective_crit") else 5.0
	var base_crit: float = float(gs.crit_rate) if gs and "crit_rate" in gs else 5.0

	var cur_spd: int = int(gs.call("effective_speed")) if gs and gs.has_method("effective_speed") else 10
	var base_spd: int = int(gs.speed) if gs and "speed" in gs else 10

	var cur_cdmg: float = float(gs.call("effective_crit_dmg")) if gs and gs.has_method("effective_crit_dmg") else 150.0
	var base_cdmg: float = float(gs.crit_dmg) if gs and "crit_dmg" in gs else 150.0

	grid.add_child(_create_stat_cell("Stat_HP", _t("生命力"), str(cur_hp), "(+%d)" % maxi(0, cur_hp - base_hp), Color("#0E8A7A")))
	grid.add_child(_create_stat_cell("Stat_ATK", _t("物理攻擊"), str(cur_atk), "(+%d)" % maxi(0, cur_atk - base_atk), COLOR_TEXT_ORANGE))
	grid.add_child(_create_stat_cell("Stat_DEF", _t("物理防禦"), str(cur_def), "(+%d)" % maxi(0, cur_def - base_def), Color("#2A5580")))
	grid.add_child(_create_stat_cell("Stat_CRIT", _t("暴擊率"), "%.1f%%" % cur_crit, "(+%.1f%%)" % maxf(0.0, cur_crit - base_crit), Color("#B83250")))
	grid.add_child(_create_stat_cell("Stat_SPD", _t("出手速度"), str(cur_spd), "(+%d)" % maxi(0, cur_spd - base_spd), Color("#3E7E1E")))
	grid.add_child(_create_stat_cell("Stat_CDMG", _t("暴擊傷害"), "%.0f%%" % cur_cdmg, "(+%.0f%%)" % maxf(0.0, cur_cdmg - base_cdmg), Color("#8B2A90")))

	return card


func _create_stat_cell(cell_name: String, label_str: String, val_str: String, extra_str: String, color_accent: Color) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = cell_name
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(0, 48)

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 10
	sb.content_margin_right = 10
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	c.add_theme_stylebox_override("panel", sb)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 6)
	c.add_child(h)

	var lbl := Label.new()
	lbl.text = label_str
	_apply_font(lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(lbl)

	var val_lbl := Label.new()
	val_lbl.name = "ValueLabel"
	val_lbl.text = val_str
	_apply_font(val_lbl, 16, color_accent, true)
	h.add_child(val_lbl)

	if not extra_str.is_empty() and extra_str != "(+0)" and extra_str != "(+0.0%)":
		var ext_lbl := Label.new()
		ext_lbl.text = extra_str
		_apply_font(ext_lbl, 11, COLOR_TEXT_MUTED)
		h.add_child(ext_lbl)

	return c


## 三欄武器裝備貢獻卡片
func _build_weapon_loadout_card(gs: Node, eq: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "WeaponLoadoutCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	var t_row := HBoxContainer.new()
	t_row.name = "WeaponHeaderRow"
	t_row.add_theme_constant_override("separation", 8)
	v.add_child(t_row)

	var t := Label.new()
	t.name = "WeaponLoadoutTitleLabel"
	t.text = _t("三欄武器裝備貢獻")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	t_row.add_child(t)

	var eq_bonus: Dictionary = {}
	if eq and eq.has_method("bonus_totals"):
		eq_bonus = eq.call("bonus_totals") as Dictionary

	var b_atk := int(eq_bonus.get("atk", 0))
	var b_def := int(eq_bonus.get("def", 0))
	var b_hp := int(eq_bonus.get("hp", 0))
	var b_crit := float(eq_bonus.get("crit", 0.0))

	var summary_lbl := Label.new()
	summary_lbl.name = "WeaponSummaryLabel"
	summary_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	summary_lbl.text = _t("裝備總加成: 攻+%d · 防+%d · 血+%d · 暴+%.1f%%") % [b_atk, b_def, b_hp, b_crit]
	_apply_font(summary_lbl, 12, COLOR_TEXT_GOLD, true)
	t_row.add_child(summary_lbl)

	# 快捷按鈕：前往鍛造 (BtnGoForge)（高>=48px，熱區>=48px，金黃果凍厚底 5px，深藍紫描邊 2px，字級 14px）
	_btn_go_forge = Button.new()
	_btn_go_forge.name = "BtnGoForge"
	_btn_go_forge.text = _t("前往鍛造")
	_btn_go_forge.custom_minimum_size = Vector2(96, 48)
	_btn_go_forge.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_forge, COLOR_GOLD, COLOR_TEXT_DARK, 14, 5, 14, COLOR_BORDER, 10, 4)
	_btn_go_forge.pressed.connect(_on_go_forge_pressed)
	t_row.add_child(_btn_go_forge)

	# 三槽武器卡片列
	var slots_h := HBoxContainer.new()
	slots_h.add_theme_constant_override("separation", 10)
	v.add_child(slots_h)

	var slot_titles: Array[String] = [
		_t("首選武器"),
		_t("副手武器"),
		_t("絕技武器")
	]

	for i in range(3):
		slots_h.add_child(_create_slot_card(i, slot_titles[i], eq))

	return card


func _create_slot_card(slot_idx: int, slot_title: String, eq: Node) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "SlotCard_%d" % slot_idx
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_GOLD if slot_idx == 0 else COLOR_CARD_SKY
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 8
	sb.content_margin_right = 8
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	c.add_theme_stylebox_override("panel", sb)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	c.add_child(v)

	var t := Label.new()
	t.text = slot_title
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(t, 12, COLOR_TEXT_MUTED)
	v.add_child(t)

	var is_unlocked := true
	if eq and eq.has_method("loadout_slot_unlocked"):
		is_unlocked = bool(eq.call("loadout_slot_unlocked", slot_idx))

	if not is_unlocked:
		var unlock_lv := 10 if slot_idx == 1 else 20
		var lock_lbl := Label.new()
		lock_lbl.text = _t("Lv.%d 解鎖" % unlock_lv)
		lock_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_apply_font(lock_lbl, 13, COLOR_TEXT_DIM)
		v.add_child(lock_lbl)
		return c

	var uid := ""
	if eq and eq.has_method("loadout_uid"):
		uid = str(eq.call("loadout_uid", slot_idx))

	if uid.is_empty():
		var empty_lbl := Label.new()
		empty_lbl.text = _t("未裝備")
		empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_apply_font(empty_lbl, 13, COLOR_TEXT_DIM)
		v.add_child(empty_lbl)
		return c

	var inst: Dictionary = {}
	if eq and eq.has_method("weapon_inst"):
		inst = eq.call("weapon_inst", uid) as Dictionary

	var w_name := str(inst.get("name", "武器"))
	var w_atk := int(inst.get("atk", 0))
	var w_tier := int(inst.get("tier", 1))

	var name_lbl := Label.new()
	name_lbl.text = _t(w_name)
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(name_lbl, 14, COLOR_TEXT_DARK, true)
	v.add_child(name_lbl)

	var stat_lbl := Label.new()
	stat_lbl.text = _t("T%d · 攻 +%d") % [w_tier, w_atk]
	stat_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(stat_lbl, 12, COLOR_TEXT_ORANGE)
	v.add_child(stat_lbl)

	return c


## 寶石孔位與招式心法加成卡片（雙欄）
func _build_gem_and_skill_card(gs: Node, gem: Node, sk: Node) -> HBoxContainer:
	var h := HBoxContainer.new()
	h.name = "GemAndSkillRow"
	h.add_theme_constant_override("separation", 10)

	# 寶石孔位卡片
	var gem_card := PanelContainer.new()
	gem_card.name = "GemBonusCard"
	gem_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	gem_card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_MINT, COLOR_BORDER, 2, 4, 14))
	h.add_child(gem_card)

	var gm := MarginContainer.new()
	gm.add_theme_constant_override("margin_left", 12)
	gm.add_theme_constant_override("margin_right", 12)
	gm.add_theme_constant_override("margin_top", 8)
	gm.add_theme_constant_override("margin_bottom", 8)
	gem_card.add_child(gm)

	var gh := HBoxContainer.new()
	gh.name = "GemCardHBox"
	gh.add_theme_constant_override("separation", 8)
	gm.add_child(gh)

	var gv := VBoxContainer.new()
	gv.name = "GemCardVBox"
	gv.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	gv.alignment = BoxContainer.ALIGNMENT_CENTER
	gv.add_theme_constant_override("separation", 4)
	gh.add_child(gv)

	var gt := Label.new()
	gt.name = "GemTitleLabel"
	gt.text = _t("寶石孔位加成")
	_apply_font(gt, 13, COLOR_TEXT_DARK, true)
	gv.add_child(gt)

	var worn_b: Dictionary = {}
	if gem and gem.has_method("worn_bonuses"):
		worn_b = gem.call("worn_bonuses") as Dictionary

	var g_atk_pct := float(worn_b.get("atk_pct", 0.0)) * 100.0
	var g_def_pct := float(worn_b.get("def_pct", 0.0)) * 100.0
	var g_hp_pct  := float(worn_b.get("hp_pct", 0.0)) * 100.0
	var g_crit    := float(worn_b.get("crit", 0.0))
	var g_hit     := float(worn_b.get("hit", 0.0))
	var g_eva     := float(worn_b.get("eva", 0.0))

	var b_list: Array[String] = []
	if g_atk_pct > 0.01:
		b_list.append("攻 +%.1f%%" % g_atk_pct)
	if g_def_pct > 0.01:
		b_list.append("防 +%.1f%%" % g_def_pct)
	if g_hp_pct > 0.01:
		b_list.append("血 +%.1f%%" % g_hp_pct)
	if g_crit > 0.01:
		b_list.append("暴 +%.1f%%" % g_crit)
	if g_hit > 0.01:
		b_list.append("命中 +%.0f" % g_hit)
	if g_eva > 0.01:
		b_list.append("閃避 +%.0f" % g_eva)

	var g_desc := Label.new()
	g_desc.name = "GemDescLabel"
	if b_list.is_empty():
		g_desc.text = _t("尚未鑲嵌寶石")
		_apply_font(g_desc, 12, COLOR_TEXT_DIM)
	else:
		g_desc.text = " · ".join(b_list)
		_apply_font(g_desc, 12, Color("#1E7538"), true)
	gv.add_child(g_desc)

	# 快捷按鈕：前往工坊 (BtnGoWorkshop)（尺寸 84x36px，熱區>=48px，果凍厚底 4px）
	_btn_go_workshop = Button.new()
	_btn_go_workshop.name = "BtnGoWorkshop"
	_btn_go_workshop.text = _t("前往工坊")
	_btn_go_workshop.custom_minimum_size = Vector2(84, 36)
	_btn_go_workshop.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_workshop, COLOR_ORANGE, COLOR_TEXT_LIGHT, 12, 4, 12, COLOR_BORDER, 6, 3)
	_btn_go_workshop.pressed.connect(_on_go_workshop_pressed)
	gh.add_child(_btn_go_workshop)

	# 招式心法卡片
	var sk_card := PanelContainer.new()
	sk_card.name = "SkillBonusCard"
	sk_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sk_card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 14))
	h.add_child(sk_card)

	var sm := MarginContainer.new()
	sm.add_theme_constant_override("margin_left", 12)
	sm.add_theme_constant_override("margin_right", 12)
	sm.add_theme_constant_override("margin_top", 8)
	sm.add_theme_constant_override("margin_bottom", 8)
	sk_card.add_child(sm)

	var sh := HBoxContainer.new()
	sh.name = "SkillCardHBox"
	sh.add_theme_constant_override("separation", 8)
	sm.add_child(sh)

	var sv := VBoxContainer.new()
	sv.name = "SkillCardVBox"
	sv.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sv.alignment = BoxContainer.ALIGNMENT_CENTER
	sv.add_theme_constant_override("separation", 4)
	sh.add_child(sv)

	var st := Label.new()
	st.name = "SkillTitleLabel"
	st.text = _t("招式心法加成")
	_apply_font(st, 13, COLOR_TEXT_DARK, true)
	sv.add_child(st)

	var patch: Dictionary = {}
	if sk and sk.has_method("battle_player_stats_patch"):
		patch = sk.call("battle_player_stats_patch") as Dictionary

	var sk_name: String = str(patch.get("skill_name", ""))
	var sk_mult: float = float(patch.get("skill_mult", 1.8))
	var sk_hits: int = int(patch.get("skill_hits", 1))

	var sk_desc := Label.new()
	sk_desc.name = "SkillDescLabel"
	if sk_name.is_empty():
		sk_desc.text = _t("未裝備招式心法")
		_apply_font(sk_desc, 12, COLOR_TEXT_DIM)
	else:
		sk_desc.text = "%s (%s: %.1fx · %s: %d)" % [sk_name, _t("傷害倍率"), sk_mult, _t("連擊段數"), sk_hits]
		_apply_font(sk_desc, 12, COLOR_TEXT_ORANGE, true)
	sv.add_child(sk_desc)

	# 快捷按鈕：前往心法 (BtnGoSkill)（尺寸 84x36px，熱區>=48px，果凍厚底 4px）
	_btn_go_skill = Button.new()
	_btn_go_skill.name = "BtnGoSkill"
	_btn_go_skill.text = _t("前往心法")
	_btn_go_skill.custom_minimum_size = Vector2(84, 36)
	_btn_go_skill.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_skill, COLOR_SKY, COLOR_TEXT_LIGHT, 12, 4, 12, COLOR_BORDER, 6, 3)
	_btn_go_skill.pressed.connect(_on_go_skill_pressed)
	sh.add_child(_btn_go_skill)

	return h


## 戰魂共鳴卡片（第四大戰力支柱）
func _build_soul_resonance_card(_gs: Node, soul_sys: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "SoulResonanceCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.name = "SoulCardVBox"
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	# 頂部列：標題 + 總加成摘要 + 前往聚魂快捷按鈕
	var t_row := HBoxContainer.new()
	t_row.name = "SoulHeaderRow"
	t_row.add_theme_constant_override("separation", 8)
	v.add_child(t_row)

	var t := Label.new()
	t.name = "SoulTitleLabel"
	t.text = _t("戰魂共鳴")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	t_row.add_child(t)

	var tot_bonus := {"atk": 0, "def": 0, "hp": 0}
	if soul_sys and soul_sys.has_method("total_equipped_bonus"):
		tot_bonus = soul_sys.call("total_equipped_bonus") as Dictionary

	var b_atk := int(tot_bonus.get("atk", 0))
	var b_def := int(tot_bonus.get("def", 0))
	var b_hp  := int(tot_bonus.get("hp", 0))

	var summary_lbl := Label.new()
	summary_lbl.name = "SoulSummaryLabel"
	summary_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	summary_lbl.text = _t("戰魂總加成: 攻+%d · 防+%d · 血+%d") % [b_atk, b_def, b_hp]
	_apply_font(summary_lbl, 12, COLOR_TEXT_GOLD, true)
	t_row.add_child(summary_lbl)

	# 快捷按鈕：前往聚魂 (BtnGoSoul)（尺寸 88x36px，熱區>=48px，果凍厚底 4px）
	_btn_go_soul = Button.new()
	_btn_go_soul.name = "BtnGoSoul"
	_btn_go_soul.text = _t("前往聚魂")
	_btn_go_soul.custom_minimum_size = Vector2(88, 36)
	_btn_go_soul.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_soul, COLOR_PINK, COLOR_TEXT_LIGHT, 12, 4, 12, COLOR_BORDER, 6, 3)
	_btn_go_soul.pressed.connect(_on_go_soul_pressed)
	t_row.add_child(_btn_go_soul)

	# 雙欄四大核心展示卡片 (CoreGrid)
	var core_grid := GridContainer.new()
	core_grid.name = "CoreGrid"
	core_grid.columns = 2
	core_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	core_grid.add_theme_constant_override("h_separation", 10)
	core_grid.add_theme_constant_override("v_separation", 8)
	v.add_child(core_grid)

	var core_data: Array = []
	if soul_sys and soul_sys.has_method("get_core_resonances"):
		core_data = soul_sys.call("get_core_resonances") as Array

	for i in range(4):
		var cd: Dictionary = core_data[i] if i < core_data.size() else {}
		core_grid.add_child(_create_core_cell(i, cd))

	return card


func _create_core_cell(idx: int, cd: Dictionary) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "CoreCell_%d" % idx
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(0, 48)

	var sb := StyleBoxFlat.new()
	match idx:
		0:
			sb.bg_color = COLOR_CARD_GOLD
		1:
			sb.bg_color = COLOR_CARD_SKY
		2:
			sb.bg_color = COLOR_CARD_MINT
		_:
			sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 10
	sb.content_margin_right = 10
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	c.add_theme_stylebox_override("panel", sb)

	var h := HBoxContainer.new()
	h.name = "CoreHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 8)
	c.add_child(h)

	var default_labels := ["齒", "甲", "簧", "衡"]
	var default_names := ["銳齒之魂", "固甲之魂", "旋簧之魂", "全衡之魂"]
	var label_char: String = str(cd.get("label", default_labels[idx]))
	var core_name: String = str(cd.get("name", _t(default_names[idx])))
	var is_lit: bool = bool(cd.get("is_lit", false))
	var quality: String = str(cd.get("quality", cd.get("tier", "")))
	var lv: int = int(cd.get("level", 0))
	var bonus: Dictionary = cd.get("bonus", {})

	# 核心代號徽章 【齒】
	var badge_lbl := Label.new()
	badge_lbl.name = "CoreBadgeLabel"
	badge_lbl.text = "【%s】" % label_char
	_apply_font(badge_lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(badge_lbl)

	# 核心名稱
	var name_lbl := Label.new()
	name_lbl.name = "CoreNameLabel"
	name_lbl.text = core_name
	_apply_font(name_lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(name_lbl)

	# 階級與等級 (例如: 凡·Lv.1 或 神·Lv.10 或 未喚醒)
	var tier_lbl := Label.new()
	tier_lbl.name = "CoreTierLabel"
	if is_lit and not quality.is_empty():
		tier_lbl.text = "%s·Lv.%d" % [_t(quality), lv]
		_apply_font(tier_lbl, 12, COLOR_TEXT_MUTED)
	else:
		tier_lbl.text = _t("未喚醒")
		_apply_font(tier_lbl, 12, COLOR_TEXT_DIM)
	h.add_child(tier_lbl)

	# 彈性間隔
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	# 屬性加成文字
	var bonus_lbl := Label.new()
	bonus_lbl.name = "CoreBonusLabel"
	var b_atk := int(bonus.get("atk", 0))
	var b_def := int(bonus.get("def", 0))
	var b_hp  := int(bonus.get("hp", 0))

	var bonus_text := ""
	var bonus_color := COLOR_TEXT_DIM
	match idx:
		0:
			bonus_text = _t("攻+%d") % b_atk if b_atk > 0 else "+0"
			bonus_color = COLOR_TEXT_ORANGE if b_atk > 0 else COLOR_TEXT_DIM
		1:
			bonus_text = _t("防+%d") % b_def if b_def > 0 else "+0"
			bonus_color = Color("#2A5580") if b_def > 0 else COLOR_TEXT_DIM
		2:
			bonus_text = _t("血+%d") % b_hp if b_hp > 0 else "+0"
			bonus_color = Color("#0E8A7A") if b_hp > 0 else COLOR_TEXT_DIM
		3:
			if b_atk > 0 or b_def > 0 or b_hp > 0:
				bonus_text = _t("全+%d") % b_atk
				bonus_color = Color("#8B2A90")
			else:
				bonus_text = "+0"
				bonus_color = COLOR_TEXT_DIM

	bonus_lbl.text = bonus_text
	_apply_font(bonus_lbl, 13, bonus_color, true)
	h.add_child(bonus_lbl)

	return c


## 機芯部件卡片（五大槽位與前往校準）
func _build_core_parts_card(gs: Node, cs: Node = null) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "CorePartsCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.name = "CorePartsVBox"
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	# 頂部列：標題 + 總加成摘要 + 前往校準快捷按鈕
	var t_row := HBoxContainer.new()
	t_row.name = "CorePartsHeaderRow"
	t_row.add_theme_constant_override("separation", 8)
	v.add_child(t_row)

	var t := Label.new()
	t.name = "CorePartsTitleLabel"
	t.text = _t("機芯部件")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	t_row.add_child(t)

	var t_alias := Label.new()
	t_alias.name = "CoreTitleLabel"
	t_alias.visible = false
	t_alias.text = _t("機芯部件")
	t_row.add_child(t_alias)

	var CsClass = load("res://scripts/systems/core_system.gd")
	var c_bonus: Dictionary = {}
	if CsClass != null and gs and "core_slots" in gs and not gs.core_slots.is_empty():
		c_bonus = CsClass.get_total_bonuses(gs.core_slots)
	elif CsClass != null and CsClass.has_method("total_core_bonuses"):
		c_bonus = CsClass.total_core_bonuses()
	elif cs and cs.has_method("total_core_bonuses"):
		c_bonus = cs.call("total_core_bonuses")

	var b_atk := int(c_bonus.get("atk", 0))
	var b_def := int(c_bonus.get("def", 0))
	var b_hp  := int(c_bonus.get("hp", 0))

	var summary_lbl := Label.new()
	summary_lbl.name = "CorePartsSummaryLabel"
	summary_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	summary_lbl.text = _t("機芯總加成: 攻+%d · 防+%d · 血+%d") % [b_atk, b_def, b_hp]
	_apply_font(summary_lbl, 12, COLOR_TEXT_GOLD, true)
	t_row.add_child(summary_lbl)

	var summary_alias := Label.new()
	summary_alias.name = "CoreSummaryLabel"
	summary_alias.visible = false
	summary_alias.text = summary_lbl.text
	t_row.add_child(summary_alias)

	# 快捷按鈕：前往校準 (BtnGoCalibrate)（尺寸 88x36px，熱區>=48px，果凍厚底 4px）
	_btn_go_calibrate = Button.new()
	_btn_go_calibrate.name = "BtnGoCalibrate"
	_btn_go_calibrate.text = _t("前往校準")
	_btn_go_calibrate.custom_minimum_size = Vector2(88, 36)
	_btn_go_calibrate.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_calibrate, COLOR_ORANGE, COLOR_TEXT_LIGHT, 12, 4, 12, COLOR_BORDER, 6, 3)
	_btn_go_calibrate.pressed.connect(_on_go_calibrate_pressed)
	t_row.add_child(_btn_go_calibrate)

	# 五大機芯槽位展示容器
	var slots_vbox := VBoxContainer.new()
	slots_vbox.name = "CoreSlotsVBox"
	slots_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	slots_vbox.add_theme_constant_override("separation", 6)
	v.add_child(slots_vbox)

	var slot_ids: Array = []
	if CsClass != null and "ALL_SLOT_IDS" in CsClass:
		slot_ids = CsClass.ALL_SLOT_IDS
	else:
		slot_ids = ["mainspring", "chassis", "escapement", "gear_train", "soul_core"]

	for i in range(slot_ids.size()):
		var sid: String = str(slot_ids[i])
		var part: Dictionary = {}
		if gs and "core_slots" in gs and gs.core_slots.has(sid):
			part = gs.core_slots[sid]
		elif CsClass != null and CsClass.has_method("get_equipped_part"):
			part = CsClass.get_equipped_part(sid)
		slots_vbox.add_child(_create_core_part_cell(i, sid, part, CsClass))

	return card


func _create_core_part_cell(idx: int, slot_id: String, part: Dictionary, CsClass: Variant) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "CoreSlotCell_%d" % idx
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(0, 48)

	var sb := StyleBoxFlat.new()
	match idx % 4:
		0: sb.bg_color = COLOR_CARD_GOLD
		1: sb.bg_color = COLOR_CARD_SKY
		2: sb.bg_color = COLOR_CARD_MINT
		_: sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 10
	sb.content_margin_right = 10
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	c.add_theme_stylebox_override("panel", sb)

	var h := HBoxContainer.new()
	h.name = "CoreSlotHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 8)
	c.add_child(h)

	# 槽位名稱
	var slot_name: String = ""
	if CsClass != null and CsClass.has_method("get_slot_name"):
		slot_name = CsClass.get_slot_name(slot_id)
	elif CsClass != null and "SLOT_NAMES" in CsClass and CsClass.SLOT_NAMES.has(slot_id):
		slot_name = str(CsClass.SLOT_NAMES[slot_id])
	else:
		slot_name = slot_id

	var slot_name_lbl := Label.new()
	slot_name_lbl.name = "SlotNameLabel"
	slot_name_lbl.text = _t(slot_name)
	_apply_font(slot_name_lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(slot_name_lbl)

	# 部件名稱
	var part_name: String = ""
	if not part.is_empty():
		part_name = str(part.get("name", part.get("slot_name", slot_name)))
	else:
		part_name = _t("未裝備")
	var part_name_lbl := Label.new()
	part_name_lbl.name = "PartNameLabel"
	part_name_lbl.text = _t(part_name)
	_apply_font(part_name_lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(part_name_lbl)

	# 色階與色票
	var score: int = int(part.get("score", 0)) if not part.is_empty() else 0
	var tier_info: Dictionary = {}
	if CsClass != null and CsClass.has_method("get_tier_by_score"):
		tier_info = CsClass.get_tier_by_score(score)
	var raw_tier_name: String = str(part.get("tier_name", tier_info.get("name", "白"))) if not part.is_empty() else "未裝備"
	var tier_color: Color = tier_info.get("color", Color.WHITE) if not part.is_empty() else COLOR_BORDER_MUTED

	var patch := ColorRect.new()
	patch.name = "TierColorPatch"
	patch.custom_minimum_size = Vector2(14, 14)
	patch.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	patch.color = tier_color
	h.add_child(patch)

	var tier_name_lbl := Label.new()
	tier_name_lbl.name = "TierNameLabel"
	tier_name_lbl.text = _t(raw_tier_name)
	_apply_font(tier_name_lbl, 12, tier_color if (not part.is_empty() and tier_color != Color.WHITE) else COLOR_TEXT_MUTED)
	h.add_child(tier_name_lbl)

	# 彈性間隔
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	# 攻防血加成
	var pstats: Dictionary = {}
	if not part.is_empty() and CsClass != null and CsClass.has_method("get_part_stats"):
		pstats = CsClass.get_part_stats(part)
	var p_atk: int = int(pstats.get("atk", 0))
	var p_def: int = int(pstats.get("def", 0))
	var p_hp: int  = int(pstats.get("hp", 0))

	var bonus_lbl := Label.new()
	bonus_lbl.name = "PartBonusLabel"
	bonus_lbl.text = _t("攻+%d · 防+%d · 血+%d") % [p_atk, p_def, p_hp] if not part.is_empty() else "+0"
	_apply_font(bonus_lbl, 13, COLOR_TEXT_ORANGE if (p_atk > 0 or p_def > 0 or p_hp > 0) else COLOR_TEXT_DIM, true)
	h.add_child(bonus_lbl)

	return c


## 佩戴稱號展示卡片
func _build_title_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "TitleCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_SKY, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "TitleCardHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	m.add_child(h)

	# 左側資訊區：標題列與稱號膠囊
	var left_v := VBoxContainer.new()
	left_v.name = "TitleLeftVBox"
	left_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 6)
	h.add_child(left_v)

	var t_row := HBoxContainer.new()
	t_row.name = "TitleRowHBox"
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	left_v.add_child(t_row)

	var t_lbl := Label.new()
	t_lbl.name = "TitleCardTitleLabel"
	t_lbl.text = _t("power_stat.title_card")
	_apply_font(t_lbl, 14, COLOR_TEXT_DARK, true)
	t_row.add_child(t_lbl)

	# 佩戴稱號名稱膠囊
	var raw_title := ""
	if gs and gs.has_method("get_equipped_title"):
		raw_title = gs.get_equipped_title()
	var display_title := _get_title_display_name(raw_title)

	var cap := PanelContainer.new()
	cap.name = "TitleCapsule"
	var cap_sb := StyleBoxFlat.new()
	cap_sb.bg_color = COLOR_CARD_GOLD
	cap_sb.border_color = COLOR_BORDER
	cap_sb.set_border_width_all(1)
	cap_sb.border_width_bottom = 3
	cap_sb.set_corner_radius_all(10)
	cap_sb.content_margin_left = 10
	cap_sb.content_margin_right = 10
	cap_sb.content_margin_top = 3
	cap_sb.content_margin_bottom = 3
	cap.add_theme_stylebox_override("panel", cap_sb)
	t_row.add_child(cap)

	var cap_lbl := Label.new()
	cap_lbl.name = "TitleNameLabel"
	cap_lbl.text = display_title
	_apply_font(cap_lbl, 13, COLOR_TEXT_DARK, true)
	cap.add_child(cap_lbl)

	# 說明文字
	var desc_lbl := Label.new()
	desc_lbl.name = "TitleDescLabel"
	desc_lbl.text = _t("power_stat.title_desc")
	_apply_font(desc_lbl, 12, COLOR_TEXT_MUTED)
	left_v.add_child(desc_lbl)

	# 右側快捷按鈕：前往稱號 (BtnGoTitleWall)
	_btn_go_title_wall = Button.new()
	_btn_go_title_wall.name = "BtnGoTitleWall"
	_btn_go_title_wall.text = _t("power_stat.btn_go_title_wall")
	_btn_go_title_wall.custom_minimum_size = Vector2(110, 48)
	_btn_go_title_wall.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_title_wall, COLOR_SKY, COLOR_TEXT_LIGHT, 14, 4, 16, COLOR_BORDER, 12, 4)
	_btn_go_title_wall.pressed.connect(_on_go_title_wall_pressed)
	h.add_child(_btn_go_title_wall)

	return card


func _get_title_display_name(raw_title: String) -> String:
	if raw_title.is_empty() or raw_title == "初出茅廬":
		return _t("初出茅廬")
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var tc: Node = (loop as SceneTree).root.get_node_or_null("TitleCatalog")
		if tc and tc.has_method("entries"):
			for e in tc.entries():
				if str(e.get("raw_name", "")) == raw_title or str(e.get("name", "")) == raw_title or str(e.get("flag", "")) == raw_title:
					return str(e.get("name", raw_title))
	return _t(raw_title)


func _build_colossus_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "ColossusCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "ColossusCardHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	m.add_child(h)

	# 左側資訊區：標題列與次數膠囊、推薦目標與說明文字
	var left_v := VBoxContainer.new()
	left_v.name = "ColossusLeftVBox"
	left_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 6)
	h.add_child(left_v)

	var t_row := HBoxContainer.new()
	t_row.name = "ColossusRowHBox"
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	left_v.add_child(t_row)

	var t_lbl := Label.new()
	t_lbl.name = "ColossusCardTitleLabel"
	t_lbl.text = _t("power_stat.colossus_card")
	_apply_font(t_lbl, 14, COLOR_TEXT_ORANGE, true)
	t_row.add_child(t_lbl)

	# 今日剩餘挑戰次數膠囊
	var left_entries := _get_colossus_remaining_entries()
	var cap := PanelContainer.new()
	cap.name = "ColossusEntriesCapsule"
	var cap_sb := StyleBoxFlat.new()
	cap_sb.bg_color = COLOR_CARD_GOLD
	cap_sb.border_color = COLOR_BORDER
	cap_sb.set_border_width_all(1)
	cap_sb.border_width_bottom = 3
	cap_sb.set_corner_radius_all(10)
	cap_sb.content_margin_left = 10
	cap_sb.content_margin_right = 10
	cap_sb.content_margin_top = 3
	cap_sb.content_margin_bottom = 3
	cap.add_theme_stylebox_override("panel", cap_sb)
	t_row.add_child(cap)

	var cap_lbl := Label.new()
	cap_lbl.name = "ColossusEntriesLabel"
	var entries_pattern := _t("power_stat.colossus_entries")
	cap_lbl.text = entries_pattern % left_entries
	_apply_font(cap_lbl, 13, COLOR_TEXT_DARK, true)
	cap.add_child(cap_lbl)

	# 推薦目標
	var target_lbl := Label.new()
	target_lbl.name = "ColossusTargetLabel"
	var rec_name := _get_recommended_colossus_name(gs)
	var target_pattern := _t("power_stat.colossus_target")
	target_lbl.text = target_pattern % rec_name
	_apply_font(target_lbl, 12, COLOR_TEXT_DARK, true)
	left_v.add_child(target_lbl)

	# 玩法說明文字
	var desc_lbl := Label.new()
	desc_lbl.name = "ColossusDescLabel"
	desc_lbl.text = _t("power_stat.colossus_desc")
	_apply_font(desc_lbl, 11, COLOR_TEXT_MUTED)
	left_v.add_child(desc_lbl)

	# 右側快捷按鈕：前往挑戰 (BtnGoColossus)
	_btn_go_colossus = Button.new()
	_btn_go_colossus.name = "BtnGoColossus"
	_btn_go_colossus.text = _t("power_stat.btn_go_colossus")
	_btn_go_colossus.custom_minimum_size = Vector2(120, 48)
	_btn_go_colossus.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_colossus, COLOR_GOLD, COLOR_TEXT_DARK, 14, 5, 18, COLOR_BORDER, 14, 6)
	_btn_go_colossus.pressed.connect(_on_go_colossus_pressed)
	h.add_child(_btn_go_colossus)

	return card


func _build_dummy_trial_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "DummyTrialCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "DummyTrialCardHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	m.add_child(h)

	# 讀取木人樁數值
	var best_dps := float(gs.get("best_dummy_dps")) if gs and "best_dummy_dps" in gs else 0.0
	var max_hit := int(gs.get("best_dummy_max_hit")) if gs and "best_dummy_max_hit" in gs else 0
	var hit_count := int(gs.get("best_dummy_hit_count")) if gs and "best_dummy_hit_count" in gs else 0
	var has_record := best_dps > 0.0

	# 左側資訊區
	var left_v := VBoxContainer.new()
	left_v.name = "DummyTrialLeftVBox"
	left_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 6)
	h.add_child(left_v)

	# 標題行與 DPS 徽章
	var t_row := HBoxContainer.new()
	t_row.name = "DummyTrialRowHBox"
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	left_v.add_child(t_row)

	var t_lbl := Label.new()
	t_lbl.name = "DummyTrialCardTitleLabel"
	var title_str := _t("power_stat.dummy_trial_card")
	if title_str == "power_stat.dummy_trial_card" or title_str.is_empty():
		title_str = _t("木人樁試招")
	t_lbl.text = title_str
	_apply_font(t_lbl, 14, COLOR_TEXT_ORANGE, true)
	t_row.add_child(t_lbl)

	# 歷史最佳 DPS 紀錄徽章
	var cap := PanelContainer.new()
	cap.name = "DpsBadgeCapsule"
	var cap_sb := StyleBoxFlat.new()
	if has_record:
		cap_sb.bg_color = COLOR_CARD_SKY
		cap_sb.border_color = COLOR_BORDER
		cap_sb.set_border_width_all(1)
		cap_sb.border_width_bottom = 3
		cap_sb.set_corner_radius_all(10)
		cap_sb.content_margin_left = 10
		cap_sb.content_margin_right = 10
		cap_sb.content_margin_top = 3
		cap_sb.content_margin_bottom = 3
	else:
		cap_sb.bg_color = COLOR_CARD_MUTED
		cap_sb.border_color = COLOR_BORDER_MUTED
		cap_sb.set_border_width_all(1)
		cap_sb.border_width_bottom = 2
		cap_sb.set_corner_radius_all(10)
		cap_sb.content_margin_left = 8
		cap_sb.content_margin_right = 8
		cap_sb.content_margin_top = 2
		cap_sb.content_margin_bottom = 2
	cap.add_theme_stylebox_override("panel", cap_sb)
	t_row.add_child(cap)

	var dps_lbl := Label.new()
	dps_lbl.name = "BestDpsLabel"
	if has_record:
		dps_lbl.text = "%.1f DPS" % best_dps
		_apply_font(dps_lbl, 13, COLOR_TEXT_DARK, true)
	else:
		var no_rec_badge := _t("power_stat.dummy_no_record_badge")
		if no_rec_badge == "power_stat.dummy_no_record_badge" or no_rec_badge.is_empty():
			no_rec_badge = _t("尚未試招")
		dps_lbl.text = no_rec_badge
		_apply_font(dps_lbl, 12, COLOR_TEXT_MUTED)
	cap.add_child(dps_lbl)

	# 詳情列 / 尚未試招引導
	if has_record:
		var stats_h := HBoxContainer.new()
		stats_h.name = "DummyStatsRowHBox"
		stats_h.add_theme_constant_override("separation", 14)
		stats_h.alignment = BoxContainer.ALIGNMENT_BEGIN
		left_v.add_child(stats_h)

		var max_hit_lbl := Label.new()
		max_hit_lbl.name = "MaxHitLabel"
		var mh_prefix := _t("power_stat.dummy_max_hit")
		if mh_prefix == "power_stat.dummy_max_hit" or mh_prefix.is_empty():
			mh_prefix = _t("最高單擊")
		max_hit_lbl.text = "%s: %d" % [mh_prefix, max_hit]
		_apply_font(max_hit_lbl, 12, COLOR_TEXT_DARK, true)
		stats_h.add_child(max_hit_lbl)

		var hit_cnt_lbl := Label.new()
		hit_cnt_lbl.name = "HitCountLabel"
		var hc_prefix := _t("power_stat.dummy_hit_count")
		if hc_prefix == "power_stat.dummy_hit_count" or hc_prefix.is_empty():
			hc_prefix = _t("出招記錄")
		hit_cnt_lbl.text = "%s: %d" % [hc_prefix, hit_count]
		_apply_font(hit_cnt_lbl, 12, COLOR_TEXT_DARK, true)
		stats_h.add_child(hit_cnt_lbl)

		var desc_lbl := Label.new()
		desc_lbl.name = "DummyDescLabel"
		var desc_str := _t("power_stat.dummy_desc")
		if desc_str == "power_stat.dummy_desc" or desc_str.is_empty():
			desc_str = _t("自由試招無消耗 · 隨時實測戰力傷害極限")
		desc_lbl.text = desc_str
		_apply_font(desc_lbl, 11, COLOR_TEXT_MUTED)
		left_v.add_child(desc_lbl)
	else:
		var no_rec_lbl := Label.new()
		no_rec_lbl.name = "NoRecordGuideLabel"
		var guide_str := _t("power_stat.dummy_no_record")
		if guide_str == "power_stat.dummy_no_record" or guide_str.is_empty():
			guide_str = _t("尚未進行試招，快前往木人樁測試最高傷害！")
		no_rec_lbl.text = guide_str
		_apply_font(no_rec_lbl, 12, COLOR_TEXT_MUTED)
		left_v.add_child(no_rec_lbl)

	# 右側快捷按鈕：前往試招 (BtnGoDummyPractice)
	_btn_go_dummy_practice = Button.new()
	_btn_go_dummy_practice.name = "BtnGoDummyPractice"
	var btn_txt := _t("power_stat.btn_go_dummy_practice")
	if btn_txt == "power_stat.btn_go_dummy_practice" or btn_txt.is_empty():
		btn_txt = _t("前往試招")
	_btn_go_dummy_practice.text = btn_txt
	_btn_go_dummy_practice.custom_minimum_size = Vector2(120, 48)
	_btn_go_dummy_practice.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_dummy_practice, COLOR_SKY, COLOR_TEXT_LIGHT, 14, 5, 18, COLOR_BORDER, 14, 6)
	_btn_go_dummy_practice.pressed.connect(_on_go_dummy_practice_pressed)
	h.add_child(_btn_go_dummy_practice)

	return card


func _build_vault_card(_gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "ClockworkVaultCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "ClockworkVaultCardHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	m.add_child(h)

	# 讀取發條儲能庫放置狀態
	var st: Dictionary = IdleClockworkVault.get_status()
	var sec: float = float(st.get("elapsed_seconds", 0.0))
	var hrs_i := int(sec / 3600.0)
	var mins_i := int(fmod(sec, 3600.0) / 60.0)
	var ratio: float = float(st.get("progress_ratio", 0.0))
	var is_full: bool = bool(st.get("is_full", false))

	# 左側資訊區：標題列與產能效率膠囊、累積能量與上限、收益說明文字
	var left_v := VBoxContainer.new()
	left_v.name = "ClockworkVaultLeftVBox"
	left_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 6)
	h.add_child(left_v)

	# 標題行與產能效率膠囊
	var t_row := HBoxContainer.new()
	t_row.name = "VaultTitleRowHBox"
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	left_v.add_child(t_row)

	var t_lbl := Label.new()
	t_lbl.name = "VaultCardTitleLabel"
	var title_str := _t("power_stat.vault_card")
	if title_str == "power_stat.vault_card" or title_str.is_empty():
		title_str = _t("發條儲能庫")
	t_lbl.text = title_str
	_apply_font(t_lbl, 14, COLOR_TEXT_ORANGE, true)
	t_row.add_child(t_lbl)

	# 當前產能效率膠囊
	var cap := PanelContainer.new()
	cap.name = "VaultRateCapsule"
	var cap_sb := StyleBoxFlat.new()
	cap_sb.bg_color = COLOR_CARD_GOLD
	cap_sb.border_color = COLOR_BORDER
	cap_sb.set_border_width_all(1)
	cap_sb.border_width_bottom = 3
	cap_sb.set_corner_radius_all(10)
	cap_sb.content_margin_left = 10
	cap_sb.content_margin_right = 10
	cap_sb.content_margin_top = 3
	cap_sb.content_margin_bottom = 3
	cap.add_theme_stylebox_override("panel", cap_sb)
	t_row.add_child(cap)

	var rate_lbl := Label.new()
	rate_lbl.name = "VaultRateLabel"
	var rate_str := _t("power_stat.vault_rate")
	if rate_str == "power_stat.vault_rate" or rate_str.is_empty():
		rate_str = _t("產能: 150金·3鐵/h")
	rate_lbl.text = rate_str
	_apply_font(rate_lbl, 12, COLOR_TEXT_DARK, true)
	cap.add_child(rate_lbl)

	# 累積放置能量值與上限文字
	var energy_lbl := Label.new()
	energy_lbl.name = "VaultEnergyLabel"
	var time_str := "%02d:%02d / 08:00" % [hrs_i, mins_i]
	var pct_str := "(%d%%)" % int(ratio * 100.0)
	if is_full:
		var full_tag := _t("vault.max_cap")
		if full_tag == "vault.max_cap" or full_tag.is_empty():
			full_tag = _t("已蓄滿 (8小時)")
		pct_str = "[%s]" % full_tag
	var energy_pattern := _t("power_stat.vault_energy")
	if energy_pattern == "power_stat.vault_energy" or energy_pattern.is_empty():
		energy_pattern = "累積能量: %s %s"
	energy_lbl.text = energy_pattern % [time_str, pct_str]
	_apply_font(energy_lbl, 12, COLOR_TEXT_DARK, true)
	left_v.add_child(energy_lbl)

	# 說明文字
	var desc_lbl := Label.new()
	desc_lbl.name = "VaultDescLabel"
	var desc_str := _t("power_stat.vault_desc")
	if desc_str == "power_stat.vault_desc" or desc_str.is_empty():
		desc_str = _t("放置收益隨時間蓄能 · 離線最高累計8小時")
	desc_lbl.text = desc_str
	_apply_font(desc_lbl, 11, COLOR_TEXT_MUTED)
	left_v.add_child(desc_lbl)

	# 右側快捷按鈕：前往儲能 (BtnGoVault)
	_btn_go_vault = Button.new()
	_btn_go_vault.name = "BtnGoVault"
	var vault_btn_txt := _t("power_stat.btn_go_vault")
	if vault_btn_txt == "power_stat.btn_go_vault" or vault_btn_txt.is_empty():
		vault_btn_txt = _t("前往儲能")
	_btn_go_vault.text = vault_btn_txt
	_btn_go_vault.custom_minimum_size = Vector2(120, 48)
	_btn_go_vault.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_vault, COLOR_GOLD, COLOR_TEXT_DARK, 14, 5, 18, COLOR_BORDER, 14, 6)
	_btn_go_vault.pressed.connect(_on_go_vault_pressed)
	h.add_child(_btn_go_vault)

	return card


func _build_windup_daily_card(_gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "WindupDailyCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "WindupDailyCardHBox"
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	m.add_child(h)

	# 讀取 QuestSystem 與 WindupDailySystem 狀態
	var loop := Engine.get_main_loop()
	var qs: Node = null
	var ws: Node = null
	if loop is SceneTree and (loop as SceneTree).root != null:
		qs = (loop as SceneTree).root.get_node_or_null("QuestSystem")
		ws = (loop as SceneTree).root.get_node_or_null("WindupDailySystem")

	var total_comm := 3
	var done_comm := 0
	var claimed_comm := 0
	var claimable_comm := 0
	if qs != null:
		if qs.has_method("refresh_daily"):
			qs.call("refresh_daily")
		if qs.has_method("todays_commissions_raw"):
			var raw_c: Array = qs.call("todays_commissions_raw")
			if not raw_c.is_empty():
				total_comm = raw_c.size()
				for c in raw_c:
					if qs.has_method("commission_done") and bool(qs.call("commission_done", c)):
						done_comm += 1
					var cid := str(c.get("id", ""))
					if qs.has_method("commission_claimed") and bool(qs.call("commission_claimed", cid)):
						claimed_comm += 1
		if qs.has_method("claimable_commissions"):
			claimable_comm = int(qs.call("claimable_commissions"))

	var is_windup_done := false
	var case_title := ""
	if ws != null:
		if ws.has_method("refresh"):
			ws.call("refresh")
		if ws.has_method("is_done_today"):
			is_windup_done = bool(ws.call("is_done_today"))
		if ws.has_method("todays_case"):
			var tc: Dictionary = ws.call("todays_case")
			case_title = str(tc.get("title", ""))

	# 左側資訊區
	var left_v := VBoxContainer.new()
	left_v.name = "WindupDailyLeftVBox"
	left_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 6)
	h.add_child(left_v)

	# 標題行與狀態/領取膠囊
	var t_row := HBoxContainer.new()
	t_row.name = "WindupTitleRowHBox"
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	left_v.add_child(t_row)

	var t_lbl := Label.new()
	t_lbl.name = "WindupCardTitleLabel"
	var title_str := _t("power_stat.windup_card")
	if title_str == "power_stat.windup_card" or title_str.is_empty():
		title_str = _t("冒險委託上發條")
	t_lbl.text = title_str
	_apply_font(t_lbl, 14, COLOR_TEXT_ORANGE, true)
	t_row.add_child(t_lbl)

	# 委託狀態標籤膠囊 (WindupStatusCapsule)
	var is_all_done: bool = (done_comm >= total_comm and total_comm > 0) or is_windup_done
	var status_cap := PanelContainer.new()
	status_cap.name = "WindupStatusCapsule"
	var status_sb := StyleBoxFlat.new()
	status_sb.bg_color = COLOR_CARD_MINT if is_all_done else COLOR_CARD_GOLD
	status_sb.border_color = COLOR_BORDER
	status_sb.set_border_width_all(1)
	status_sb.border_width_bottom = 3
	status_sb.set_corner_radius_all(10)
	status_sb.content_margin_left = 10
	status_sb.content_margin_right = 10
	status_sb.content_margin_top = 3
	status_sb.content_margin_bottom = 3
	status_cap.add_theme_stylebox_override("panel", status_sb)
	t_row.add_child(status_cap)

	var status_lbl := Label.new()
	status_lbl.name = "WindupStatusLabel"
	var status_str := ""
	if is_all_done:
		status_str = _t("power_stat.windup_status_done")
		if status_str == "power_stat.windup_status_done" or status_str.is_empty():
			status_str = _t("今日已完成")
	else:
		status_str = _t("power_stat.windup_status_ready")
		if status_str == "power_stat.windup_status_ready" or status_str.is_empty():
			status_str = _t("待完成委託")
	status_lbl.text = status_str
	_apply_font(status_lbl, 12, Color("#1E8238") if is_all_done else COLOR_TEXT_ORANGE, true)
	status_cap.add_child(status_lbl)

	# 今日領取膠囊 (WindupClaimCapsule)
	var is_claimed: bool = (claimed_comm >= total_comm and total_comm > 0) or is_windup_done
	var claim_cap := PanelContainer.new()
	claim_cap.name = "WindupClaimCapsule"
	var claim_sb := StyleBoxFlat.new()
	claim_sb.bg_color = COLOR_CARD_SKY if is_claimed else (COLOR_CARD_GOLD if claimable_comm > 0 else COLOR_CARD_WARM)
	claim_sb.border_color = COLOR_BORDER
	claim_sb.set_border_width_all(1)
	claim_sb.border_width_bottom = 3
	claim_sb.set_corner_radius_all(10)
	claim_sb.content_margin_left = 10
	claim_sb.content_margin_right = 10
	claim_sb.content_margin_top = 3
	claim_sb.content_margin_bottom = 3
	claim_cap.add_theme_stylebox_override("panel", claim_sb)
	t_row.add_child(claim_cap)

	var claim_lbl := Label.new()
	claim_lbl.name = "WindupClaimLabel"
	var claim_str := ""
	if is_claimed:
		claim_str = _t("power_stat.windup_claimed")
		if claim_str == "power_stat.windup_claimed" or claim_str.is_empty():
			claim_str = _t("今日已領取")
	elif claimable_comm > 0:
		claim_str = _t("power_stat.windup_claimable")
		if claim_str == "power_stat.windup_claimable" or claim_str.is_empty():
			claim_str = _t("可領取獎勵")
	else:
		claim_str = _t("power_stat.windup_unclaimed")
		if claim_str == "power_stat.windup_unclaimed" or claim_str.is_empty():
			claim_str = _t("今日未領取")
	claim_lbl.text = claim_str
	_apply_font(claim_lbl, 12, COLOR_TEXT_DARK if is_claimed else (COLOR_TEXT_ORANGE if claimable_comm > 0 else COLOR_TEXT_MUTED), true)
	claim_cap.add_child(claim_lbl)

	# 委託進度標籤 (WindupProgressLabel)
	var prog_lbl := Label.new()
	prog_lbl.name = "WindupProgressLabel"
	var prog_pattern := _t("power_stat.windup_progress")
	if prog_pattern == "power_stat.windup_progress" or prog_pattern.is_empty():
		prog_pattern = "今日委託進度: %d/%d"
	var prog_text := prog_pattern % [done_comm, total_comm]
	if not case_title.is_empty():
		prog_text += " · " + _t(case_title)
	prog_lbl.text = prog_text
	_apply_font(prog_lbl, 12, COLOR_TEXT_DARK, true)
	left_v.add_child(prog_lbl)

	# 說明文字 (WindupDescLabel)
	var desc_lbl := Label.new()
	desc_lbl.name = "WindupDescLabel"
	var desc_str := _t("power_stat.windup_desc")
	if desc_str == "power_stat.windup_desc" or desc_str.is_empty():
		desc_str = _t("每天一件發條小事 · 完成日常委託領取星屑與金幣")
	desc_lbl.text = desc_str
	_apply_font(desc_lbl, 11, COLOR_TEXT_MUTED)
	left_v.add_child(desc_lbl)

	# 右側快捷按鈕：前往委託 (BtnGoWindupDaily)
	_btn_go_windup_daily = Button.new()
	_btn_go_windup_daily.name = "BtnGoWindupDaily"
	var btn_txt := _t("power_stat.btn_go_windup")
	if btn_txt == "power_stat.btn_go_windup" or btn_txt.is_empty():
		btn_txt = _t("前往委託")
	_btn_go_windup_daily.text = btn_txt
	_btn_go_windup_daily.custom_minimum_size = Vector2(120, 48)
	_btn_go_windup_daily.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_style_jelly_btn(_btn_go_windup_daily, COLOR_GOLD, COLOR_TEXT_DARK, 14, 5, 18, COLOR_BORDER, 14, 6)
	_btn_go_windup_daily.pressed.connect(_on_go_windup_daily_pressed)
	h.add_child(_btn_go_windup_daily)

	return card


func _get_colossus_remaining_entries() -> int:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var cds: Node = (loop as SceneTree).root.get_node_or_null("ColossusDailySystem")
		if cds and cds.has_method("get_remaining_entries"):
			return int(cds.call("get_remaining_entries"))
	var gs := _gs()
	if gs and "colossus_daily_entries" in gs:
		return maxi(0, int(gs.get("colossus_daily_entries")))
	return 3


func _get_recommended_colossus_name(gs: Node) -> String:
	var plv: int = 1
	if gs and "level" in gs:
		plv = int(gs.get("level"))
	if plv >= 18:
		return _t("黑鏽蒸氣巨象") + " (Lv.28)"
	elif plv >= 10:
		return _t("霧鐘提線人偶") + " (Lv.20)"
	else:
		return _t("失控發條獅") + " (Lv.12)"


func _on_go_equip_pressed() -> void:
	equip_requested.emit()
	_on_close_pressed()


func _on_go_workshop_pressed() -> void:
	workshop_requested.emit()
	_on_close_pressed()


func _on_go_skill_pressed() -> void:
	skill_requested.emit()
	_on_close_pressed()


func _on_go_soul_pressed() -> void:
	soul_requested.emit()
	_on_close_pressed()


func _on_go_calibrate_pressed() -> void:
	calibrate_requested.emit()
	_on_close_pressed()


func _on_go_forge_pressed() -> void:
	forge_requested.emit()
	_on_close_pressed()


func get_go_skill_button() -> Button:
	return _btn_go_skill


func get_go_soul_button() -> Button:
	return _btn_go_soul


func get_go_forge_button() -> Button:
	return _btn_go_forge


func _on_go_title_wall_pressed() -> void:
	title_wall_requested.emit()
	_on_close_pressed()


func get_go_title_wall_button() -> Button:
	return _btn_go_title_wall


func _on_go_inventory_pressed() -> void:
	inventory_requested.emit()
	_on_close_pressed()


func get_go_inventory_button() -> Button:
	return _btn_go_inventory


func _on_go_colossus_pressed() -> void:
	colossus_requested.emit()
	_on_close_pressed()


func get_go_colossus_button() -> Button:
	return _btn_go_colossus


func get_colossus_card() -> PanelContainer:
	return find_child("ColossusCard", true, false) as PanelContainer


func _on_go_dummy_practice_pressed() -> void:
	go_dummy_practice.emit()
	_on_close_pressed()


func get_go_dummy_practice_button() -> Button:
	return _btn_go_dummy_practice


func get_dummy_trial_card() -> PanelContainer:
	return find_child("DummyTrialCard", true, false) as PanelContainer


func _on_go_vault_pressed() -> void:
	vault_requested.emit()
	_on_close_pressed()


func _on_go_windup_daily_pressed() -> void:
	windup_daily_requested.emit()
	_on_close_pressed()


func get_go_vault_button() -> Button:
	return _btn_go_vault


func get_go_windup_daily_button() -> Button:
	return _btn_go_windup_daily


func get_clockwork_vault_card() -> PanelContainer:
	return find_child("ClockworkVaultCard", true, false) as PanelContainer


func get_vault_card() -> PanelContainer:
	return get_clockwork_vault_card()


func get_windup_daily_card() -> PanelContainer:
	return find_child("WindupDailyCard", true, false) as PanelContainer


func get_scroll_box() -> ScrollContainer:
	return _scroll_box


func scroll_to_bottom() -> void:
	if _scroll_box:
		var vbar := _scroll_box.get_v_scroll_bar()
		if vbar:
			vbar.value = vbar.max_value - vbar.page
			_scroll_box.scroll_vertical = int(vbar.value)
		else:
			_scroll_box.scroll_vertical = 99999
		var card := get_windup_daily_card()
		if card == null:
			card = get_vault_card()
		if card:
			_scroll_box.ensure_control_visible(card)


func scroll_to_vault_card() -> void:
	scroll_to_bottom()


func scroll_to_windup_daily_card() -> void:
	scroll_to_bottom()


func _on_close_pressed() -> void:
	closed.emit()
	queue_free()


func _create_card_style(bg: Color, border: Color, b_width: int = 1, b_bottom: int = 3, radius: int = 12) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(b_width)
	sb.border_width_bottom = b_bottom
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)
	return sb


func _style_jelly_btn(btn: Button, bg: Color, text_col: Color, font_sz: int, bottom_px: int = 5, radius: int = 16, border_col: Color = COLOR_BORDER, pad_h: int = 12, pad_v: int = 6) -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border_col
	sb.set_border_width_all(2)
	sb.border_width_bottom = bottom_px
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = pad_h
	sb.content_margin_right = pad_h
	sb.content_margin_top = pad_v
	sb.content_margin_bottom = pad_v
	if bottom_px > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = bg.lightened(0.1)

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = maxi(2, bottom_px - 3)

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)
	btn.add_theme_stylebox_override("disabled", sb)

	_apply_font(btn, font_sz, text_col, true)


func _apply_font(node: Control, sz: int, color: Color = COLOR_TEXT_DARK, bold: bool = false) -> void:
	if _cached_font:
		node.add_theme_font_override("font", _cached_font)
	node.add_theme_font_size_override("font_size", sz)
	if node is Label:
		node.add_theme_color_override("font_color", color)
	elif node is Button:
		node.add_theme_color_override("font_color", color)
		node.add_theme_color_override("font_hover_color", color)
		node.add_theme_color_override("font_pressed_color", color)
		node.add_theme_color_override("font_disabled_color", COLOR_TEXT_DIM)
		if bold and color == COLOR_TEXT_LIGHT:
			node.add_theme_color_override("font_outline_color", COLOR_BORDER)
			node.add_theme_constant_override("outline_size", 2)


func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


func _eq() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	return null


func _gem() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GemSystem")
	return null


func _sk() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("SkillSystem")
	return null


func _soul() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("SoulSystem")
	return null


func _core_sys() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("CoreSystem")
	return null
