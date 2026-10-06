extends SceneTree
## 大廳右側裝備槽完整可見性測試與實機截圖 (t_f523f8fa)
## 驗收標準：
## 1. 1280x720 與 1600x720 兩種橫屏實機圖，四格卡完整可見、不重疊、不穿模。
## 2. 自動測試斷言：四個 EquipSlot 的 rect 完全落在 viewport 內（含 margin >= 8px）。
## 3. 按鈕熱區 >= 48px。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _ok := true
var _target_size: Vector2i = Vector2i(1280, 720)
var _target_proof: String = "res://../proofs/lobby_equip_slots_1280x720.png"
var _frames: int = 0
var _lobby: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() >= 2:
		_target_size = Vector2i(int(args[0]), int(args[1]))
		_target_proof = "res://../proofs/lobby_equip_slots_%dx%d.png" % [_target_size.x, _target_size.y]

	var dir := DirAccess.open("res://..")
	if dir and not dir.dir_exists("proofs"):
		dir.make_dir("proofs")

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.player_race = "rabbit"

	root.size = _target_size
	var win := root.get_window()
	if win != null:
		win.size = _target_size

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	print("\n=== 開始檢測與截圖 Viewport %dx%d ===" % [_target_size.x, _target_size.y])

func _process(_delta: float) -> bool:
	_frames += 1
	if _frames < 10:
		return false

	_verify_equip_slots(_target_size)

	# 嘗試截圖存檔（在具備真實渲染器如 xvfb / opengl3 時執行）
	var vp_tex = root.get_viewport().get_texture()
	if vp_tex != null:
		var img = vp_tex.get_image()
		if img != null and not img.is_empty():
			var save_p: String = ProjectSettings.globalize_path(_target_proof)
			var err = img.save_png(save_p)
			if err == OK:
				print("  📸 實機截圖成功已存檔: %s (尺寸: %dx%d)" % [save_p, img.get_width(), img.get_height()])
			else:
				push_warning("截圖存檔失敗: %s, code=%d" % [save_p, err])
		else:
			print("  (Headless dummy 渲染環境，略過截圖檔案輸出)")
	else:
		print("  (Headless dummy 渲染環境，略過截圖檔案輸出)")

	return _finish()

func _verify_equip_slots(vp_size: Vector2i) -> void:
	var equip_schematic: Control = _lobby.get("_equip_schematic") as Control
	if equip_schematic == null:
		equip_schematic = _find_named(_lobby, "EquipSchematic") as Control

	if equip_schematic == null:
		_fail("找不到 EquipSchematic 節點")
		return

	var slots: Array[Control] = []
	for c in equip_schematic.get_children():
		if c is Control and c.visible:
			slots.append(c)

	print("  ✓ 找到 EquipSchematic 裝備槽容器，顯示中槽位數量: %d" % slots.size())
	if slots.size() != 4:
		_fail("裝備槽數量應為 4，實際為 %d" % slots.size())
		return

	var rects: Array[Rect2] = []
	for slot in slots:
		var r: Rect2 = Rect2(slot.global_position, slot.size)
		rects.append(r)

		# 1. 熱區 >= 48px
		if r.size.x < 48.0 or r.size.y < 48.0:
			_fail("裝備槽 %s 熱區不足 48px: %s" % [slot.name, r.size])
		else:
			print("  ✓ 裝備槽 %s 熱區達標: %.1fx%.1f (>= 48px)" % [slot.name, r.size.x, r.size.y])

		# 2. 完全落在 viewport 內 (含 margin >= 8px)
		var m_left: float = r.position.x
		var m_top: float = r.position.y
		var m_right: float = float(vp_size.x) - r.end.x
		var m_bottom: float = float(vp_size.y) - r.end.y

		if m_left < 8.0:
			_fail("裝備槽 %s 左邊距不足 8px: %.1f" % [slot.name, m_left])
		if m_top < 8.0:
			_fail("裝備槽 %s 頂部邊距不足 8px: %.1f" % [slot.name, m_top])
		if m_right < 8.0:
			_fail("裝備槽 %s 右邊距不足 8px (超出或切邊): %.1f" % [slot.name, m_right])
		if m_bottom < 8.0:
			_fail("裝備槽 %s 底部邊距不足 8px: %.1f" % [slot.name, m_bottom])

		if m_left >= 8.0 and m_top >= 8.0 and m_right >= 8.0 and m_bottom >= 8.0:
			print("  ✓ 裝備槽 %s 完全落在 viewport 內，安全邊距達標: L=%.1f, R=%.1f, T=%.1f, B=%.1f (全部 >= 8px)" % [slot.name, m_left, m_right, m_top, m_bottom])

	# 3. 四格裝備卡互不重疊
	for i in range(slots.size()):
		for j in range(i + 1, slots.size()):
			var inter: Rect2 = rects[i].intersection(rects[j])
			if inter.size.x > 0.01 and inter.size.y > 0.01:
				_fail("裝備槽 %s 與 %s 發生重疊! intersection: %s" % [slots[i].name, slots[j].name, inter])
			else:
				print("  ✓ 裝備槽 %s 與 %s 互不重疊" % [slots[i].name, slots[j].name])

	# 4. 與右側戰情報告板互不重疊
	var sortie_card: Control = _find_named(_lobby, "RightSortieCard") as Control
	if sortie_card != null and sortie_card.visible:
		var sortie_rect: Rect2 = Rect2(sortie_card.global_position, sortie_card.size)
		for slot in slots:
			var r: Rect2 = Rect2(slot.global_position, slot.size)
			var inter: Rect2 = r.intersection(sortie_rect)
			if inter.size.x > 0.01 and inter.size.y > 0.01:
				_fail("裝備槽 %s 與 RightSortieCard 發生重疊! intersection: %s" % [slot.name, inter])
		print("  ✓ 四格裝備槽與右側戰情報告板 (RightSortieCard) 互不重疊")

func _find_named(n: Node, target_name: String) -> Node:
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null

func _finish() -> bool:
	if _ok:
		print("\n🎉 LOBBY_EQUIP_SLOTS_VISIBLE_OK (%dx%d): 全部安全距與無切邊斷言通過！\n" % [_target_size.x, _target_size.y])
		quit(0)
	else:
		push_error("LOBBY_EQUIP_SLOTS_VISIBLE_FAIL")
		quit(1)
	return true
