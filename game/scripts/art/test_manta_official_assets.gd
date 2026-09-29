extends SceneTree
## 《發條之心》第六十七族潮汐蝠魟 (manta) 官方資產套件無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_manta_official_assets.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第六十七族潮汐蝠魟 (manta) 官方資產套件無頭驗證測試 ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("無法取得 GameState 單例")
		quit(1)
		return

	gs.set("player_race", "manta")
	if "paperdoll_slots" in gs:
		gs.paperdoll_slots = {}

	# 1. 驗證基礎 SpriteDB.player_idle()
	var idle: Texture2D = SpriteDB.player_idle()
	if idle == null:
		push_error("潮汐蝠魟 player_idle() 為 null")
		ok = false
	else:
		print("  ✓ 潮汐蝠魟基礎 idle 載入成功: %s, 尺寸: %s" % [idle.resource_path, idle.get_size()])

	# 2. 驗證 4 幀走路基礎貼圖
	for f in range(4):
		var w: Texture2D = SpriteDB.player_walk(f)
		if w == null:
			push_error("潮汐蝠魟 player_walk(%d) 為 null" % f)
			ok = false
		else:
			print("  ✓ 潮汐蝠魟基礎 walk(%d) 載入成功: %s, 尺寸: %s" % [f, w.resource_path, w.get_size()])

	# 3. 驗證 512 高清行走幀與紙娃娃動態合成
	SpriteDB.clear_equipped_cache()
	for f in range(4):
		var ew: Texture2D = SpriteDB.player_equipped_walk(f, "manta", {})
		if ew == null:
			push_error("潮汐蝠魟 player_equipped_walk(%d) 為 null" % f)
			ok = false
		elif ew.get_width() < 256 or ew.get_height() < 256:
			push_error("潮汐蝠魟 player_equipped_walk(%d) 尺寸不足 256: %dx%d" % [f, ew.get_width(), ew.get_height()])
			ok = false
		else:
			print("  ✓ 潮汐蝠魟 512 高清行走幀 frame %d 驗證合格: %dx%d" % [f, ew.get_width(), ew.get_height()])

	# 4. 驗證頭像與半身像
	var hud: Texture2D = SpriteDB.portrait_tex("manta")
	if hud == null:
		push_error("潮汐蝠魟 portrait_tex('manta') 為 null")
		ok = false
	else:
		print("  ✓ 潮汐蝠魟 HUD 戰鬥頭像載入成功: %s, 尺寸: %s" % [hud.resource_path, hud.get_size()])

	var bust: Texture2D = SpriteDB.portrait_tex("tidal_manta")
	if bust == null:
		push_error("潮汐蝠魟 portrait_tex('tidal_manta') 為 null")
		ok = false
	else:
		print("  ✓ 潮汐蝠魟 對話半身像載入成功: %s, 尺寸: %s" % [bust.resource_path, bust.get_size()])

	if ok:
		print("\n🎉 MANTA_OFFICIAL_ASSETS_TEST_OK: 潮汐蝠魟官方資產套件 Godot 引擎無頭驗證全數通過！")
		quit(0)
	else:
		push_error("\n❌ 潮汐蝠魟官方資產套件驗證有紅燈！")
		quit(1)
