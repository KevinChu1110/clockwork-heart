extends SceneTree
## 衣櫥名牌與區塊標題（#60）：godot --headless -s res://scripts/ui/test_wardrobe_nameplate.gd
## 守：
##   1. 名牌是目前外裝所屬的玩具家族（例：【胡桃鉗兔 · 近衛】），不再出現舊種族名、職業英文 id。
##   2. 換上別家族的外裝，名牌跟著換（錫兵外裝 → 【錫兵 · 儀隊】）。
##   3. 七個區塊標題不夾括號英文；六語系都有譯文（非繁中語系不能原樣掉回中文）。

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_PLATE := {
	"zh_TW": "【胡桃鉗兔 · 近衛】",
	"zh_CN": "【胡桃钳兔 · 近卫】",
	"en": "【Nutcracker Rabbit · Guard】",
	"ja": "【くるみ割りウサギ · 近衛】",
	"ko": "【호두까기 토끼 · 근위】",
	"es": "【Conejo Cascanueces · Guardia】",
}
const OLD_BITS := ["白金兔", "劍士", "(knight)", "knight", "("]

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
	var loc: Node = root.get_node_or_null("Loc")
	var dlg = WardrobeDialog.new()
	root.add_child(dlg)

	for code in LOCALES:
		if loc:
			loc.call("set_locale", code)
		dlg._update_ui_texts()
		var plate: String = dlg._badge_race_label.text
		for bit in OLD_BITS:
			if bit in plate:
				_fail("[%s] 名牌仍帶「%s」：%s" % [code, bit, plate])
		if plate != EXPECTED_PLATE[code]:
			_fail("[%s] 預設名牌應為 %s，實際 %s" % [code, EXPECTED_PLATE[code], plate])
		for t in [dlg._costume_section_title, dlg._chassis_section_title]:
			if t and ("(" in (t as Label).text or "Costume" in (t as Label).text):
				_fail("[%s] 區塊標題仍夾英文：%s" % [code, (t as Label).text])
		for sid in dlg._section_nodes.keys():
			for lbl in (dlg._section_nodes[sid] as Node).find_children("*", "Label", true, false):
				var s := (lbl as Label).text
				for eng in ["(Costume)", "(Chassis", "(Head Unit)", "(Weapon)", "(Wind-up Key)", "(Optic Core)", "(Back Curio)"]:
					if eng in s:
						_fail("[%s] %s 區塊標題仍夾英文：%s" % [code, sid, s])
		print("  ok  [%s] 名牌 %s" % [code, plate])

	if loc:
		loc.call("set_locale", "zh_TW")
	dlg._on_slot_item_selected("costume", 0, "costume_viking_harness")
	if dlg._badge_race_label.text != "【錫兵 · 儀隊】":
		_fail("換上錫兵家族外裝（costume_viking_harness）後名牌應為【錫兵 · 儀隊】，實際 %s" % dlg._badge_race_label.text)
	else:
		print("  ok  換錫兵外裝 → ", dlg._badge_race_label.text)
	dlg._on_reset_pressed()
	if dlg._badge_race_label.text != "【胡桃鉗兔 · 近衛】":
		_fail("還原預設後名牌應回【胡桃鉗兔 · 近衛】，實際 %s" % dlg._badge_race_label.text)

	if _ok:
		print("WARDROBE_NAMEPLATE_OK")
	quit(0 if _ok else 1)
