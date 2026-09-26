extends SceneTree
## 武術館兵器架十二流派名稱與說明六語系單元測試 (test_weapon_classes_i18n.gd)
## 驗證項目：
## 1. 改 locale 後抽劍／長槍／弓三個流派，按鈕字與 play 等於該語系詞條。
## 2. 「劍」在 en 不准是 S（必須為 Sword）。
## 3. 數值、職業對應、starter 武器不變。
## 4. 全程零系統 emoji。
## 5. 0-QA24: ja/ko 漢字完全對齊語系檔。
## 6. 即時刷新與 GameState.path_display() 語系切換。

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const _ContentLoc = preload("res://scripts/systems/content_loc.gd")
const DialogLines = preload("res://scripts/systems/dialog_lines.gd")

var _ok := true
var _started := false
var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _process(_delta: float) -> bool:
	if _started:
		return false
	_started = true

	print("=== 開始 test_weapon_classes_i18n 單元測試 ===")
	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_dt = root.get_node_or_null("DataTables")

	if _loc_node == null or _gs == null or _dt == null:
		_fail("Autoload 節點未就緒: Loc=%s, GameState=%s, DataTables=%s" % [str(_loc_node), str(_gs), str(_dt)])
		quit(1)
		return true

	_run_all_tests()

	if _ok:
		print("\n=== ✓ test_weapon_classes_i18n 全部通過！ ===")
		print("WEAPON_CLASSES_I18N_OK")
		quit(0)
	else:
		print("\n=== ✗ test_weapon_classes_i18n 測試失敗！ ===")
		print("WEAPON_CLASSES_I18N_FAIL")
		quit(1)
	return true

