extends SceneTree
## 戰鬥武器 overlay 顯示與握持定位自動化回歸測試
## 執行指令：godot --headless -s res://scripts/battle/test_battle_weapon_overlay.gd
##
## 鎖住兩大歷史回歸瑕疵：
##   1. 角色裝備武器時 _battle_weapon.visible == true（鎖住 review.md 第 19i-6 條武器層永遠不顯示之缺陷）
##   2. 武器 overlay 定位座標落在右前手握持範圍，非預設 (0,0) 且非懸空離體（鎖住第 19i-7 條定位缺陷）
##   3. 當武器貼圖為空時 _battle_weapon.visible == false（正確隱藏）

var _ok := true
var _frame := 0
var _battle: Control = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _setup_player_loadout() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("gold", 1500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 18)
		gs.set("weapon_name", "精煉長劍")
		gs.set("path_style", "sword")
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "c1_entered_city", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
		if inst.is_empty():
			inst = eq.call("roll_instance", "knight_saber", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid
			gs.set("weapon_name", inst.get("name", "晨光長劍"))
			gs.set("weapon_atk", int((inst.get("rolled", {}) as Dictionary).get("atk", 24)))
			gs.set("path_style", "sword")


func _process(_delta: float) -> bool:
	_frame += 1
	match _frame:
		2:
			_setup_player_loadout()
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			if b_scn == null:
				_fail("無法載入 res://scenes/battle/battle.tscn")
				return _finish()
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "bandit")
			else:
				_fail("battle 場景沒有 setup 方法")
				return _finish()
		5:
			# 讓 layout_deferred 和 resized 訊號完成排版
			_verify_equipped_weapon()
		6:
			# 測試卸下武器/無貼圖時 visible 必須為 false
			_verify_unequipped_weapon()
			return _finish()
	return false


func _verify_equipped_weapon() -> void:
	if _battle == null or not is_instance_valid(_battle):
		_fail("戰鬥實例無效")
		return

	var player_body: TextureRect = _battle.get("player_body")
	if player_body == null or not is_instance_valid(player_body):
		_fail("無法取得 player_body")
		return

	var weapon_overlay: TextureRect = player_body.get_node_or_null("PlayerWeaponOverlay")
	if weapon_overlay == null:
		weapon_overlay = _battle.get("_battle_weapon")
	if weapon_overlay == null or not is_instance_valid(weapon_overlay):
		_fail("PlayerWeaponOverlay 節點不存在於 player_body 底下")
		return

	# 1. 斷言可見度：裝備武器時 visible 必須為 true（鎖住 19i-6 條）
	if not weapon_overlay.visible:
		_fail("裝備武器時 PlayerWeaponOverlay.visible 應為 true，實測為 false（第 19i-6 條回歸！）")
		return
	print("  ok [19i-6] 裝備武器時武器 overlay visible == true")

	# 2. 斷言貼圖有效且已掛載
	if weapon_overlay.texture == null:
		_fail("裝備武器時 PlayerWeaponOverlay.texture 不應為 null")
		return
	print("  ok 武器 overlay texture 載入成功：%s" % weapon_overlay.texture.resource_path)

	# 3. 斷言尺寸合理（bs.y * 0.50）
	var bs: Vector2 = player_body.size
	if bs.x < 8.0 or bs.y < 8.0:
		bs = player_body.custom_minimum_size
	if bs.x < 8.0:
		bs = Vector2(200, 250)

	var expected_sz := Vector2(bs.y * 0.50, bs.y * 0.50)
	var sz: Vector2 = weapon_overlay.size
	if sz.x <= 0 or sz.y <= 0:
		_fail("武器 overlay 尺寸無效：%s" % str(sz))
		return
	if abs(sz.x - expected_sz.x) > 2.0 or abs(sz.y - expected_sz.y) > 2.0:
		_fail("武器 overlay 尺寸 %s 與預期 %s 偏離過大" % [str(sz), str(expected_sz)])
		return
	print("  ok 武器 overlay 尺寸為 %s（符合 bs.y * 0.50）" % str(sz))

	# 4. 斷言定位座標落在右前手握持範圍（鎖住 19i-7 條）：
	#    - 絕不可停在預設 (0,0)
	#    - 必須在角色本體邊界內 (0 < pos.x < bs.x, 0 < pos.y < bs.y)
	#    - 公式基準為 bs.x * 0.36, bs.y * 0.20
	var pos: Vector2 = weapon_overlay.position
	if pos == Vector2.ZERO:
		_fail("武器 overlay 位置停在預設 Vector2.ZERO (0,0)，未正確定位！")
		return
	if pos.x < 0 or pos.y < 0 or pos.x >= bs.x or pos.y >= bs.y:
		_fail("武器 overlay 位置 %s 明顯偏離角色素體範圍 [0, %s] x [0, %s]" % [str(pos), bs.x, bs.y])
		return

	var expected_pos := Vector2(bs.x * 0.36, bs.y * 0.20)
	if abs(pos.x - expected_pos.x) > 5.0 or abs(pos.y - expected_pos.y) > 5.0:
		_fail("武器 overlay 位置 %s 與右前手握持定位基準 %s 偏離過大" % [str(pos), str(expected_pos)])
		return
	print("  ok [19i-7] 武器 overlay 位置 %s 落在右前手握持合理範圍（基準 %s）" % [str(pos), str(expected_pos)])

	# 5. 斷言 z_index 與層級
	if weapon_overlay.z_index < 1:
		_fail("武器 overlay z_index 應 >= 1 以正確覆蓋或對齊圖層，實測為 %d" % weapon_overlay.z_index)
		return
	print("  ok 武器 overlay z_index == %d" % weapon_overlay.z_index)


func _verify_unequipped_weapon() -> void:
	if _battle == null or not is_instance_valid(_battle):
		return

	var player_body: TextureRect = _battle.get("player_body")
	var weapon_overlay: TextureRect = player_body.get_node_or_null("PlayerWeaponOverlay") if player_body else null
	if weapon_overlay == null:
		weapon_overlay = _battle.get("_battle_weapon")

	# 模擬無武器狀態：將 sim unit 的 weapon_class 清空，且 SpriteDB 無武器疊層
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.set("weapon_name", "空手")
		gs.set("path_style", "")
		gs.equip_slots["weapon"] = ""
		gs.equip_worn.clear()
		gs.set("weapon_loadout", ["", "", ""])

	var sim = _battle.get("sim")
	if sim:
		var p_live = sim.call("get_unit", "player")
		if p_live:
			p_live.set("weapon_class", "")
			p_live.set("bare_fisted", false)

	# 重新排版
	_battle.call("_layout_battle_equipment_overlays")

	if weapon_overlay and weapon_overlay.visible:
		_fail("無武器狀態下 PlayerWeaponOverlay.visible 應為 false，實測為 true")
		return
	print("  ok 無裝備武器時武器 overlay 正確維持 visible == false")


func _finish() -> bool:
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	if _ok:
		print("BATTLE_WEAPON_OVERLAY_OK")
		quit(0)
	else:
		print("BATTLE_WEAPON_OVERLAY_FAIL")
		quit(1)
	return true
