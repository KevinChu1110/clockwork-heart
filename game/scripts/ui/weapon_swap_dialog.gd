class_name WeaponSwapDialog
extends Control
## 《發條之心》大廳角色頁三欄武器槽更換裝備彈窗 (WeaponSwapDialog)
## 依多巴胺鮮亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 750px（740~760px），高 540px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 50x50px，底部與卡片內按鈕熱區均 >= 48px。
## 3. 多巴胺鮮亮高飽和色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 16~22px，按鈕立體果凍厚底 5px。
## 5. 零系統 Emoji，使用粉圓體 (Open Huninn)。
## 6. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換)。
## 7. 支援三欄槽位分頁切換、背包/庫存武器清單、數值對比、即時連動 GameState 與 EquipmentSystem。

signal weapon_swapped(slot_idx: int, uid: String)
signal slot_unequipped(slot_idx: int)
signal closed()
signal line_filter_changed(line_id: String)

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
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


static func get_weapon_atk(inst: Dictionary) -> int:
	var atk: int = int(inst.get("weapon_atk", 0))
	if atk <= 0 and inst.has("rolled") and inst["rolled"] is Dictionary:
		atk = int(inst["rolled"].get("atk", 0))
	return atk


static func sort_weapons_by_atk_desc(weapons: Array) -> Array:
	var list: Array = weapons.duplicate(true)
	list.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var atkA := get_weapon_atk(a)
		var atkB := get_weapon_atk(b)
		if atkA != atkB:
			return atkA > atkB
		return str(a.get("uid", "")) < str(b.get("uid", ""))
	)
	return list

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD         := Color("#FFD028")  ## 金黃
const COLOR_ORANGE       := Color("#FFA010")  ## 暖橘
const COLOR_MINT         := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY          := Color("#38A0FF")  ## 天藍
const COLOR_PINK         := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER       := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM     := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM    := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD    := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_SKY     := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_MUTED   := Color("#EFEBE0")  ## 壓暗奶油底
const COLOR_BORDER_MUTED := Color("#D2CCC0")  ## 壓暗淡邊框

## ── 亮底合規文字色 ──
const COLOR_TEXT_DARK    := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD    := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE  := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MUTED   := Color("#6B6680")  ## 次要輔助文字
const COLOR_TEXT_DIM     := Color("#888294")  ## 壓暗提示文字

## ── 攻擊力差額對比膠囊多巴胺高對比配色 ──
const COLOR_DIFF_POS_BG   := Color("#DDF7E3")  ## 薄荷綠柔底 (高於當前)
const COLOR_DIFF_POS_TEXT := Color("#1B7535")  ## 薄荷綠加粗深字 (高於當前)
const COLOR_DIFF_POS_BD   := Color("#38B653")  ## 薄荷綠邊框 (高於當前)

const COLOR_DIFF_NEG_BG   := Color("#EFEBE0")  ## 柔和灰底 (低於當前)
const COLOR_DIFF_NEG_TEXT := Color("#6B6680")  ## 柔和灰文字 (低於當前)
const COLOR_DIFF_NEG_BD   := Color("#D2CCC0")  ## 柔和灰邊框 (低於當前)

const COLOR_DIFF_EQ_BG    := Color("#F4F1EA")  ## 相等/為空底
const COLOR_DIFF_EQ_TEXT  := Color("#888294")  ## 相等/為空文字
const COLOR_DIFF_EQ_BD    := Color("#DCD7CC")  ## 相等/為空邊框

const LINE_NAMES: Dictionary = {
	"sword": "劍",
	"spear": "長槍",
	"axe": "斧",
	"hammer": "鎚",
	"dagger": "匕首",
	"dart": "鏢",
	"fist": "拳套",
	"claw": "爪",
	"magic": "法杖",
	"crystal": "靈晶",
	"bow": "弓",
	"gun": "銃",
}

const LINE_HITS: Dictionary = {
	"sword": "4 次打擊",
	"bow": "4 次打擊",
	"fist": "5 連擊",
	"dagger": "4 次打擊",
	"claw": "5 連擊",
	"dart": "4 次打擊",
	"spear": "3 次打擊",
	"axe": "3 次打擊",
	"hammer": "2 次打擊",
	"gun": "3 次打擊",
	"magic": "4 次打擊",
	"crystal": "4 次打擊",
}

const SLOT_TITLES: Array[String] = [
	"首選武器",
	"副手武器",
	"絕技武器",
]

const FILTER_CHIPS: Array[Dictionary] = [
	{"id": "all", "key": "全部", "line": "all"},
	{"id": "sword", "key": "劍", "line": "sword"},
	{"id": "spear", "key": "長槍", "line": "spear"},
	{"id": "axe", "key": "斧", "line": "axe"},
	{"id": "hammer_alt", "key": "錘", "line": "hammer"},
	{"id": "dagger", "key": "匕首", "line": "dagger"},
	{"id": "hammer", "key": "鎚", "line": "hammer"},
	{"id": "fist", "key": "拳套", "line": "fist"},
	{"id": "claw", "key": "爪", "line": "claw"},
	{"id": "magic", "key": "法杖", "line": "magic"},
	{"id": "crystal", "key": "靈晶", "line": "crystal"},
	{"id": "bow", "key": "弓", "line": "bow"},
	{"id": "gun", "key": "銃", "line": "gun"},
]

