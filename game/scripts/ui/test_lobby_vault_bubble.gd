extends SceneTree
## 大廳發條儲能庫微動氣泡與滿溢提示單元測試 (test_lobby_vault_bubble.gd)
## 測試項：
## 1. 8 幀發條旋轉小動效（資源數量 8、貼圖有效、步進轉動）
## 2. 氣泡熱區、果凍厚底、零 Emoji 規範（熱區 >= 48px，厚底 5-6px，零 emoji）
## 3. 即時放置累積時數顯示（0h, 4h, 8h 封頂）
## 4. 滿 8 小時金黃呼吸光暈與「可領取」提醒
## 5. 點擊直達收穫彈窗與領取後即時更新
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 在地化同步
## 執行指令：godot --path game --headless -s res://scripts/ui/test_lobby_vault_bubble.gd

var _ok: bool = true
var _step: int = 0
var _wait: int = 0
var _lobby: Node = null

const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ClockworkVaultDialog = preload("res://scripts/ui/clockwork_vault_dialog.gd")

const FORBIDDEN_CHARS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑", "💰", "📦"
]


func _fail(msg: String) -> void:
	push_error("FAIL: " + msg)
	print("  FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		if gs.has_method("reset_new_game"):
			gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.gold = 1000

	var inv := root.get_node_or_null("InventorySystem")
	if inv != null and inv.has_method("clear"):
		inv.clear()

	_lobby = MobileLobby.new()
	root.add_child(_lobby)


func _process(_delta: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 6:
			return false
		_step = 1

		print("── [1/6] 8 幀發條旋轉小動效資源與推進測試 ──")
		_test_bubble_key_animation()

		print("── [2/6] 氣泡規格規範測試 (熱區 >= 48px / 果凍厚底 / 零 Emoji) ──")
		_test_bubble_spec()

		print("── [3/6] 當前累積時數即時顯示測試 (0h / 4h / 8h) ──")
		_test_bubble_time_display()

		print("── [4/6] 滿 8 小時金黃呼吸光暈與「可領取」提醒測試 ──")
		_test_bubble_full_glow_and_alert()

		print("── [5/6] 點擊直達收穫彈窗與領取後即時更新測試 ──")
		_test_bubble_click_and_claim_refresh()

		print("── [6/6] 六語系在地化翻譯就緒測試 ──")
		_test_i18n_locales()

		_finish()
		return true
	return false


func _test_bubble_key_animation() -> void:
	var textures: Array[Texture2D] = _lobby.call("get_vault_bubble_key_textures")
	if textures.size() != 8:
		_fail("發條氣泡 8 幀貼圖數量不為 8，實際: %d" % textures.size())
		return

	for i in range(textures.size()):
		var tex: Texture2D = textures[i]
		if tex == null:
			_fail("發條氣泡第 %d 幀貼圖為 null" % i)
			return
		var img: Image = tex.get_image()
		if img == null or img.is_empty():
			_fail("發條氣泡第 %d 幀 Image 無效" % i)
			return

	var img0: Image = textures[0].get_image()
	var img2: Image = textures[2].get_image()
	if img0.get_format() != Image.FORMAT_RGBA8:
		img0.convert(Image.FORMAT_RGBA8)
	if img2.get_format() != Image.FORMAT_RGBA8:
		img2.convert(Image.FORMAT_RGBA8)

	var diff_px: int = 0
	for y in range(min(img0.get_height(), img2.get_height())):
		for x in range(min(img0.get_width(), img2.get_width())):
			if img0.get_pixel(x, y) != img2.get_pixel(x, y):
				diff_px += 1

	if diff_px <= 0:
		_fail("第 0 幀與第 2 幀像素差為 0，旋轉幀無差異！")
		return
	print("  ✓ 8 幀發條旋轉小動效資源齊全，相鄰幀旋轉像素差檢驗通過 (diff: %d px)" % diff_px)

	# 測試手動與自動步進幀推進
	var initial_idx: int = _lobby.call("get_vault_bubble_frame_index")
	_lobby.call("step_vault_bubble_frame")
	var next_idx: int = _lobby.call("get_vault_bubble_frame_index")
	if next_idx != (initial_idx + 1) % 8:
		_fail("步進推進幀索引不正確！預期: %d, 實際: %d" % [(initial_idx + 1) % 8, next_idx])
		return

	var key_icon: TextureRect = _lobby.call("get_vault_bubble_key_icon")
	if key_icon == null or key_icon.texture != textures[next_idx]:
		_fail("發條氣泡圖示未更新為當前幀貼圖！")
		return
	print("  ✓ 氣泡發條鑰匙步進轉動機制正常 (幀索引: %d -> %d)" % [initial_idx, next_idx])


func _test_bubble_spec() -> void:
	var bubble: Control = _lobby.call("get_vault_bubble")
	if bubble == null or not is_instance_valid(bubble):
		_fail("未找到 VaultBubble 氣泡節點！")
		return
	if not bubble.visible:
		_fail("VaultBubble 節點預設不可見！")
		return

	var btn: Button = _lobby.call("get_vault_bubble_button")
	if btn == null or not is_instance_valid(btn):
		_fail("未找到 VaultBubbleBtn 按鈕節點！")
		return

	# 熱區 >= 48px
	var btn_sz: Vector2 = btn.custom_minimum_size
	if btn_sz.x < 48.0 or btn_sz.y < 48.0:
		_fail("VaultBubbleBtn 熱區不足 48px！尺寸: (%f, %f)" % [btn_sz.x, btn_sz.y])
		return
	print("  ✓ 按鈕熱區規範通過 (尺寸: %.1f x %.1f >= 48px)" % [btn_sz.x, btn_sz.y])

	# 果凍厚底 StyleBoxFlat
	var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("VaultBubbleBtn normal 未設定 StyleBoxFlat！")
		return
	if sb.border_width_bottom < 5:
		_fail("果凍厚底不足 5px！實際: %d" % sb.border_width_bottom)
		return
	if sb.corner_radius_top_left < 16:
		_fail("圓角小於 16px！實際: %d" % sb.corner_radius_top_left)
		return
	print("  ✓ 果凍厚底樣式規範通過 (border_bottom: %d px >= 5px, 圓角: %d px)" % [sb.border_width_bottom, sb.corner_radius_top_left])

	# 零系統 Emoji 檢查
	var time_lbl: Label = _lobby.call("get_vault_bubble_time_label")
	var status_lbl: Label = _lobby.call("get_vault_bubble_status_label")
	var texts_to_check: Array[String] = [
		time_lbl.text if time_lbl else "",
		status_lbl.text if status_lbl else "",
		btn.text
	]
	for txt in texts_to_check:
		for fc in FORBIDDEN_CHARS:
			if txt.contains(fc):
				_fail("VaultBubble 出現禁止符號 '%s': %s" % [fc, txt])
				return
	print("  ✓ 零系統 Emoji 檢查 100% 通過")


func _test_bubble_time_display() -> void:
	var now_t := Time.get_unix_time_from_system()

	# 0 小時狀態
	IdleClockworkVault.set_last_claim_ts(now_t)
	_lobby.call("refresh_vault_display")
	var time_lbl: Label = _lobby.call("get_vault_bubble_time_label")
	if not time_lbl.text.contains("0h") or not time_lbl.text.contains("8h"):
		_fail("0h 累積時數顯示不正確！實際: %s" % time_lbl.text)
		return
	var is_glow_0h: bool = _lobby.call("is_vault_bubble_full_glow")
	if is_glow_0h:
		_fail("0h 狀態不應觸發金黃滿溢光暈！")
		return
	print("  ✓ 0 小時累積時數即時更新正確: '%s' (未滿，無光暈)" % time_lbl.text)

	# 4 小時狀態
	IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)
	_lobby.call("refresh_vault_display")
	if not time_lbl.text.contains("4h") or not time_lbl.text.contains("8h"):
		_fail("4h 累積時數顯示不正確！實際: %s" % time_lbl.text)
		return
	var is_glow_4h: bool = _lobby.call("is_vault_bubble_full_glow")
	if is_glow_4h:
		_fail("4h 狀態不應觸發金黃滿溢光暈！")
		return
	print("  ✓ 4 小時累積時數即時更新正確: '%s' (未滿，無光暈)" % time_lbl.text)

	# 8 小時滿溢狀態
	IdleClockworkVault.set_last_claim_ts(now_t - 28800.0)
	_lobby.call("refresh_vault_display")
	if not time_lbl.text.contains("8h"):
		_fail("8h 累積時數顯示不正確！實際: %s" % time_lbl.text)
		return
	print("  ✓ 8 小時滿額累積時數即時更新正確: '%s'" % time_lbl.text)


func _test_bubble_full_glow_and_alert() -> void:
	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t - 28800.0) # 8 小時
	_lobby.call("refresh_vault_display")

	var is_glow: bool = _lobby.call("is_vault_bubble_full_glow")
	if not is_glow:
		_fail("滿 8 小時時未激活 is_vault_bubble_full_glow！")
		return

	var glow_panel: Panel = _lobby.call("get_vault_bubble_glow_panel")
	if glow_panel == null or not glow_panel.visible:
		_fail("滿 8 小時時 VaultBubbleGlow 面板未顯示！")
		return

	var status_lbl: Label = _lobby.call("get_vault_bubble_status_label")
	if status_lbl == null or not status_lbl.text.contains("可領取"):
		_fail("滿 8 小時時狀態提示未顯示「可領取」！實際: %s" % (status_lbl.text if status_lbl else "null"))
		return
	print("  ✓ 滿 8 小時金黃呼吸光暈激活且「可領取」提醒正確顯示: '%s'" % status_lbl.text)


