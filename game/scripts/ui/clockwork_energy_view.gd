class_name ClockworkEnergyView
extends Control
## 戰鬥原型介面：共用發條能量條 ＋ 四職業手動/逾時分配視窗
## 符合手遊人體工學、多巴胺色盤、無 Emoji、防止卡死之短暫倒數機制

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ClockworkEnergyPrototype = preload("res://scripts/battle/clockwork_energy_prototype.gd")

var sim: ClockworkEnergyPrototype

var energy_bar: ProgressBar
var modal_scrim: ColorRect
var hero_buttons: Dictionary = {}

## UI 節點參考
var _top_panel: PanelContainer
var _energy_bar: ProgressBar
var _energy_label: Label
var _status_banner: Label

var _party_container: HBoxContainer
var _hero_cards: Dictionary = {}  ## profession_id -> Dictionary of nodes

var _boss_card: PanelContainer
var _boss_hp_bar: ProgressBar
var _boss_hp_label: Label
var _boss_armor_bar: ProgressBar
var _boss_armor_label: Label

var _modal_scrim: ColorRect
var _modal_panel: PanelContainer
var _countdown_bar: ProgressBar
var _countdown_label: Label
var _hero_buttons: Dictionary = {}

var _log_label: RichTextLabel
var _auto_run: bool = true


func _init() -> void:
	sim = ClockworkEnergyPrototype.new()
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_build_ui()
	energy_bar = _energy_bar
	modal_scrim = _modal_scrim
	hero_buttons = _hero_buttons
	_connect_sim_signals()
	_refresh_all()


func _ready() -> void:
	_refresh_all()


func _connect_sim_signals() -> void:
	sim.state_changed.connect(_on_sim_state_changed)
	sim.allocation_started.connect(_on_allocation_started)
	sim.allocation_completed.connect(_on_allocation_completed)
	sim.combat_log_added.connect(_on_combat_log_added)
	sim.battle_ended.connect(_on_battle_ended)


func _process(delta: float) -> void:
	if _auto_run and sim != null and not sim.battle_over:
		sim.update(delta)