const FILTER_CHIP_I18N: Dictionary = {
	"全部": {"zh_TW": "全部", "zh_CN": "全部", "en": "All", "ja": "全部", "ko": "전체", "es": "Todo"},
	"劍": {"zh_TW": "劍", "zh_CN": "剑", "en": "Sword", "ja": "剣", "ko": "검", "es": "Espada"},
	"長槍": {"zh_TW": "長槍", "zh_CN": "长枪", "en": "Spear", "ja": "長槍", "ko": "창", "es": "Lanza"},
	"斧": {"zh_TW": "斧", "zh_CN": "斧", "en": "Axe", "ja": "斧", "ko": "도끼", "es": "Hacha"},
	"錘": {"zh_TW": "錘", "zh_CN": "锤", "en": "Mace", "ja": "金槌", "ko": "철퇴", "es": "Maza"},
	"匕首": {"zh_TW": "匕首", "zh_CN": "匕首", "en": "Dagger", "ja": "短剣", "ko": "단검", "es": "Daga"},
	"鎚": {"zh_TW": "鎚", "zh_CN": "锤", "en": "Hammer", "ja": "槌", "ko": "망치", "es": "Martillo"},
	"拳套": {"zh_TW": "拳套", "zh_CN": "拳套", "en": "Gauntlets", "ja": "拳套", "ko": "건틀릿", "es": "Guantelete"},
	"爪": {"zh_TW": "爪", "zh_CN": "爪", "en": "Claw", "ja": "爪", "ko": "클로", "es": "Garra"},
	"法杖": {"zh_TW": "法杖", "zh_CN": "法杖", "en": "Staff", "ja": "法杖", "ko": "지팡이", "es": "Báculo"},
	"靈晶": {"zh_TW": "靈晶", "zh_CN": "灵晶", "en": "Crystal", "ja": "霊晶", "ko": "영정", "es": "Cristal"},
	"弓": {"zh_TW": "弓", "zh_CN": "弓", "en": "Bow", "ja": "弓", "ko": "활", "es": "Arco"},
	"銃": {"zh_TW": "銃", "zh_CN": "铳", "en": "Gun", "ja": "銃", "ko": "총", "es": "Fusil"},
}

static func _normalize_line(raw: String) -> String:
	match raw.to_lower():
		"sword", "劍", "剑":
			return "sword"
		"spear", "長槍", "长枪", "槍", "枪":
			return "spear"
		"axe", "斧":
			return "axe"
		"hammer", "hammer_alt", "鎚", "錘", "锤":
			return "hammer"
		"dagger", "匕首", "匕":
			return "dagger"
		"dart", "鏢", "镖":
			return "dart"
		"fist", "拳套", "拳":
			return "fist"
		"claw", "爪":
			return "claw"
		"magic", "法杖", "杖":
			return "magic"
		"crystal", "靈晶", "灵晶", "水晶":
			return "crystal"
		"bow", "弓":
			return "bow"
		"gun", "銃", "铳", "火槍", "火枪":
			return "gun"
		_:
			return raw.to_lower()

static func matches_line_filter(w_line: String, filter: String) -> bool:
	if filter == "all" or filter == "全部" or filter.is_empty():
		return true
	var norm_w := _normalize_line(w_line)
	var norm_f := _normalize_line(filter)
	return norm_w == norm_f

var _target_slot: int = 0
var current_filter_line: String = "all"
var _dialog_card: PanelContainer
var _title_lbl: Label
var _sub_title_lbl: Label
var _close_x_btn: Button
var _bottom_close_btn: Button
var _slot_tab_buttons: Array[Button] = []
var _slot_summary_panel: PanelContainer
var _slot_summary_lbl: Label
var _btn_unequip: Button
var _chip_scroll: ScrollContainer
var _chips_box: HBoxContainer
var _filter_chip_buttons: Dictionary = {}
var _scroll_box: ScrollContainer
var _weapons_box: VBoxContainer
var _empty_panel: PanelContainer
var _empty_title_lbl: Label
var _empty_sub_lbl: Label
var _bottom_hint_lbl: Label
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
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_refresh_texts()
	_refresh_slot_tabs()
	_refresh_slot_summary()
	_refresh_filter_chips()
	_rebuild_weapon_list()


func _init(initial_slot: int = 0) -> void:
	_target_slot = clampi(initial_slot, 0, 2)


func setup(slot_idx: int) -> void:
	_target_slot = clampi(slot_idx, 0, 2)
	if _built:
		_refresh_slot_tabs()
		_refresh_slot_summary()
		_refresh_filter_chips()
		_rebuild_weapon_list()


func _ready() -> void:
	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_ui()
	_refresh_slot_tabs()
	_refresh_slot_summary()
	_refresh_filter_chips()
	_rebuild_weapon_list()


