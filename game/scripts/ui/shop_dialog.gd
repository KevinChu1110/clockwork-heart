class_name ShopDialog
extends Control
## 《發條之心》商城/儲值頁面骨架 (ShopDialog)
## 依據 docs/BUSINESS.md 變現架構與 review.md 手遊 UI 規範：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，所有互動按鈕高度均 >= 50px（觸控熱區 >= 48px）。
## 3. 多巴胺鮮亮高飽和色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 採用開源粉圓體 (jf-openhuninn-2.1.ttf)，字級 >= 16px，無零碎小字。
## 6. 100% 零系統 Emoji、零特殊符號作為圖示。
## 7. 內購品項為佔位資料（docs/BUSINESS.md 明寫『定價帶：待定』），以 TODO 註記等 Kevin 定案。
## 8. 串接 MockAdDialog 獎勵型廣告與 GameState.has_removed_ads 去廣告開關，全走 mock 邏輯。

signal closed()

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const MockAdDialogScript := preload("res://scripts/ui/mock_ad_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

static func tr_ui(s: String) -> String:
	return _t(s)

## ── 多巴胺鮮亮色盤 ──
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM   := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃卡片底
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MINT   := Color("#1A7A30")  ## 壓明度薄荷綠
const COLOR_TEXT_MUTED  := Color("#6E6885")  ## 輔助深藍灰

var _dialog_card: PanelContainer
var _title_lbl: Label
var _mode_pill_lbl: Label
var _notice_lbl: Label
var _remove_ads_title_lbl: Label
var _remove_ads_desc_lbl: Label
var _remove_ads_btn: Button
var _remove_ads_status_lbl: Label
var _reward_ad_title_lbl: Label
var _reward_ad_desc_lbl: Label
var _reward_ad_note_lbl: Label
var _reward_ad_btn: Button
var _items_title_lbl: Label
var _item_name_labels: Dictionary = {}
var _item_desc_labels: Dictionary = {}
var _item_buy_buttons: Dictionary = {}
var _item_note_labels: Dictionary = {}
var _status_msg_lbl: Label
var _cached_font: Font = null

## IAP 佔位品項定義（TODO: 內購定價帶尚未定案，依據 docs/BUSINESS.md 待 Kevin 裁定）
var _iap_items: Array[Dictionary] = [
	{
		"id": "energy_pack",
		"title": "發條能量補給箱",
		"desc": "冒險能量立即補充 +15 點\n突破每日體力上限",
		"price_label": "NT$ 30",  # TODO: 定價待定，目前為佔位定價
		"pricing_note": "TODO: 定價待定",
		"icon": "res://assets/icons/hud/icon_energy_key.png",
		"accent": COLOR_ORANGE,
		"grant_func": "_grant_energy"
	},
	{
		"id": "soul_pack",
		"title": "神殿聚魂召喚包",
		"desc": "聚魂殿戰魂抽取專用道具\n獲得召喚石 ×10",
		"price_label": "NT$ 90",  # TODO: 定價待定，目前為佔位定價
		"pricing_note": "TODO: 定價待定",
		"icon": "res://assets/icons/hud/icon_dock_soul.png",
		"accent": COLOR_PINK,
		"grant_func": "_grant_soul_stones"
	},
	{
		"id": "forge_pack",
		"title": "工坊鍛造資源箱",
		"desc": "裝備器階鍛造與精煉素材\n獲得金幣 500 與鍛造精粹",
		"price_label": "NT$ 150",  # TODO: 定價待定，目前為佔位定價
		"pricing_note": "TODO: 定價待定",
		"icon": "res://assets/icons/hud/icon_hall_forge.png",
		"accent": COLOR_GOLD,
		"grant_func": "_grant_forge_mats"
	}
]


static func show_shop(parent: Node) -> Control:
	var dlg: Control = load("res://scripts/ui/shop_dialog.gd").new()
	dlg.z_index = 85
	parent.add_child(dlg)
	return dlg


func _ready() -> void:
	name = "ShopDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 85

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_connect_loc_signal()
	_build_ui()
	_apply_locale_texts()
	_refresh_services_state()


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
	_apply_locale_texts()
	_refresh_services_state()


func _apply_locale_texts() -> void:
	if _title_lbl and is_instance_valid(_title_lbl):
		_title_lbl.text = _t("發條補給 · 道具商城")
	if _mode_pill_lbl and is_instance_valid(_mode_pill_lbl):
		_mode_pill_lbl.text = _t("商業化測試骨架")
	if _notice_lbl and is_instance_valid(_notice_lbl):
		_notice_lbl.text = _t("商業變現模型：定價帶待定（docs/BUSINESS.md 定案）。全品項為測試佔位 Mock 邏輯，點擊不扣款。")
	if _remove_ads_title_lbl and is_instance_valid(_remove_ads_title_lbl):
		_remove_ads_title_lbl.text = _t("免廣告特權")
	if _remove_ads_desc_lbl and is_instance_valid(_remove_ads_desc_lbl):
		_remove_ads_desc_lbl.text = _t("買斷免除全廣告播映，直接領取所有獎勵")
	if _reward_ad_title_lbl and is_instance_valid(_reward_ad_title_lbl):
		_reward_ad_title_lbl.text = _t("工坊贊助補給")
	if _reward_ad_desc_lbl and is_instance_valid(_reward_ad_desc_lbl):
		_reward_ad_desc_lbl.text = _t("觀看工坊廣告短片，立即補充 3 點能量")
	if _reward_ad_note_lbl and is_instance_valid(_reward_ad_note_lbl):
		_reward_ad_note_lbl.text = _t("每日免費補給 · 無需消耗金幣")
	if _items_title_lbl and is_instance_valid(_items_title_lbl):
		_items_title_lbl.text = _t("熱門儲值品項（佔位預覽）")

	for item in _iap_items:
		var item_id: String = str(item["id"])
		if _item_name_labels.has(item_id):
			var nl: Label = _item_name_labels[item_id]
			if nl and is_instance_valid(nl):
				nl.text = _t(str(item["title"]))
		if _item_desc_labels.has(item_id):
			var dl: Label = _item_desc_labels[item_id]
			if dl and is_instance_valid(dl):
				dl.text = _t(str(item["desc"]))
		if _item_buy_buttons.has(item_id):
			var bb: Button = _item_buy_buttons[item_id]
			if bb and is_instance_valid(bb):
				bb.text = _t("模擬購買")
		if _item_note_labels.has(item_id):
			var ntl: Label = _item_note_labels[item_id]
			if ntl and is_instance_valid(ntl):
				ntl.text = "(%s)" % _t(str(item["pricing_note"]))

	if _status_msg_lbl and is_instance_valid(_status_msg_lbl):
		_status_msg_lbl.text = _t("歡迎來到發條工坊商城！請點擊各項功能進行模擬測試。")


func _build_ui() -> void:
	# 1. 全螢幕半透明遮罩 (Scrim)
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

	# 2. 置中卡片 (寬 750px，符合橫屏 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "ShopCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 520)
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 22)
	margin.add_theme_constant_override("margin_right", 22)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 10)
	margin.add_child(v)

	# ── 頂部標題列 ──
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(head)

	_title_lbl = Label.new()
	_title_lbl.name = "ShopTitleLabel"
	_title_lbl.text = _t("發條補給 · 道具商城")
	_title_lbl.add_theme_font_size_override("font_size", 22)
	_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_title_lbl.add_theme_font_override("font", _cached_font)
	_title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(_title_lbl)

	# 骨架標籤
	var mode_pill := _create_info_pill(_t("商業化測試骨架"), COLOR_MINT)
	_mode_pill_lbl = mode_pill.get_child(0) as Label
	head.add_child(mode_pill)

	# 右上「✕」關閉按鈕 (50x50, 果凍厚底 5px)
	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# ── 商業模式定價備註欄 ──
	var notice_box := PanelContainer.new()
	notice_box.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 3, 14))
	notice_box.custom_minimum_size = Vector2(0, 38)
	v.add_child(notice_box)

	var nm := MarginContainer.new()
	nm.add_theme_constant_override("margin_left", 12)
	nm.add_theme_constant_override("margin_right", 12)
	nm.add_theme_constant_override("margin_top", 4)
	nm.add_theme_constant_override("margin_bottom", 4)
	notice_box.add_child(nm)

	_notice_lbl = Label.new()
	_notice_lbl.text = _t("商業變現模型：定價帶待定（docs/BUSINESS.md 定案）。全品項為測試佔位 Mock 邏輯，點擊不扣款。")
	_notice_lbl.add_theme_font_size_override("font_size", 14)
	_notice_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_notice_lbl.add_theme_font_override("font", _cached_font)
	nm.add_child(_notice_lbl)

	# ── 特殊增值服務列（去廣告買斷 ＋ 觀看廣告領取獎勵）──
	var services_h := HBoxContainer.new()
	services_h.add_theme_constant_override("separation", 12)
	v.add_child(services_h)

	# 服務 1：一次性去廣告服務卡
	var remove_ads_card := _build_service_card(
		_t("免廣告特權"),
		_t("買斷免除全廣告播映，直接領取所有獎勵"),
		"RemoveAdsCard"
	)
	_remove_ads_title_lbl = remove_ads_card.get_node("Margin/VBox").get_child(0) as Label
	_remove_ads_desc_lbl = remove_ads_card.get_node("Margin/VBox").get_child(1) as Label
	remove_ads_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	services_h.add_child(remove_ads_card)

	var ra_v: VBoxContainer = remove_ads_card.get_node("Margin/VBox")
	_remove_ads_status_lbl = Label.new()
	_remove_ads_status_lbl.text = _t("狀態：未購買（NT$ 60 TODO: 定價待定）")
	_remove_ads_status_lbl.add_theme_font_size_override("font_size", 13)
	_remove_ads_status_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_remove_ads_status_lbl.add_theme_font_override("font", _cached_font)
	ra_v.add_child(_remove_ads_status_lbl)

	_remove_ads_btn = Button.new()
	_remove_ads_btn.name = "RemoveAdsBtn"
	_remove_ads_btn.text = _t("一次性去廣告（Mock買斷）")
	_remove_ads_btn.custom_minimum_size = Vector2(0, 50)
	_remove_ads_btn.add_theme_font_size_override("font_size", 16)
	_remove_ads_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	_remove_ads_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_remove_ads_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_remove_ads_btn.add_theme_font_override("font", _cached_font)
	_remove_ads_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 16))
	_remove_ads_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB030"), COLOR_BORDER, 5, 16))
	_remove_ads_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#E08000"), COLOR_BORDER, 2, 16))
	_remove_ads_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#7EAE8B"), COLOR_BORDER, 3, 16))
	_remove_ads_btn.pressed.connect(_on_remove_ads_clicked)
	ra_v.add_child(_remove_ads_btn)

	# 服務 2：獎勵型廣告補給卡
	var reward_ad_card := _build_service_card(
		_t("工坊贊助補給"),
		_t("觀看工坊廣告短片，立即補充 3 點能量"),
		"RewardAdCard"
	)
	_reward_ad_title_lbl = reward_ad_card.get_node("Margin/VBox").get_child(0) as Label
	_reward_ad_desc_lbl = reward_ad_card.get_node("Margin/VBox").get_child(1) as Label
	reward_ad_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	services_h.add_child(reward_ad_card)

	var rad_v: VBoxContainer = reward_ad_card.get_node("Margin/VBox")
	_reward_ad_note_lbl = Label.new()
	_reward_ad_note_lbl.text = _t("每日免費補給 · 無需消耗金幣")
	_reward_ad_note_lbl.add_theme_font_size_override("font_size", 13)
	_reward_ad_note_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_reward_ad_note_lbl.add_theme_font_override("font", _cached_font)
	rad_v.add_child(_reward_ad_note_lbl)

	_reward_ad_btn = Button.new()
	_reward_ad_btn.name = "WatchAdBtn"
	_reward_ad_btn.text = _t("觀看廣告領取 (+3能量)")
	_reward_ad_btn.custom_minimum_size = Vector2(0, 50)
	_reward_ad_btn.add_theme_font_size_override("font_size", 16)
	_reward_ad_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	_reward_ad_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_reward_ad_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_reward_ad_btn.add_theme_font_override("font", _cached_font)
	_reward_ad_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 16))
	_reward_ad_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5CE879"), COLOR_BORDER, 5, 16))
	_reward_ad_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3DBB55"), COLOR_BORDER, 2, 16))
	_reward_ad_btn.pressed.connect(_on_watch_ad_clicked)
	rad_v.add_child(_reward_ad_btn)

	# ── 3 個佔位品項卡 (IAP 禮包區) ──
	_items_title_lbl = Label.new()
	_items_title_lbl.text = _t("熱門儲值品項（佔位預覽）")
	_items_title_lbl.add_theme_font_size_override("font_size", 17)
	_items_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_items_title_lbl.add_theme_font_override("font", _cached_font)
	v.add_child(_items_title_lbl)

	var items_grid := HBoxContainer.new()
	items_grid.add_theme_constant_override("separation", 10)
	v.add_child(items_grid)

	for item in _iap_items:
		var item_card := _build_iap_item_card(item)
		item_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		items_grid.add_child(item_card)

	# ── 底部即時回饋提示列 ──
	_status_msg_lbl = Label.new()
	_status_msg_lbl.name = "StatusMessageLabel"
	_status_msg_lbl.text = _t("歡迎來到發條工坊商城！請點擊各項功能進行模擬測試。")
	_status_msg_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_status_msg_lbl.add_theme_font_size_override("font_size", 14)
	_status_msg_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	if _cached_font:
		_status_msg_lbl.add_theme_font_override("font", _cached_font)
	v.add_child(_status_msg_lbl)