func _test_bubble_click_and_claim_refresh() -> void:
	var btn: Button = _lobby.call("get_vault_bubble_button")
	if btn == null:
		_fail("get_vault_bubble_button 為 null！")
		return

	# 模擬點擊按鈕開啟彈窗
	btn.emit_signal("pressed")
	var dlg: Control = _lobby.get_node_or_null("ClockworkVaultDialog") as Control
	if dlg == null:
		_fail("點擊 VaultBubbleBtn 後未開啟 ClockworkVaultDialog！")
		return
	print("  ✓ 點擊發條氣泡成功直達收穫彈窗 ClockworkVaultDialog")

	# 領取收益並關閉彈窗
	IdleClockworkVault.claim()
	_lobby.call("refresh_vault_display")

	var time_lbl: Label = _lobby.call("get_vault_bubble_time_label")
	var status_lbl: Label = _lobby.call("get_vault_bubble_status_label")
	var is_glow: bool = _lobby.call("is_vault_bubble_full_glow")

	if not time_lbl.text.contains("0h"):
		_fail("領取收益後氣泡時數未即時歸零！實際: %s" % time_lbl.text)
		return
	if is_glow:
		_fail("領取收益後金黃呼吸光暈未關閉！")
		return
	print("  ✓ 領取收益後氣泡即時刷新歸零: '%s'，呼吸光暈解除，狀態更新為: '%s'" % [time_lbl.text, status_lbl.text])

	if is_instance_valid(dlg):
		dlg.queue_free()


