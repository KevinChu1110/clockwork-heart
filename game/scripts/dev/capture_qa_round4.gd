extends SceneTree
## 全面探索性 QA 盤點第四輪 (t_9823fb23)
## 覆蓋：
## 1. C0–C6 場景與獵場、聚魂殿、大廳
## 2. 針對 road 與 crossroads 新 2048x1152 尺寸檢查（底圖拉伸、實體座標、走路區域）
## 3. 抽查 6 位近期重繪非雷歐敵人戰鬥實機（wolf, fog, abo, falcon, boar, demon）開場、部位破壞與對話半身像

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/qa_round4",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ef61dc07/screenshots",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9823fb23/screenshots"
]

var _main: Node = null
var _phase: int = 0
var _sub_idx: int = 0
var _sub_step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _diagnostics: Array[Dictionary] = []

## ── Phase 1: C0-C6 場景、獵場、聚魂殿、大廳 ──
var _scene_checks: Array[Dictionary] = [
	{"type": "lobby", "name": "大廳 (Mobile Lobby)", "file": "proof_01_lobby.png"},
	{"type": "explore", "id": "village", "name": "C0 閣樓 (Village)", "file": "proof_02_c0_village.png"},
	{"type": "explore", "id": "town", "name": "C1 騎士堡壘 (Town)", "file": "proof_03_c1_town.png"},
	{"type": "explore", "id": "mist_village", "name": "C2 霧隱村 (Mist)", "file": "proof_04_c2_mist.png"},
	{"type": "explore", "id": "dojo", "name": "C3 道場 (Dojo)", "file": "proof_05_c3_dojo.png"},
	{"type": "explore", "id": "forest", "name": "C4 森林 (Forest)", "file": "proof_06_c4_forest.png"},
	{"type": "explore", "id": "coast", "name": "C5 海岸 (Coast)", "file": "proof_07_c5_coast.png"},
	{"type": "explore", "id": "tower_foyer", "name": "C6 法師之塔門廳 (Tower Foyer)", "file": "proof_08_c6_tower.png"},
	{"type": "explore", "id": "hunting_grounds", "name": "星途獵場 (Hunting Grounds)", "file": "proof_09_hunting_grounds.png"},
	{"type": "explore", "id": "town_soul", "name": "聚魂殿實體場景 (Town Soul)", "file": "proof_10_town_soul.png"},
	{"type": "soul_hall_tab", "name": "大廳聚魂殿分頁 (Soul Hall Tab)", "file": "proof_11_soul_hall_tab.png"},
]

## ── Phase 2: 地圖 road / crossroads 深度檢驗 ──
var _map_checks: Array[Dictionary] = [
	{"id": "road", "title": "玩具堆外緣 · 朝向世界大鐘", "file": "proof_12_map_road_spawn.png"},
	{"id": "crossroads", "title": "六域岔路 · 沙盤之心道", "file": "proof_13_map_crossroads_spawn.png"},
]

## ── Phase 3: 近期重繪非雷歐敵人戰鬥實機抽查 ──
var _battle_enemies: Array[Dictionary] = [
	{"id": "wolf", "name": "失控的鏽蝕玩具（狼）", "has_parts": false, "speaker": "失控的鏽蝕玩具", "dialogue": "喀啦喀啦……（發條劇烈顫動，齒輪咬合聲刺耳，金屬殘肢在荒路拖曳）"},
	{"id": "fog", "name": "白霧", "has_parts": true, "speaker": "白霧", "dialogue": "嘻嘻～真的假的，你分得清嗎？"},
	{"id": "abo", "name": "阿波", "has_parts": true, "speaker": "阿波", "dialogue": "發條最鬆的。來打我的架勢。打不穿的時候，別急——一下一下，把殼撞鬆。"},
	{"id": "falcon", "name": "疾影", "has_parts": true, "speaker": "疾影", "dialogue": "……把發條最鬆的送來了？眼睛，跟得上我嗎？追，會迷路。等，才見我。"},
	{"id": "boar", "name": "石拳", "has_parts": true, "speaker": "石拳", "dialogue": "……把發條最鬆的送來了？還站著？那就接下這一拳——力氣該砸向誰？"},
	{"id": "demon", "name": "停擺核", "has_parts": true, "speaker": "停擺核", "dialogue": "……沉寂的時間……將歸於永恆停擺……你的發條，終將停止旋動。"},
]

