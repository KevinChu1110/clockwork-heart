extends SceneTree
## 大廳主角戳碰氣泡與聚魂完畢提示六語系單元測試 (test_lobby_poke_toast_i18n.gd)
## 驗證：
## 1. 五句氣泡台詞、聚魂完畢提示與金幣在六語系 (zh_TW, zh_CN, en, ja, ko, es) 下均有正確對應，無漏翻、無系統 emoji。
## 2. 封靈罐卡片初次建立時 CostLabel 走語系 _t("金幣")，非寫死繁中。
## 3. 點擊大廳主角時，氣泡台詞根據當前語系呈現正確譯文。
## 4. 氣泡顯示中切換語系，氣泡台詞即時同步刷新為新語系譯文。
## 5. 聚魂殿完成時產生的 toast 提示依當前語系顯示。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_SPEECHES: Dictionary = {
	"看我的旋風斬～喝！": {
		"zh_TW": "看我的旋風斬～喝！",
		"zh_CN": "看我的旋风斩～喝！",
		"en": "Take my Whirlwind Slash—Hah!",
		"ja": "我が旋風斬を見よ～ハッ！",
		"ko": "내 회오리 베기를 받아라~ 핫!",
		"es": "¡Mira mi Corte Torbellino... Ja!"
	},
	"背後的發條上得剛剛好，出發吧！": {
		"zh_TW": "背後的發條上得剛剛好，出發吧！",
		"zh_CN": "背后的发条上得刚刚好，出发吧！",
		"en": "The wind-up key on my back is wound just right, let's go!",
		"ja": "背中のゼンマイはバッチリ巻けた、出発だ！",
		"ko": "등 뒤의 태엽이 딱 맞게 감겼어, 출발하자!",
		"es": "¡La cuerda de mi espalda está perfecta, en marcha!"
	},
	"聽見神殿齒輪的轉動聲了嗎？": {
		"zh_TW": "聽見神殿齒輪的轉動聲了嗎？",
		"zh_CN": "听见神殿齿轮的转动声了吗？",
		"en": "Can you hear the temple gears turning?",
		"ja": "神殿の歯車が回る音が聞こえるかい？",
		"ko": "신전 톱니바퀴가 돌아가는 소리가 들리나요?",
		"es": "¿Oyes el girar de los engranajes del templo?"
	},
	"神殿的以太核心正在共鳴……": {
		"zh_TW": "神殿的以太核心正在共鳴……",
		"zh_CN": "神殿的以太核心正在共鸣……",
		"en": "The temple's ether core is resonating...",
		"ja": "神殿のエーテルコアが共鳴している……",
		"ko": "신전의 에테르 코어가 공명하고 있어……",
		"es": "El núcleo de éter del templo está resonando..."
	},
	"隨時準備好去挑戰大首領！": {
		"zh_TW": "隨時準備好去挑戰大首領！",
		"zh_CN": "随时准备好去挑战大首领！",
		"en": "Always ready to challenge the Grand Boss!",
		"ja": "大ボスに挑む準備はいつでも万全だ！",
		"ko": "언제든 대보스에게 도전할 준비 완료!",
		"es": "¡Siempre listos para desafiar al Gran Jefe!"
	}
}

const EXPECTED_TOAST: Dictionary = {
	"zh_TW": "聚魂完畢！獲得了戰魂碎片與戰魂經驗！",
	"zh_CN": "聚魂完毕！获得了战魂碎片与战魂经验！",
	"en": "Soul gathering complete! Received Soul Shards and Soul EXP!",
	"ja": "聚魂完了！戦魂の欠片と戦魂経験を獲得！",
	"ko": "전혼 집중 완료! 전혼 조각과 전혼 경험치를 획득했습니다!",
	"es": "¡Reunión de almas completada! ¡Obtuviste fragmentos de alma y EXP de alma!"
}

