extends SceneTree
## 大廳／據點 HUD 必須讀存檔真值，不准寫死 Lv.12／戰力 482／12,500／350。
## godot --headless -s res://scripts/ui/test_energy_hud.gd

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Node = null
var _hud: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs == null:
		_fail("GameState autoload missing")
		return _finish()
	gs.reset_new_game()
	gs.player_name = "測試兔"
	gs.level = 7
	gs.gold = 23456
	gs.stardust = 88
	gs.energy = 9
	gs.energy_ts = Time.get_unix_time_from_system()

	var Lobby := load("res://scripts/ui/mobile_lobby.gd")
	_lobby = Lobby.new()
	root.add_child(_lobby)

	var Hud := load("res://scripts/ui/maple_hud.gd")
	_hud = Hud.new()
	root.add_child(_hud)


func _process(_d: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 8:
			return false
		_check_lobby()
		_check_maple()
		return _finish()
	return false


func _check_lobby() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("MobileLobby 沒建起來")
		return
	if _lobby.has_method("refresh_hud"):
		_lobby.call("refresh_hud")
	var gs := root.get_node_or_null("GameState")
	var en := root.get_node_or_null("EnergySystem")
	var lv := str(_lobby.get("_lv_label").text) if _lobby.get("_lv_label") else ""
	var pwr := str(_lobby.get("_power_label").text) if _lobby.get("_power_label") else ""
	var energy := str(_lobby.get("_energy_label").text) if _lobby.get("_energy_label") else ""
	var gold := str(_lobby.get("_gold_label").text) if _lobby.get("_gold_label") else ""
	var gem := str(_lobby.get("_gem_label").text) if _lobby.get("_gem_label") else ""
	print("  lobby lv=", lv, " pwr=", pwr, " energy=", energy, " gold=", gold, " gem=", gem)

	if lv.find("7") < 0:
		_fail("大廳等級應含 7，得 %s" % lv)
	if lv.find("12") >= 0:
		_fail("大廳等級仍寫死 12：%s" % lv)
	var want_pow := str(int(gs.power_score()))
	if pwr.find(want_pow) < 0:
		_fail("大廳戰力應含 %s，得 %s" % [want_pow, pwr])
	if pwr.find("482") >= 0 and want_pow != "482":
		_fail("大廳戰力仍寫死 482：%s" % pwr)
	if energy.find("9") < 0 or energy.find("15") < 0:
		_fail("大廳能量應含 9/15，得 %s" % energy)
	if energy.find("15/15") >= 0:
		_fail("大廳能量未滿卻顯示 15/15：%s" % energy)
	## 未滿要有倒數
	if energy.find("分") < 0:
		_fail("大廳能量未滿應顯示倒數，得 %s" % energy)
	if gold.find("23,456") < 0 and gold.find("23456") < 0:
		_fail("大廳金幣應含 23456，得 %s" % gold)
	if gold.find("12,500") >= 0 or gold.find("12500") >= 0:
		_fail("大廳金幣仍寫死 12500：%s" % gold)
	if gem.find("88") < 0:
		_fail("大廳星屑應含 88，得 %s" % gem)
	if gem.find("350") >= 0:
		_fail("大廳仍寫死晶石 350：%s" % gem)
	if en == null:
		_fail("EnergySystem missing")
	print("  ok 大廳 HUD 讀真值")


func _check_maple() -> void:
	if _hud == null or not is_instance_valid(_hud):
		_fail("MapleHud 沒建起來")
		return
	if _hud.has_method("refresh"):
		_hud.call("refresh")
	var gold_l: Label = _hud.get("_gold_l")
	var lv_l: Label = _hud.get("_lv_l")
	if gold_l == null or lv_l == null:
		_fail("MapleHud 缺 _gold_l／_lv_l")
		return
	var visible := str(gold_l.text)
	var tip := str(gold_l.tooltip_text)
	print("  maple lv=", lv_l.text, " gold=", visible, " tip=", tip)
	if str(lv_l.text).find("7") < 0:
		_fail("據點 HUD 等級應含 7，得 %s" % lv_l.text)
	if visible.find("能量") < 0 and visible.to_lower().find("energy") < 0:
		_fail("據點 HUD 能量應常駐可見，得 text=%s tooltip=%s" % [visible, tip])
	if visible.find("9") < 0:
		_fail("據點 HUD 可見文字應含當前能量 9，得 %s" % visible)
	print("  ok 據點 HUD 能量常駐可見")


func _finish() -> bool:
	if _ok:
		print("ENERGY_HUD_OK")
		quit(0)
	else:
		print("ENERGY_HUD_FAIL")
		quit(1)
	return true