func _test_i18n_locales() -> void:
	var locales: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var required_keys: Array[String] = [
		"vault.bubble_accumulated",
		"vault.bubble_claim_ready",
		"vault.bubble_full"
	]

	for loc in locales:
		var path := "res://data/i18n/%s.json" % loc
		if not FileAccess.file_exists(path):
			_fail("缺少語系檔案: %s" % path)
			return
		var f := FileAccess.open(path, FileAccess.READ)
		var json_str := f.get_as_text()
		f.close()
		var d = JSON.parse_string(json_str)
		if typeof(d) != TYPE_DICTIONARY:
			_fail("語系檔案 JSON 解析失敗: %s" % path)
			return
		for k in required_keys:
			if not d.has(k) or str(d[k]).strip_edges().is_empty():
				_fail("語系 %s 缺少鍵值: %s" % [loc, k])
				return

	print("  ✓ 六大語系 (zh_TW, zh_CN, en, ja, ko, es) 氣泡文字 100% 翻譯就緒")


func _finish() -> void:
	if _lobby:
		_lobby.queue_free()
	if _ok:
		print("========================================")
		print("  LOBBY_VAULT_BUBBLE_TEST_OK")
		print("========================================")
		quit(0)
	else:
		push_error("LOBBY_VAULT_BUBBLE_TEST_FAIL")
		print("  LOBBY_VAULT_BUBBLE_TEST_FAIL")
		quit(1)