const EXPECTED_GOLD: Dictionary = {
	"zh_TW": "金幣",
	"zh_CN": "金币",
	"en": "Gold",
	"ja": "金",
	"ko": "골드",
	"es": "Oro"
}

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_lobby_poke_toast_i18n 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	var gs := root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	# 1. 字典映射檢查
	_test_dictionary_mappings()

	# 2. 實例化大廳並加入場景樹
	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _test_dictionary_mappings() -> void:
	print("[Check 1] 六語系字典映射檢驗")
	for loc in LOCALES:
		_set_locale(loc)
		for origin_k in EXPECTED_SPEECHES.keys():
			var exp_val: String = EXPECTED_SPEECHES[origin_k][loc]
			var act_val := ContentLoc.text("ui", origin_k)
			if act_val != exp_val:
				_fail("語系 %s 台詞 [%s] 映射不符！預期: '%s', 實際: '%s'" % [loc, origin_k, exp_val, act_val])
			if _contains_emoji(act_val):
				_fail("語系 %s 台詞 [%s] 含系統 emoji: '%s'" % [loc, origin_k, act_val])

		var exp_toast: String = EXPECTED_TOAST[loc]
		var act_toast := ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
		if act_toast != exp_toast:
			_fail("語系 %s 聚魂 toast 映射不符！預期: '%s', 實際: '%s'" % [loc, exp_toast, act_toast])
		if _contains_emoji(act_toast):
			_fail("語系 %s 聚魂 toast 含系統 emoji: '%s'" % [loc, act_toast])

		var exp_gold: String = EXPECTED_GOLD[loc]
		var act_gold := ContentLoc.text("ui", "金幣")
		if act_gold != exp_gold:
			_fail("語系 %s 金幣 映射不符！預期: '%s', 實際: '%s'" % [loc, exp_gold, act_gold])

	print("  ✓ [通過] 六語系字典完整對齊無遺漏，零系統 emoji")

