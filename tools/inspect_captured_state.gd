extends SceneTree

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

func _init() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null: win.size = Vector2i(1280, 720)

	var LocClass = load("res://scripts/autoload/loc.gd")
	var loc_node = LocClass.new()
	loc_node.name = "Loc"
	root.add_child(loc_node)

	var GsClass = load("res://scripts/autoload/game_state.gd")
	var gs = GsClass.new()
	gs.name = "GameState"
	root.add_child(gs)
	gs.call("reset_new_game", "rabbit")
	gs.set("level", 25)
	gs.set("hp", 150)
	gs.set("max_hp", 150)

	# 測試繁中
	loc_node.call("set_locale", "zh_TW")
	ContentLocClass.reload()
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "colossus_lion")

	var sim: Object = battle.get("sim")
	sim.call("trigger_colossus_windup")
	var lion = sim.call("get_unit", "colossus_lion")
	sim.call("_resolve_king_slash_hit", lion)

	var log_label: RichTextLabel = battle.find_child("Log", true, false)
	var parsed_zh: String = log_label.get_parsed_text()
	print("--- ZH PARSED LOG ---")
	print(parsed_zh)
	print("---------------------")

	# 驗證繁中日誌
	assert(parsed_zh.contains("敵手金屬板件厚實（防爆高）——爆擊難進，發條重擊最實在。"), "繁中日誌必須有新世界觀句")
	assert(not parsed_zh.contains("筋骨"), "繁中日誌不可有筋骨")
	assert(not parsed_zh.contains("斧鎚"), "繁中日誌不可有斧鎚")
	assert(parsed_zh.contains("【王者斬】 失控發條獅 造成"), "繁中王者斬技能名與敵名有空格")

	battle.queue_free()

	# 測試英文
	loc_node.call("set_locale", "en")
	ContentLocClass.reload()
	battle = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "colossus_lion")

	sim = battle.get("sim")
	sim.call("trigger_colossus_windup")
	lion = sim.call("get_unit", "colossus_lion")
	sim.call("_resolve_king_slash_hit", lion)

	log_label = battle.find_child("Log", true, false)
	var parsed_en: String = log_label.get_parsed_text()
	print("--- EN PARSED LOG ---")
	print(parsed_en)
	print("---------------------")

	# 驗證英文日誌
	assert(not parsed_en.contains("[/b]"), "英文日誌不可露出 [/b]")
	assert(parsed_en.contains("[The King's Cut] Rampant Clockwork Lion"), "英文技能名與敵名必須有空格")
	assert(parsed_en.contains("Sturdy metal plates (high crit guard)"), "英文日誌包含金屬板件發條句")

	# 驗證英文按鈕
	var btn_attack: Button = battle.get("_btn_attack")
	print("--- EN ATTACK BTN ---")
	print("text: '", btn_attack.text, "'")
	print("contains newline: ", btn_attack.text.contains("\n"))
	print("autowrap_mode: ", btn_attack.autowrap_mode)
	print("size: ", btn_attack.size, ", min_size: ", btn_attack.custom_minimum_size)
	print("---------------------")
	assert(btn_attack.text == "Attack", "英文常態按鈕文字為 Attack")
	assert(not btn_attack.text.contains("\n"), "英文常態按鈕文字不可有換行")
	assert(btn_attack.autowrap_mode == TextServer.AUTOWRAP_OFF, "英文常態按鈕關閉自動折行")
	assert(btn_attack.custom_minimum_size.y >= 48.0, "按鈕熱區高 >= 48")

	print("ALL AUDIT CHECKS PASSED!")
	quit(0)