func _build_ui() -> void:
	_built = true
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP

	# 1. 全螢幕半透明遮罩
	var scrim := ColorRect.new()
	scrim.name = "ModalScrim"
	scrim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim.color = Color(0.12, 0.10, 0.15, 0.75)
	scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(scrim)

	# 2. 置中卡片 (750 x 540)
	var card := PanelContainer.new()
	card.name = "DialogCard"
	card.custom_minimum_size = Vector2(750, 540)
	card.set_anchors_preset(Control.PRESET_CENTER)
	card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	card.grow_vertical = Control.GROW_DIRECTION_BOTH
	card.mouse_filter = Control.MOUSE_FILTER_STOP

	var card_sb := StyleBoxFlat.new()
	card_sb.bg_color = COLOR_BG_CREAM
	card_sb.border_color = COLOR_BORDER
	card_sb.set_border_width_all(2)
	card_sb.border_width_bottom = 6
	card_sb.set_corner_radius_all(22)
	card_sb.content_margin_left = 20
	card_sb.content_margin_right = 20
	card_sb.content_margin_top = 16
	card_sb.content_margin_bottom = 16
	card_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	card_sb.shadow_size = 8
	card_sb.shadow_offset = Vector2(0, 4)
	card.add_theme_stylebox_override("panel", card_sb)
	add_child(card)
	_dialog_card = card

	var root_v := VBoxContainer.new()
	root_v.name = "RootVBox"
	root_v.add_theme_constant_override("separation", 10)
	root_v.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.add_child(root_v)

	# 3. 頂部列（標題 + 右上✕）
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
	_apply_font(_title_lbl, 20, COLOR_TEXT_DARK, true)
	title_box.add_child(_title_lbl)

	_sub_title_lbl = Label.new()
	_sub_title_lbl.name = "SubTitleLabel"
	_apply_font(_sub_title_lbl, 13, COLOR_TEXT_MUTED)
	title_box.add_child(_sub_title_lbl)

	_close_x_btn = Button.new()
	_close_x_btn.name = "BtnCloseX"
	_close_x_btn.text = "✕"
	_close_x_btn.custom_minimum_size = Vector2(50, 50)
	_style_jelly_btn(_close_x_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 18, 5, 18)
	_close_x_btn.pressed.connect(_on_close_pressed)
	top_h.add_child(_close_x_btn)

	# 4. 槽位切換 Tab (首選 / 副手 / 絕技)
	var tab_row := HBoxContainer.new()
	tab_row.name = "SlotTabRow"
	tab_row.add_theme_constant_override("separation", 10)
	root_v.add_child(tab_row)

	_slot_tab_buttons.clear()
	for i in range(3):
		var tab_btn := Button.new()
		tab_btn.name = "SlotTab_%d" % i
		tab_btn.custom_minimum_size = Vector2(0, 48)
		tab_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var slot_idx := i
		tab_btn.pressed.connect(func(): _select_target_slot(slot_idx))
		tab_row.add_child(tab_btn)
		_slot_tab_buttons.append(tab_btn)

	# 5. 當前槽位配置摘要橫條
	_slot_summary_panel = PanelContainer.new()
	_slot_summary_panel.name = "SlotSummaryPanel"
	var sum_sb := StyleBoxFlat.new()
	sum_sb.bg_color = COLOR_CARD_GOLD
	sum_sb.border_color = COLOR_BORDER
	sum_sb.set_border_width_all(2)
	sum_sb.border_width_bottom = 4
	sum_sb.set_corner_radius_all(14)
	sum_sb.content_margin_left = 14
	sum_sb.content_margin_right = 14
	sum_sb.content_margin_top = 8
	sum_sb.content_margin_bottom = 8
	_slot_summary_panel.add_theme_stylebox_override("panel", sum_sb)
	root_v.add_child(_slot_summary_panel)

	var sum_h := HBoxContainer.new()
	sum_h.add_theme_constant_override("separation", 12)
	_slot_summary_panel.add_child(sum_h)

	_slot_summary_lbl = Label.new()
	_slot_summary_lbl.name = "SummaryLabel"
	_slot_summary_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_apply_font(_slot_summary_lbl, 14, COLOR_TEXT_DARK)
	sum_h.add_child(_slot_summary_lbl)

	_btn_unequip = Button.new()
	_btn_unequip.name = "BtnUnequip"
	_btn_unequip.text = _t("卸下武器")
	_btn_unequip.custom_minimum_size = Vector2(100, 48)
	_style_jelly_btn(_btn_unequip, COLOR_CARD_WARM, COLOR_TEXT_ORANGE, 13, 5, 14)
	_btn_unequip.pressed.connect(_on_unequip_pressed)
	sum_h.add_child(_btn_unequip)

	# 5.5 流派篩選 Chip 列 (水平捲動，按鈕熱區 >= 48px，果凍厚底)
	var filter_scroll := ScrollContainer.new()
	filter_scroll.name = "LineFilterScroll"
	filter_scroll.custom_minimum_size = Vector2(0, 52)
	filter_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	filter_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	filter_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	root_v.add_child(filter_scroll)
	_chip_scroll = filter_scroll

	var filter_h := HBoxContainer.new()
	filter_h.name = "LineFilterHBox"
	filter_h.add_theme_constant_override("separation", 6)
	filter_scroll.add_child(filter_h)
	_chips_box = filter_h

	_build_filter_chips()

	# 6. 武器清單捲動容器
	_scroll_box = ScrollContainer.new()
	_scroll_box.name = "WeaponsScroll"
	_scroll_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_scroll_box.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root_v.add_child(_scroll_box)

	_weapons_box = VBoxContainer.new()
	_weapons_box.name = "WeaponsBox"
	_weapons_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_weapons_box.add_theme_constant_override("separation", 8)
	_scroll_box.add_child(_weapons_box)

	# 空狀態提示
	_empty_panel = PanelContainer.new()
	_empty_panel.name = "EmptyPanel"
	var emp_sb := StyleBoxFlat.new()
	emp_sb.bg_color = COLOR_CARD_WARM
	emp_sb.border_color = COLOR_BORDER
	emp_sb.set_border_width_all(2)
	emp_sb.border_width_bottom = 4
	emp_sb.set_corner_radius_all(16)
	emp_sb.content_margin_left = 16
	emp_sb.content_margin_right = 16
	emp_sb.content_margin_top = 30
	emp_sb.content_margin_bottom = 30
	_empty_panel.add_theme_stylebox_override("panel", emp_sb)
	_empty_panel.visible = false
	_weapons_box.add_child(_empty_panel)

	var emp_v := VBoxContainer.new()
	emp_v.alignment = BoxContainer.ALIGNMENT_CENTER
	emp_v.add_theme_constant_override("separation", 6)
	_empty_panel.add_child(emp_v)

	var emp_t := Label.new()
	emp_t.name = "EmptyTitle"
	emp_t.text = _t("背包與庫存尚無可替換武器")
	emp_t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(emp_t, 16, COLOR_TEXT_DARK, true)
	emp_v.add_child(emp_t)
	_empty_title_lbl = emp_t

	var emp_sub := Label.new()
	emp_sub.name = "EmptySub"
	emp_sub.text = _t("可前往冒險出征獲取或在鍛造殿堂打造新武器")
	emp_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(emp_sub, 13, COLOR_TEXT_MUTED)
	emp_v.add_child(emp_sub)
	_empty_sub_lbl = emp_sub

	# 7. 底部列（提示文字 + 關閉按鈕）
	var bot_h := HBoxContainer.new()
	bot_h.name = "BottomBar"
	bot_h.add_theme_constant_override("separation", 12)
	root_v.add_child(bot_h)

	_bottom_hint_lbl = Label.new()
	_bottom_hint_lbl.name = "BottomHintLabel"
	_bottom_hint_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_apply_font(_bottom_hint_lbl, 12, COLOR_TEXT_MUTED)
	bot_h.add_child(_bottom_hint_lbl)

	_bottom_close_btn = Button.new()
	_bottom_close_btn.name = "BtnBottomClose"
	_bottom_close_btn.text = _t("關閉")
	_bottom_close_btn.custom_minimum_size = Vector2(110, 48)
	_style_jelly_btn(_bottom_close_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 15, 5, 16)
	_bottom_close_btn.pressed.connect(_on_close_pressed)
	bot_h.add_child(_bottom_close_btn)

	_refresh_texts()