func _build_service_card(title: String, desc: String, card_name: String) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = card_name
	card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 16))

	var m := MarginContainer.new()
	m.name = "Margin"
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var cv := VBoxContainer.new()
	cv.name = "VBox"
	cv.add_theme_constant_override("separation", 6)
	m.add_child(cv)

	var t_lbl := Label.new()
	t_lbl.text = title
	t_lbl.add_theme_font_size_override("font_size", 17)
	t_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		t_lbl.add_theme_font_override("font", _cached_font)
	cv.add_child(t_lbl)

	var d_lbl := Label.new()
	d_lbl.text = desc
	d_lbl.add_theme_font_size_override("font_size", 13)
	d_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		d_lbl.add_theme_font_override("font", _cached_font)
	cv.add_child(d_lbl)

	return card


func _build_iap_item_card(item: Dictionary) -> PanelContainer:
	var item_id := str(item["id"])
	var card := PanelContainer.new()
	card.name = "IapCard_" + item_id
	card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 16))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 12)
	m.add_theme_constant_override("margin_right", 12)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var iv := VBoxContainer.new()
	iv.add_theme_constant_override("separation", 6)
	m.add_child(iv)

	# 圖示與標題列
	var head_h := HBoxContainer.new()
	head_h.add_theme_constant_override("separation", 6)
	head_h.alignment = BoxContainer.ALIGNMENT_CENTER
	iv.add_child(head_h)

	var icon_path := str(item.get("icon", ""))
	if ResourceLoader.exists(icon_path):
		var icon_rect := TextureRect.new()
		icon_rect.texture = load(icon_path)
		icon_rect.custom_minimum_size = Vector2(28, 28)
		icon_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		head_h.add_child(icon_rect)

	var name_lbl := Label.new()
	name_lbl.name = "ItemTitleLabel_" + item_id
	name_lbl.text = _t(str(item["title"]))
	name_lbl.add_theme_font_size_override("font_size", 16)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	head_h.add_child(name_lbl)
	_item_name_labels[item_id] = name_lbl

	# 內容描述
	var desc_lbl := Label.new()
	desc_lbl.name = "ItemDescLabel_" + item_id
	desc_lbl.text = _t(str(item["desc"]))
	desc_lbl.custom_minimum_size = Vector2(0, 36)
	desc_lbl.add_theme_font_size_override("font_size", 12)
	desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		desc_lbl.add_theme_font_override("font", _cached_font)
	iv.add_child(desc_lbl)
	_item_desc_labels[item_id] = desc_lbl

	# 定價與 TODO 備註
	var price_h := HBoxContainer.new()
	price_h.alignment = BoxContainer.ALIGNMENT_CENTER
	price_h.add_theme_constant_override("separation", 4)
	iv.add_child(price_h)

	var price_lbl := Label.new()
	price_lbl.text = _t(str(item["price_label"]))
	price_lbl.add_theme_font_size_override("font_size", 18)
	price_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	if _cached_font:
		price_lbl.add_theme_font_override("font", _cached_font)
	price_h.add_child(price_lbl)

	var note_lbl := Label.new()
	note_lbl.name = "ItemNoteLabel_" + item_id
	note_lbl.text = "(%s)" % _t(str(item["pricing_note"]))
	note_lbl.add_theme_font_size_override("font_size", 11)
	note_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		note_lbl.add_theme_font_override("font", _cached_font)
	price_h.add_child(note_lbl)
	_item_note_labels[item_id] = note_lbl

	# 購買按鈕 (熱區 >= 50px，果凍厚底 5px)
	var buy_btn := Button.new()
	buy_btn.name = "BuyBtn_" + item_id
	buy_btn.text = _t("模擬購買")
	buy_btn.custom_minimum_size = Vector2(0, 50)
	buy_btn.add_theme_font_size_override("font_size", 16)
	buy_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	buy_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	buy_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		buy_btn.add_theme_font_override("font", _cached_font)

	var accent: Color = item.get("accent", COLOR_GOLD)
	buy_btn.add_theme_stylebox_override("normal", _create_button_style(accent, COLOR_BORDER, 5, 16))
	buy_btn.add_theme_stylebox_override("hover", _create_button_style(accent.lightened(0.15), COLOR_BORDER, 5, 16))
	buy_btn.add_theme_stylebox_override("pressed", _create_button_style(accent.darkened(0.15), COLOR_BORDER, 2, 16))

	buy_btn.pressed.connect(func(): _on_iap_item_clicked(item_id))
	iv.add_child(buy_btn)
	_item_buy_buttons[item_id] = buy_btn

	return card


