extends SceneTree
## 亮底彈窗強調字壓明度測試
## 驗證 6 個亮底彈窗（背包、鍛造、寶石、每日委託、衣櫥、設定）
## 的所有文字與標籤均不使用暗底舊亮色 (#FFD028, #FFA010, #FF5E8A)，而使用壓明度深色 (#9A6B00, #C2600A, #D62E5C)

const FORBIDDEN_COLORS := [
	Color("#FFD028"),
	Color("#FFA010"),
	Color("#FF5E8A"),
]

var _step := 0
var _wait := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("DIALOG_CONTRAST_FAIL: ", msg)
	quit(1)
	return true


func _check_node_colors(dlg_name: String, node: Node) -> bool:
	if node is Label:
		var col: Color = node.get_theme_color("font_color")
		for fc in FORBIDDEN_COLORS:
			if col.is_equal_approx(fc):
				return _fail("%s: Label '%s' 使用了未壓明度字色 %s" % [dlg_name, node.name, col.to_html()])
	elif node is RichTextLabel:
		var text: String = node.text
		for hex in ["#FFD028", "#ffd028", "#FFA010", "#ffa010", "#FF5E8A", "#ff5e8a"]:
			if hex in text:
				return _fail("%s: RichTextLabel '%s' 包含未壓明度色碼 %s: %s" % [dlg_name, node.name, hex, text])
	for child in node.get_children():
		if not _check_node_colors(dlg_name, child):
			return false
	return true


func _process(_delta: float) -> bool:
	_wait += 1
	if _wait < 15:
		return false
	_wait = 0

	match _step:
		0:
			# 1. 冒險者背包 MapleInventory
			var MapleInventoryScn = load("res://scripts/ui/maple_inventory.gd")
			var inv: Control = MapleInventoryScn.new()
			root.add_child(inv)
			inv.open()
			if not _check_node_colors("MapleInventory", inv):
				return false
			print("  ok MapleInventory 壓明度檢查通過")
			inv.queue_free()
			_step = 1

		1:
			# 2. 裝備鍛造 ForgeDialog
			var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
			var forge: Control = ForgeDialogScn.new()
			root.add_child(forge)
			if not _check_node_colors("ForgeDialog", forge):
				return false
			print("  ok ForgeDialog 壓明度檢查通過")
			forge.queue_free()
			_step = 2

		2:
			# 3. 寶石工坊 GemWorkshopDialog
			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			var gem: Control = GemWorkshopDialogScn.new()
			root.add_child(gem)
			if not _check_node_colors("GemWorkshopDialog (Smelt)", gem):
				return false
			var tab_case_btn: Button = gem.get("_tab_case_btn")
			if tab_case_btn:
				tab_case_btn.pressed.emit()
			if not _check_node_colors("GemWorkshopDialog (Case)", gem):
				return false
			print("  ok GemWorkshopDialog 壓明度檢查通過")
			gem.queue_free()
			_step = 3

		3:
			# 4. 每日上發條 WindupDailyDialog
			var WindupDailyDialogScn = load("res://scripts/ui/windup_daily_dialog.gd")
			var daily: Control = WindupDailyDialogScn.new()
			root.add_child(daily)
			if not _check_node_colors("WindupDailyDialog", daily):
				return false
			print("  ok WindupDailyDialog 壓明度檢查通過")
			daily.queue_free()
			_step = 4

		4:
			# 5. 英雄換裝衣櫥 WardrobeDialog
			var WardrobeDialogScn = load("res://scripts/ui/wardrobe_dialog.gd")
			var wardrobe: Control = WardrobeDialogScn.new()
			root.add_child(wardrobe)
			if not _check_node_colors("WardrobeDialog", wardrobe):
				return false
			print("  ok WardrobeDialog 壓明度檢查通過")
			wardrobe.queue_free()
			_step = 5

		5:
			# 6. 系統設定 MobileSettings
			var MobileSettingsScn = load("res://scripts/ui/mobile_settings.gd")
			var settings: Control = MobileSettingsScn.new()
			root.add_child(settings)
			if not _check_node_colors("MobileSettings (Lang)", settings):
				return false
			print("  ok MobileSettings 壓明度檢查通過")
			settings.queue_free()
			_step = 6

		6:
			print("DIALOG_CONTRAST_OK")
			quit(0)
			return true

	return false
