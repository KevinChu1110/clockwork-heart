extends SceneTree
## 神殿黑曜石大廳改版測試：四大殿堂卡片、白兔 Poke 點擊粒子、腳底軟影節點
## godot --headless -s res://scripts/ui/test_mobile_lobby.gd

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Node = null

const FORBIDDEN_SYMBOLS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
]


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.level = 10
		gs.gold = 50000
		gs.energy = 15

	var Lobby := load("res://scripts/ui/mobile_lobby.gd")
	if Lobby == null:
		_fail("無法加載 res://scripts/ui/mobile_lobby.gd")
		_finish()
		return

	_lobby = Lobby.new()
	root.add_child(_lobby)


func _process(_d: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 8:
			return false
		_step = 1
		_test_hall_cards()
		_test_soft_shadow()
		_test_hero_click_and_particles()
		_test_hero_nameplate()
		_test_hero_race_poses()
		return _finish()
	return false


func _find_named(n: Node, target_name: String) -> Node:
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null


func _has_forbidden_symbols_or_emoji(text: String) -> bool:
	for sym in FORBIDDEN_SYMBOLS:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		# 雜項符號與 Dingbats (0x2600-0x27BF) 以及 Emoji 區域 (0x1F300-0x1FAFF)
		if (cp >= 0x2600 and cp <= 0x27BF) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


## ──────────────────────────────────────────
## 1. 斷言 _add_hall_card 四張黑曜石浮雕卡片
## ──────────────────────────────────────────
func _test_hall_cards() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("大廳節點無效，無法測試殿堂卡片")
		return

	if not _lobby.has_method("_add_hall_card"):
		_fail("大廳缺少 _add_hall_card 方法")
	else:
		print("  ok 大廳具備 _add_hall_card 方法")

	# 1.1 抓取四大殿堂卡片按鈕
	var cards: Array[Button] = []
	var group_nodes := _lobby.get_tree().get_nodes_in_group("hall_cards")
	for n in group_nodes:
		if n is Button:
			cards.append(n as Button)

	if cards.is_empty():
		# 從村莊層 (_village_layer) 內的容器中尋找殿堂卡片按鈕群
		var village = _lobby.get("_village_layer") as Node
		if village != null:
			for child in village.get_children():
				if child is VBoxContainer:
					var btns: Array[Button] = []
					for sub in child.get_children():
						if sub is Button:
							btns.append(sub as Button)
					if btns.size() == 4:
						cards = btns
						break

	print("  [殿堂卡片] 找到卡片數量: %d" % cards.size())
	if cards.size() != 4:
		_fail("殿堂卡片數量應為 4，實際取得: %d" % cards.size())
		return
	else:
		print("  ok 殿堂卡片數量正確 (4 張)")

	# 1.2 斷言四張卡片的標題關鍵字、圖示格文字，以及無 Emoji / 符號
	var expected_cards := [
		{"keyword": "鐵匠", "full_title": "王都鐵匠", "icon": "鐵"},
		{"keyword": "工坊", "full_title": "手藝工坊", "icon": "工"},
		{"keyword": "演武", "full_title": "演武競技", "icon": "武"},
		{"keyword": "委託", "full_title": "冒險委託", "icon": "委"},
	]

	for i in range(cards.size()):
		var card := cards[i]
		if card == null:
			_fail("第 %d 張殿堂卡不是 Button" % (i + 1))
			continue

		var exp_info: Dictionary = expected_cards[i]
		var found_title := ""
		var found_subtitle := ""
		var found_icon := ""

		# 從 meta 或子節點中抽取標題與圖示格文字
		if card.has_meta("hall_title"):
			found_title = str(card.get_meta("hall_title"))
		if card.has_meta("hall_subtitle"):
			found_subtitle = str(card.get_meta("hall_subtitle"))
		if card.has_meta("hall_icon"):
			found_icon = str(card.get_meta("hall_icon"))

		# 遍歷子節點尋找 Label
		if found_title.is_empty() or found_icon.is_empty():
			var labels: Array[Label] = []
			_collect_labels(card, labels)
			for lbl in labels:
				var t := lbl.text.strip_edges()
				if t.length() == 1:
					found_icon = t
				elif t.find("·") >= 0 or t.find("裝備") >= 0 or t.find("熔煉") >= 0 or t.find("抽獎") >= 0 or t.find("領獎") >= 0:
					found_subtitle = t
				elif t.length() >= 2 and found_title.is_empty():
					found_title = t

		print("  [殿堂卡片 %d] 標題: 「%s」, 圖示: 「%s」, 副標題: 「%s」" % [i + 1, found_title, found_icon, found_subtitle])

		# 斷言標題內容
		var want_keyword: String = exp_info["keyword"]
		if found_title.find(want_keyword) < 0:
			_fail("卡片 %d 標題應含「%s」，實際為「%s」" % [i + 1, want_keyword, found_title])
		else:
			print("  ok 卡片 %d 標題符合「%s」" % [i + 1, want_keyword])

		# 斷言圖示格內容
		var want_icon: String = exp_info["icon"]
		if found_icon != want_icon:
			_fail("卡片 %d 圖示應為「%s」，實際為「%s」" % [i + 1, want_icon, found_icon])
		else:
			print("  ok 卡片 %d 圖示符合「%s」" % [i + 1, want_icon])

		# 斷言無 Emoji 與系統字型符號 (t_76f84d91 回歸防線)
		if _has_forbidden_symbols_or_emoji(found_title):
			_fail("卡片 %d 標題含有禁止符號或 Emoji：「%s」" % [i + 1, found_title])
		if _has_forbidden_symbols_or_emoji(found_subtitle):
			_fail("卡片 %d 副標題含有禁止符號或 Emoji：「%s」" % [i + 1, found_subtitle])
		if _has_forbidden_symbols_or_emoji(found_icon):
			_fail("卡片 %d 圖示含有禁止符號或 Emoji：「%s」" % [i + 1, found_icon])

	print("  ok 殿堂卡片無 Emoji、無字型殘留符號回歸防線通過")

	# 1.3 斷言點擊卡片開啟真畫面，而非僅跳 toast (review.md 第 28、29 條)
	_test_hall_card_real_screens(cards)


## ──────────────────────────────────────────
## 1.3 斷言三張殿堂卡片點擊會開啟手遊規範真畫面彈窗
## ──────────────────────────────────────────
func _test_hall_card_real_screens(cards: Array[Button]) -> void:
	# A. 王都鐵匠
	cards[0].pressed.emit()
	var forge_dlg = _lobby.get_node_or_null("ForgeDialog")
	if forge_dlg == null or not is_instance_valid(forge_dlg):
		_fail("點擊王都鐵匠未開啟 ForgeDialog 真畫面")
	else:
		print("  ok 點擊王都鐵匠成功開啟 ForgeDialog")
		var card = _find_named(forge_dlg, "ForgeCard") as Control
		if card == null:
			_fail("ForgeDialog 缺少 ForgeCard 節點")
		else:
			var w: float = card.custom_minimum_size.x
			if w < 740.0 or w > 760.0:
				_fail("ForgeCard 寬度 %.1f 不符合橫屏彈窗 740~760px 規範" % w)
			else:
				print("  ok ForgeCard 寬度符合手遊彈窗規範 (%.1f px)" % w)

		var close_btn = _find_named(forge_dlg, "CloseBtn") as Button
		if close_btn == null or close_btn.text != "✕":
			_fail("ForgeDialog 缺少右上「✕」關閉按鈕")
		else:
			print("  ok ForgeDialog 具備右上「✕」關閉按鈕")

		var pity_row = _find_named(forge_dlg, "PityBarRow")
		if pity_row == null or pity_row.get_child_count() != 3:
			_fail("ForgeDialog 缺少連敗保底 3 格進度條")
		else:
			print("  ok ForgeDialog 具備鍛造連敗保底 3 格進度條")

		var btn_forge = _find_named(forge_dlg, "BtnForge") as Button
		if btn_forge == null or btn_forge.custom_minimum_size.y < 50.0:
			_fail("ForgeDialog 鍛造按鈕高度小於 50px")
		else:
			print("  ok ForgeDialog 鍛造按鈕高度符合防誤觸規範 (>=50px)")

		forge_dlg._on_close()
		if not forge_dlg.is_queued_for_deletion():
			_fail("ForgeDialog 關閉失敗 (未標記 queue_free)")
		else:
			print("  ok ForgeDialog 成功關閉 (已標記 queue_free)")

	# B. 手藝工坊
	cards[1].pressed.emit()
	var gem_dlg = _lobby.get_node_or_null("GemWorkshopDialog")
	if gem_dlg == null or not is_instance_valid(gem_dlg):
		_fail("點擊手藝工坊未開啟 GemWorkshopDialog 真畫面")
	else:
		print("  ok 點擊手藝工坊成功開啟 GemWorkshopDialog")
		var card = _find_named(gem_dlg, "GemWorkshopCard") as Control
		if card == null:
			_fail("GemWorkshopDialog 缺少 GemWorkshopCard 節點")
		else:
			var w: float = card.custom_minimum_size.x
			if w < 740.0 or w > 760.0:
				_fail("GemWorkshopCard 寬度 %.1f 不符合橫屏彈窗 740~760px 規範" % w)
			else:
				print("  ok GemWorkshopCard 寬度符合手遊彈窗規範 (%.1f px)" % w)

		var close_btn = _find_named(gem_dlg, "CloseBtn") as Button
		if close_btn == null or close_btn.text != "✕":
			_fail("GemWorkshopDialog 缺少右上「✕」關閉按鈕")
		else:
			print("  ok GemWorkshopDialog 具備右上「✕」關閉按鈕")

		var tab_smelt = _find_named(gem_dlg, "TabSmeltBtn") as Button
		var tab_case = _find_named(gem_dlg, "TabCaseBtn") as Button
		if tab_smelt == null or tab_case == null:
			_fail("GemWorkshopDialog 缺少熔煉或寶石櫃分頁按鈕")
		else:
			print("  ok GemWorkshopDialog 具備熔煉與寶石櫃分頁切換功能")

		gem_dlg._on_close()
		if not gem_dlg.is_queued_for_deletion():
			_fail("GemWorkshopDialog 關閉失敗 (未標記 queue_free)")
		else:
			print("  ok GemWorkshopDialog 成功關閉 (已標記 queue_free)")

	# C. 冒險委託
	cards[3].pressed.emit()
	var windup_dlg = _lobby.get_node_or_null("WindupDailyDialog")
	if windup_dlg == null or not is_instance_valid(windup_dlg):
		_fail("點擊冒險委託未開啟 WindupDailyDialog 真畫面")
	else:
		print("  ok 點擊冒險委託成功開啟 WindupDailyDialog")
		var card = _find_named(windup_dlg, "WindupDailyCard") as Control
		if card == null:
			_fail("WindupDailyDialog 缺少 WindupDailyCard 節點")
		else:
			var w: float = card.custom_minimum_size.x
			if w < 740.0 or w > 760.0:
				_fail("WindupDailyCard 寬度 %.1f 不符合橫屏彈窗 740~760px 規範" % w)
			else:
				print("  ok WindupDailyCard 寬度符合手遊彈窗規範 (%.1f px)" % w)

		var close_btn = _find_named(windup_dlg, "CloseBtn") as Button
		if close_btn == null or close_btn.text != "✕":
			_fail("WindupDailyDialog 缺少右上「✕」關閉按鈕")
		else:
			print("  ok WindupDailyDialog 具備右上「✕」關閉按鈕")

		var case_title = _find_named(windup_dlg, "CaseTitle") as Label
		var case_desc = _find_named(windup_dlg, "CaseDesc") as Label
		if case_title == null or case_title.text.is_empty() or case_desc == null:
			_fail("WindupDailyDialog 缺少當日個案標題或說明")
		else:
			print("  ok WindupDailyDialog 顯示當日個案：「%s」" % case_title.text)

		# 測試個案選項與獎勵領取流程
		var choices_box = _find_named(windup_dlg, "ChoicesBox")
		if choices_box == null:
			_fail("WindupDailyDialog 缺少選項容器")
		else:
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			if ws != null and ws.has_method("is_ready") and ws.call("is_ready"):
				var choice_btns: Array[Button] = []
				for ch in choices_box.get_children():
					if ch is Button and not ch.disabled:
						choice_btns.append(ch as Button)
				if choice_btns.size() < 2:
					_fail("未完成的當日個案應提供至少 2 個選項，實際取得: %d" % choice_btns.size())
				else:
					print("  ok 當日個案提供 %d 個可選行動選項" % choice_btns.size())
					for cb in choice_btns:
						if cb.custom_minimum_size.y < 50.0:
							_fail("委託選項按鈕高度小於 50px: %s" % cb.text)
					# 點擊第一個選項完成委託
					choice_btns[0].pressed.emit()
					if not ws.call("is_done_today"):
						_fail("點擊選項後委託未標記為今日已完成")
					else:
						print("  ok 成功完成委託並領取獎勵，當日狀態切換為已完成")

		windup_dlg._on_close()
		if not windup_dlg.is_queued_for_deletion():
			_fail("WindupDailyDialog 關閉失敗 (未標記 queue_free)")
		else:
			print("  ok WindupDailyDialog 成功關閉 (已標記 queue_free)")



func _collect_labels(n: Node, out: Array[Label]) -> void:
	if n is Label:
		out.append(n as Label)
	for c in n.get_children():
		_collect_labels(c, out)


## ──────────────────────────────────────────
## 2. 斷言腳底接地軟影節點 (Foot Soft Shadow / 第16條規範)
## ──────────────────────────────────────────
func _test_soft_shadow() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("大廳節點無效，無法測試軟影節點")
		return

	# 2.1 依變數名 _hero_shadow 抓取
	var hero_shadow = _lobby.get("_hero_shadow") as TextureRect
	if hero_shadow == null:
		_fail("大廳缺少 _hero_shadow 變數或該節點為 null")
	else:
		print("  ok 成功依變數名取得 _hero_shadow")
		if not hero_shadow.is_inside_tree():
			_fail("_hero_shadow 未掛載於場景樹內")
		if not hero_shadow.visible:
			_fail("_hero_shadow.visible 應為 true，實際為 false")
		if hero_shadow.modulate.a <= 0.0 or hero_shadow.self_modulate.a <= 0.0:
			_fail("_hero_shadow alpha 應大於 0，得 modulate.a=%.2f self_modulate.a=%.2f" % [
				hero_shadow.modulate.a, hero_shadow.self_modulate.a
			])
		else:
			print("  ok _hero_shadow 可見度與 alpha 正確 (visible=true, alpha=%.2f)" % hero_shadow.modulate.a)

		if hero_shadow.texture == null:
			_fail("_hero_shadow 缺少貼圖 (texture 為 null)")
		elif hero_shadow.texture.get_width() <= 0 or hero_shadow.texture.get_height() <= 0:
			_fail("_hero_shadow 貼圖尺寸異常: %s" % str(hero_shadow.texture.get_size()))
		else:
			print("  ok _hero_shadow 貼圖存在且尺寸正常 (%dx%d)" % [
				hero_shadow.texture.get_width(), hero_shadow.texture.get_height()
			])
			# 驗證貼圖來源即為 _soft_shadow_tex()
			var LobbyClass := load("res://scripts/ui/mobile_lobby.gd")
			if LobbyClass != null and LobbyClass.has_method("_soft_shadow_tex"):
				var expected_tex = LobbyClass._soft_shadow_tex()
				if hero_shadow.texture != expected_tex:
					_fail("_hero_shadow.texture 應來自 _soft_shadow_tex()")
				else:
					print("  ok _hero_shadow 貼圖確認由 _soft_shadow_tex() 生成")

	# 2.2 依節點名稱 HeroFootShadow 於樹中抓取
	var shadow_by_name := _find_named(_lobby, "HeroFootShadow") as TextureRect
	if shadow_by_name == null:
		_fail("場景樹中找不到名稱為「HeroFootShadow」的節點")
	else:
		print("  ok 場景樹中存在名為「HeroFootShadow」的軟影節點")

	# 2.3 檢查場景樹中軟影群組或閉塞陰影節點
	var contact_shadow := _find_named(_lobby, "HeroContactShadow") as TextureRect
	if contact_shadow != null:
		print("  ok 場景樹中存在接觸陰影節點 HeroContactShadow")
		if contact_shadow.modulate.a <= 0.0:
			_fail("HeroContactShadow modulate.a 應大於 0")

	var shadow_group := _lobby.get_tree().get_nodes_in_group("soft_shadow")
	if not shadow_group.is_empty():
		print("  ok soft_shadow 群組節點數: %d" % shadow_group.size())
		for s in shadow_group:
			var ci := s as CanvasItem
			if ci != null and ci.modulate.a <= 0.0:
				_fail("軟影群組節點 %s modulate.a 應大於 0" % ci.name)


## ──────────────────────────────────────────
## 3. 斷言 _on_hero_clicked 呼叫後 _burst_click_particles 產生粒子節點
## ──────────────────────────────────────────
func _test_hero_click_and_particles() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("大廳節點無效，無法測試白兔 Poke 點擊")
		return

	# 3.1 取得點擊前的粒子數量
	var before_count := _count_burst_particles()

	# 3.2 呼叫 _on_hero_clicked
	if not _lobby.has_method("_on_hero_clicked"):
		_fail("大廳缺少 _on_hero_clicked 方法")
		return

	_lobby.call("_on_hero_clicked")

	# 3.3 取得點擊後的粒子數量
	var after_count := _count_burst_particles()
	var spawned := after_count - before_count
	print("  [Poke 點擊] 產生星芒粒子數量: %d (前=%d, 後=%d)" % [spawned, before_count, after_count])

	if spawned <= 0:
		_fail("_on_hero_clicked 呼叫後未產生任何粒子節點 (spawned=%d)" % spawned)
	else:
		print("  ok _burst_click_particles 確實產生粒子節點 (共 %d 個)" % spawned)

	# 3.4 驗證粒子節點屬性（存在、在場景樹中、顏色或尺寸正常）
	var particles := _get_burst_particle_nodes()
	for p in particles:
		if not p.is_inside_tree():
			_fail("粒子節點 %s 不在場景樹內" % p.name)

	# 3.5 驗證對話氣泡與互動旗標
	var is_interacting = _lobby.get("_is_interacting")
	if is_interacting != true:
		_fail("點擊白兔後 _is_interacting 應為 true")
	else:
		print("  ok 白兔進入互動狀態 (_is_interacting=true)")

	var bubble = _lobby.get("_speech_bubble") as Control
	if bubble == null or not bubble.visible:
		_fail("點擊白兔後對話氣泡 _speech_bubble 應為可見 (visible=true)")
	else:
		print("  ok 對話氣泡可見")


func _count_burst_particles() -> int:
	return _get_burst_particle_nodes().size()


func _get_burst_particle_nodes() -> Array[Node]:
	var result: Array[Node] = []
	# 優先從 group 抓取
	var from_group := _lobby.get_tree().get_nodes_in_group("burst_particles")
	if not from_group.is_empty():
		for n in from_group:
			if is_instance_valid(n):
				result.append(n)
		return result

	# 後備：尋找 _lobby 底下所有旋轉約 45 度、尺寸 6x6 的 ColorRect 粒子
	for c in _lobby.get_children():
		if c is ColorRect and is_instance_valid(c):
			var cr := c as ColorRect
			if cr.name.begins_with("BurstParticle") or is_equal_approx(cr.size.x, 6.0):
				result.append(cr)
	return result


## ──────────────────────────────────────────
## 4. 斷言英雄頭頂名牌位置（上移避開齒輪核心）與主次文字層級
## ──────────────────────────────────────────
func _test_hero_nameplate() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("大廳節點無效，無法測試頭頂名牌")
		return

	var name_tag = _lobby.get("_hero_name_tag") as Label
	if name_tag == null or not is_instance_valid(name_tag):
		_fail("大廳缺少 _hero_name_tag 節點")
		return

	var tag_vbox := name_tag.get_parent() as VBoxContainer
	if tag_vbox == null:
		_fail("_hero_name_tag 未置於 VBoxContainer 容器內")
		return

	var tag_panel := tag_vbox.get_parent() as PanelContainer
	if tag_panel == null:
		_fail("名牌 VBoxContainer 未置於 PanelContainer 底襯內")
		return

	# 4.1 驗證名牌已上移，避開齒輪核心 (offset_top 應 <= -140)
	print("  [名牌位置] offset_top: %.1f, offset_bottom: %.1f" % [tag_panel.offset_top, tag_panel.offset_bottom])
	if tag_panel.offset_top > -140.0:
		_fail("名牌 offset_top 應 <= -140.0 以避開齒輪核心，實際為 %.1f" % tag_panel.offset_top)
	else:
		print("  ok 名牌位置已成功上移避開齒輪核心區 (offset_top=%.1f)" % tag_panel.offset_top)

	# 4.2 驗證標籤互換：角色名應為第一個子節點，稱號為第二個子節點
	var children := tag_vbox.get_children()
	if children.size() < 2:
		_fail("名牌容器子節點數量應至少為 2 (角色名與稱號)")
		return

	if children[0] != name_tag:
		_fail("名牌首項應為角色名標籤 (_hero_name_tag)，以突出角色主體")
	else:
		print("  ok 名牌首項為角色名標籤")

	var title_tag: Label = null
	for c in children:
		if c != name_tag and c is Label:
			title_tag = c as Label
			break

	if title_tag == null:
		_fail("名牌容器內未找到稱號 Label")
		return

	# 4.3 驗證字級主次層級：角色名 >= 18px，稱號 <= 14px
	var name_size: int = name_tag.get_theme_font_size("font_size")
	var title_size: int = title_tag.get_theme_font_size("font_size")
	print("  [字級層級] 角色名: %d px, 稱號: %d px" % [name_size, title_size])
	if name_size < 18:
		_fail("角色名字級應加大 (>= 18px)，實際為 %d px" % name_size)
	elif title_size > 14:
		_fail("稱號字級應縮小 (<= 14px) 以降低權重，實際為 %d px" % title_size)
	elif name_size <= title_size:
		_fail("角色名字級 (%d px) 應大於稱號字級 (%d px)" % [name_size, title_size])
	else:
		print("  ok 角色名與稱號字級主次層級正確 (角色名 %d px > 稱號 %d px)" % [name_size, title_size])

	# 4.4 驗證色彩主次
	var name_color: Color = name_tag.get_theme_color("font_color")
	print("  [文字顏色] 角色名顏色: %s, 稱號顏色: %s" % [str(name_color), str(title_tag.get_theme_color("font_color"))])


## ──────────────────────────────────────────
## 5. 斷言大廳各族真戰鬥姿態（非兔族戳碰非同一張底圖，review.md 第 4b）
## ──────────────────────────────────────────
func _test_hero_race_poses() -> void:
	if _lobby == null or not is_instance_valid(_lobby):
		_fail("大廳節點無效，無法測試各族戰鬥姿態")
		return

	var gs := root.get_node_or_null("GameState")
	if gs == null:
		_fail("無法取得 GameState 單例")
		return

	var races := ["rabbit", "lion", "fox", "macaque", "boar"]
	for r in races:
		gs.player_race = r
		gs.paperdoll_slots = {}
		_lobby._load_hero_poses()

		var tex_idle: Texture2D = _lobby.get("_tex_idle")
		var tex_attack: Texture2D = _lobby.get("_tex_attack")
		var tex_skill: Texture2D = _lobby.get("_tex_skill")
		var tex_telegraph: Texture2D = _lobby.get("_tex_telegraph")
		var tex_recover: Texture2D = _lobby.get("_tex_recover")
		var tex_hit: Texture2D = _lobby.get("_tex_hit")

		if tex_idle == null:
			_fail("種族 %s 之 _tex_idle 為空" % r)
		if tex_attack == null:
			_fail("種族 %s 之 _tex_attack 為空" % r)
		if tex_skill == null:
			_fail("種族 %s 之 _tex_skill 為空" % r)
		if tex_telegraph == null:
			_fail("種族 %s 之 _tex_telegraph 為空" % r)
		if tex_recover == null:
			_fail("種族 %s 之 _tex_recover 為空" % r)
		if tex_hit == null:
			_fail("種族 %s 之 _tex_hit 為空" % r)

		if r == "rabbit":
			# 兔族回歸：attack 應指向 poses/attack.png
			if tex_attack.resource_path != "res://assets/sprites/player/poses/attack.png":
				_fail("兔族 _tex_attack 路徑非 res://assets/sprites/player/poses/attack.png: %s" % tex_attack.resource_path)
			else:
				print("  ok 兔族回歸：_tex_attack 指向既有 poses/attack.png")

		# 驗證動作變數不可全指向同一張 Texture2D (review.md 第 4b)
		if tex_idle == tex_attack and tex_attack == tex_skill and tex_skill == tex_recover:
			_fail("種族 %s 之所有動作變數指向同一張貼圖，違反 review.md 第 4b 條" % r)
		else:
			print("  ok 種族 %s 各動作姿態非同一張貼圖" % r)

		# 像素比較：idle 與 attack 必須有非零差異
		var img_idle: Image = tex_idle.get_image()
		var img_atk: Image = tex_attack.get_image()
		if img_idle == null or img_atk == null:
			_fail("種族 %s 無法取得貼圖 Image" % r)
			continue

		var diff_count := 0
		var w := mini(img_idle.get_width(), img_atk.get_width())
		var h := mini(img_idle.get_height(), img_atk.get_height())
		for y in h:
			for x in w:
				if img_idle.get_pixel(x, y) != img_atk.get_pixel(x, y):
					diff_count += 1
		if diff_count == 0:
			_fail("種族 %s 之 _tex_idle 與 _tex_attack 像素完全相同 (diff=0)，未載入真姿態！" % r)
		else:
			print("  ok 種族 %s idle vs attack 像素差異非零 (差異像素數: %d)" % [r, diff_count])

	# 測試換裝槽位影響待機預覽，但戳碰仍為真戰鬥姿態
	gs.player_race = "lion"
	gs.paperdoll_slots = {"costume": "costume_nutcracker_guard"}
	_lobby._load_hero_poses()
	var lion_costumed_idle: Texture2D = _lobby.get("_tex_idle")
	var lion_costumed_atk: Texture2D = _lobby.get("_tex_attack")
	if lion_costumed_idle == lion_costumed_atk:
		_fail("獅子裝備換裝後，_tex_attack 與 _tex_idle 變成同一張合成圖，未維持真戰鬥姿態！")
	else:
		print("  ok 獅子有換裝槽時，_tex_attack 仍維持真姿態，未被合成圖覆蓋")

	# 測試完恢復預設
	gs.player_race = "rabbit"
	gs.paperdoll_slots = {}
	_lobby._load_hero_poses()


func _finish() -> bool:
	if _ok:
		print("MOBILE_LOBBY_OK")
		quit(0)
	else:
		print("MOBILE_LOBBY_FAIL")
		quit(1)
	return true