func _create_info_pill(text: String, accent: Color) -> PanelContainer:
	var pill := PanelContainer.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = COLOR_CARD_WARM
	psb.border_color = accent
	psb.set_border_width_all(2)
	psb.border_width_bottom = 3
	psb.set_corner_radius_all(12)
	psb.content_margin_left = 10
	psb.content_margin_right = 10
	psb.content_margin_top = 4
	psb.content_margin_bottom = 4
	pill.add_theme_stylebox_override("panel", psb)

	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 13)
	l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		l.add_theme_font_override("font", _cached_font)
	pill.add_child(l)
	return pill


func _refresh_services_state() -> void:
	var gs := _gs()
	var has_removed := false
	if gs != null:
		if "has_removed_ads" in gs:
			has_removed = bool(gs.has_removed_ads)
		elif gs.has_method("get_flag"):
			has_removed = bool(gs.get_flag("has_removed_ads", false))

	if _remove_ads_btn:
		if has_removed:
			_remove_ads_btn.text = _t("已擁有去廣告特權")
			_remove_ads_btn.disabled = true
			if _remove_ads_status_lbl:
				_remove_ads_status_lbl.text = _t("狀態：已啟用買斷特權（永久免廣告）")
				_remove_ads_status_lbl.add_theme_color_override("font_color", COLOR_TEXT_MINT)
		else:
			_remove_ads_btn.text = _t("一次性去廣告（Mock買斷）")
			_remove_ads_btn.disabled = false
			if _remove_ads_status_lbl:
				_remove_ads_status_lbl.text = _t("狀態：未購買（NT$ 60 TODO: 定價待定）")
				_remove_ads_status_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)

	if _reward_ad_btn:
		if has_removed:
			_reward_ad_btn.text = _t("免看廣告直接領取 (+3能量)")
		else:
			_reward_ad_btn.text = _t("觀看廣告領取 (+3能量)")