func _refresh_texts() -> void:
	if _title_lbl:
		_title_lbl.text = _t("武器庫 · 更換裝備")
	if _sub_title_lbl:
		var slot_name := _t(SLOT_TITLES[_target_slot])
		_sub_title_lbl.text = _t("選擇要裝備至【%s】的武器 · 即時連動紙娃娃與屬性") % slot_name
	if _bottom_hint_lbl:
		_bottom_hint_lbl.text = _t("點擊武器卡片即可立即更換，即時更新戰鬥屬性與外觀紙娃娃")
	if _bottom_close_btn:
		_bottom_close_btn.text = _t("關閉")
	if _btn_unequip:
		_btn_unequip.text = _t("卸下武器")


func _select_target_slot(slot_idx: int) -> void:
	var eq := _get_equip_sys()
	if eq and eq.has_method("loadout_slot_unlocked"):
		if not bool(eq.call("loadout_slot_unlocked", slot_idx)):
			var req_lv: int = 10 if slot_idx == 1 else 16
			if eq.has_method("loadout_unlock_level"):
				req_lv = int(eq.call("loadout_unlock_level", slot_idx))
			_toast(_t("需達 Lv%d 解鎖") % req_lv)
			return

	_target_slot = slot_idx
	_refresh_texts()
	_refresh_slot_tabs()
	_refresh_slot_summary()
	_rebuild_weapon_list()


