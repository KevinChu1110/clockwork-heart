extends SceneTree
## Product Lock §4：公會週貢獻／NG+／裂縫的玩家入口必須看不見、進不去。
## godot --headless -s res://scripts/ui/test_cut_systems.gd

const FORBIDDEN: Array[String] = [
	"黑焰裂縫", "黑焰迴響", "NG+", "再走一次",
	"公會", "盟約", "週貢", "公庫", "本週焦點", "心魔", "二周目",
]

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			_gs = root.get_node_or_null("GameState")
			if _main == null or _gs == null:
				_fail("main / GameState 沒載起來")
				return _finish()
			_gs.call("reset_new_game")
			_gs.call("set_flag", "game_cleared", true)
			_gs.set("ng_plus", 2)
			_gs.call("set_flag", "boss.demon_cleared", true)
			_step = 1
			_wait = 0
		1:
			_main.call("_go_title")
			_step = 2
			_wait = 0
		2:
			if _wait < 8:
				return false
			_assert_no_forbidden("標題", _host_buttons())
			_main.call("_go_title_start_menu")
			_step = 3
			_wait = 0
		3:
			if _wait < 8:
				return false
			_assert_no_forbidden("開始遊戲子選單", _host_buttons())
			_main.call("_go_title_wall")
			_step = 4
			_wait = 0
		4:
			if _wait < 8:
				return false
			_assert_no_forbidden("稱號牆按鈕", _host_buttons())
			_main.call("_go_ending")
			_step = 5
			_wait = 0
		5:
			if _wait < 8:
				return false
			_assert_no_forbidden("通關後終章", _host_buttons())
			_assert_no_forbidden("通關後終章正文", _host_labels())
			_main.call("_go_postgame_hub")
			_step = 6
			_wait = 0
		6:
			if _wait < 10:
				return false
			_assert_no_forbidden("postgame_hub 轉送後", _host_buttons())
			_main.call("_go_ng_plus_menu")
			_step = 7
			_wait = 0
		7:
			if _wait < 8:
				return false
			_assert_no_forbidden("ng_plus 入口轉送後", _host_buttons())
			_main.call("_go_guild_panel")
			_step = 8
			_wait = 0
		8:
			if _wait < 8:
				return false
			_assert_no_forbidden("公會入口轉送後", _host_buttons())
			_main.call("_go_c1_town")
			_step = 9
			_wait = 0
		9:
			if _wait < 10:
				return false
			_main.call("_open_pause")
			_step = 10
			_wait = 0
		10:
			if _wait < 8:
				return false
			_assert_no_forbidden("暫停選單", _all_buttons())
			_check_quests()
			return _finish()
	return false


func _check_quests() -> void:
	var qs: Node = root.get_node_or_null("QuestSystem")
	if qs == null:
		_fail("QuestSystem missing")
		return
	var listed := str(qs.call("list_missions_bbcode"))
	for needle in PackedStringArray(["裂縫試煉", "二周目啟程", "盟約之契", "公會貢獻", "黑焰迴響"]):
		if listed.find(needle) >= 0:
			_fail("長遠任務還看得到「%s」" % needle)
	var ids: Array = []
	for m in qs.call("missions"):
		ids.append(str(m.get("id", "")))
	for hid in PackedStringArray(["m_rift3", "m_ng1", "m_guild"]):
		if hid in ids:
			_fail("missions() 還露出 %s" % hid)
	if _ok:
		print("  ok 長遠任務已藏公會／NG+／裂縫")


func _assert_no_forbidden(where: String, texts: Array) -> void:
	for t in texts:
		var s := str(t)
		for needle in FORBIDDEN:
			if s.find(needle) >= 0:
				_fail("%s 看得到「%s」（全文：%s）" % [where, needle, s])
				return
	print("  ok ", where, " 按鈕/文案無禁詞（", texts.size(), "）")


func _host_buttons() -> Array:
	var host: Node = _main.get("host")
	if host == null:
		return []
	var labels: Array = []
	var buttons: Array = []
	_collect(host, labels, buttons)
	return buttons


func _host_labels() -> Array:
	var host: Node = _main.get("host")
	if host == null:
		return []
	var labels: Array = []
	var buttons: Array = []
	_collect(host, labels, buttons)
	return labels


func _all_buttons() -> Array:
	var labels: Array = []
	var buttons: Array = []
	_collect(_main, labels, buttons)
	return buttons


func _collect(n: Node, labels: Array, buttons: Array) -> void:
	if n is Label:
		labels.append((n as Label).text)
	elif n is RichTextLabel:
		labels.append((n as RichTextLabel).get_parsed_text())
	elif n is Button:
		buttons.append((n as Button).text)
	for c in n.get_children():
		_collect(c, labels, buttons)


func _finish() -> bool:
	if _ok:
		print("CUT_SYSTEMS_OK")
		quit(0)
	else:
		print("CUT_SYSTEMS_FAIL")
		quit(1)
	return true