func _on_remove_ads_clicked() -> void:
	var gs := _gs()
	if gs == null:
		return

	if "has_removed_ads" in gs:
		gs.has_removed_ads = true
	elif gs.has_method("set_flag"):
		gs.set_flag("has_removed_ads", true)

	_refresh_services_state()
	_set_status(_t("【模擬買斷成功】已啟用一次性去廣告服務！所有廣告節點已免除。"))


func _on_watch_ad_clicked() -> void:
	var gs := _gs()
	var has_removed := false
	if gs != null:
		if "has_removed_ads" in gs:
			has_removed = bool(gs.has_removed_ads)
		elif gs.has_method("get_flag"):
			has_removed = bool(gs.get_flag("has_removed_ads", false))

	if has_removed:
		# 已去廣告：直接跳過播放領取獎勵
		_grant_ad_energy()
		_set_status(_t("【免廣告特權生效】已跳過廣告播映，直接領取 3 點發條能量！"))
		return

	# 未去廣告：開啟 MockAdDialog 假播映彈窗
	MockAdDialogScript.show_ad(
		self,
		"energy",
		func():
			_grant_ad_energy()
			_set_status(_t("【觀看廣告成功】發條補給完成！已領取 3 點發條能量。")),
		func():
			_set_status(_t("廣告播放已中斷，未領取獎勵。"))
	)


