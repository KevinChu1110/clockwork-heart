extends SceneTree
## 探索與戰鬥換裝失敗不准退回 128 糊圖無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_explore_battle_no_128_fallback.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectDemo = preload("res://scripts/ui/paperdoll_select_demo.gd")

var _ok := true
var _step := 0
var _wait := 0
var _gs: Node = null
var _battle: Control = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始探索與戰鬥換裝不准退回 128 糊圖驗證 (0-QA18, 0-QA21, 31d) ===")
	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		_fail("無法取得 GameState 單例")
		quit(1)
		return

	# 1. 驗證 SpriteDB.player_equipped_idle 換裝成功走 512
	print("\n--- 檢查斷言 ①：換裝成功時回傳 >=256 (512) 高清貼圖 ---")
	SpriteDB.clear_equipped_cache()
	var rab_slots := {
		"race": "rabbit",
		"costume": "costume_royal_parade",
		"chassis": "paint_ivory_stock",
		"head_unit": "ear_rabbit_straight",
		"optic_core": "core_cyan_emerald",
		"winding_key": "key_classic_brass",
		"weapon": "wpn_dawn_blade"
	}
	var rab_tex: Texture2D = SpriteDB.player_equipped_idle("rabbit", rab_slots)
	if rab_tex == null or rab_tex.get_width() < 256:
		_fail("兔族皇家巡遊換裝待機圖應 >= 256，實際: %s" % (str(rab_tex.get_width()) if rab_tex else "null"))
	else:
		print("  ✓ 兔族皇家巡遊成功回傳高清貼圖，尺寸: %dx%d" % [rab_tex.get_width(), rab_tex.get_height()])

	for f in range(4):
		var rab_walk := SpriteDB.player_equipped_walk(f, "rabbit", rab_slots)
		if rab_walk == null or rab_walk.get_width() < 256:
			_fail("兔族皇家巡遊走路幀 %d 應 >= 256，實際: %s" % [f, (str(rab_walk.get_width()) if rab_walk else "null")])
	print("  ✓ 兔族皇家巡遊走路四幀皆 >= 256 (512x512)")

	var fox_slots := {
		"race": "fox",
		"costume": "costume_astral_observer",
		"chassis": "paint_fox_orange",
		"weapon": "wpn_astral_staff"
	}
	var fox_tex: Texture2D = SpriteDB.player_equipped_idle("fox", fox_slots)
	if fox_tex == null or fox_tex.get_width() < 256:
		_fail("狐族觀星者換裝待機圖應 >= 256，實際: %s" % (str(fox_tex.get_width()) if fox_tex else "null"))
	else:
		print("  ✓ 狐族觀星者成功回傳高清貼圖，尺寸: %dx%d" % [fox_tex.get_width(), fox_tex.get_height()])
	for f in range(4):
		var fox_walk := SpriteDB.player_equipped_walk(f, "fox", fox_slots)
		if fox_walk == null or fox_walk.get_width() < 256:
			_fail("狐族觀星者走路幀 %d 應 >= 256，實際: %s" % [f, (str(fox_walk.get_width()) if fox_walk else "null")])
	print("  ✓ 狐族觀星者走路四幀皆 >= 256 (512x512)")

	# 2. 驗證 512 合成失敗時安全退回官方立牌或 showcase 256，⛔ 絕不退回 128
	print("\n--- 檢查斷言 ②：512 合成失敗時改讀官方立牌或 showcase 256，⛔ 絕不退回 128 ---")
	var broken_slots := {
		"costume": "invalid_broken_costume",
		"chassis": "invalid_broken_chassis"
	}
	SpriteDB.clear_equipped_cache()
	var lion_fail_tex: Texture2D = SpriteDB.player_equipped_idle("lion", broken_slots)
	if lion_fail_tex == null:
		_fail("獅族換裝失敗時應退回官方立牌，不可為 null")
	elif lion_fail_tex.get_width() < 256:
		_fail("獅族換裝失敗時不可退回 128 糊圖，實際寬度: %d" % lion_fail_tex.get_width())
	else:
		print("  ✓ 獅族換裝合成失敗時安全退回官方立牌: 尺寸 = %dx%d (>=256)" % [lion_fail_tex.get_width(), lion_fail_tex.get_height()])

	SpriteDB.clear_equipped_cache()
	var rab_fail_tex: Texture2D = SpriteDB.player_equipped_idle("rabbit", broken_slots)
	if rab_fail_tex == null:
		_fail("兔族換裝失敗時應退回展示立牌，不可為 null")
	elif rab_fail_tex.get_width() < 256:
		_fail("兔族換裝失敗時不可退回 128 糊圖，實際寬度: %d" % rab_fail_tex.get_width())
	else:
		print("  ✓ 兔族換裝合成失敗時安全退回展示立牌: 尺寸 = %dx%d (>=256)" % [rab_fail_tex.get_width(), rab_fail_tex.get_height()])

	# 3. 驗證 PaperdollRenderer.get_race_composite_texture_512 失敗時不再退回 128
	print("\n--- 檢查斷言 ③：PaperdollRenderer.get_race_composite_texture_512 失敗回傳 null ---")
	var comp_fail: Texture2D = PaperdollRenderer.get_race_composite_texture_512("rabbit", broken_slots)
	if comp_fail != null and comp_fail.get_width() < 256:
		_fail("PaperdollRenderer.get_race_composite_texture_512 失敗時不准退回 128 貼圖: %d" % comp_fail.get_width())
	else:
		print("  ✓ PaperdollRenderer.get_race_composite_texture_512 失敗時不退回 128 糊圖 (回傳: %s)" % str(comp_fail))

	# 4. 驗證開局選族中央舞台 (PaperdollSelectDemo) 合成失敗時改讀立牌／512，不退回 128 模組切片
	print("\n--- 檢查斷言 ④：開局選族中央舞台合成失敗不退回 128 模組切片 ---")
	var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
	if demo_packed == null:
		_fail("無法載入 res://scenes/ui/paperdoll_select_demo.tscn")
	else:
		var demo: Node = demo_packed.instantiate()
		root.add_child(demo)
		demo.set("_current_race_id", "lion")
		demo.call("_update_stage_512", broken_slots)
		var stage_tex: Texture2D = demo.call("get_stage_texture")
		var sprite_512: Sprite2D = demo.call("get_stage_sprite_512")
		var ch: Node = demo.call("_get_character")
		var layers: CanvasItem = ch.get_node_or_null("Layers") as CanvasItem if ch else null

		if stage_tex == null or stage_tex.get_width() < 256:
			_fail("中央舞台合成失敗應改讀官方立牌 (>=256)，實際: %s" % (str(stage_tex.get_width()) if stage_tex else "null"))
		elif sprite_512 == null or sprite_512.texture_filter != CanvasItem.TEXTURE_FILTER_LINEAR:
			_fail("中央舞台立牌濾鏡必須為 LINEAR！")
		elif layers != null and layers.visible:
			_fail("中央舞台合成失敗時 layers (128 切片) 不可設為 visible！")
		else:
			print("  ✓ 中央舞台換裝失敗時改讀官方立牌且使用 LINEAR 濾鏡 (尺寸: %dx%d, 128切片層隱藏)" % [stage_tex.get_width(), stage_tex.get_height()])
		demo.queue_free()

	# 5. 驗證戰鬥場景套用狐族換裝待機貼圖
	print("\n--- 檢查斷言 ⑤：戰鬥場景載入狐族換裝待機貼圖 (>=256, LINEAR) ---")
	_gs.reset_new_game("fox")
	_gs.player_name = "靈尾狐"
	_gs.paperdoll_slots = fox_slots.duplicate()
	SpriteDB.clear_equipped_cache()

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if b_scn == null:
		_fail("無法載入 res://scenes/battle/battle.tscn")
		quit(1)
		return
	_battle = b_scn.instantiate()
	root.add_child(_battle)

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	if _step == 1:
		if _wait == 3:
			if _battle != null and _battle.has_method("setup"):
				_battle.call("setup", "wolf")
		elif _wait >= 10:
			if _battle != null:
				var player_body: TextureRect = _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
				if player_body == null or player_body.texture == null:
					_fail("戰鬥場景 PlayerBody 或貼圖為空！")
				else:
					var tex := player_body.texture
					var filter := player_body.texture_filter
					if tex.get_width() < 256:
						_fail("戰鬥場景 PlayerBody 貼圖尺寸不足 256 (為 128 糊圖): %dx%d" % [tex.get_width(), tex.get_height()])
					elif filter != CanvasItem.TEXTURE_FILTER_LINEAR:
						_fail("戰鬥場景 PlayerBody 濾鏡必須為 LINEAR，實際為: %s" % str(filter))
					else:
						print("  ✓ 戰鬥場景 PlayerBody 貼圖尺寸: %dx%d (>=256), 濾鏡: LINEAR" % [tex.get_width(), tex.get_height()])

				_battle.queue_free()
				_battle = null

			if _ok:
				print("\nEXPLORE_BATTLE_NO_128_FALLBACK_OK")
				quit(0)
			else:
				print("\nEXPLORE_BATTLE_NO_128_FALLBACK_FAIL")
				quit(1)
			return true

	return false