func _build_ui() -> void:
	## 1. 背景底色：溫和奶油童話底色
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.96, 0.94, 0.90, 1.0)
	add_child(bg)

	## 主垂直排版
	var main_vbox := VBoxContainer.new()
	main_vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	main_vbox.offset_left = 24
	main_vbox.offset_top = 16
	main_vbox.offset_right = -24
	main_vbox.offset_bottom = -16
	main_vbox.add_theme_constant_override("separation", 12)
	add_child(main_vbox)

	## 2. 頂部發條能量核心面板
	_top_panel = PanelContainer.new()
	_top_panel.add_theme_stylebox_override("panel", UiStyle.panel_style(UiStyle.TATA_GOLD))
	main_vbox.add_child(_top_panel)

	var top_vbox := VBoxContainer.new()
	top_vbox.add_theme_constant_override("separation", 6)
	_top_panel.add_child(top_vbox)

	var header_hbox := HBoxContainer.new()
	top_vbox.add_child(header_hbox)

	var title_lbl := Label.new()
	title_lbl.text = "發條之心 · 戰鬥原型：共用發條能量分配系統"
	title_lbl.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	title_lbl.add_theme_font_size_override("font_size", 20)
	header_hbox.add_child(title_lbl)

	header_hbox.add_spacer(false)

	_status_banner = Label.new()
	_status_banner.text = "戰鬥進行中"
	_status_banner.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	_status_banner.add_theme_font_size_override("font_size", 16)
	header_hbox.add_child(_status_banner)

	## 共用發條能量條
	var energy_box := VBoxContainer.new()
	top_vbox.add_child(energy_box)

	var energy_header_hbox := HBoxContainer.new()
	energy_box.add_child(energy_header_hbox)

	var energy_title := Label.new()
	energy_title.text = "【小隊共用發條能量】四職業技能共享單一能量池"
	energy_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	energy_title.add_theme_font_size_override("font_size", 15)
	energy_header_hbox.add_child(energy_title)

	energy_header_hbox.add_spacer(false)

	_energy_label = Label.new()
	_energy_label.text = "0 / 100"
	_energy_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_energy_label.add_theme_font_size_override("font_size", 15)
	energy_header_hbox.add_child(_energy_label)

	_energy_bar = ProgressBar.new()
	_energy_bar.min_value = 0.0
	_energy_bar.max_value = ClockworkEnergyPrototype.MAX_SHARED_ENERGY
	_energy_bar.value = 0.0
	_energy_bar.show_percentage = false
	_energy_bar.custom_minimum_size = Vector2(0, 24)

	var bar_bg := StyleBoxFlat.new()
	bar_bg.bg_color = Color(0.24, 0.18, 0.14, 0.95)
	bar_bg.set_corner_radius_all(12)
	bar_bg.border_width_bottom = 3
	bar_bg.border_color = Color(0.38, 0.28, 0.18, 1.0)
	_energy_bar.add_theme_stylebox_override("background", bar_bg)

	var bar_fill := StyleBoxFlat.new()
	bar_fill.bg_color = UiStyle.TATA_YELLOW
	bar_fill.set_corner_radius_all(12)
	bar_fill.border_width_bottom = 3
	bar_fill.border_color = UiStyle.TATA_ORANGE
	_energy_bar.add_theme_stylebox_override("fill", bar_fill)

	energy_box.add_child(_energy_bar)

	## 3. 中部：四職業小隊 vs 首領
	var battle_hbox := HBoxContainer.new()
	battle_hbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	battle_hbox.add_theme_constant_override("separation", 16)
	main_vbox.add_child(battle_hbox)

	## 3A. 左側：四職業卡片
	var party_panel := PanelContainer.new()
	party_panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	party_panel.size_flags_stretch_ratio = 2.2
	party_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	battle_hbox.add_child(party_panel)

	var party_vbox := VBoxContainer.new()
	party_vbox.add_theme_constant_override("separation", 8)
	party_panel.add_child(party_vbox)

	var p_title := Label.new()
	p_title.text = "發條特遣隊（四大職業）"
	p_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	p_title.add_theme_font_size_override("font_size", 16)
	party_vbox.add_child(p_title)

	_party_container = HBoxContainer.new()
	_party_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_party_container.add_theme_constant_override("separation", 8)
	party_vbox.add_child(_party_container)

	_build_hero_cards()

	## 3B. 右側：發條巨像卡片
	_boss_card = PanelContainer.new()
	_boss_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_boss_card.size_flags_stretch_ratio = 1.0
	_boss_card.add_theme_stylebox_override("panel", UiStyle.panel_style(UiStyle.TATA_ORANGE))
	battle_hbox.add_child(_boss_card)

	var boss_vbox := VBoxContainer.new()
	boss_vbox.add_theme_constant_override("separation", 10)
	_boss_card.add_child(boss_vbox)

	var b_title := Label.new()
	b_title.text = "敵方首領：發條巨像"
	b_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	b_title.add_theme_font_size_override("font_size", 16)
	boss_vbox.add_child(b_title)

	## 首領血條
	var b_hp_title := Label.new()
	b_hp_title.text = "核心耐久度 (HP)"
	b_hp_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	b_hp_title.add_theme_font_size_override("font_size", 13)
	boss_vbox.add_child(b_hp_title)

	_boss_hp_bar = ProgressBar.new()
	_boss_hp_bar.min_value = 0.0
	_boss_hp_bar.max_value = sim.enemy["max_hp"]
	_boss_hp_bar.value = sim.enemy["hp"]
	_boss_hp_bar.show_percentage = false
	_boss_hp_bar.custom_minimum_size = Vector2(0, 18)
	var bhp_fill := StyleBoxFlat.new()
	bhp_fill.bg_color = UiStyle.HP_FILL
	bhp_fill.set_corner_radius_all(8)
	_boss_hp_bar.add_theme_stylebox_override("fill", bhp_fill)
	boss_vbox.add_child(_boss_hp_bar)

	_boss_hp_label = Label.new()
	_boss_hp_label.text = "%d / %d" % [sim.enemy["hp"], sim.enemy["max_hp"]]
	_boss_hp_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_boss_hp_label.add_theme_font_size_override("font_size", 12)
	boss_vbox.add_child(_boss_hp_label)

	## 首領裝甲板件
	var b_arm_title := Label.new()
	b_arm_title.text = "外層裝甲板件 (Armor)"
	b_arm_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	b_arm_title.add_theme_font_size_override("font_size", 13)
	boss_vbox.add_child(b_arm_title)

	_boss_armor_bar = ProgressBar.new()
	_boss_armor_bar.min_value = 0.0
	_boss_armor_bar.max_value = sim.enemy["max_armor"]
	_boss_armor_bar.value = sim.enemy["armor"]
	_boss_armor_bar.show_percentage = false
	_boss_armor_bar.custom_minimum_size = Vector2(0, 14)
	var barm_fill := StyleBoxFlat.new()
	barm_fill.bg_color = UiStyle.TATA_BLUE
	barm_fill.set_corner_radius_all(6)
	_boss_armor_bar.add_theme_stylebox_override("fill", barm_fill)
	boss_vbox.add_child(_boss_armor_bar)

	_boss_armor_label = Label.new()
	_boss_armor_label.text = "裝甲值: %d (減傷中)" % sim.enemy["armor"]
	_boss_armor_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_boss_armor_label.add_theme_font_size_override("font_size", 12)
	boss_vbox.add_child(_boss_armor_label)

	## 4. 底部：戰鬥日誌 ＋ 測試控制區
	var bottom_hbox := HBoxContainer.new()
	bottom_hbox.custom_minimum_size = Vector2(0, 130)
	bottom_hbox.add_theme_constant_override("separation", 12)
	main_vbox.add_child(bottom_hbox)

	var log_panel := PanelContainer.new()
	log_panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	log_panel.size_flags_stretch_ratio = 2.5
	log_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	bottom_hbox.add_child(log_panel)

	_log_label = RichTextLabel.new()
	_log_label.bbcode_enabled = true
	_log_label.scroll_following = true
	_log_label.add_theme_color_override("default_color", UiStyle.TATA_BROWN)
	_log_label.add_theme_font_size_override("normal_font_size", 12)
	log_panel.add_child(_log_label)

	var ctrl_panel := PanelContainer.new()
	ctrl_panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	ctrl_panel.size_flags_stretch_ratio = 1.0
	ctrl_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	bottom_hbox.add_child(ctrl_panel)

	var ctrl_vbox := VBoxContainer.new()
	ctrl_vbox.add_theme_constant_override("separation", 6)
	ctrl_panel.add_child(ctrl_vbox)

	var ctrl_title := Label.new()
	ctrl_title.text = "原型測試控制"
	ctrl_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	ctrl_title.add_theme_font_size_override("font_size", 14)
	ctrl_vbox.add_child(ctrl_title)

	var btn_quick_charge := Button.new()
	btn_quick_charge.text = "注入發條能量 (+30)"
	UiStyle.style_button(btn_quick_charge, false)
	btn_quick_charge.custom_minimum_size = Vector2(0, 36)
	btn_quick_charge.pressed.connect(func():
		sim.shared_energy = minf(ClockworkEnergyPrototype.MAX_SHARED_ENERGY, sim.shared_energy + 30.0)
		sim.add_log("［除錯］手動注入發條能量 +30！")
	)
	ctrl_vbox.add_child(btn_quick_charge)

	var btn_restart := Button.new()
	btn_restart.text = "重置戰鬥原型"
	UiStyle.style_button(btn_restart, false)
	btn_restart.custom_minimum_size = Vector2(0, 36)
	btn_restart.pressed.connect(func():
		sim.reset_battle()
		_log_label.clear()
		_refresh_all()
	)
	ctrl_vbox.add_child(btn_restart)

	## 5. 倒數決策懸浮視窗 (Overlay Modal)
	_build_allocation_modal()