func _refresh_slot_tabs() -> void:
	var eq := _get_equip_sys()
	var gs := _gs()
	for i in range(_slot_tab_buttons.size()):
		var btn := _slot_tab_buttons[i]
		var unlocked := true
		var req_lv := 10 if i == 1 else 16
		if eq and eq.has_method("loadout_slot_unlocked"):
			unlocked = bool(eq.call("loadout_slot_unlocked", i))
			if eq.has_method("loadout_unlock_level"):
				req_lv = int(eq.call("loadout_unlock_level", i))

		var cur_wname := _t("空槽")
		var wuid := ""
		if eq and eq.has_method("loadout_uid"):
			wuid = str(eq.call("loadout_uid", i))
		elif gs and "weapon_loadout" in gs and i < gs.weapon_loadout.size():
			wuid = str(gs.weapon_loadout[i])

		if not wuid.is_empty():
			var inst: Dictionary = {}
			if eq and eq.has_method("weapon_inst"):
				inst = eq.call("weapon_inst", wuid)
			if inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
				inst = gs.equip_worn.get(wuid, {})
			if not inst.is_empty():
				cur_wname = _t(str(inst.get("name", "武器")))

		var slot_title := _t(SLOT_TITLES[i])
		if not unlocked:
			btn.text = "%s · %s" % [slot_title, _t("需達 Lv%d 解鎖") % req_lv]
			_style_jelly_btn(btn, COLOR_CARD_MUTED, COLOR_TEXT_DIM, 13, 3, 14, COLOR_BORDER_MUTED)
		elif i == _target_slot:
			btn.text = "%s · %s" % [slot_title, cur_wname]
			_style_jelly_btn(btn, COLOR_ORANGE, COLOR_TEXT_DARK, 14, 5, 16)
		else:
			btn.text = "%s · %s" % [slot_title, cur_wname]
			_style_jelly_btn(btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 13, 4, 14)


func _refresh_slot_summary() -> void:
	var eq := _get_equip_sys()
	var gs := _gs()
	var slot_title := _t(SLOT_TITLES[_target_slot])
	var cur_uid := ""
	if eq and eq.has_method("loadout_uid"):
		cur_uid = str(eq.call("loadout_uid", _target_slot))
	elif gs and "weapon_loadout" in gs and _target_slot < gs.weapon_loadout.size():
		cur_uid = str(gs.weapon_loadout[_target_slot])

	if cur_uid.is_empty():
		_slot_summary_lbl.text = "【%s】%s" % [slot_title, _t("當前槽位尚未裝備武器")]
		_btn_unequip.visible = false
	else:
		var inst: Dictionary = {}
		if eq and eq.has_method("weapon_inst"):
			inst = eq.call("weapon_inst", cur_uid)
		if inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
			inst = gs.equip_worn.get(cur_uid, {})
		var wname := _t(str(inst.get("name", "武器")))
		var line := str(inst.get("line", "sword"))
		var hits := _t(LINE_HITS.get(line, "4 次打擊"))
		var q_label := _t(str(inst.get("quality_label", "凡品")))
		var atk := get_weapon_atk(inst)
		_slot_summary_lbl.text = "【%s】%s · %s · %s (攻擊 +%d)" % [slot_title, wname, q_label, hits, atk]
		_btn_unequip.visible = (_target_slot > 0)


func _rebuild_weapon_list() -> void:
	for c in _weapons_box.get_children():
		if c != _empty_panel:
			_weapons_box.remove_child(c)
			c.queue_free()

	var candidates := _collect_candidate_weapons()
	if candidates.is_empty():
		_empty_panel.visible = true
		if _empty_title_lbl != null and _empty_sub_lbl != null:
			if current_filter_line != "all" and not current_filter_line.is_empty():
				_empty_title_lbl.text = _t("尚無該流派可替換武器")
				_empty_sub_lbl.text = _t("可嘗試切換其他流派或前往鍛造殿堂打造")
			else:
				_empty_title_lbl.text = _t("背包與庫存尚無可替換武器")
				_empty_sub_lbl.text = _t("可前往冒險出征獲取或在鍛造殿堂打造新武器")
		return

	_empty_panel.visible = false
	for winst in candidates:
		var row := _build_weapon_card(winst)
		_weapons_box.add_child(row)


