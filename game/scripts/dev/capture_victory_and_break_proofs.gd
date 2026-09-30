extends SceneTree
## 戰鬥勝利結算多巴胺化與部位破壞特寫截圖腳本 (capture_victory_and_break_proofs.gd)
## 執行方式：xvfb-run -a godot --path game -s res://scripts/dev/capture_victory_and_break_proofs.gd

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const CombatHitFxScript := preload("res://scripts/battle/combat_hit_fx.gd")
const CoreSystemScript := preload("res://scripts/systems/core_system.gd")

var _step := 0
var _wait := 0
var _out_dir: String = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c21ebe66/proofs/settlement"
var _current_node: Node = null
var _current_dialog: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_setup_gamestate()
	_step = 1
	_wait = 0


func _setup_gamestate() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
		gs.set("gold", 2500)
		gs.set("level", 15)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 24)
		gs.set("weapon_name", "晨光長劍")
		gs.set("path_style", "sword")


func _save_viewport(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p := _out_dir.path_join(filename)
		img.save_png(p)
		print("  [SAVED SHOT] -> %s (%dx%d)" % [p, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 步驟 1：建立戰鬥場景，待畫面穩定後觸發部位破壞特寫 (Shockwave, Stars, Sparks, Slow-Mo Gears)
			if _wait == 2:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_current_node = b_scn.instantiate()
					root.add_child(_current_node)
					if _current_node.has_method("setup"):
						_current_node.call("setup", "road_bandit")

			if _wait == 16:
				if _current_node != null:
					_current_node.call("_set_player_pose", "attack")
					_current_node.call("_set_boss_pose", "recover")
					_current_node.call("_on_event", "part_broken", {
						"boss_id": "road_bandit",
						"part_name": "重裝板件",
						"staggered": false
					})
					print("  >>> 觸發部位破壞特寫 (part_broken: road_bandit 重裝板件)")

			if _wait == 20:
				_save_viewport("proof_part_break_moment.png")
				if is_instance_valid(_current_node):
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2：巨偶戰鬥場景中的部位破壞特寫 (Colossus Part Break)
			if _wait == 2:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_current_node = b_scn.instantiate()
					root.add_child(_current_node)
					if _current_node.has_method("setup"):
						_current_node.call("setup", "colossus_puppet")

			if _wait == 16:
				if _current_node != null:
					_current_node.call("_set_player_pose", "attack")
					_current_node.call("_set_boss_pose", "recover")
					_current_node.call("_on_event", "part_broken", {
						"boss_id": "colossus_puppet",
						"part_name": "發條機芯",
						"staggered": true
					})
					print("  >>> 觸發巨偶部位破壞特寫 (part_broken: colossus_puppet 發條機芯)")

			if _wait == 20:
				_save_viewport("proof_colossus_part_break.png")
				if is_instance_valid(_current_node):
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3：金階勝利結算畫面 (立體金色大勝獎牌、齒輪寶箱解鎖、金階光環)
			if _wait == 2:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_current_node = b_scn.instantiate()
					root.add_child(_current_node)
					if _current_node.has_method("setup"):
						_current_node.call("setup", "wolf")
				var sample_gold := {
					"id": "part_gold_01",
					"slot": "mainspring",
					"tier": "gold",
					"tier_name": "金",
					"slot_name": "發條發電機",
					"exp_gain": 150,
					"scrap_gain": 4,
					"is_colossus": true,
					"stats": {"ATK": 32, "HP": 140}
				}
				_current_dialog = BattleVictoryDialogScript.show_dialog(root, sample_gold, Callable(), 150, 4)

			if _wait == 26:
				_save_viewport("proof_victory_settlement_gold.png")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				if is_instance_valid(_current_node):
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4：紫階勝利結算畫面 (立體大勝獎牌、齒輪寶箱、紫階光環、經驗與鐵屑)
			if _wait == 2:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_current_node = b_scn.instantiate()
					root.add_child(_current_node)
					if _current_node.has_method("setup"):
						_current_node.call("setup", "boar")
				var sample_purple := {
					"id": "part_purple_01",
					"slot": "gear_train",
					"tier": "purple",
					"tier_name": "紫",
					"slot_name": "傳動齒輪組",
					"exp_gain": 85,
					"scrap_gain": 2,
					"stats": {"ATK": 20, "DEF": 15}
				}
				_current_dialog = BattleVictoryDialogScript.show_dialog(root, sample_purple, Callable(), 85, 2)

			if _wait == 26:
				_save_viewport("proof_victory_settlement_purple.png")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				if is_instance_valid(_current_node):
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5：八色階光環矩陣展示 (gray/white/orange/blue/purple/gold/green/red)
			if _wait == 2:
				_build_tier_matrix_display()

			if _wait == 16:
				_save_viewport("proof_victory_eight_tiers_matrix.png")
				if is_instance_valid(_current_node):
					_current_node.queue_free()
					_current_node = null
				print("CAPTURE_ALL_PROOFS_COMPLETED_SUCCESSFULLY")
				quit(0)
				return true
	return false


func _build_tier_matrix_display() -> void:
	var bg := PanelContainer.new()
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color("#FFFDF8")
	bg.add_theme_stylebox_override("panel", sb)
	root.add_child(bg)
	_current_node = bg

	var v := VBoxContainer.new()
	v.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	v.add_theme_constant_override("separation", 20)
	bg.add_child(v)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 36)
	margin.add_theme_constant_override("margin_right", 36)
	margin.add_theme_constant_override("margin_top", 30)
	margin.add_theme_constant_override("margin_bottom", 30)
	v.add_child(margin)

	var inner_v := VBoxContainer.new()
	inner_v.add_theme_constant_override("separation", 24)
	margin.add_child(inner_v)

	var title_lbl := Label.new()
	title_lbl.text = "《發條之心》戰鬥勝利結算 · 八色階光環矩陣 (8-Tier Auric Halos)"
	title_lbl.add_theme_font_size_override("font_size", 24)
	title_lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
	inner_v.add_child(title_lbl)

	var grid := GridContainer.new()
	grid.columns = 4
	grid.add_theme_constant_override("h_separation", 28)
	grid.add_theme_constant_override("v_separation", 24)
	inner_v.add_child(grid)

	var tiers := [
		{"id": "gray", "name": "灰階", "color": Color("#8E8E93")},
		{"id": "white", "name": "白階", "color": Color("#FFFFFF")},
		{"id": "orange", "name": "橘階", "color": Color("#FFA010")},
		{"id": "blue", "name": "藍階", "color": Color("#38A0FF")},
		{"id": "purple", "name": "紫階", "color": Color("#A855F7")},
		{"id": "gold", "name": "金階", "color": Color("#FFD028")},
		{"id": "green", "name": "綠階", "color": Color("#4ED86A")},
		{"id": "red", "name": "紅階", "color": Color("#FF5E8A")},
	]

	var sdb = root.get_node_or_null("SpriteDB")
	if sdb == null:
		sdb = load("res://scripts/art/sprite_db.gd")

	for t_info in tiers:
		var card := PanelContainer.new()
		card.custom_minimum_size = Vector2(260, 110)
		var c_st := StyleBoxFlat.new()
		c_st.bg_color = Color("#FFF8E7")
		c_st.border_color = Color("#1F1A3A")
		c_st.set_border_width_all(2)
		c_st.border_width_bottom = 4
		c_st.set_corner_radius_all(14)
		card.add_theme_stylebox_override("panel", c_st)
		grid.add_child(card)

		var c_m := MarginContainer.new()
		c_m.add_theme_constant_override("margin_left", 14)
		c_m.add_theme_constant_override("margin_right", 14)
		c_m.add_theme_constant_override("margin_top", 10)
		c_m.add_theme_constant_override("margin_bottom", 10)
		card.add_child(c_m)

		var h := HBoxContainer.new()
		h.add_theme_constant_override("separation", 16)
		c_m.add_child(h)

		var icon_box := PanelContainer.new()
		icon_box.custom_minimum_size = Vector2(80, 80)
		var ib_st := StyleBoxFlat.new()
		ib_st.bg_color = Color(0.96, 0.95, 0.98, 1)
		ib_st.border_color = Color("#1F1A3A")
		ib_st.set_border_width_all(2)
		ib_st.set_corner_radius_all(12)
		icon_box.add_theme_stylebox_override("panel", ib_st)
		h.add_child(icon_box)

		# 八色階光環
		var halo_cls = BattleVictoryDialogScript.TierHaloEffect
		var halo = halo_cls.new()
		halo.call("set_tier", t_info.id, t_info.color)
		icon_box.add_child(halo)

		var icon := TextureRect.new()
		icon.custom_minimum_size = Vector2(64, 64)
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		if sdb:
			icon.texture = sdb.call("core_slot_icon", "mainspring")
		icon.modulate = t_info.color
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		icon_box.add_child(icon)

		var col := VBoxContainer.new()
		col.alignment = BoxContainer.ALIGNMENT_CENTER
		col.add_theme_constant_override("separation", 4)
		h.add_child(col)

		var tag := Label.new()
		tag.text = "【%s】" % t_info.name
		tag.add_theme_font_size_override("font_size", 16)
		tag.add_theme_color_override("font_color", t_info.color if t_info.id != "white" else Color("#1F1A3A"))
		col.add_child(tag)

		var desc := Label.new()
		desc.text = "光環: " + str(t_info.id)
		desc.add_theme_font_size_override("font_size", 12)
		desc.add_theme_color_override("font_color", Color("#7A6E8A"))
		col.add_child(desc)
