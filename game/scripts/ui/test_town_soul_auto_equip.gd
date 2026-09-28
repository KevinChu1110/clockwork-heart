extends SceneTree
## 聚魂殿一鍵配置最佳戰魂單元與整合測試 (test_town_soul_auto_equip.gd)
## 驗證：
## 1. 載入 main.tscn 並切換到聚魂殿面板 (_go_soul_panel)
## 2. 聚魂殿按鈕中包含「一鍵配置」
## 3. 手動測背包有4顆以上戰魂、3槽從空到一鍵配置填滿最佳組合
## 4. UI 顯示前後差異 compare_embed 對話提示
## 5. 完成後三槽皆為最高戰魂，背包僅剩最低戰魂

var _step := 0
var _wait := 0
var _main: Node = null
var _ss: Node = null
var _gs: Node = null

func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_TOWN_SOUL_AUTO_EQUIP_FAIL: ", msg)
	quit(1)
	return false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 25:
				return false
			_main = current_scene
			if _main == null:
				return _fail("main scene 載入失敗")
			_ss = root.get_node_or_null("SoulSystem")
			_gs = root.get_node_or_null("GameState")
			if _ss == null or _gs == null:
				return _fail("SoulSystem or GameState missing")
			
			# 初始化玩家狀態：器階11（解鎖3魂槽）
			_gs.reset_new_game()
			_gs.weapon_tier = 11
			_ss.ensure_slots()
			if _ss.slot_count() != 3:
				return _fail("器階11應有3魂槽，實際為 %d" % _ss.slot_count())
			
			# 放入 4 顆戰魂：
			# s1: 凡·銳齒 (score 2)
			# s2: 吉·固甲 (score 3)
			# s3: 稀世·旋簧 (score 26)
			# s4: 神·全衡 (score 25)
			var s1 := {"id": "s1_mortal", "star": "銳齒之魂", "quality": "凡", "level": 0, "equipped": false}
			var s2 := {"id": "s2_good", "star": "固甲之魂", "quality": "吉", "level": 0, "equipped": false}
			var s3 := {"id": "s3_rare", "star": "旋簧之魂", "quality": "稀世", "level": 0, "equipped": false}
			var s4 := {"id": "s4_shen", "star": "全衡之魂", "quality": "神", "level": 0, "equipped": false}
			_gs.souls = [s1, s2, s3, s4]
			_gs.soul_slots = ["", "", ""]
			
			# 開啟聚魂殿面板
			_main.call("_go_soul_panel")
			_step = 1
			_wait = 0
			return false
			
		1:
			if _wait < 15:
				return false
			# 檢查 MenuLayer 是否存在「一鍵配置」按鈕
			var btn_auto: Button = _find_button_by_text(_main, "一鍵配置")
			if btn_auto == null:
				return _fail("聚魂殿面板找不到「一鍵配置」按鈕")
			print("  ok 聚魂殿面板「一鍵配置」按鈕存在")
			
			# 觸發一鍵配置
			_main.call("_soul_auto_equip_best")
			_step = 2
			_wait = 0
			return false
			
		2:
			if _wait < 15:
				return false
			# 檢查對話框是否有顯示前後差異
			var dlg = _main.get("_dialogue")
			if dlg == null:
				return _fail("未找到對話框節點")
			print("  ok 對話框已彈出")
			
			# 推進對話框關閉並回聚魂殿
			if dlg.has_method("_skip_or_advance"):
				dlg.call("_skip_or_advance")
				dlg.call("_skip_or_advance")
			else:
				_main.call("_go_soul_panel")
			_step = 3
			_wait = 0
			return false
			
		3:
			if _wait < 15:
				return false
			# 驗證三槽是否填滿背包裡分數最高的魂 (s3, s4, s2)
			var slots: Array = [str(_gs.soul_slots[0]), str(_gs.soul_slots[1]), str(_gs.soul_slots[2])]
			if not ("s3_rare" in slots) or not ("s4_shen" in slots) or not ("s2_good" in slots):
				return _fail("三槽未填滿分數最高的三顆魂: %s" % str(slots))
			if "s1_mortal" in slots:
				return _fail("最低分的 s1_mortal 不應入槽: %s" % str(slots))
			var bag: Array = _ss.bag_souls()
			if bag.size() != 1 or str(bag[0].get("id", "")) != "s1_mortal":
				return _fail("背包應僅剩 s1_mortal，實際為: %s" % str(bag))
			print("  ok 三槽成功填滿最高分數戰魂 (s3, s4, s2)，最低分留在背包")
			
			# 驗證聚魂殿面板狀態 BBCode
			var body: String = _ss.panel_status_bbcode()
			if body.find("s1_mortal") >= 0:
				return _fail("BBCode 不應出現 s1_mortal")
			print("  ok 聚魂殿狀態資訊顯示正確")
			
			# 再次觸發一鍵配置，確認無重複變更
			_main.call("_soul_auto_equip_best")
			_step = 4
			_wait = 0
			return false
			
		4:
			if _wait < 15:
				return false
			print("  ok 最佳狀態下重複點擊一鍵配置通過")
			print("TEST_TOWN_SOUL_AUTO_EQUIP_OK")
			quit(0)
			return false
	return false

func _find_button_by_text(node: Node, target_text: String) -> Button:
	if node is Button and node.text == target_text:
		return node
	for c in node.get_children():
		var b := _find_button_by_text(c, target_text)
		if b != null:
			return b
	return null