func _collect_candidate_weapons() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var seen_uids: Dictionary = {}
	var eq := _get_equip_sys()
	var gs := _gs()

	# 1. 當前目標欄位武器 (置頂)
	var target_uid := ""
	if eq and eq.has_method("loadout_uid"):
		target_uid = str(eq.call("loadout_uid", _target_slot))
	elif gs and "weapon_loadout" in gs and _target_slot < gs.weapon_loadout.size():
		target_uid = str(gs.weapon_loadout[_target_slot])

	if not target_uid.is_empty():
		var t_inst: Dictionary = {}
		if eq and eq.has_method("weapon_inst"):
			t_inst = eq.call("weapon_inst", target_uid)
		if t_inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
			t_inst = gs.equip_worn.get(target_uid, {})
		if not t_inst.is_empty():
			var entry := t_inst.duplicate(true)
			entry["_status"] = "current_slot"
			result.append(entry)
			seen_uids[target_uid] = true

	# 2. 其他兩個欄位中已裝備的武器 (可支援跨欄調換)
	for i in range(3):
		if i == _target_slot:
			continue
		var s_uid := ""
		if eq and eq.has_method("loadout_uid"):
			s_uid = str(eq.call("loadout_uid", i))
		elif gs and "weapon_loadout" in gs and i < gs.weapon_loadout.size():
			s_uid = str(gs.weapon_loadout[i])
		if s_uid.is_empty() or seen_uids.has(s_uid):
			continue
		var s_inst: Dictionary = {}
		if eq and eq.has_method("weapon_inst"):
			s_inst = eq.call("weapon_inst", s_uid)
		if s_inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
			s_inst = gs.equip_worn.get(s_uid, {})
		if not s_inst.is_empty():
			var entry := s_inst.duplicate(true)
			entry["_status"] = "other_slot"
			entry["_other_slot_idx"] = i
			result.append(entry)
			seen_uids[s_uid] = true

	# 3. 背包中的武器 (equip_bag)
	var bag_weapons: Array[Dictionary] = []
	if gs and "equip_bag" in gs and gs.equip_bag is Array:
		for item in gs.equip_bag:
			if not (item is Dictionary):
				continue
			var uid: String = str(item.get("uid", ""))
			if uid.is_empty() or seen_uids.has(uid):
				continue
			var is_weapon := false
			if eq and eq.has_method("normalize_slot"):
				is_weapon = (eq.call("normalize_slot", str(item.get("slot", "weapon"))) == "weapon")
			else:
				var slot_str := str(item.get("slot", "")).to_lower()
				is_weapon = (slot_str == "weapon" or slot_str == "" or item.has("line") or item.has("weapon_atk"))
			if is_weapon:
				var entry: Dictionary = (item as Dictionary).duplicate(true)
				entry["_status"] = "bag"
				bag_weapons.append(entry)
				seen_uids[uid] = true

	# 背包武器依攻擊力 (atk) 降序排序
	bag_weapons.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var atkA := get_weapon_atk(a)
		var atkB := get_weapon_atk(b)
		if atkA != atkB:
			return atkA > atkB
		return str(a.get("uid", "")) < str(b.get("uid", ""))
	)
	result.append_array(bag_weapons)

	# 4. 依照目前流派篩選過濾候選武器
	if current_filter_line != "all" and not current_filter_line.is_empty():
		var filtered: Array[Dictionary] = []
		for w in result:
			var w_line := str(w.get("line", ""))
			if w_line.is_empty() and w.has("base_id"):
				w_line = str(w.get("base_id", ""))
			if matches_line_filter(w_line, current_filter_line):
				filtered.append(w)
		return filtered

	return result


func get_candidate_weapons() -> Array[Dictionary]:
	return _collect_candidate_weapons()


func _build_filter_chips() -> void:
	if _chips_box == null:
		return
	_filter_chip_buttons.clear()
	for child in _chips_box.get_children():
		_chips_box.remove_child(child)
		child.queue_free()

	for info in FILTER_CHIPS:
		var chip_id: String = str(info["id"])
		var btn := Button.new()
		btn.name = "Chip_" + chip_id
		btn.custom_minimum_size = Vector2(58, 48)
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn.pressed.connect(func(): set_line_filter(chip_id))
		_chips_box.add_child(btn)
		_filter_chip_buttons[chip_id] = btn

	_refresh_filter_chips()


func _refresh_filter_chips() -> void:
	for chip_id in _filter_chip_buttons.keys():
		var btn: Button = _filter_chip_buttons[chip_id]
		var info := _get_chip_info(chip_id)
		btn.text = _get_chip_localized_name(info)
	_update_filter_chips_visual()


func _get_chip_info(chip_id: String) -> Dictionary:
	for info in FILTER_CHIPS:
		if info.get("id", "") == chip_id:
			return info
	return {"id": chip_id, "key": chip_id, "line": chip_id}


func _get_chip_localized_name(info: Dictionary) -> String:
	var key: String = str(info.get("key", ""))
	var lc := ContentLoc.locale()
	if lc == "zh_TW":
		return key
	var trans := _t(key)
	if trans != key and not trans.is_empty():
		return trans
	if FILTER_CHIP_I18N.has(key) and FILTER_CHIP_I18N[key].has(lc):
		return str(FILTER_CHIP_I18N[key][lc])
	return key


func _update_filter_chips_visual() -> void:
	for chip_id in _filter_chip_buttons.keys():
		var btn: Button = _filter_chip_buttons[chip_id]
		var is_selected: bool = (chip_id == current_filter_line)
		if is_selected:
			_style_jelly_btn(btn, COLOR_ORANGE, COLOR_TEXT_DARK, 13, 5, 14)
		else:
			_style_jelly_btn(btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 13, 4, 14)


func set_line_filter(line_id: String) -> void:
	var target_chip := "all"
	for info in FILTER_CHIPS:
		if info.get("id", "") == line_id or info.get("key", "") == line_id or info.get("line", "") == line_id:
			target_chip = str(info["id"])
			break
	if line_id == "all" or line_id == "全部":
		target_chip = "all"

	current_filter_line = target_chip
	_update_filter_chips_visual()
	_rebuild_weapon_list()
	if _filter_chip_buttons.has(target_chip):
		_scroll_to_chip(_filter_chip_buttons[target_chip])
	line_filter_changed.emit(current_filter_line)


func get_current_filter_line() -> String:
	return current_filter_line


func get_filter_chips() -> Dictionary:
	return _filter_chip_buttons


func get_filter_chip(key_or_id: String) -> Button:
	if _filter_chip_buttons.has(key_or_id):
		return _filter_chip_buttons[key_or_id]
	for info in FILTER_CHIPS:
		if info.get("key", "") == key_or_id or info.get("id", "") == key_or_id or info.get("line", "") == key_or_id:
			var cid: String = str(info["id"])
			if _filter_chip_buttons.has(cid):
				return _filter_chip_buttons[cid]
	return null


