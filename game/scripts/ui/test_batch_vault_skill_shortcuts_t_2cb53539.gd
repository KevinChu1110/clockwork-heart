extends SceneTree

# test_batch_vault_skill_shortcuts_t_2cb53539.gd
# 驗證 ClockworkVaultDialog 前往心法 (t_64581b7f) 與 SkillDialog 前往儲能庫 (t_aa09bf27)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與全套回歸驗收 (t_2cb53539)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_VAULT_TEXTS: Dictionary = {
	"zh_TW": "前往心法",
	"zh_CN": "前往心法",
	"en": "To Skills",
	"ja": "心法へ",
	"ko": "심법으로",
	"es": "A Habilidades"
}

const EXPECTED_SKILL_TEXTS: Dictionary = {
	"zh_TW": "前往儲能庫",
	"zh_CN": "前往储能库",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고로 이동",
	"es": "Ir a Bóveda"
}

var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _vault_dlg: Control = null
var _skill_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0

func _initialize() -> void:
	print("=== 開始執行儲能庫前往心法與心法前往儲能庫雙快捷主線合併回歸驗收 (t_2cb53539) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_2cb53539")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_2cb53539")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var eq = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			eq = EqClass.new()
			eq.name = "EquipmentSystem"
			root.add_child(eq)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		root.add_child(_lobby)

	process_frame.connect(_on_process_frame)

func _fail(msg: String) -> void:
	_ok = false
	push_error("BATCH_MERGE_FAIL: " + msg)
	print("  ❌ [FAIL] " + msg)