func _process(_delta: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 5:
			return false
		_step = 1
		_test_gourd_card_initial_cost()
		_test_poke_speech_locales()
		_test_speech_bubble_live_locale_switch()
		_test_soul_gourd_draw_toast()
		return _finish()
	return false

func _test_gourd_card_initial_cost() -> void:
	print("[Check 2] 封靈罐卡片初次建立 CostLabel 走語系")
	_set_locale("en")
	var card_btn: Button = _lobby.call("_build_gourd_card", {"name": "Test", "cost": 80, "color": Color.WHITE}, 0)
	var cl: Label = card_btn.find_child("CostLabel", true, false) as Label
	if cl == null:
		_fail("封靈罐卡片建立後缺少 CostLabel")
	else:
		if not cl.text.begins_with("Gold 80"):
			_fail("en 語系下封靈罐初次建立 CostLabel 應為 'Gold 80'，實際: '%s'" % cl.text)
		else:
			print("  ✓ [通過] en 語系下初次建立即為 '%s'" % cl.text)
	card_btn.queue_free()

func _test_poke_speech_locales() -> void:
	print("[Check 3] 大廳點擊主角各語系氣泡台詞驗證")
	var speech_label = _lobby.get("_speech_label") as Label
	var speech_bubble = _lobby.get("_speech_bubble") as Control
	if speech_label == null or speech_bubble == null:
		_fail("找不到大廳 _speech_label 或 _speech_bubble")
		return

	var keys: Array = EXPECTED_SPEECHES.keys()
	for loc in LOCALES:
		_set_locale(loc)
		for i in range(keys.size()):
			var key: String = keys[i]
			var expected_str: String = EXPECTED_SPEECHES[key][loc]
			# 強制戳碰指定 speech index
			_lobby.call("_on_hero_clicked", 0, i)
			if speech_label.text != expected_str:
				_fail("點擊主角台詞 %d 在語系 %s 顯示錯誤！預期: '%s', 實際: '%s'" % [i, loc, expected_str, speech_label.text])
			if not speech_bubble.visible:
				_fail("點擊主角後氣泡未顯示")

	print("  ✓ [通過] 點擊主角氣泡台詞在全部六語系均精準對應")

func _test_speech_bubble_live_locale_switch() -> void:
	print("[Check 4] 氣泡顯示中切換語系即時刷新驗證")
	var speech_label = _lobby.get("_speech_label") as Label
	var speech_bubble = _lobby.get("_speech_bubble") as Control
	if speech_label == null or speech_bubble == null:
		_fail("找不到大廳 _speech_label 或 _speech_bubble")
		return

	# 先在 zh_TW 點擊主角產生台詞 2: "聽見神殿齒輪的轉動聲了嗎？"
	_set_locale("zh_TW")
	_lobby.call("_on_hero_clicked", 0, 2)
	speech_bubble.visible = true
	speech_bubble.modulate.a = 1.0

	if speech_label.text != "聽見神殿齒輪的轉動聲了嗎？":
		_fail("zh_TW 初始化台詞錯誤: %s" % speech_label.text)

	# 切換到 en
	_set_locale("en")
	if speech_label.text != "Can you hear the temple gears turning?":
		_fail("氣泡在畫面時切換至 en 未即時刷新！實際: '%s'" % speech_label.text)
	else:
		print("  ✓ 切換至 en 即時刷新為: '%s'" % speech_label.text)

	# 切換到 ja
	_set_locale("ja")
	if speech_label.text != "神殿の歯車が回る音が聞こえるかい？":
		_fail("氣泡在畫面時切換至 ja 未即時刷新！實際: '%s'" % speech_label.text)
	else:
		print("  ✓ 切換至 ja 即時刷新為: '%s'" % speech_label.text)

	# 切換到 ko
	_set_locale("ko")
	if speech_label.text != "신전 톱니바퀴가 돌아가는 소리가 들리나요?":
		_fail("氣泡在畫面時切換至 ko 未即時刷新！實際: '%s'" % speech_label.text)
	else:
		print("  ✓ 切換至 ko 即時刷新為: '%s'" % speech_label.text)

	# 切換到 es
	_set_locale("es")
	if speech_label.text != "¿Oyes el girar de los engranajes del templo?":
		_fail("氣泡在畫面時切換至 es 未即時刷新！實際: '%s'" % speech_label.text)
	else:
		print("  ✓ 切換至 es 即時刷新為: '%s'" % speech_label.text)

	print("  ✓ [通過] 氣泡顯示中即時切換語系完全同步")

func _test_soul_gourd_draw_toast() -> void:
	print("[Check 5] 聚魂完畢 toast 提示語系驗證")
	for loc in ["zh_TW", "en", "ja"]:
		_set_locale(loc)
		# 執行抽罐（idx 0, false）
		# 為了確保走到聚魂完畢分支，將 _gourd_lit 設為全 false，並呼叫 _do_gourd_draw
		# 但因 randf() 有可能走到 0.35 點亮更高階，我們多測幾次或測試 _do_gourd_draw
		var found_finish_toast := false
		for attempt in range(20):
			_lobby.call("_do_gourd_draw", 0, false)
			var toast = _lobby.get("_current_toast") as Label
			if toast and toast.text == EXPECTED_TOAST[loc]:
				found_finish_toast = true
				break
		if not found_finish_toast:
			_fail("語系 %s 下聚魂殿未觸發預期之 toast: '%s'" % [loc, EXPECTED_TOAST[loc]])
		else:
			print("  ✓ [通過] 語系 %s 觸發聚魂完畢 toast: '%s'" % [loc, EXPECTED_TOAST[loc]])

func _set_locale(code: String) -> void:
	if _loc_node:
		_loc_node.call("set_locale", code)
	else:
		ContentLoc.reload()
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")

func _contains_emoji(s: String) -> bool:
	for ch in ["⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑", "🗡", "🌀"]:
		if ch in s:
			return true
	return false

func _finish() -> bool:
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
	if _ok:
		print("=== test_lobby_poke_toast_i18n 全部通過 ===")
		print("LOBBY_POKE_TOAST_I18N_OK")
		quit(0)
		return true
	else:
		print("=== test_lobby_poke_toast_i18n 測試失敗 ===")
		print("LOBBY_POKE_TOAST_I18N_FAIL")
		quit(1)
		return true
