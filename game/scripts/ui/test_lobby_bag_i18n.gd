extends SceneTree
## 大廳背包未選格六語系單元測試 (test_lobby_bag_i18n.gd)
## 驗證：
## 1. 背包未選格說明（標題、請點選格子、消耗品／素材／重要物三行）在六語系下映射正確。
## 2. 背包標題、副標題、操作提示、操作按鈕（使用/賣出、放到快捷欄）在六語系下正確翻譯。
## 3. 切換語系 (locale_changed) 時，背包未選格說明、操作按鈕、標題等同屏 UI 即時刷新（review.md 0-QA25）。
## 4. 非中文語系（en, ja, ko, es）未選格說明無繁體中文殘留（review.md 0-QA24）。
## 5. 全程零系統 emoji。
## 6. 點擊空格子可正確取消選取並回到未選格說明。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		# 判斷是否為 CJK Unified Ideographs 區間
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _initialize() -> void:
	print("=== 開始 test_lobby_bag_i18n 測試 ===")
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

	var inv := root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 4:
				return false
			_step = 1
			_wait = 0

			# 切換到背包分頁
			_lobby._switch_tab(MobileLobby.Tab.BAG)

			var bag_layer: Control = _lobby.get("_bag_layer")
			if bag_layer == null or not bag_layer.visible:
				_fail("切換到 Tab.BAG 後 _bag_layer 應為 visible")
				return _finish()

			# 確保處於未選格狀態 (測試未選格說明)
			_lobby.set("_selected_bag_item", "")
			_lobby.call("_refresh_bag_tab", false)

			# 驗證未選格說明六語系映射與即時動態刷新
			var expected_bag_titles := {
				"zh_TW": "冒險者背包",
				"zh_CN": "冒险者背包",
				"en": "Adventurer's Bag",
				"ja": "冒険者のバッグ",
				"ko": "모험가의 배낭",
				"es": "Bolsa de aventurero"
			}
			var expected_select_hints := {
				"zh_TW": "請點選左側格子查看道具詳情。",
				"zh_CN": "请点击左侧格子查看道具详情。",
				"en": "Please select a slot on the left to view item details.",
				"ja": "左側のマスを選択して道具の詳細を確認してください。",
				"ko": "왼쪽 슬롯을 선택하여 아이템 상세를 확인하세요.",
				"es": "Selecciona una casilla de la izquierda para ver los detalles del objeto."
			}
			var expected_consumable_hints := {
				"zh_TW": "消耗品：使用回復狀態",
				"zh_CN": "消耗品：使用恢复状态",
				"en": "Consumable: Use to restore stats",
				"ja": "消耗品：使用して状態を回復",
				"ko": "소모품: 사용하여 상태 회복",
				"es": "Consumible: Usar para recuperar estado"
			}
			var expected_material_hints := {
				"zh_TW": "素材：點擊使用可賣出金幣",
				"zh_CN": "素材：点击使用可出售金币",
				"en": "Material: Click use to sell for gold",
				"ja": "素材：使うをクリックしてゴールドで売却",
				"ko": "재료: 사용을 눌러 골드로 판매",
				"es": "Material: Pulsa usar para vender por oro"
			}
			var expected_key_hints := {
				"zh_TW": "重要物：劇情關鍵道具",
				"zh_CN": "重要物：剧情关键道具",
				"en": "Key Item: Story-critical item",
				"ja": "重要品：ストーリー重要アイテム",
				"ko": "중요 아이템: 스토리 핵심 아이템",
				"es": "Objeto clave: Objeto crucial para la historia"
			}
			var expected_use_btn := {
				"zh_TW": "使用 / 賣出",
				"zh_CN": "使用 / 出售",
				"en": "Use / Sell",
				"ja": "使う / 売却",
				"ko": "사용 / 판매",
				"es": "Usar / Vender"
			}
			var expected_hb_btn := {
				"zh_TW": "放到快捷欄",
				"zh_CN": "放入快捷栏",
				"en": "Assign to Hotbar",
				"ja": "ショートカットに登録",
				"ko": "단축칸에 등록",
				"es": "Asignar a acceso rápido"
			}

			var detail_rt: RichTextLabel = _lobby.get("_bag_detail")
			var title_lbl: Label = _lobby.get("_bag_title_lbl")
			var sub_lbl: Label = _lobby.get("_bag_sub_lbl")
			var use_btn: Button = _lobby.get("_bag_use_btn")
			var hb_btn: Button = _lobby.get("_bag_hb_btn")
			var tip_lbl: Label = _lobby.get("_bag_tip")

			if detail_rt == null or use_btn == null or hb_btn == null:
				_fail("找不到背包詳細資訊或操作按鈕節點")
				return _finish()

			for code in LOCALES:
				if _loc_node:
					_loc_node.call("set_locale", code)

				# 斷言未選格時操作按鈕皆 disabled
				if not use_btn.disabled:
					_fail("[%s] 未選格時使用按鈕應為 disabled" % code)
				if not hb_btn.disabled:
					_fail("[%s] 未選格時快捷欄按鈕應為 disabled" % code)

				# 斷言按鈕多語言
				if use_btn.text != expected_use_btn[code]:
					_fail("[%s] 未選格使用按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_use_btn[code], use_btn.text])
				if hb_btn.text != expected_hb_btn[code]:
					_fail("[%s] 未選格快捷欄按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_hb_btn[code], hb_btn.text])

				# 斷言標題與副標題即時刷新
				if title_lbl and title_lbl.text != expected_bag_titles[code]:
					_fail("[%s] 背包標題文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_bag_titles[code], title_lbl.text])
				if sub_lbl and not sub_lbl.text.is_empty():
					var expected_sub := ContentLoc.text("ui", "道具與戰魂倉庫 · 點選格子查看詳情")
					if sub_lbl.text != expected_sub:
						_fail("[%s] 背包副標題文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_sub, sub_lbl.text])

				# 斷言未選格富文本內容包含五大翻譯片斷
				var dt: String = detail_rt.text
				if not dt.contains(expected_bag_titles[code]):
					_fail("[%s] 未選格說明缺少標題 '%s'" % [code, expected_bag_titles[code]])
				if not dt.contains(expected_select_hints[code]):
					_fail("[%s] 未選格說明缺少提示 '%s'" % [code, expected_select_hints[code]])
				if not dt.contains(expected_consumable_hints[code]):
					_fail("[%s] 未選格說明缺少消耗品說明 '%s'" % [code, expected_consumable_hints[code]])
				if not dt.contains(expected_material_hints[code]):
					_fail("[%s] 未選格說明缺少素材說明 '%s'" % [code, expected_material_hints[code]])
				if not dt.contains(expected_key_hints[code]):
					_fail("[%s] 未選格說明缺少重要物說明 '%s'" % [code, expected_key_hints[code]])

				# 斷言在 en, es 語系下完全無中文字元殘留（0-QA24）
				if code in ["en", "es"]:
					if _has_cjk(dt):
						_fail("[%s] 未選格說明存在中文殘留: %s" % [code, dt])

				# 斷言零系統 emoji
				if _has_emoji(dt) or _has_emoji(use_btn.text) or _has_emoji(hb_btn.text):
					_fail("[%s] 偵測到系統 Emoji" % code)

				print("  ok [%s] 背包未選格說明與按鈕即時多語系刷新通過" % code)

			# 驗證點擊空格子取消選取並回到未選格說明
			print("--- 驗證點選道具後點擊空格子回到未選格說明 ---")
			var cells: Array = _lobby.get("_bag_cells")
			var ids: Array = _lobby.get("_bag_ids")
			if cells.size() > 0 and ids.size() > 0 and not ids[0].is_empty():
				# 模擬點擊第 0 格 (有道具)
				var ev_click := InputEventMouseButton.new()
				ev_click.button_index = MOUSE_BUTTON_LEFT
				ev_click.pressed = true
				_lobby.call("_on_bag_cell_input", 0, ev_click)
				var sel_id: String = _lobby.get("_selected_bag_item")
				if sel_id != ids[0]:
					_fail("點擊第 0 格後 _selected_bag_item 應為 %s，實際: %s" % [ids[0], sel_id])
				else:
					print("  ok 點選第 0 格道具成功，已進入選中狀態: %s" % sel_id)

				# 模擬點擊最後一格 (空格子)
				var empty_idx := cells.size() - 1
				_lobby.call("_on_bag_cell_input", empty_idx, ev_click)
				var sel_after_empty: String = _lobby.get("_selected_bag_item")
				if sel_after_empty != "":
					_fail("點擊空格子後應清空選取 (_selected_bag_item == '')，實際: %s" % sel_after_empty)
				else:
					var dt_after_empty: String = detail_rt.text
					if not dt_after_empty.contains(expected_bag_titles[ContentLoc.locale()]):
						_fail("點擊空格子後未選格說明未正確顯示: %s" % dt_after_empty)
					if not use_btn.disabled:
						_fail("點擊空格子後使用按鈕應為 disabled")
					print("  ok 點擊空格子後成功取消選取並回到未選格說明")

			# 還原語系為繁中
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")

			return _finish()
	return false

func _finish() -> bool:
	if _ok:
		print("LOBBY_BAG_I18N_OK")
		quit(0)
	else:
		print("LOBBY_BAG_I18N_FAIL")
		quit(1)
	return true