func _grant_ad_energy() -> void:
	var gs := _gs()
	if gs != null and "energy" in gs:
		gs.energy = min(int(gs.energy) + 3, 15)
	var es := _es()
	if es != null and es.has_method("record_ad_watch"):
		es.call("record_ad_watch")


func _on_iap_item_clicked(item_id: String) -> void:
	match item_id:
		"energy_pack":
			_grant_energy()
			_set_status(_t("【模擬購買成功】已購入發條能量補給箱，能量 +15 點！"))
		"soul_pack":
			_grant_soul_stones()
			_set_status(_t("【模擬購買成功】已購入神殿聚魂召喚包，聚魂石 ×10 入庫！"))
		"forge_pack":
			_grant_forge_mats()
			_set_status(_t("【模擬購買成功】已購入工坊鍛造資源箱，金幣 +500 與鍛造精粹入庫！"))


func _grant_energy() -> void:
	var gs := _gs()
	if gs != null and "energy" in gs:
		gs.energy = int(gs.energy) + 15


func _grant_soul_stones() -> void:
	# 聚魂石佔位模擬發放
	pass


func _grant_forge_mats() -> void:
	var gs := _gs()
	if gs != null and gs.has_method("add_gold"):
		gs.add_gold(500)
	elif gs != null and "gold" in gs:
		gs.gold = int(gs.gold) + 500


func _set_status(msg: String) -> void:
	if _status_msg_lbl:
		_status_msg_lbl.text = msg
	if get_parent() != null and get_parent().has_method("refresh_hud"):
		get_parent().call("refresh_hud")


func _on_close() -> void:
	closed.emit()
	queue_free()


func _gs() -> Node:
	var loop = Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return get_node_or_null("/root/GameState")


func _es() -> Node:
	var loop = Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("EnergySystem")
	return get_node_or_null("/root/EnergySystem")


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 5, radius: int = 18) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
	sb.shadow_size = 6
	sb.shadow_offset = Vector2(0, 3)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 5, radius: int = 18, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 14
	sb.content_margin_right = 14
	sb.content_margin_top = 8
	sb.content_margin_bottom = 10
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
		sb.shadow_size = 5
		sb.shadow_offset = Vector2(0, 3)
	return sb