func _build_hero_cards() -> void:
	var order := ["swordsman", "knight", "mage", "warrior"]
	for p_id in order:
		var hero: Dictionary = sim.heroes[p_id]

		var card := PanelContainer.new()
		card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		card.size_flags_vertical = Control.SIZE_EXPAND_FILL
		var csb := StyleBoxFlat.new()
		csb.bg_color = Color(1.0, 1.0, 1.0, 0.9)
		csb.border_color = UiStyle.TATA_CARD_BORDER
		csb.set_border_width_all(2)
		csb.border_width_bottom = 4
		csb.set_corner_radius_all(14)
		csb.content_margin_left = 10
		csb.content_margin_right = 10
		csb.content_margin_top = 8
		csb.content_margin_bottom = 8
		card.add_theme_stylebox_override("panel", csb)
		_party_container.add_child(card)

		var vbox := VBoxContainer.new()
		vbox.add_theme_constant_override("separation", 4)
		card.add_child(vbox)

		var name_lbl := Label.new()
		name_lbl.text = "%s·%s" % [hero["name"], hero["profession"]]
		name_lbl.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
		name_lbl.add_theme_font_size_override("font_size", 14)
		vbox.add_child(name_lbl)

		var role_lbl := Label.new()
		role_lbl.text = hero["role_desc"]
		role_lbl.add_theme_color_override("font_color", UiStyle.CREAM_DIM)
		role_lbl.add_theme_font_size_override("font_size", 11)
		vbox.add_child(role_lbl)

		var hp_bar := ProgressBar.new()
		hp_bar.min_value = 0.0
		hp_bar.max_value = hero["max_hp"]
		hp_bar.value = hero["hp"]
		hp_bar.show_percentage = false
		hp_bar.custom_minimum_size = Vector2(0, 12)
		var hp_fill := StyleBoxFlat.new()
		hp_fill.bg_color = UiStyle.HP_FILL
		hp_fill.set_corner_radius_all(6)
		hp_bar.add_theme_stylebox_override("fill", hp_fill)
		vbox.add_child(hp_bar)

		var hp_lbl := Label.new()
		hp_lbl.text = "HP: %d/%d" % [hero["hp"], hero["max_hp"]]
		hp_lbl.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
		hp_lbl.add_theme_font_size_override("font_size", 11)
		vbox.add_child(hp_lbl)

		var shield_lbl := Label.new()
		shield_lbl.text = "護盾: 0"
		shield_lbl.add_theme_color_override("font_color", UiStyle.TATA_BLUE)
		shield_lbl.add_theme_font_size_override("font_size", 11)
		vbox.add_child(shield_lbl)

		var skill_lbl := Label.new()
		skill_lbl.text = "絕技: %s" % hero["skill_name"]
		skill_lbl.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
		skill_lbl.add_theme_font_size_override("font_size", 11)
		vbox.add_child(skill_lbl)

		_hero_cards[p_id] = {
			"card": card,
			"hp_bar": hp_bar,
			"hp_lbl": hp_lbl,
			"shield_lbl": shield_lbl,
			"skill_lbl": skill_lbl
		}