func _scroll_to_chip(btn: Button) -> void:
	if _chip_scroll == null or btn == null:
		return
	var btn_left: float = btn.position.x
	var btn_right: float = btn_left + btn.size.x
	var scroll_left: float = float(_chip_scroll.scroll_horizontal)
	var scroll_right: float = scroll_left + _chip_scroll.size.x
	if btn_left < scroll_left:
		_chip_scroll.scroll_horizontal = int(btn_left)
	elif btn_right > scroll_right and _chip_scroll.size.x > 0:
		_chip_scroll.scroll_horizontal = int(btn_right - _chip_scroll.size.x)


func get_target_slot_weapon_info() -> Dictionary:
	var eq := _get_equip_sys()
	var gs := _gs()
	var target_uid := ""
	if eq and eq.has_method("loadout_uid"):
		target_uid = str(eq.call("loadout_uid", _target_slot))
	elif gs and "weapon_loadout" in gs and _target_slot < gs.weapon_loadout.size():
		target_uid = str(gs.weapon_loadout[_target_slot])

	if target_uid.is_empty():
		return {"has_weapon": false, "atk": 0, "uid": ""}

	var t_inst: Dictionary = {}
	if eq and eq.has_method("weapon_inst"):
		t_inst = eq.call("weapon_inst", target_uid)
	if t_inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
		t_inst = gs.equip_worn.get(target_uid, {})

	if t_inst.is_empty():
		return {"has_weapon": false, "atk": 0, "uid": target_uid}

	return {
		"has_weapon": true,
		"atk": get_weapon_atk(t_inst),
		"uid": target_uid,
		"inst": t_inst
	}


func _build_weapon_card(winst: Dictionary) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "WeaponCard_" + str(winst.get("uid", ""))
	card.custom_minimum_size = Vector2(0, 68)
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var status: String = str(winst.get("_status", "bag"))
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 4
	sb.set_corner_radius_all(16)
	sb.content_margin_left = 14
	sb.content_margin_right = 14
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	card.add_theme_stylebox_override("panel", sb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 12)
	card.add_child(h)

	# 左側：品質與流派膠囊
	var quality: String = str(winst.get("quality", "common"))
	var q_col := _get_quality_color(quality)
	var q_label := _t(str(winst.get("quality_label", "凡品")))
	var line: String = str(winst.get("line", "sword"))
	var line_name := _t(LINE_NAMES.get(line, "武器"))

	var badge_p := PanelContainer.new()
	badge_p.custom_minimum_size = Vector2(80, 48)
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = COLOR_CARD_GOLD
	bsb.border_color = COLOR_BORDER
	bsb.set_border_width_all(1)
	bsb.border_width_bottom = 3
	bsb.set_corner_radius_all(10)
	bsb.content_margin_left = 6
	bsb.content_margin_right = 6
	bsb.content_margin_top = 4
	bsb.content_margin_bottom = 4
	badge_p.add_theme_stylebox_override("panel", bsb)
	h.add_child(badge_p)

	var bv := VBoxContainer.new()
	bv.alignment = BoxContainer.ALIGNMENT_CENTER
	badge_p.add_child(bv)

	var q_lbl := Label.new()
	q_lbl.text = q_label
	q_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(q_lbl, 11, q_col, true)
	bv.add_child(q_lbl)

	var l_lbl := Label.new()
	l_lbl.text = line_name
	l_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(l_lbl, 12, COLOR_TEXT_DARK)
	bv.add_child(l_lbl)

	# 中間：名稱、打擊段數、屬性值
	var info_v := VBoxContainer.new()
	info_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info_v.alignment = BoxContainer.ALIGNMENT_CENTER
	info_v.add_theme_constant_override("separation", 2)
	h.add_child(info_v)

	var name_row := HBoxContainer.new()
	name_row.add_theme_constant_override("separation", 8)
	info_v.add_child(name_row)

	var name_lbl := Label.new()
	name_lbl.text = _t(str(winst.get("name", "神兵")))
	_apply_font(name_lbl, 15, COLOR_TEXT_DARK, true)
	name_row.add_child(name_lbl)

	if status == "current_slot":
		var cur_tag := Label.new()
		cur_tag.text = "【%s】" % _t("當前槽位裝備中")
		_apply_font(cur_tag, 12, COLOR_TEXT_ORANGE)
		name_row.add_child(cur_tag)
	elif status == "other_slot":
		var other_idx: int = int(winst.get("_other_slot_idx", 0))
		var other_tag := Label.new()
		other_tag.text = "【%s %s】" % [_t(SLOT_TITLES[other_idx]), _t("使用中")]
		_apply_font(other_tag, 12, COLOR_TEXT_MUTED)
		name_row.add_child(other_tag)

	var stat_lbl := Label.new()
	var hits_str := _t(LINE_HITS.get(line, "4 次打擊"))
	var atk := get_weapon_atk(winst)

	var stat_desc := "%s · %s +%d" % [hits_str, _t("攻擊"), atk]
	if winst.has("rolled") and winst["rolled"] is Dictionary:
		var crit: float = float(winst["rolled"].get("crit", 0.0))
		if crit > 0:
			stat_desc += " · %s +%.1f%%" % [_t("暴擊"), crit]
	stat_lbl.text = stat_desc
	_apply_font(stat_lbl, 12, COLOR_TEXT_MUTED)
	info_v.add_child(stat_lbl)

	# 差額對比膠囊
	var t_info := get_target_slot_weapon_info()
	var has_target_w: bool = bool(t_info.get("has_weapon", false))
	var target_atk: int = int(t_info.get("atk", 0))

	var diff_text := "--"
	var diff_bg: Color = COLOR_DIFF_EQ_BG
	var diff_bd: Color = COLOR_DIFF_EQ_BD
	var diff_col: Color = COLOR_DIFF_EQ_TEXT

	if has_target_w:
		var diff := atk - target_atk
		if diff > 0:
			diff_text = "+%d %s" % [diff, _t("攻擊")]
			diff_bg = COLOR_DIFF_POS_BG
			diff_bd = COLOR_DIFF_POS_BD
			diff_col = COLOR_DIFF_POS_TEXT
		elif diff < 0:
			diff_text = "-%d %s" % [absi(diff), _t("攻擊")]
			diff_bg = COLOR_DIFF_NEG_BG
			diff_bd = COLOR_DIFF_NEG_BD
			diff_col = COLOR_DIFF_NEG_TEXT
		else:
			diff_text = "--"
			diff_bg = COLOR_DIFF_EQ_BG
			diff_bd = COLOR_DIFF_EQ_BD
			diff_col = COLOR_DIFF_EQ_TEXT
	else:
		diff_text = "--"
		diff_bg = COLOR_DIFF_EQ_BG
		diff_bd = COLOR_DIFF_EQ_BD
		diff_col = COLOR_DIFF_EQ_TEXT

	var diff_p := PanelContainer.new()
	diff_p.name = "DiffCapsule"
	diff_p.custom_minimum_size = Vector2(86, 32)
	diff_p.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = diff_bg
	dsb.border_color = diff_bd
	dsb.set_border_width_all(1)
	dsb.border_width_bottom = 3
	dsb.set_corner_radius_all(12)
	dsb.content_margin_left = 6
	dsb.content_margin_right = 6
	dsb.content_margin_top = 4
	dsb.content_margin_bottom = 4
	diff_p.add_theme_stylebox_override("panel", dsb)

	var diff_lbl := Label.new()
	diff_lbl.name = "DiffLabel"
	diff_lbl.text = diff_text
	diff_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	diff_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_font(diff_lbl, 12, diff_col, true)
	diff_p.add_child(diff_lbl)

	h.add_child(diff_p)

	# 右側：操作按鈕
	var act_btn := Button.new()
	act_btn.name = "BtnAction"
	act_btn.custom_minimum_size = Vector2(100, 48)

	var target_uid: String = str(winst.get("uid", ""))
	if status == "current_slot":
		act_btn.text = _t("使用中")
		act_btn.disabled = true
		_style_jelly_btn(act_btn, COLOR_CARD_MUTED, COLOR_TEXT_DIM, 13, 2, 14, COLOR_BORDER_MUTED)
	elif status == "other_slot":
		act_btn.text = _t("調換至此欄")
		_style_jelly_btn(act_btn, COLOR_SKY, COLOR_TEXT_DARK, 13, 5, 14)
		act_btn.pressed.connect(func(): _equip_weapon(target_uid))
	else:
		act_btn.text = _t("更換裝備")
		_style_jelly_btn(act_btn, COLOR_ORANGE, COLOR_TEXT_DARK, 14, 5, 14)
		act_btn.pressed.connect(func(): _equip_weapon(target_uid))

	h.add_child(act_btn)
	return card


