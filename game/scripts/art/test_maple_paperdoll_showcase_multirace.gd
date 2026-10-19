extends SceneTree
## 《發條之心》MaplePaperdollShowcase 多族即時切換與骨骼錨點聯動實機驗證測試
## 執行方式：xvfb-run -a godot --path game -s res://scripts/art/test_maple_paperdoll_showcase_multirace.gd

var _frame: int = 0
var _showcase: MaplePaperdollShowcase = null
var _out_dir: String = ""
var _proofs_dir: String = ""
var _errors: Array[String] = []


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://assets/sprites/player/paperdoll/showcase")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_proofs_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/t_d7d5ff53")
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	print("=== 開始 MaplePaperdollShowcase 多族即時切換與骨骼錨點聯動實機測試 ===")

	var scn: PackedScene = load("res://scenes/art/maple_paperdoll_showcase.tscn")
	if scn == null:
		push_error("無法載入 maple_paperdoll_showcase.tscn")
		quit(1)
		return

	_showcase = scn.instantiate() as MaplePaperdollShowcase
	root.add_child(_showcase)


func _process(_delta: float) -> bool:
	_frame += 1

	match _frame:
		12:
			print("\n--- 1. 驗證首發發條白兔初始狀態與骨骼錨點 ---")
			_assert(_showcase.current_race == "rabbit", "初始種族應為白兔")
			var doll = _showcase.paperdoll
			_assert(doll != null, "紙娃娃節點不應為空")
			_assert(doll.get_anchor_base_position("neck") == Vector2(248, 290), "白兔 neck 基準座標應為 (248, 290)")
			_assert(doll.get_anchor_base_position("navel") == Vector2(256, 350), "白兔 navel 基準座標應為 (256, 350)")
			_assert(doll.get_anchor_base_position("hand") == Vector2(320, 440), "白兔 hand 基準座標應為 (320, 440)")
			_assert(doll.get_anchor_base_position("back_key") == Vector2(190, 296), "白兔 back_key 基準座標應為 (190, 296)")
			_assert(doll.get_anchor_base_position("brow") == Vector2(2, -60), "白兔 brow 相對 neck 座標應為 (2, -60)")
			_assert(abs(doll.node_neck.position.y - 290.0) <= 1.0, "白兔 neck 呼吸動態應在振幅內")
			_save_screenshot("proof_01_showcase_rabbit.png")
			print("  ✓ 白兔初始骨骼錨點與展示介面驗證通過")

			# 切換至赤狐
			print("\n--- 2. 觸發切換種族至「熾火赤狐」---")
			_showcase.select_race("fox")

		28:
			print("--- 2.1 驗證赤狐即時載入、骨骼錨點連動與專屬部件 ---")
			_assert(_showcase.current_race == "fox", "當前種族應切換為赤狐")
			var doll = _showcase.paperdoll
			_assert(doll.get_anchor_base_position("neck") == Vector2(260, 255), "赤狐 neck 基準座標應為 (260, 255)")
			_assert(doll.get_anchor_base_position("navel") == Vector2(256, 350), "赤狐 navel 基準座標應為 (256, 350)")
			_assert(doll.get_anchor_base_position("hand") == Vector2(358, 363), "赤狐 hand 基準座標應為 (358, 363)")
			_assert(doll.get_anchor_base_position("back_key") == Vector2(370, 280), "赤狐 back_key 基準座標應為 (370, 280)")
			_assert(doll.get_anchor_base_position("brow") == Vector2(0, -60), "赤狐 brow 相對 neck 座標應為 (0, -60)")
			_assert(abs(doll.node_neck.position.y - 255.0) <= 1.0, "赤狐 neck 呼吸動態應在振幅內")
			_assert(doll.get_part_item("costume") == "costume_astral_cape", "赤狐預設外裝應為 costume_astral_cape")
			_assert(doll.get_part_item("weapon") == "wpn_astral_staff", "赤狐預設武器應為 wpn_astral_staff")
			_save_screenshot("proof_02_showcase_fox.png")
			print("  ✓ 赤狐骨骼錨點與專屬星相外觀即時切換驗證通過")

			# 切換至雄獅
			print("\n--- 3. 觸發切換種族至「烈金雄獅」---")
			_showcase.select_race("lion")

		44:
			print("--- 3.1 驗證雄獅即時載入、含 tail 骨骼錨點連動與重裝外觀 ---")
			_assert(_showcase.current_race == "lion", "當前種族應切換為雄獅")
			var doll = _showcase.paperdoll
			_assert(doll.get_anchor_base_position("neck") == Vector2(250, 274), "雄獅 neck 基準座標應為 (250, 274)")
			_assert(doll.get_anchor_base_position("navel") == Vector2(256, 348), "雄獅 navel 基準座標應為 (256, 348)")
			_assert(doll.get_anchor_base_position("hand") == Vector2(144, 320), "雄獅 hand 基準座標應為 (144, 320)")
			_assert(doll.get_anchor_base_position("back_key") == Vector2(342, 296), "雄獅 back_key 基準座標應為 (342, 296)")
			_assert(doll.get_anchor_base_position("brow") == Vector2(-22, -101), "雄獅 brow 相對 neck 座標應為 (-22, -101)")
			_assert(is_instance_valid(doll.node_tail), "雄獅應具備 tail 錨點節點")
			_assert(doll.get_anchor_base_position("tail") == Vector2(360, 380), "雄獅 tail 基準座標應為 (360, 380)")
			_assert(abs(doll.node_neck.position.y - 274.0) <= 1.0, "雄獅 neck 呼吸動態應在振幅內")
			_assert(doll.get_part_item("costume") == "costume_royal_guard", "雄獅預設外裝應為 costume_royal_guard")
			_assert(doll.get_part_item("weapon") == "wpn_knight_lance", "雄獅預設武器應為 wpn_knight_lance")
			_assert(doll.get_part_item("back_curio") == "curio_lion_fan_tail", "雄獅預設背飾應為 curio_lion_fan_tail")
			_save_screenshot("proof_03_showcase_lion.png")
			print("  ✓ 雄獅骨骼錨點與重裝禁衛外觀即時切換驗證通過")

			# 進行雄獅部件置換與 Z-Order 調控
			print("\n--- 4. 驗證雄獅部件自由置換與動態 Z-Order ---")
			_showcase.select_costume("costume_steam_artisan")
			_showcase.select_eyes("eyes_cyan_emerald")
			_showcase.toggle_weapon_z_order()
			_showcase.toggle_key_z_order()

		60:
			print("--- 4.1 驗證雄獅置換後的外觀與 Z-Order 層級 ---")
			var doll = _showcase.paperdoll
			_assert(doll.get_part_item("costume") == "costume_steam_artisan", "雄獅外裝應換為工匠套裝")
			_assert(doll.get_part_item("eyes") == "eyes_cyan_emerald", "雄獅面部光學應換為天青祖母綠")
			_assert(doll.get_part_z_index("weapon") == 4, "雄獅武器 Z-index 應切換至 4 (背持)")
			_assert(doll.get_part_z_index("winding_key") == 15, "雄獅發條鑰匙 Z-index 應切換至 15 (前方立體)")
			_save_screenshot("proof_04_showcase_lion_customized.png")
			print("  ✓ 雄獅部件置換與 Z-Order 動態控制驗證通過")

			# 切換回白兔
			print("\n--- 5. 觸發無縫切換回「發條白兔」---")
			_showcase.select_race("rabbit")

		76:
			print("--- 5.1 驗證無縫切回白兔且零殘留 ---")
			_assert(_showcase.current_race == "rabbit", "當前種族應恢復為白兔")
			var doll = _showcase.paperdoll
			_assert(doll.get_anchor_base_position("neck") == Vector2(248, 290), "白兔 neck 基準座標應恢復 (248, 290)")
			_assert(doll.get_anchor_base_position("navel") == Vector2(256, 350), "白兔 navel 基準座標應恢復 (256, 350)")
			_assert(doll.get_part_item("back_curio") in ["none", ""], "白兔應無殘留背飾扇尾")
			_save_screenshot("proof_05_showcase_rabbit_returned.png")
			print("  ✓ 無縫切回白兔且骨骼與部件完全復原")

		82:
			print("\n=======================================================")
			if _errors.is_empty():
				print("MAPLE_SHOWCASE_MULTIRACE_OK: 所有多族切換與骨骼錨點聯動測試 100% 通過！")
				quit(0)
			else:
				print("MAPLE_SHOWCASE_MULTIRACE_FAILED: 發現以下錯誤：")
				for err in _errors:
					print("  ✗ ", err)
				quit(1)

	return false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		push_error("斷言失敗: " + msg)
		_errors.append(msg)


func _save_screenshot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		var path1 := _out_dir.path_join(filename)
		img.save_png(path1)
		var path2 := _proofs_dir.path_join(filename)
		img.save_png(path2)
		print("  [截圖存證] 已輸出: ", path1, " 及 ", path2)
	else:
		push_error("無法截取 Viewport 圖像: " + filename)
		_errors.append("無法截取 Viewport 圖像: " + filename)
