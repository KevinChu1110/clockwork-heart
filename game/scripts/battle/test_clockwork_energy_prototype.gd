extends SceneTree
## 無頭測試：戰鬥原型 - 發條能量條分配機制
## 驗證：共用能量累積、四職業技能消耗、手動分配、逾時自動智慧分配（永不卡關）、UI 初始化
## 執行指令：godot --headless -s res://scripts/battle/test_clockwork_energy_prototype.gd

const ClockworkEnergyPrototype = preload("res://scripts/battle/clockwork_energy_prototype.gd")
const ClockworkEnergyView = preload("res://scripts/ui/clockwork_energy_view.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error("FAIL: " + msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始測試：發條能量條分配原型 ===")

	_test_initialization()
	_test_manual_allocation()
	_test_auto_allocation_timeout_prevention()
	_test_stress_battle_flow()
	_test_ui_instantiation()

	if _ok:
		print("=== 所有發條能量原型測試通過 ===")
		print("CLOCKWORK_ENERGY_PROTOTYPE_OK")
		quit(0)
	else:
		print("=== 測試未通過 ===")
		print("CLOCKWORK_ENERGY_PROTOTYPE_FAIL")
		quit(1)


## 1. 基礎初始化測試
func _test_initialization() -> void:
	var sim := ClockworkEnergyPrototype.new()
	if sim.heroes.size() != 4:
		_fail("四大職業數量應為 4，實得 %d" % sim.heroes.size())
		return

	for req_id in ["swordsman", "knight", "mage", "warrior"]:
		if not sim.heroes.has(req_id):
			_fail("缺少必備職業：%s" % req_id)
			return

	if sim.enemy["hp"] <= 0:
		_fail("敵方巨像初始血量異常")
		return

	if sim.shared_energy < 0.0 or sim.shared_energy > ClockworkEnergyPrototype.MAX_SHARED_ENERGY:
		_fail("共用發條能量初始值超出範圍：%f" % sim.shared_energy)
		return

	print("  [OK] 1. 四大職業與共用能量池初始化正常")


## 2. 手動分配流程測試
func _test_manual_allocation() -> void:
	var sim := ClockworkEnergyPrototype.new()
	sim.shared_energy = 49.0
	sim.update(0.2)  ## 充能達 50

	if not sim.is_allocating:
		_fail("能量滿 50 應進入分配視窗")
		return

	if sim.allocation_countdown <= 0.0:
		_fail("分配倒數計時初始值異常：%f" % sim.allocation_countdown)
		return

	var initial_enemy_hp: int = sim.enemy["hp"]
	var success := sim.allocate_manual("swordsman")
	if not success:
		_fail("手動分配給劍士應回傳成功")
		return

	if sim.is_allocating:
		_fail("手動分配後應關閉分配視窗")
		return

	if sim.shared_energy > 5.0:
		_fail("手動分配後應扣除 50 點共用發條能量，剩餘：%f" % sim.shared_energy)
		return

	if sim.enemy["hp"] >= initial_enemy_hp:
		_fail("劍士技能應對敵方造成傷害")
		return

	if sim.stats["manual_allocations"] != 1:
		_fail("手動分配統計次數不正確：%d" % sim.stats["manual_allocations"])
		return

	print("  [OK] 2. 手動指派能量與技能施放消耗運算正常")


## 3. 逾時自動分配（防卡死核心機制）測試
func _test_auto_allocation_timeout_prevention() -> void:
	var sim := ClockworkEnergyPrototype.new()
	sim.shared_energy = 55.0
	sim.update(0.1)  ## 觸發分配

	if not sim.is_allocating:
		_fail("未能觸發分配狀態")
		return

	## 模擬玩家放置 4.0 秒（超過 3.5 秒倒數）
	sim.update(4.0)

	if sim.is_allocating:
		_fail("逾時後分配視窗仍未關閉，發生卡關！")
		return

	if sim.stats["auto_allocations"] != 1:
		_fail("逾時後未觸發自動智慧分配，次數：%d" % sim.stats["auto_allocations"])
		return

	## 驗證智慧保底挑選：首領有裝甲且全員健康，應優先選擇戰士破甲
	if sim.stats["hero_picks"]["warrior"] < 1:
		_fail("首領裝甲完整時，智慧保底應挑選戰士破甲，實得分配：%s" % str(sim.stats["hero_picks"]))
		return

	## 驗證戰鬥依然流暢進行，無卡住狀態
	var energy_before := sim.shared_energy
	sim.update(1.0)
	if sim.shared_energy <= energy_before:
		_fail("逾時自動分配後，戰鬥進程未恢復流轉")
		return

	print("  [OK] 3. 逾時智慧自動分配順暢，防卡死驗證通過")


## 4. 長時戰鬥壓力模擬（混合手動與超時放置）
func _test_stress_battle_flow() -> void:
	var sim := ClockworkEnergyPrototype.new()
	var steps := 0
	var max_steps := 120

	while not sim.battle_over and steps < max_steps:
		steps += 1
		## 隨機模擬：50% 機率玩家手動選擇，50% 機率玩家發呆由系統自動分配
		if sim.is_allocating:
			if randf() < 0.5:
				var candidates := ["swordsman", "knight", "mage", "warrior"]
				sim.allocate_manual(candidates.pick_random())
			else:
				## 步進超過倒數時間，觸發自動分配
				sim.update(4.0)
				continue

		sim.update(0.5)

	if steps >= max_steps and not sim.battle_over:
		_fail("戰鬥在 %d 步內未能正常推進至終局" % max_steps)
		return

	if sim.stats["total_allocations"] < 2:
		_fail("整場戰鬥能量分配次數過少：%d" % sim.stats["total_allocations"])
		return

	print("  [OK] 4. 戰鬥壓力循環完成：共 %d 次分配（手動 %d / 自動 %d），勝負結算正常" % [
		sim.stats["total_allocations"],
		sim.stats["manual_allocations"],
		sim.stats["auto_allocations"]
	])


## 5. UI 介面載入與渲染節點結構測試
func _test_ui_instantiation() -> void:
	root.size = Vector2i(1280, 720)
	var view := ClockworkEnergyView.new()
	root.add_child(view)

	## 驗證核心 UI 元件
	var energy_bar: ProgressBar = view.energy_bar
	var modal: ColorRect = view.modal_scrim
	var hero_buttons: Dictionary = view.hero_buttons

	if energy_bar == null:
		_fail("UI 缺少共用發條能量條")
		return

	if modal == null:
		_fail("UI 缺少分配倒數視窗遮罩")
		return

	if hero_buttons.size() != 4:
		_fail("UI 四職業分配按鈕數量應為 4，實得 %d" % hero_buttons.size())
		return

	## 測試觸發 UI 分配視窗
	view.sim.shared_energy = 50.0
	view.sim.update(0.1)

	if not modal.visible:
		_fail("能量達門檻時，UI 分配視窗應自動彈出顯示")
		return

	## 模擬點擊手動按鈕
	hero_buttons["swordsman"].emit_signal("pressed")

	if modal.visible:
		_fail("手動選擇後，UI 分配視窗應隱藏關閉")
		return

	view.queue_free()
	print("  [OK] 5. UI 介面節點與互動信號驗證正常")