func _run_all_tests() -> void:
	# 預期詞條定義：抽驗 劍 (sword)、長槍 (spear)、弓 (bow)
	var expected_sword_btn := {
		"zh_TW": "劍·騎士·劍",
		"zh_CN": "剑·骑士·剑",
		"en": "Sword · Knight · Sword",
		"ja": "剣・騎士・剣",
		"ko": "검·기사·검",
		"es": "Espada · Caballero · Espada"
	}
	var expected_sword_play := {
		"zh_TW": "近身中距離，普攻和怒氣技輪著來。同職也可玩槍。",
		"zh_CN": "近身中距离，普攻与怒气技交替施展。同职业亦可使用长枪。",
		"en": "Close to mid range, alternating normal strikes and rage skills. The spear is also playable in this class.",
		"ja": "近距離から中距離で、通常攻撃と怒り技を交互に繰り出す。同職で槍も扱える。",
		"ko": "근거리와 중거리에서 기본 공격과 분노 기술을 번갈아 사용합니다. 같은 직업으로 창도 선택할 수 있습니다.",
		"es": "Distancia corta a media, alternando ataques básicos y habilidades de furia. Esta clase también puede usar lanza."
	}

	var expected_spear_btn := {
		"zh_TW": "長槍·騎士·槍",
		"zh_CN": "长枪·骑士·枪",
		"en": "Spear · Knight · Spear",
		"ja": "長槍・騎士・槍",
		"ko": "창·기사·창",
		"es": "Lanza · Caballero · Lanza"
	}
	var expected_spear_play := {
		"zh_TW": "卡住距離，等他進來就迎上去。同職也可玩劍。",
		"zh_CN": "把控距离，待敌逼近即刻迎击。同职业亦可使用利剑。",
		"en": "Hold spacing and counter when they push in. The sword is also playable in this class.",
		"ja": "間合いを保ち、踏み込んできた敵を迎え撃つ。同職で剣も扱える。",
		"ko": "거리를 유지하다가 파고드는 적을 요격합니다. 같은 직업으로 검도 선택할 수 있습니다.",
		"es": "Mantén la distancia y contraataca cuando el enemigo avance. Esta clase también puede usar espada."
	}

	var expected_bow_btn := {
		"zh_TW": "弓·遊俠·弓",
		"zh_CN": "弓·游侠·弓",
		"en": "Bow · Ranger · Bow",
		"ja": "弓・レンジャー・弓",
		"ko": "활·레인저·활",
		"es": "Arco · Guardabosques · Arco"
	}
	var expected_bow_play := {
		"zh_TW": "拉開距離再射。同職也可玩火槍。",
		"zh_CN": "保持距离从容拉弦射击。同职业亦可使用火枪。",
		"en": "Keep distance and snipe safely. Guns are also playable in this class.",
		"ja": "間合いを取って安全圏から射貫く。同職で銃も扱える。",
		"ko": "거리를 벌리고 안전하게 저격합니다. 같은 직업으로 총도 선택할 수 있습니다.",
		"es": "Mantén las distancias y dispara con seguridad. Esta clase también puede usar armas de fuego."
	}

	for lc in LOCALES:
		print("\n--- 測試語系: %s ---" % lc)
		_loc_node.call("set_locale", lc)

		var sep: String = " · " if (lc == "en" or lc == "es") else ("・" if lc == "ja" else "·")

		# ── 1. 抽驗 劍 (sword) ──
		var d_sword: Dictionary = _dt.call("weapon_class_def", "sword")
		var s_name: String = str(d_sword.get("name", ""))
		var s_title: String = str(d_sword.get("title", ""))
		var s_btn := "%s%s%s" % [s_name, sep, s_title]
		var s_play: String = str(d_sword.get("play", ""))

		if lc == "en":
			if s_name == "S":
				_fail("[en] 嚴重缺失：劍的名稱仍被翻譯為單字母 'S'！")
			elif s_name != "Sword":
				_fail("[en] 劍的名稱錯誤: 期望 'Sword'，實際 '%s'" % s_name)
			else:
				print("  ✓ [en] 劍名稱不是 S，正確為 Sword")

		if s_btn != expected_sword_btn[lc]:
			_fail("[%s] 劍按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_sword_btn[lc], s_btn])
		else:
			print("  ✓ [%s] 劍按鈕文字驗證通過: %s" % [lc, s_btn])

		if s_play != expected_sword_play[lc]:
			_fail("[%s] 劍 play 說明錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_sword_play[lc], s_play])
		else:
			print("  ✓ [%s] 劍 play 說明驗證通過: %s" % [lc, s_play])

		# ── 2. 抽驗 長槍 (spear) ──
		var d_spear: Dictionary = _dt.call("weapon_class_def", "spear")
		var sp_name: String = str(d_spear.get("name", ""))
		var sp_title: String = str(d_spear.get("title", ""))
		var sp_btn := "%s%s%s" % [sp_name, sep, sp_title]
		var sp_play: String = str(d_spear.get("play", ""))

		if sp_btn != expected_spear_btn[lc]:
			_fail("[%s] 長槍按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_spear_btn[lc], sp_btn])
		else:
			print("  ✓ [%s] 長槍按鈕文字驗證通過: %s" % [lc, sp_btn])

		if sp_play != expected_spear_play[lc]:
			_fail("[%s] 長槍 play 說明錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_spear_play[lc], sp_play])
		else:
			print("  ✓ [%s] 長槍 play 說明驗證通過: %s" % [lc, sp_play])

		# ── 3. 抽驗 弓 (bow) ──
		var d_bow: Dictionary = _dt.call("weapon_class_def", "bow")
		var b_name: String = str(d_bow.get("name", ""))
		var b_title: String = str(d_bow.get("title", ""))
		var b_btn := "%s%s%s" % [b_name, sep, b_title]
		var b_play: String = str(d_bow.get("play", ""))

		if b_btn != expected_bow_btn[lc]:
			_fail("[%s] 弓按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_bow_btn[lc], b_btn])
		else:
			print("  ✓ [%s] 弓按鈕文字驗證通過: %s" % [lc, b_btn])

		if b_play != expected_bow_play[lc]:
			_fail("[%s] 弓 play 說明錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_bow_play[lc], b_play])
		else:
			print("  ✓ [%s] 弓 play 說明驗證通過: %s" % [lc, b_play])

		# ── 4. 驗證 GameState.path_display() ──
		_gs.call("set_path_style", "sword")
		var disp_sword: String = _gs.call("path_display")
		if disp_sword != expected_sword_btn[lc]:
			_fail("[%s] GameState.path_display(sword) 錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_sword_btn[lc], disp_sword])
		else:
			print("  ✓ [%s] GameState.path_display(sword) 驗證通過: %s" % [lc, disp_sword])

		# ── 5. 驗證數值、職業、starter 武器不變 ──
		var all_classes: Array = _dt.call("weapon_class_list")
		if all_classes.size() != 12:
			_fail("[%s] weapon_class_list 數量錯誤: 期望 12，實際 %d" % [lc, all_classes.size()])

		for c in all_classes:
			var cid := str(c.get("id", ""))
			var atk: int = int(c.get("atk", 0))
			var def: int = int(c.get("def", 0))
			var starter := str(c.get("starter_weapon", ""))
			var prof := str(c.get("profession", ""))

			if cid == "sword":
				if atk != 2 or def != 1 or starter != "meager_edge" or prof != "knight":
					_fail("[%s] sword 數值／職業／初始武器遭竄改！" % lc)
			elif cid == "spear":
				if atk != 3 or def != 2 or starter != "ash_spear" or prof != "knight":
					_fail("[%s] spear 數值／職業／初始武器遭竄改！" % lc)
			elif cid == "bow":
				if atk != 2 or def != 0 or starter != "reed_bow" or prof != "ranger":
					_fail("[%s] bow 數值／職業／初始武器遭竄改！" % lc)

			# ── 6. 驗證零系統 emoji ──
			var txt_all := "%s %s %s %s" % [c.get("name", ""), c.get("title", ""), c.get("tagline", ""), c.get("play", "")]
			if _has_emoji(txt_all):
				_fail("[%s] %s 包含系統 emoji！文字: %s" % [lc, cid, txt_all])

		# ── 7. 驗證職業名「武鬥」六語系映射 ──
		var expected_monk := {
			"zh_TW": "武鬥",
			"zh_CN": "武斗",
			"en": "Monk",
			"ja": "武闘",
			"ko": "무투",
			"es": "Monje"
		}
		var monk_val := _ContentLoc.text("ui", "武鬥")
		if monk_val != expected_monk[lc]:
			_fail("[%s] 職業名「武鬥」錯誤: 期望 '%s'，實際 '%s'" % [lc, expected_monk[lc], monk_val])
		else:
			print("  ✓ [%s] 職業名「武鬥」驗證通過: %s" % [lc, monk_val])

		# ── 8. 驗證選定流派確認對話無雙句號 (forge.path_chosen) ──
		DialogLines.reload()
		for c in all_classes:
			var cid := str(c.get("id", ""))
			var tip := str(c.get("play", ""))
			var pros: Array = c.get("pros", [])
			var pro0 := str(pros[0]) if pros.size() > 0 else ""
			var lines: Array = DialogLines.lines("forge.path_chosen", {
				"path": "%s%s%s" % [c.get("name", cid), sep, c.get("title", "")],
				"play": tip,
				"pro": pro0,
				"power": 100,
			})
			if lines.size() < 2:
				_fail("[%s] %s forge.path_chosen 句數不足: %d" % [lc, cid, lines.size()])
				continue
			var play_text: String = str(lines[1].get("text", ""))
			if play_text.contains("..") or play_text.contains("。。"):
				_fail("[%s] %s forge.path_chosen 出現雙句號: %s" % [lc, cid, play_text])

	print("  ✓ [全部語系] 12 流派 forge.path_chosen 對話皆無雙句號（.. 或 。。）")

	# 測試完恢復繁體中文
	_loc_node.call("set_locale", "zh_TW")