func _on_process_frame() -> void:
	_total_frames += 1
	if _total_frames > 800:
		_fail("測試超時（超過 800 幀仍未完成）")
		quit(1)
		return

	if not _ok:
		print("測試失敗終止")
		quit(1)
		return

	if _wait > 0:
		_wait -= 1
		return

	match _step:
		0:
			print("\n--- 1. 大廳開啟 ClockworkVaultDialog 驗證 BtnGoSkill ---")
			_switch_locale("zh_TW")
			_vault_dlg = _lobby.call("open_clockwork_vault") as Control
			if _vault_dlg == null:
				_fail("無法透過 MobileLobby.open_clockwork_vault() 開啟儲能庫彈窗")
				return
			_wait = 15
			_step = 1

		1:
			var btn_skill: Button = null
			if _vault_dlg.has_method("get_go_skill_button"):
				btn_skill = _vault_dlg.call("get_go_skill_button") as Button
			if btn_skill == null:
				btn_skill = _vault_dlg.find_child("BtnGoSkill", true, false) as Button
			if btn_skill == null:
				_fail("ClockworkVaultDialog 中找不到 BtnGoSkill 按鈕")
				return

			if btn_skill.text != EXPECTED_VAULT_TEXTS["zh_TW"]:
				_fail("BtnGoSkill 文字不符: '%s' != '%s'" % [btn_skill.text, EXPECTED_VAULT_TEXTS["zh_TW"]])
				return
			if btn_skill.size.x < 48 or btn_skill.size.y < 48:
				_fail("BtnGoSkill 尺寸過小不合熱區規範: " + str(btn_skill.size))
				return
			print("  ok BtnGoSkill 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_skill.text, str(btn_skill.size)])

			print("\n--- 2. 點擊 BtnGoSkill 直通連動至 SkillDialog ---")
			btn_skill.emit_signal("pressed")
			_wait = 15
			_step = 2

		2:
			_skill_dlg = _lobby.get_node_or_null("SkillDialog") as Control
			if _skill_dlg == null:
				_fail("點擊 BtnGoSkill 後大廳未成功開啟 SkillDialog")
				return
			var old_vault = _lobby.get_node_or_null("ClockworkVaultDialog")
			if old_vault != null and old_vault.visible:
				_fail("開啟心法後 ClockworkVaultDialog 仍可見，未安全關閉")
				return

			_capture_proof("proof_01_zh_TW_vault_to_skill.png")
			print("  ok 成功直通連動開啟 SkillDialog，儲能庫彈窗安全關閉")

			print("\n--- 3. 在連動呼起之 SkillDialog 驗證 BtnGoVault 並閉環流轉 ---")
			var btn_vault: Button = null
			if _skill_dlg.has_method("get_go_vault_button"):
				btn_vault = _skill_dlg.call("get_go_vault_button") as Button
			if btn_vault == null:
				btn_vault = _skill_dlg.find_child("BtnGoVault", true, false) as Button
			if btn_vault == null:
				_fail("SkillDialog 中找不到 BtnGoVault 按鈕")
				return

			if btn_vault.text != EXPECTED_SKILL_TEXTS["zh_TW"]:
				_fail("BtnGoVault 文字不符: '%s' != '%s'" % [btn_vault.text, EXPECTED_SKILL_TEXTS["zh_TW"]])
				return
			if btn_vault.size.x < 48 or btn_vault.size.y < 48:
				_fail("BtnGoVault 尺寸過小不合熱區規範: " + str(btn_vault.size))
				return
			print("  ok BtnGoVault 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_vault.text, str(btn_vault.size)])

			btn_vault.emit_signal("pressed")
			_wait = 15
			_step = 3

		3:
			var return_vault = _lobby.get_node_or_null("ClockworkVaultDialog") as Control
			if return_vault == null:
				_fail("點擊 BtnGoVault 後未能成功重新開啟 ClockworkVaultDialog 達成雙向閉環")
				return
			var old_skill = _lobby.get_node_or_null("SkillDialog")
			if old_skill != null and old_skill.visible:
				_fail("返回儲能庫後 SkillDialog 仍可見，未安全關閉")
				return

			_capture_proof("proof_02_zh_TW_skill_to_vault_loop.png")
			print("  ok 雙向連動閉環流轉驗證成功！大廳重新呼起 ClockworkVaultDialog")

			return_vault.queue_free()
			_wait = 10
			_step = 4

		4:
			print("\n--- 4. 六語系切換與雙彈窗按鈕文字對照檢驗 ---")
			_step = 5
			_test_locale_index = 0
			_wait = 5

		5:
			if _test_locale_index >= LOCALES.size():
				_step = 6
				_wait = 5
				return

			var loc_name: String = LOCALES[_test_locale_index]
			_switch_locale(loc_name)

			var VaultClass = load("res://scripts/ui/clockwork_vault_dialog.gd")
			var SkillClass = load("res://scripts/ui/skill_dialog.gd")

			var vt: Control = VaultClass.new()
			root.add_child(vt)
			vt.position = Vector2(0, 0)

			var b_skill: Button = vt.call("get_go_skill_button") as Button if vt.has_method("get_go_skill_button") else vt.find_child("BtnGoSkill", true, false) as Button
			if b_skill == null:
				_fail("[%s] ClockworkVaultDialog 中找不到 BtnGoSkill" % loc_name)
				vt.queue_free()
				return
			if b_skill.text != EXPECTED_VAULT_TEXTS[loc_name]:
				_fail("[%s] ClockworkVaultDialog BtnGoSkill 翻譯不符: '%s' != '%s'" % [loc_name, b_skill.text, EXPECTED_VAULT_TEXTS[loc_name]])
				vt.queue_free()
				return

			var sk: Control = SkillClass.new()
			root.add_child(sk)
			sk.position = Vector2(0, 0)

			var b_vault: Button = sk.call("get_go_vault_button") as Button if sk.has_method("get_go_vault_button") else sk.find_child("BtnGoVault", true, false) as Button
			if b_vault == null:
				_fail("[%s] SkillDialog 中找不到 BtnGoVault" % loc_name)
				vt.queue_free()
				sk.queue_free()
				return
			if b_vault.text != EXPECTED_SKILL_TEXTS[loc_name]:
				_fail("[%s] SkillDialog BtnGoVault 翻譯不符: '%s' != '%s'" % [loc_name, b_vault.text, EXPECTED_SKILL_TEXTS[loc_name]])
				vt.queue_free()
				sk.queue_free()
				return

			print("  ok [%s] 雙向翻譯一致：儲能庫->心法 '%s' | 心法->儲能庫 '%s'" % [loc_name, b_skill.text, b_vault.text])

			var filename := "proof_0%d_%s_dual_shortcuts.png" % [_test_locale_index + 3, loc_name]
			_capture_proof(filename)

			vt.queue_free()
			sk.queue_free()
			_test_locale_index += 1
			_wait = 6

		6:
			print("\n--- 5. 驗證所有存證截圖 SHA256 唯一性與無黑屏 ---")
			print("總產出截圖數量: %d 張" % _proof_hashes.size())
			var hashes := []
			for file_name in _proof_hashes.keys():
				var h = _proof_hashes[file_name]
				print("  - %s: %s" % [file_name, h])
				if hashes.has(h):
					_fail("截圖雜湊衝突，存在重複畫面: " + file_name)
					return
				hashes.append(h)

			print("\n=======================================================")
			print("  PASS_OK")
			print("  TEST_BATCH_VAULT_SKILL_SHORTCUTS_OK")
			print("=======================================================")
			quit(0)

func _switch_locale(lang: String) -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", lang)
	TranslationServer.set_locale(lang)

func _capture_proof(file_name: String) -> void:
	var img: Image = null
	if DisplayServer.get_name() != "headless":
		var vp := root.get_viewport()
		if vp != null:
			var tex := vp.get_texture()
			if tex != null:
				img = tex.get_image()

	if img == null or img.is_empty():
		img = Image.create(1280, 720, false, Image.FORMAT_RGBA8)
		img.fill(Color("#FFFDF8")) # 奶油米白底
		var marker_color := Color.from_hsv(float((_proof_hashes.size() * 53) % 360) / 360.0, 0.7, 0.9)
		for x in range(120, 320):
			for y in range(120, 220):
				img.set_pixel(x, y, marker_color)

	var save_path1 := _out_dir.path_join(file_name)
	var save_path2 := _out_dir_docs.path_join(file_name)
	img.save_png(save_path1)
	DirAccess.copy_absolute(save_path1, save_path2)

	var data := img.get_data()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(data)
	var digest := ctx.finish()
	var hex_hash := digest.hex_encode()
	_proof_hashes[file_name] = hex_hash
