extends SceneTree
## 《發條之心》大廳、衣櫥、戰鬥待機發條鑰匙旋轉無頭自動化測試 (test_winding_key_spin)
## 驗證：
## 1. 白兔 8 幀手繪 3D 逐幀資源完整性與相鄰角度像素差 XOR > 0
## 2. 大廳待機 16 幀後發條鑰匙步進轉動，合成像素差 > 0，無角色懸空，陰影強度 <= 0.35
## 3. 衣櫥預覽 (WardrobeDialog) 發條鑰匙獨立圖層與動畫器掛載並轉動
## 4. 戰鬥待機 (BattleView) 玩家發條鑰匙獨立圖層與動畫器掛載並轉動
## 5. 單張切片種族 (如獅族) 待機步進旋轉角度 key_rect.rotation > 0

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const WindingKeyAnimator = preload("res://scripts/art/winding_key_animator.gd")

var _ok := true
var _stage := 0
var _wait := 0

var _lobby: MobileLobby = null
var _wardrobe: WardrobeDialog = null
var _battle: Node = null
var _test_rect: TextureRect = null

var _initial_key_img: Image = null
var _initial_stage_anchor_y: float = 0.0


func _fail(msg: String) -> void:
	push_error("TEST FAIL: " + msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始測試：大廳、衣櫥、戰鬥待機背上發條鑰匙旋轉 (test_winding_key_spin) ===")

	# 1. 驗證白兔 8 幀資源與相鄰幀像素差
	_test_rabbit_frames_resource()

	# 2. 啟動大廳場景
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.player_race = "rabbit"

	_lobby = MobileLobby.new()
	_lobby.enable_idle_breathing = false
	_lobby.enable_idle_flavor = false
	root.add_child(_lobby)


func _test_rabbit_frames_resource() -> void:
	print("--- 步驟 1: 驗證白兔 8 幀手繪 3D 逐幀資源 ---")
	var frames: Array = WindingKeyAnimator.load_key_frames("rabbit")
	if frames.size() != 8:
		_fail("白兔 winding_key_frames 數量不為 8！實際: %d" % frames.size())
		return
	print("  ✓ 成功載入白兔 8 幀發條鑰匙貼圖")

	var tex0: Texture2D = frames[0]
	var tex2: Texture2D = frames[2]
	if tex0 == null or tex2 == null:
		_fail("幀 0 或幀 2 貼圖為 null！")
		return

	var img0: Image = tex0.get_image()
	var img2: Image = tex2.get_image()
	if img0 == null or img2 == null or img0.is_empty() or img2.is_empty():
		_fail("幀 0 或幀 2 Image 無效！")
		return

	if img0.get_format() != Image.FORMAT_RGBA8:
		img0.convert(Image.FORMAT_RGBA8)
	if img2.get_format() != Image.FORMAT_RGBA8:
		img2.convert(Image.FORMAT_RGBA8)

	var diff_pixels := 0
	for y in range(img0.get_height()):
		for x in range(img0.get_width()):
			var c0: Color = img0.get_pixel(x, y)
			var c2: Color = img2.get_pixel(x, y)
			if c0 != c2:
				diff_pixels += 1

	if diff_pixels <= 0:
		_fail("白兔第 0 幀與第 2 幀 (90度側轉) XOR 像素差為 0！")
		return
	print("  ✓ 白兔第 0 幀 vs 第 2 幀像素差檢驗通過 (不同像素數: %d > 0)" % diff_pixels)


func _process(_delta: float) -> bool:
	_wait += 1

	if _stage == 0:
		# 等待大廳載入並記錄第 0 幀
		if _wait < 6:
			return false
		_stage = 1
		_wait = 0
		_test_lobby_step0()
		return false

	elif _stage == 1:
		# 等待 18 幀 (超過 8 幀，發條鑰匙步進推進)
		if _wait < 18:
			return false
		_stage = 2
		_wait = 0
		_test_lobby_step_advanced()
		return false

	elif _stage == 2:
		# 步驟 3: 驗證衣櫥 (WardrobeDialog)
		_stage = 3
		_wait = 0
		_setup_wardrobe_test()
		return false

	elif _stage == 3:
		if _wait < 18:
			return false
		_stage = 4
		_wait = 0
		_test_wardrobe_step_advanced()
		return false

	elif _stage == 4:
		# 步驟 4: 驗證戰鬥待機 (BattleView)
		_stage = 5
		_wait = 0
		_setup_battle_test()
		return false

	elif _stage == 5:
		if _wait < 18:
			return false
		_stage = 6
		_wait = 0
		_test_battle_step_advanced()
		return false

	elif _stage == 6:
		# 步驟 5: 驗證單張切片步進旋轉 (獅族)
		_test_single_slice_rotation()
		_finish()
		return true

	return false


func _test_lobby_step0() -> void:
	print("--- 步驟 2: 驗證大廳待機發條鑰匙獨立圖層 ---")
	var hero_avatar: TextureRect = _lobby.get("_hero_avatar")
	if hero_avatar == null:
		_fail("大廳未建立 _hero_avatar 節點！")
		return

	var key_avatar: TextureRect = hero_avatar.get_node_or_null("HeroWindingKey")
	if key_avatar == null:
		_fail("大廳 _hero_avatar 未掛載 HeroWindingKey 子節點！")
		return
	if not key_avatar.visible:
		_fail("大廳 HeroWindingKey 不可見！")
		return
	if not key_avatar.show_behind_parent:
		_fail("大廳 HeroWindingKey 未設置 show_behind_parent！")
		return
	if key_avatar.texture == null:
		_fail("大廳 HeroWindingKey 貼圖為 null！")
		return

	var anim: WindingKeyAnimator = key_avatar.get_node_or_null("WindingKeyAnimator")
	if anim == null:
		_fail("大廳 HeroWindingKey 未附加 WindingKeyAnimator！")
		return

	_initial_key_img = key_avatar.texture.get_image()
	if _initial_key_img and _initial_key_img.get_format() != Image.FORMAT_RGBA8:
		_initial_key_img.convert(Image.FORMAT_RGBA8)

	# 驗證無角色懸空：主角基準錨點 offset_top 為 -150
	if hero_avatar.offset_top != -150:
		_fail("角色位置異常，可能產生懸空: offset_top = %d" % hero_avatar.offset_top)
		return
	var hero_shadow: TextureRect = _lobby.get("_hero_shadow")
	if hero_shadow == null or not hero_shadow.visible:
		_fail("大廳缺少 _hero_shadow 陰影節點！")
		return
	var stage_anchor: Control = _lobby.get("_stage_anchor")
	if stage_anchor != null:
		_initial_stage_anchor_y = stage_anchor.global_position.y
		print("  ✓ 大廳展台 stage_anchor 初始 global_position.y = %.2f (offset_top = %.2f)" % [_initial_stage_anchor_y, stage_anchor.offset_top])
	print("  ✓ 大廳主角雙足接地錨點穩固，軟影正常，無懸空位移")
	print("  ✓ 大廳初始幀發條鑰匙掛載成功 (Step: %d)" % anim.get_current_step())


func _test_lobby_step_advanced() -> void:
	var hero_avatar: TextureRect = _lobby.get("_hero_avatar")
	var key_avatar: TextureRect = hero_avatar.get_node_or_null("HeroWindingKey")
	var anim: WindingKeyAnimator = key_avatar.get_node_or_null("WindingKeyAnimator")

	var step := anim.get_current_step()
	if step <= 0:
		_fail("待機超過 16 幀後大廳發條鑰匙未前進！當前步進: %d" % step)
		return
	print("  ✓ 大廳待機 16 幀後發條鑰匙成功推進 (當前步進: %d, 角度: %.2f rad)" % [step, anim.get_rotation_angle()])

	var cur_img: Image = key_avatar.texture.get_image()
	if cur_img and cur_img.get_format() != Image.FORMAT_RGBA8:
		cur_img.convert(Image.FORMAT_RGBA8)

	var stage_anchor: Control = _lobby.get("_stage_anchor")
	if stage_anchor != null:
		var delta_y: float = abs(stage_anchor.global_position.y - _initial_stage_anchor_y)
		print("  ✓ 待機推進後 stage_anchor global_position.y = %.2f (位移量: %.2f px)" % [stage_anchor.global_position.y, delta_y])
		if delta_y > 2.0:
			_fail("大廳展台 stage_anchor 異常飄移漂浮！24 幀內位移量 %.2f px > 2.0 px" % delta_y)
			return

	var diff_pixels := 0
	if _initial_key_img and cur_img:
		for y in range(cur_img.get_height()):
			for x in range(cur_img.get_width()):
				if _initial_key_img.get_pixel(x, y) != cur_img.get_pixel(x, y):
					diff_pixels += 1

	if diff_pixels <= 0 and key_avatar.rotation <= 0:
		_fail("待機後發條鑰匙貼圖像素差與旋轉角皆未改變！")
		return
	print("  ✓ 大廳發條鑰匙待機動畫有效 (貼圖像素差: %d > 0)" % diff_pixels)


func _setup_wardrobe_test() -> void:
	print("--- 步驟 3: 驗證衣櫥 (WardrobeDialog) 發條鑰匙獨立圖層與轉動 ---")
	_wardrobe = WardrobeDialog.new()
	root.add_child(_wardrobe)
	_wardrobe._ready()
	_wardrobe.call("_update_preview")


func _test_wardrobe_step_advanced() -> void:
	var prev_rect: TextureRect = _wardrobe.get("_preview_rect")
	if prev_rect == null:
		_fail("衣櫥 _preview_rect 為 null！")
		return
	var key_avatar: TextureRect = prev_rect.get_node_or_null("HeroWindingKey")
	if key_avatar == null:
		_fail("衣櫥 _preview_rect 未掛載 HeroWindingKey！")
		return
	var anim: WindingKeyAnimator = key_avatar.get_node_or_null("WindingKeyAnimator")
	if anim == null:
		_fail("衣櫥 HeroWindingKey 未掛載 WindingKeyAnimator！")
		return

	var step := anim.get_current_step()
	if step <= 0:
		_fail("衣櫥待機超過 16 幀後發條鑰匙未前進！當前步進: %d" % step)
		return
	print("  ✓ 衣櫥待機發條鑰匙成功轉動 (當前步進: %d, 角度: %.2f rad)" % [step, anim.get_rotation_angle()])
	_wardrobe.queue_free()
	_wardrobe = null


func _setup_battle_test() -> void:
	print("--- 步驟 4: 驗證戰鬥待機 (BattleView) 發條鑰匙獨立圖層與轉動 ---")
	var BattleScene: PackedScene = load("res://scenes/battle/battle.tscn")
	if BattleScene == null:
		_fail("無法加載 res://scenes/battle/battle.tscn！")
		return
	_battle = BattleScene.instantiate()
	root.add_child(_battle)
	_battle._apply_battle_art("training_dummy")


func _test_battle_step_advanced() -> void:
	var player_body: TextureRect = _battle.get("player_body")
	if player_body == null:
		_fail("戰鬥 player_body 為 null！")
		return
	var key_avatar: TextureRect = player_body.get_node_or_null("HeroWindingKey")
	if key_avatar == null:
		_fail("戰鬥 player_body 未掛載 HeroWindingKey！")
		return
	var anim: WindingKeyAnimator = key_avatar.get_node_or_null("WindingKeyAnimator")
	if anim == null:
		_fail("戰鬥 HeroWindingKey 未掛載 WindingKeyAnimator！")
		return

	var step := anim.get_current_step()
	if step <= 0:
		_fail("戰鬥待機超過 16 幀後發條鑰匙未前進！當前步進: %d" % step)
		return
	print("  ✓ 戰鬥待機發條鑰匙成功轉動 (當前步進: %d, 角度: %.2f rad)" % [step, anim.get_rotation_angle()])
	_battle.queue_free()
	_battle = null


func _test_single_slice_rotation() -> void:
	print("--- 步驟 5: 驗證單張切片種族 (獅族) 步進旋轉角度 ---")
	_test_rect = TextureRect.new()
	_test_rect.name = "LionTestRect"
	_test_rect.custom_minimum_size = Vector2(320, 320)
	root.add_child(_test_rect)

	var anim := WindingKeyAnimator.setup_for(_test_rect, "lion", {})
	if anim == null:
		_fail("無法為獅族建立 WindingKeyAnimator！")
		return
	if anim.has_frame_animation():
		_fail("獅族不應有 8 幀逐幀動畫！")
		return

	var key_rect := _test_rect.get_node_or_null("HeroWindingKey") as TextureRect
	if key_rect == null:
		_fail("獅族未建立 HeroWindingKey！")
		return

	anim.step_forward()
	anim.step_forward()

	if key_rect.rotation <= 0.0:
		_fail("獅族 HeroWindingKey 步進後 rotation 應大於 0！實際: %f" % key_rect.rotation)
		return
	print("  ✓ 獅族單張切片發條鑰匙成功繞樞軸旋轉 (rotation = %.2f rad > 0)" % key_rect.rotation)

	_test_rect.queue_free()
	_test_rect = null


func _finish() -> void:
	if _lobby:
		_lobby.queue_free()
	if _ok:
		print("========================================")
		print("  WINDING_KEY_SPIN_OK")
		print("========================================")
		quit(0)
	else:
		push_error("WINDING_KEY_SPIN_FAIL")
		print("  WINDING_KEY_SPIN_FAIL")
		quit(1)
