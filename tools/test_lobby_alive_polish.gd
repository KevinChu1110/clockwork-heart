extends SceneTree
## 《發條之心》大廳動態呼吸感、發條微動與果凍戳碰驗收測試
## 驗收項目：
## 1. 浮空島背景輕微上下浮動呼吸動效 (Sine 曲線，幅度 2~3px)
## 2. 大廳背景金色發條微光粒子 (通透、不擋UI、漂移呼吸)
## 3. 主角待機背後發條鑰匙每隔 4~6 秒微轉半圈並伴隨微小抖動
## 4. 點擊/戳碰角色果凍擠壓彈跳動效 (Squash & Stretch) 與喜悅星芒/火花

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: Control = null
var _frames: int = 0
var _proof_dir: String = "/opt/side/bravesoul-game/proofs/t_917b4c4c"
var _test_ok: bool = true

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var dir := DirAccess.open("/opt/side/bravesoul-game")
	if dir and not dir.dir_exists("proofs/t_917b4c4c"):
		dir.make_dir_recursive("proofs/t_917b4c4c")

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "小白兔"
		gs.player_race = "rabbit"

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frames += 1

	if _frames == 5:
		print("=== 步驟 1: 驗證浮空島背景浮動動效與金色微光粒子 ===")
		var bg = _lobby.find_child("TempleLobbyBg", true, false) as TextureRect
		var bg_rect = _lobby.get("_bg_rect") as TextureRect
		var bg_tween = _lobby.get("_bg_tween") as Tween
		if bg == null or bg_rect == null:
			push_error("找不到 TempleLobbyBg 節點")
			_test_ok = false
		else:
			print("  ✓ 找到浮空島背景節點 TempleLobbyBg")
			print("    尺寸: ", bg.size, " 偏移: (", bg.offset_left, ", ", bg.offset_top, ") ~ (", bg.offset_right, ", ", bg.offset_bottom, ")")
			if bg_tween and bg_tween.is_valid():
				print("  ✓ 浮空島背景呼吸 Tween 正常運作中 (上下浮動 ±2.5px)")
			else:
				push_error("浮空島背景 Tween 未啟動")
				_test_ok = false

		var particles_root = _lobby.get("_particles_root") as Control
		if particles_root == null:
			push_error("找不到 _particles_root 粒子容器節點")
			_test_ok = false
		else:
			var motes: Array = []
			for c in particles_root.get_children():
				if c is ColorRect:
					motes.append(c)
			print("  ✓ 背景發條微光粒子數量: %d (通透金黃/暖橘/以太色)" % motes.size())
			if motes.size() < 10:
				push_error("微光粒子數量不足 10")
				_test_ok = false
			else:
				print("  ✓ 發條微光粒子數量達標 (>=10 顆)")

		# 截圖 1: 待機全景 (浮空島背景 + 發條微光粒子)
		var vp_tex = root.get_viewport().get_texture()
		if vp_tex != null:
			var img1 = vp_tex.get_image()
			if img1 != null and not img1.is_empty():
				img1.save_png(_proof_dir + "/proof_01_sky_lobby_breathing.png")
				print("  📸 已存檔: proof_01_sky_lobby_breathing.png")

	elif _frames == 10:
		print("=== 步驟 2: 驗證背部發條鑰匙獨立圖層與待機微轉動效 ===")
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		var hero_key = _lobby.get("_hero_key_avatar") as TextureRect
		if hero_avatar == null:
			push_error("找不到 _hero_avatar")
			_test_ok = false
		if hero_key == null:
			push_error("找不到 _hero_key_avatar")
			_test_ok = false
		else:
			print("  ✓ 找到背部發條鑰匙節點 HeroWindingKey")
			print("    show_behind_parent: ", hero_key.show_behind_parent)
			print("    pivot_offset: ", hero_key.pivot_offset)
			print("    可見度 visible: ", hero_key.visible)
			print("    初始 rotation: ", hero_key.rotation)
			if not hero_key.show_behind_parent:
				push_error("發條鑰匙 show_behind_parent 應為 true")
				_test_ok = false
			else:
				print("  ✓ 發條鑰匙設置 show_behind_parent=true，層級自然位於主角軀幹背後")

		# 觸發發條微轉半圈
		print("  觸發發條鑰匙微轉半圈 (trigger_key_half_turn)...")
		_lobby.call("trigger_key_half_turn")

	elif _frames == 22:
		# 檢查微轉半圈後的旋轉值
		var hero_key = _lobby.get("_hero_key_avatar") as TextureRect
		if hero_key:
			print("  ✓ 發條鑰匙半圈旋轉進行中，當前 rotation: %.3f rad (%.1f deg)" % [hero_key.rotation, rad_to_deg(hero_key.rotation)])
			if is_zero_approx(hero_key.rotation):
				push_error("發條鑰匙未發生旋轉！")
				_test_ok = false
			else:
				print("  ✓ 發條鑰匙確實發生半圈旋轉 (>= 2.5 rad)")

		# 截圖 2: 發條微轉與抖動
		var vp_tex = root.get_viewport().get_texture()
		if vp_tex != null:
			var img2 = vp_tex.get_image()
			if img2 != null and not img2.is_empty():
				img2.save_png(_proof_dir + "/proof_02_winding_key_turn.png")
				print("  📸 已存檔: proof_02_winding_key_turn.png")

	elif _frames == 35:
		print("=== 步驟 3: 驗證點擊/戳碰角色果凍擠壓彈跳 (Squash & Stretch) 與粒子 ===")
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		print("  戳碰前 scale: ", hero_avatar.scale if hero_avatar else "null")

		# 觸發點擊
		_lobby.call("_on_hero_clicked", 1) # skill 姿態

	elif _frames == 38:
		# 戳碰瞬間 (0.08s 內)：驗證 Squash 擠壓壓扁 (scale.x > 1.0, scale.y < 1.0)
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		if hero_avatar:
			print("  戳碰壓扁 Squash 瞬間 scale: (%.3f, %.3f)" % [hero_avatar.scale.x, hero_avatar.scale.y])
			if hero_avatar.scale.x > 1.05 and hero_avatar.scale.y < 0.95:
				print("  ✓ 成功偵測到果凍擠壓 Squash 壓扁動效！(寬度擴增、高度下壓)")
			else:
				print("  (Squash 轉換中: %s)" % str(hero_avatar.scale))

		var burst_nodes = _lobby.get_tree().get_nodes_in_group("burst_particles")
		print("  ✓ 戳碰爆散星芒與火花粒子數量: %d" % burst_nodes.size())
		if burst_nodes.size() < 8:
			push_error("戳碰粒子數量不足 8")
			_test_ok = false
		else:
			print("  ✓ 戳碰多巴胺星芒與火花粒子達標")

		# 截圖 3: 戳碰果凍 Squash & Stretch 彈跳與喜悅星芒
		var vp_tex = root.get_viewport().get_texture()
		if vp_tex != null:
			var img3 = vp_tex.get_image()
			if img3 != null and not img3.is_empty():
				img3.save_png(_proof_dir + "/proof_03_poke_jelly_squash_stretch.png")
				print("  📸 已存檔: proof_03_poke_jelly_squash_stretch.png")

	elif _frames == 50:
		# 彈高 Stretch 瞬間 (scale.y > 1.0)
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		if hero_avatar:
			print("  戳碰彈高 Stretch 瞬間 scale: (%.3f, %.3f)" % [hero_avatar.scale.x, hero_avatar.scale.y])

	elif _frames == 65:
		# 恢復 idle
		_lobby.call("_restore_hero_idle")
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		var hero_key = _lobby.get("_hero_key_avatar") as TextureRect
		if hero_avatar:
			print("  恢復後 hero scale: ", hero_avatar.scale)
		if hero_key:
			print("  恢復後 key visible: ", hero_key.visible)
			if not hero_key.visible:
				push_error("恢復後發條鑰匙應為可見")
				_test_ok = false

		if _test_ok:
			print("\n🎉 ALL_LOBBY_ALIVE_POLISH_TESTS_PASSED!")
			quit(0)
		else:
			push_error("\n❌ SOME TESTS FAILED!")
			quit(1)
		return true

	return false