func _equip_weapon(uid: String) -> void:
	var eq := _get_equip_sys()
	if eq and eq.has_method("equip_weapon_to_loadout"):
		var res: Dictionary = eq.equip_weapon_to_loadout(uid, _target_slot)
		var msg := str(res.get("msg", ""))
		if not msg.is_empty():
			_toast(msg)
	weapon_swapped.emit(_target_slot, uid)
	queue_free()


func _on_unequip_pressed() -> void:
	if _target_slot == 0:
		_toast(_t("首選武器不可卸下。"))
		return
	var eq := _get_equip_sys()
	if eq and eq.has_method("unequip_loadout_slot"):
		var res: Dictionary = eq.unequip_loadout_slot(_target_slot)
		var msg := str(res.get("msg", ""))
		if not msg.is_empty():
			_toast(msg)
	slot_unequipped.emit(_target_slot)
	queue_free()


func _on_close_pressed() -> void:
	closed.emit()
	queue_free()


func _toast(msg: String) -> void:
	var p := get_parent()
	if p and p.has_method("_show_toast"):
		p.call("_show_toast", msg)


func _get_quality_color(q: String) -> Color:
	match q:
		"common": return Color("#8E8A9F")
		"uncommon": return Color("#2E9E4A")
		"rare": return Color("#2575FC")
		"epic": return Color("#9B51E0")
		_: return Color("#8E8A9F")


func _style_jelly_btn(btn: Button, bg: Color, text_col: Color, font_sz: int, bottom_px: int = 5, radius: int = 16, border_col: Color = COLOR_BORDER) -> void:
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


func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


func _get_equip_sys() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	return null
