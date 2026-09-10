extends SceneTree
## 《發條之心》大廳戳碰換裝還原實機截圖產生器 (xvfb 驗證用)
## 依據任務規範：
## 1. 兩套外裝 (外裝 A: 胡桃鉗+象牙白+發條鴿 / 外裝 B: 皇家巡遊+午夜藍+蒸汽排氣管)
## 2. 每套各截三張 1280x720 完整畫面原圖：
##    - proof_lobby_poke_<a|b>_before.png (戳前待機)
##    - proof_lobby_poke_<a|b>_during.png (戳中動作)
##    - proof_lobby_poke_<a|b>_after.png (戳後待機)
## 3. 驗證戳後還原為當前裝備之 SpriteDB.player_equipped_idle

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生大廳戳碰換裝還原實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p := _out_dir.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ 成功存證截圖: ", p)
		else:
			push_error("截圖失敗: %s" % p)


func _run_captures() -> void:
	await _wait_frames(3)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "小白"
		_gs.chapter = "c0"
		# 第一套外裝：胡桃鉗近衛軍裝 + 象牙白塗裝 + 發條白鴿
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"back_curio": "curio_clockwork_pigeon",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	_lobby = MobileLobby.new()
	# 關閉自動背景隨機伸展與呼吸浮動，鎖定基準 Vector2.ONE 姿態以進行像素級 diff 檢驗
	_lobby.enable_idle_breathing = false
	_lobby.enable_idle_flavor = false
	root.add_child(_lobby)
	_lobby._ready()

	# ── 外裝 A: 胡桃鉗近衛軍裝 ──
	await _wait_frames(10)
	print(">>> [外裝 A: 胡桃鉗] 截取戳前待機畫面...")
	await _capture_frame("proof_lobby_poke_a_before.png")

	print(">>> [外裝 A: 胡桃鉗] 觸發戳碰動作 (attack 姿態)...")
	_lobby._on_hero_clicked(0)
	await _wait_frames(8)
	print(">>> [外裝 A: 胡桃鉗] 截取戳中動作畫面...")
	await _capture_frame("proof_lobby_poke_a_during.png")

	# 等待戳碰動作結束並回到 equipped idle (動作長度 60 幀 = 1.0s，等待 70 幀確保還原完畢)
	await _wait_frames(70)
	print(">>> [外裝 A: 胡桃鉗] 截取戳後還原待機畫面...")
	await _capture_frame("proof_lobby_poke_a_after.png")

	# ── 外裝 B: 皇家巡遊金屬禮服 + 午夜深藍塗裝 + 蒸汽排氣管 ──
	print(">>> 切換外裝為 [外裝 B: 皇家巡遊金屬禮服]...")
	if _gs:
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_royal_parade",
			"chassis": "paint_midnight_navy",
			"back_curio": "curio_steam_exhaust",
			"costume_id": "costume_royal_parade",
			"paint_id": "paint_midnight_navy"
		}
	_lobby._load_hero_poses()

	await _wait_frames(10)
	print(">>> [外裝 B: 皇家巡遊] 截取戳前待機畫面...")
	await _capture_frame("proof_lobby_poke_b_before.png")

	print(">>> [外裝 B: 皇家巡遊] 觸發戳碰動作 (attack 姿態)...")
	_lobby._on_hero_clicked(0)
	await _wait_frames(8)
	print(">>> [外裝 B: 皇家巡遊] 截取戳中動作畫面...")
	await _capture_frame("proof_lobby_poke_b_during.png")

	await _wait_frames(70)
	print(">>> [外裝 B: 皇家巡遊] 截取戳後還原待機畫面...")
	await _capture_frame("proof_lobby_poke_b_after.png")

	print("=== 六張實機截圖全部完成 ===")
	quit(0)