func _initialize() -> void:
	print("QA_ROUND4: Initializing Full Exploratory QA Audit...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND4: change_scene_to_file err=", err)
	_phase = 0
	_sub_idx = 0
	_sub_step = 0
	_wait = 0

func _setup_player_env(race: String = "rabbit") -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	var es: Node = root.get_node_or_null("EnergySystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("energy", 100)
		gs.set("gold", 50000)
		gs.set("hp", 150)
		gs.set("max_hp", 150)
		gs.set("weapon_uses_left", 30)
		gs.set("weapon_uses_max", 30)
		gs.set_flag("tut_done", true)
		gs.set_flag("c0_first_battle", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
		gs.set_flag("boss.leo_cleared", true)
		gs.set_flag("boss.white_fog_cleared", true)
		gs.set_flag("boss.abo_cleared", true)
		gs.set_flag("boss.shadowwind_cleared", true)
		gs.set_flag("boss.stonefist_cleared", true)
	if sk:
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")
	if es:
		es.set("energy", 100)

func _process(_delta: float) -> bool:
	_wait += 1
	match _phase:
		0:
			# 等待 main.tscn 載入就緒
			if _wait >= 25:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("QA_ROUND4: main ready. Moving to Phase 1: C0-C6, hunting, soul hall, lobby")
				_setup_player_env("rabbit")
				_phase = 1
				_sub_idx = 0
				_sub_step = 0
				_wait = 0

		1:
			# ── Phase 1: 場景抽查 ──
			var item: Dictionary = _scene_checks[_sub_idx]
			match _sub_step:
				0:
					print("QA_ROUND4: Phase 1 [%d/%d] -> %s" % [_sub_idx + 1, _scene_checks.size(), item["name"]])
					var t: String = item["type"]
					if t == "lobby":
						_main.call("_go_mobile_lobby")
					elif t == "soul_hall_tab":
						_main.call("_go_mobile_lobby")
					elif t == "explore":
						_main.call("proof_jump_explore", item["id"])
					_sub_step = 1
					_wait = 0
				1:
					if item["type"] == "soul_hall_tab" and _wait == 10:
						var lobby = _find_lobby()
						if lobby and lobby.has_method("_switch_tab"):
							lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
					if _wait >= 20:
						_save_viewport(item["file"], item["name"])
						_sub_idx += 1
						if _sub_idx >= _scene_checks.size():
							print("QA_ROUND4: Phase 1 finished. Moving to Phase 2: road & crossroads audit")
							_phase = 2
							_sub_idx = 0
							_sub_step = 0
							_wait = 0
						else:
							_sub_step = 0
							_wait = 0

		2:
			# ── Phase 2: road & crossroads 深度檢驗 ──
			var mitem: Dictionary = _map_checks[_sub_idx]
			var map_id: String = mitem["id"]
			match _sub_step:
				0:
					print("QA_ROUND4: Phase 2 [%d/%d] Inspecting map: %s" % [_sub_idx + 1, _map_checks.size(), map_id])
					_main.call("proof_jump_explore", map_id)
					_sub_step = 1
					_wait = 0
				1:
					if _wait >= 20:
						# 擷取開場 spawn 視角截圖
						_save_viewport(mitem["file"], "Map View - " + mitem["title"])
						# 蒐集地圖診斷資料
						_inspect_map_mechanics(map_id)
						_sub_step = 2
						_wait = 0
				2:
					# 測試相機捲動至北部邊界（針對 crossroads 頂部出口）
					var exp_view: Node = _find_explore()
					if exp_view and is_instance_valid(exp_view):
						if map_id == "crossroads":
							# 走向北部道場／森林路徑附近
							exp_view.set("player_pos", Vector2(1189, 150))
							if exp_view.has_method("_update_camera"):
								exp_view.call("_update_camera")
							if exp_view.has_method("_ysort_world"):
								exp_view.call("_ysort_world")
						elif map_id == "road":
							# 走向大橋出口處附近
							exp_view.set("player_pos", Vector2(393, 350))
							if exp_view.has_method("_update_camera"):
								exp_view.call("_update_camera")
							if exp_view.has_method("_ysort_world"):
								exp_view.call("_ysort_world")
					_sub_step = 3
					_wait = 0
				3:
					if _wait >= 15:
						var edge_file := "proof_%s_edge_scroll.png" % map_id
						_save_viewport(edge_file, "Map Edge Scroll - " + map_id)
						_sub_idx += 1
						if _sub_idx >= _map_checks.size():
							print("QA_ROUND4: Phase 2 finished. Moving to Phase 3: Battles")
							_phase = 3
							_sub_idx = 0
							_sub_step = 0
							_wait = 0
						else:
							_sub_step = 0
							_wait = 0

		3:
			# ── Phase 3: 6 位非雷歐敵人實機戰鬥 ──
			var edata: Dictionary = _battle_enemies[_sub_idx]
			var eid: String = edata["id"]
			match _sub_step:
				0:
					print("QA_ROUND4: Starting Battle [%d/%d] eid=%s (%s)" % [_sub_idx + 1, _battle_enemies.size(), eid, edata["name"]])
					var dbox_pre: Node = _main.get("_dialogue")
					if dbox_pre and is_instance_valid(dbox_pre):
						dbox_pre.set("visible", false)
						dbox_pre.set("mouse_filter", Control.MOUSE_FILTER_IGNORE)
					_setup_player_env("rabbit")
					_main.call("_start_battle_raw", eid)
					_sub_step = 1
					_wait = 0
				1:
					# 等待開場畫面穩定
					if _wait >= 20:
						var filename := "proof_battle_open_%s.png" % eid
						_save_viewport(filename, "Battle Open - " + edata["name"])
						if edata["has_parts"]:
							_sub_step = 2
							_wait = 0
						else:
							_sub_step = 4 # 直接跳對話
							_wait = 0
				2:
					# 觸發部位破壞
					var host: Control = _main.get("host") as Control
					var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
					if bnode and is_instance_valid(bnode):
						var sim = bnode.get("sim")
						if sim != null:
							var boss = sim.call("_primary_boss_unit")
							if boss and not boss.parts.is_empty():
								sim.parts_break_unlocked = true
								boss.hp = int(boss.max_hp * 0.6)
								var part = boss.parts[0]
								sim.focus_part_id = str(part.get("id", ""))
								var p_max = int(part.get("max_hp", 60))
								sim.call("_process_part_damage", boss, p_max + 20, true)
								if bnode.has_method("_append_log"):
									bnode.call("_append_log", "[color=#fc0]QA測試：部位破壞觸發【%s】！[/color]" % str(part.get("name", "部位")))
								if bnode.has_method("_refresh_part_bars"):
									bnode.call("_refresh_part_bars", boss)
								if bnode.has_method("_refresh_part_focus_hint"):
									bnode.call("_refresh_part_focus_hint")
								if bnode.has_method("_refresh_hud"):
									bnode.call("_refresh_hud")
					_sub_step = 3
					_wait = 0
				3:
					if _wait >= 15:
						var pfile := "proof_battle_part_break_%s.png" % eid
						_save_viewport(pfile, "Battle Part Break - " + edata["name"])
						_sub_step = 4
						_wait = 0
				4:
					# 測試對話半身像
					var lines := [
						{"speaker": edata["speaker"], "text": edata["dialogue"]}
					]
					_main.call("_play_dialog", lines)
					_sub_step = 5
					_wait = 0
				5:
					var dbox: Node = _main.get("_dialogue")
					if dbox and is_instance_valid(dbox):
						if dbox.has_method("_finish_typing"):
							dbox.call("_finish_typing")
					if _wait >= 15:
						var dfile := "proof_dialogue_%s.png" % eid
						_save_viewport(dfile, "Dialogue - " + edata["speaker"])
						if dbox and is_instance_valid(dbox):
							if dbox.has_method("_skip_or_advance"):
								dbox.call("_skip_or_advance")
							dbox.set("visible", false)
							dbox.set("mouse_filter", Control.MOUSE_FILTER_IGNORE)
						_sub_idx += 1
						if _sub_idx >= _battle_enemies.size():
							print("QA_ROUND4: All battles completed!")
							_phase = 4
							_wait = 0
						else:
							_sub_step = 0
							_wait = 0

		4:
			if _wait >= 10:
				_finish()
				return false

	return false

func _inspect_map_mechanics(map_id: String) -> void:
	var MapCatalogClass = preload("res://scripts/world/map_catalog.gd")
	var SpriteDBClass = preload("res://scripts/art/sprite_db.gd")
	var data: Dictionary = MapCatalogClass.build(map_id)
	var msize: Vector2 = data.get("size", Vector2.ZERO)
	var spawn: Vector2 = data.get("spawn", Vector2.ZERO)
	var art_id: String = str(data.get("art", map_id))
	var bg_path: String = SpriteDBClass.map_bg_path(art_id)
	if bg_path == "" and art_id != map_id:
		bg_path = SpriteDBClass.map_bg_path(map_id)

	var tex: Texture2D = load(bg_path) if ResourceLoader.exists(bg_path) else null
	var tex_size: Vector2 = tex.get_size() if tex != null else Vector2.ZERO
	var map_ratio: float = msize.x / msize.y if msize.y > 0.0 else 0.0
	var tex_ratio: float = tex_size.x / tex_size.y if tex_size.y > 0.0 else 0.0
	var ratio_diff: float = absf(map_ratio - tex_ratio)

	print("  [DIAGNOSTIC] Map ID: %s" % map_id)
	print("    Catalog Title: %s" % str(data.get("title", "")))
	print("    Catalog Size: %s (aspect ratio %.4f)" % [msize, map_ratio])
	print("    BG Art ID: %s | Path: %s" % [art_id, bg_path])
	print("    Texture Size: %s (aspect ratio %.4f) | Diff: %.4f" % [tex_size, tex_ratio, ratio_diff])
	print("    Spawn Pos: %s" % spawn)

	var origin: Vector2 = data.get("origin", Vector2(40, 80))
	var floor_rect: Rect2 = Rect2(origin, msize)
	var bounds: Rect2 = Rect2(origin + Vector2(20, 20), msize - Vector2(40, 40))
	print("    Floor Rect: %s | Bounds: %s" % [floor_rect, bounds])

	var entities: Array = data.get("entities", [])
	var out_of_bounds_ents: Array[String] = []
	var above_floor_ents: Array[String] = []
	for e in entities:
		var eid: String = str(e.get("id", ""))
		var pos: Vector2 = e.get("pos", Vector2.ZERO) as Vector2
		var sz: Vector2 = e.get("size", Vector2.ZERO) as Vector2
		if pos.y < floor_rect.position.y:
			above_floor_ents.append("%s(pos=%s, label=%s)" % [eid, pos, e.get("label", "")])
		if not bounds.has_point(pos):
			out_of_bounds_ents.append("%s(pos=%s, label=%s)" % [eid, pos, e.get("label", "")])

	print("    Entities total: %d" % entities.size())
	if not above_floor_ents.is_empty():
		print("    ⚠️ Entities with Y < floor_top (%d): %s" % [above_floor_ents.size(), str(above_floor_ents)])
	else:
		print("    ✓ All entities inside floor vertical range")
	if not out_of_bounds_ents.is_empty():
		print("    ⚠️ Entities outside walk bounds (%d): %s" % [out_of_bounds_ents.size(), str(out_of_bounds_ents)])
	else:
		print("    ✓ All entities inside walk bounds")

	_diagnostics.append({
		"map_id": map_id,
		"msize": msize,
		"map_ratio": map_ratio,
		"tex_size": tex_size,
		"tex_ratio": tex_ratio,
		"ratio_diff": ratio_diff,
		"bounds": bounds,
		"above_floor": above_floor_ents,
		"out_of_bounds": out_of_bounds_ents
	})

func _find_lobby() -> Node:
	if _main == null:
		return null
	var host: Control = _main.get("host") as Control
	if host and host.get_child_count() > 0:
		for c in host.get_children():
			if c.get_script() and c.get_script().resource_path.ends_with("mobile_lobby.gd"):
				return c
	return null

func _find_explore() -> Node:
	if _main == null:
		return null
	return _main.get("_explore")

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])

func _finish() -> void:
	print("QA_ROUND4: Finished execution. total_saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  SAVED: ", s)
	for e in _errors:
		print("  ERROR: ", e)
	quit(0 if _errors.is_empty() else 1)