func _build_allocation_modal() -> void:
	## 遮罩
	_modal_scrim = ColorRect.new()
	_modal_scrim.set_anchors_preset(Control.PRESET_FULL_RECT)
	_modal_scrim.color = Color(0.15, 0.10, 0.08, 0.70)
	_modal_scrim.visible = false
	add_child(_modal_scrim)

	## 視窗面板（寬度 750px，符合規範）
	_modal_panel = PanelContainer.new()
	_modal_panel.custom_minimum_size = Vector2(750, 420)
	_modal_panel.set_anchors_preset(Control.PRESET_CENTER)
	_modal_panel.offset_left = -375
	_modal_panel.offset_top = -210
	_modal_panel.offset_right = 375
	_modal_panel.offset_bottom = 210
	_modal_panel.add_theme_stylebox_override("panel", UiStyle.panel_style(UiStyle.TATA_GOLD))
	_modal_scrim.add_child(_modal_panel)

	var mvbox := VBoxContainer.new()
	mvbox.add_theme_constant_override("separation", 12)
	_modal_panel.add_child(mvbox)

	var m_title := Label.new()
	m_title.text = "發條能量過載　請選擇技能注入對象"
	m_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	m_title.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	m_title.add_theme_font_size_override("font_size", 20)
	mvbox.add_child(m_title)

	var cd_box := VBoxContainer.new()
	cd_box.add_theme_constant_override("separation", 4)
	mvbox.add_child(cd_box)

	_countdown_label = Label.new()
	_countdown_label.text = "手動決策倒數：3.5 秒（逾時將由系統智慧自動挑選，絕不卡關）"
	_countdown_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_countdown_label.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	_countdown_label.add_theme_font_size_override("font_size", 14)
	cd_box.add_child(_countdown_label)

	_countdown_bar = ProgressBar.new()
	_countdown_bar.min_value = 0.0
	_countdown_bar.max_value = ClockworkEnergyPrototype.COUNTDOWN_SECONDS
	_countdown_bar.value = ClockworkEnergyPrototype.COUNTDOWN_SECONDS
	_countdown_bar.show_percentage = false
	_countdown_bar.custom_minimum_size = Vector2(0, 16)
	var cd_fill := StyleBoxFlat.new()
	cd_fill.bg_color = UiStyle.TATA_GREEN
	cd_fill.set_corner_radius_all(8)
	_countdown_bar.add_theme_stylebox_override("fill", cd_fill)
	cd_box.add_child(_countdown_bar)

	## 四職業選擇網格（2x2 排列，每顆按鈕 >= 50px）
	var grid := GridContainer.new()
	grid.columns = 2
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 14)
	grid.add_theme_constant_override("v_separation", 12)
	mvbox.add_child(grid)

	var order := ["swordsman", "knight", "mage", "warrior"]
	for p_id in order:
		var hero: Dictionary = sim.heroes[p_id]

		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.size_flags_vertical = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(340, 75)
		UiStyle.style_button(btn, true)

		var btn_vbox := VBoxContainer.new()
		btn_vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
		btn_vbox.offset_left = 12
		btn_vbox.offset_top = 8
		btn_vbox.offset_right = -12
		btn_vbox.offset_bottom = -8
		btn_vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
		btn.add_child(btn_vbox)

		var h_top := HBoxContainer.new()
		btn_vbox.add_child(h_top)

		var h_name := Label.new()
		h_name.text = "【%s】%s" % [hero["profession"], hero["name"]]
		h_name.add_theme_color_override("font_color", Color(0.20, 0.10, 0.02, 1.0))
		h_name.add_theme_font_size_override("font_size", 16)
		h_top.add_child(h_name)

		h_top.add_spacer(false)

		var h_skill := Label.new()
		h_skill.text = "招式: %s" % hero["skill_name"]
		h_skill.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
		h_skill.add_theme_font_size_override("font_size", 14)
		h_top.add_child(h_skill)

		var h_desc := Label.new()
		h_desc.text = hero["skill_desc"]
		h_desc.add_theme_color_override("font_color", Color(0.35, 0.25, 0.15, 1.0))
		h_desc.add_theme_font_size_override("font_size", 12)
		h_desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		btn_vbox.add_child(h_desc)

		btn.pressed.connect(func():
			_on_hero_chosen(p_id)
		)

		grid.add_child(btn)
		_hero_buttons[p_id] = btn

	var hint := Label.new()
	hint.text = "策略提示：殘血選騎士護盾、強敵有甲選戰士破甲、缺能選法師加速、搶攻選劍士貫穿！"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_color_override("font_color", UiStyle.CREAM_DIM)
	hint.add_theme_font_size_override("font_size", 12)
	mvbox.add_child(hint)


