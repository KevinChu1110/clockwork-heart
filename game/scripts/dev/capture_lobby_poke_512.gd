extends SceneTree
## 《發條之心》大廳戳碰 512 戰鬥姿態實機截圖產生器 (xvfb 1280x720)
## 驗證兔族與獅族戳中揮劍 (act_type 0: attack) 走 512 高清貼圖與 LINEAR 濾鏡

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生大廳戳碰 512 實機截圖 (xvfb 1280x720) ===")
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
	await _wait_frames(5)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		push_error("找不到 GameState 節點")
		quit(1)
		return

	# ── 1. 兔族戳中揮劍 (attack) ──
	_gs.player_race = "rabbit"
	_gs.player_name = "小白"
	_gs.chapter = "c0"
	_gs.paperdoll_slots = {}

	_lobby = MobileLobby.new()
	_lobby.enable_idle_breathing = false
	_lobby.enable_idle_flavor = false
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)

	await _wait_frames(10)
	print(">>> [兔族] 觸發戳碰揮劍 (act_type 0)...")
	_lobby._on_hero_clicked(0)
	await _wait_frames(6)

	var rabbit_avatar: TextureRect = _lobby.get("_hero_avatar")
	if rabbit_avatar:
		var tex := rabbit_avatar.texture
		print("  [兔族戳中] 貼圖: %s, 尺寸: %s, 濾鏡: %d (0=INHERIT, 1=NEAREST, 2=LINEAR)" % [
			tex.resource_path if tex else "null",
			str(tex.get_size()) if tex else "null",
			rabbit_avatar.texture_filter
		])

	await _capture_frame("proof_lobby_poke_rabbit_attack_512.png")

	# 等待恢復
	await _wait_frames(60)

	# ── 2. 獅族戳中揮劍 (attack) ──
	_gs.player_race = "lion"
	_gs.player_name = "辛巴"
	_gs.paperdoll_slots = {}
	_lobby._load_hero_poses()
	_lobby._restore_hero_idle()

	await _wait_frames(10)
	print(">>> [獅族] 觸發戳碰揮劍 (act_type 0)...")
	_lobby._on_hero_clicked(0)
	await _wait_frames(6)

	var lion_avatar: TextureRect = _lobby.get("_hero_avatar")
	if lion_avatar:
		var tex := lion_avatar.texture
		print("  [獅族戳中] 貼圖: %s, 尺寸: %s, 濾鏡: %d (0=INHERIT, 1=NEAREST, 2=LINEAR)" % [
			tex.resource_path if tex else "null",
			str(tex.get_size()) if tex else "null",
			lion_avatar.texture_filter
		])

	await _capture_frame("proof_lobby_poke_lion_attack_512.png")

	print("=== 大廳戳碰 512 截圖完成 ===")
	quit(0)