func _on_hero_chosen(profession_id: String) -> void:
	sim.allocate_manual(profession_id)


func _on_allocation_started(countdown_sec: float) -> void:
	_modal_scrim.visible = true
	_countdown_bar.max_value = countdown_sec
	_countdown_bar.value = countdown_sec


func _on_allocation_completed(profession_id: String, hero_name: String, is_auto: bool, skill_name: String) -> void:
	_modal_scrim.visible = false
	_refresh_all()


func _on_combat_log_added(text: String, is_highlight: bool) -> void:
	if _log_label == null:
		return
	if is_highlight:
		_log_label.append_text("[color=#ff8800][b]%s[/b][/color]\\n" % text)
	else:
		_log_label.append_text("%s\\n" % text)


func _on_battle_ended(won: bool) -> void:
	_status_banner.text = "戰鬥結算：" + ("小隊獲勝！" if won else "小隊潰敗")
	_status_banner.add_theme_color_override("font_color", UiStyle.TATA_GREEN if won else UiStyle.HP_FILL)
	_refresh_all()


func _on_sim_state_changed() -> void:
	_refresh_all()


func _refresh_all() -> void:
	if sim == null or _energy_bar == null:
		return

	## 1. 能量池刷新
	_energy_bar.value = sim.shared_energy
	_energy_label.text = "%d / %d (分配門檻: %d)" % [
		int(sim.shared_energy),
		int(ClockworkEnergyPrototype.MAX_SHARED_ENERGY),
		int(ClockworkEnergyPrototype.ALLOCATION_THRESHOLD)
	]

	## 2. 英雄卡片刷新
	for p_id in sim.heroes.keys():
		var hero: Dictionary = sim.heroes[p_id]
		var h_ui: Dictionary = _hero_cards.get(p_id, {})
		if h_ui.is_empty():
			continue

		var hp_bar: ProgressBar = h_ui["hp_bar"]
		var hp_lbl: Label = h_ui["hp_lbl"]
		var shield_lbl: Label = h_ui["shield_lbl"]

		hp_bar.value = hero["hp"]
		hp_lbl.text = "HP: %d/%d" % [hero["hp"], hero["max_hp"]]
		shield_lbl.text = "護盾: %d" % hero["shield"]
		shield_lbl.visible = (hero["shield"] > 0)

	## 3. 首領刷新
	_boss_hp_bar.value = sim.enemy["hp"]
	_boss_hp_label.text = "%d / %d" % [sim.enemy["hp"], sim.enemy["max_hp"]]
	_boss_armor_bar.value = sim.enemy["armor"]
	if sim.enemy["armor"] > 0:
		_boss_armor_label.text = "裝甲值: %d (減傷 50%%)" % sim.enemy["armor"]
		_boss_armor_label.add_theme_color_override("font_color", UiStyle.TATA_BLUE)
	else:
		_boss_armor_label.text = "裝甲破碎！易傷狀態 (持續中)"
		_boss_armor_label.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)

	## 4. 倒數視窗更新
	if sim.is_allocating:
		_modal_scrim.visible = true
		_countdown_bar.value = sim.allocation_countdown
		_countdown_label.text = "手動決策倒數：%.1f 秒（逾時將由系統智慧自動挑選，絕不卡關）" % maxf(0.0, sim.allocation_countdown)
	else:
		_modal_scrim.visible = false
