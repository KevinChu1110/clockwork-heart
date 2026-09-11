class_name S8SmokeFlow
extends RefCounted
## Wave-2 §8 煙測流程：探索 → 戰鬥 → 拆一部位。
## 對齊 Bingo W4_B1_S8_DIALOGUE_POLISH；數值對齊 Ken W2-K1。
## 刻意極薄：不拉整包 RPG／main.gd，專供 Mac 可開切片與無頭證明。

signal phase_changed(phase: String, line: String)
signal log_line(text: String)
signal finished(ok: bool, summary: String)
## View／VFX：部位打碎時（drop_id 供糖果屑 tint）
signal part_break_fx(drop_id: String, part_name: String)
## View：發條扣點（Ken costs）— HUD 已聽 WindStamina.spent，此信號供額外 UI
signal stamina_spent(action_id: String, amount: int, remaining: int)

const DIALOG := {
	"s8.e01": "背上一緊……有人替我上了發條。",
	"s8.e02_hud": "（系統・首次）胸口那圈＝發條。轉不動就停一下。",
	"s8.e03": "這裡的齒輪，好像還沒完全停。",
	"s8.e04": "黃銅屑……有人拆過這裡。",
	"s8.e05": "那邊在響——不太友善。",
	"s8.b01": "擋路的，先請開。",
	"s8.b02_hint": "（系統・首次）點敵人。接縫亮了就能拆。",
	"s8.b03": "接縫開了！鎖那一塊！",
	"s8.b05": "下來——糖果屑也一起！",
	"s8.b07": "還走得動。零件，收。",
	"s8.d01": "一顆一顆來。選發光的那顆。",
	"s8.d03": "……轉開。",
	"s8.d04": "黃銅齒輪，進圖鑑了。",
	"s8.d04b": "發條彈簧，還在跳。",
	"s8.d05": "青綠亮了一下……核心碎片。",
	"s8.d06": "發條還沒停。下一格，給誰？",
	"s8.err_stamina": "發條轉不動了——先休息。",
}

enum Phase {
	IDLE,
	E01_ENTER,
	E02_WIND,
	E03_AMBIENT,
	E04_INTERACT,
	E05_SHADOW,
	E06_TO_BATTLE,
	B01_START,
	B02_COMBAT,
	B03_PART_UNLOCK,
	B05_PART_BROKEN,
	B06_ENEMY_DOWN,
	B07_END,
	D01_START,
	D02_SELECT,
	D03_UNSCREW,
	D04_EXTRACT,
	D06_COMPLETE,
	DONE,
}

var wind: WindStamina
var phase: int = Phase.IDLE
var enemy_max_hp: int = 40
var enemy_hp: int = 40
var part_max_hp: int = 10
var part_hp: int = 10
var part_unlocked: bool = false
var part_broken: bool = false
var loot: Array[String] = []
var last_error: String = ""
var auto_advance: bool = true
var _strike_count: int = 0
var _shown_e02_hud: bool = false
var _shown_b02_hint: bool = false


func setup() -> void:
	wind = WindStamina.new()
	wind.load_defaults()
	wind.reset_scene()
	if not wind.spent.is_connected(_on_wind_spent):
		wind.spent.connect(_on_wind_spent)
	enemy_max_hp = 40
	enemy_hp = enemy_max_hp
	part_max_hp = maxi(4, int(float(enemy_max_hp) * wind.part_hp_ratio()))
	part_hp = part_max_hp
	part_unlocked = false
	part_broken = false
	loot.clear()
	last_error = ""
	_strike_count = 0
	_shown_e02_hud = false
	_shown_b02_hint = false
	phase = Phase.IDLE


func _on_wind_spent(action_id: String, amount: int, remaining: int) -> void:
	stamina_spent.emit(action_id, amount, remaining)


func dialog(key: String) -> String:
	return str(DIALOG.get(key, key))


func phase_name() -> String:
	return Phase.keys()[phase]


## 三相分組：explore / combat / dismantle（給 View 按鈕高亮）
func phase_group() -> String:
	if phase >= Phase.D01_START and phase <= Phase.D06_COMPLETE:
		return "dismantle"
	if phase >= Phase.B01_START and phase <= Phase.B07_END:
		return "combat"
	if phase >= Phase.E01_ENTER and phase <= Phase.E06_TO_BATTLE:
		return "explore"
	return "idle"


func start() -> void:
	if wind == null:
		setup()
	_enter(Phase.E01_ENTER)


func _enter(p: int) -> void:
	phase = p
	match phase:
		Phase.E01_ENTER:
			_emit_phase(dialog("s8.e01"))
			_log("cue sfx.ui.wind_tick (silent ok)")
			if auto_advance:
				_enter(Phase.E02_WIND)
		Phase.E02_WIND:
			if not _spend("E02_exploreTick"):
				return
			# Bingo：首次系統提示胸口光 HUD；附成本回饋（非「藍條」用語）
			var hud_line := dialog("s8.e02_hud")
			if _shown_e02_hud:
				hud_line = "發條 −%d（胸口那圈）" % wind.cost_of("E02_exploreTick")
			_shown_e02_hud = true
			_emit_phase(hud_line)
			_log("WindStamina → %d/%d (E02_exploreTick=%d)" % [
				wind.current, wind.max_stamina, wind.cost_of("E02_exploreTick")
			])
			if auto_advance:
				_enter(Phase.E03_AMBIENT)
		Phase.E03_AMBIENT:
			_emit_phase(dialog("s8.e03"))
			if auto_advance:
				_enter(Phase.E04_INTERACT)
		Phase.E04_INTERACT:
			_emit_phase(dialog("s8.e04"))
			_log("picked loose screw (optional)")
			if auto_advance:
				_enter(Phase.E05_SHADOW)
		Phase.E05_SHADOW:
			_emit_phase(dialog("s8.e05"))
			if auto_advance:
				_enter(Phase.E06_TO_BATTLE)
		Phase.E06_TO_BATTLE:
			_emit_phase("—")
			_log("cue sfx.explore.to_battle (silent ok)")
			if auto_advance:
				_enter(Phase.B01_START)
		Phase.B01_START:
			if not _spend("B01_combatEnter"):
				return
			_emit_phase(dialog("s8.b01"))
			_log("combat enter cost=%d; WindStamina → %d/%d" % [
				wind.cost_of("B01_combatEnter"), wind.current, wind.max_stamina
			])
			if auto_advance:
				_enter(Phase.B02_COMBAT)
		Phase.B02_COMBAT:
			if not _shown_b02_hint:
				_shown_b02_hint = true
				_emit_phase(dialog("s8.b02_hint"))
			_run_combat_loop()
		Phase.B03_PART_UNLOCK:
			_emit_phase(dialog("s8.b03"))
			_log("part unlock at ≤%.0f%% HP" % (wind.part_unlock_hp() * 100.0))
			if auto_advance:
				_enter(Phase.B05_PART_BROKEN)
		Phase.B05_PART_BROKEN:
			_break_part()
			_emit_phase(dialog("s8.b05"))
			if auto_advance:
				_enter(Phase.B06_ENEMY_DOWN)
		Phase.B06_ENEMY_DOWN:
			enemy_hp = 0
			_emit_phase("—")
			_log("enemy down: 鏽蝕發條鼠")
			if auto_advance:
				_enter(Phase.B07_END)
		Phase.B07_END:
			_emit_phase(dialog("s8.b07"))
			if auto_advance:
				_enter(Phase.D01_START)
		Phase.D01_START:
			if not _spend("D01_dismantleEnter"):
				return
			_emit_phase(dialog("s8.d01"))
			_log("dismantle enter cost=%d; WindStamina → %d/%d" % [
				wind.cost_of("D01_dismantleEnter"), wind.current, wind.max_stamina
			])
			if auto_advance:
				_enter(Phase.D02_SELECT)
		Phase.D02_SELECT:
			_emit_phase("—")
			_log("highlight gear_brass")
			if auto_advance:
				_enter(Phase.D03_UNSCREW)
		Phase.D03_UNSCREW:
			_emit_phase(dialog("s8.d03"))
			if auto_advance:
				_enter(Phase.D04_EXTRACT)
		Phase.D04_EXTRACT:
			if not _spend("D_pullPart"):
				return
			var drop_id := wind.primary_drop()
			loot.append(drop_id)
			_emit_phase(_dialog_for_drop(drop_id))
			_log("loot +%s (%s)" % [drop_id, wind.drop_display_name(drop_id)])
			# 抽出也播一次糖果屑（與 B05 打碎呼應）
			part_break_fx.emit(drop_id, "gear_brass")
			if auto_advance:
				_enter(Phase.D06_COMPLETE)
		Phase.D06_COMPLETE:
			_emit_phase(dialog("s8.d06"))
			_finish(true)
		_:
			pass


func _dialog_for_drop(drop_id: String) -> String:
	match drop_id:
		"drop_spring_coil":
			return dialog("s8.d04b")
		"drop_core_shard":
			return dialog("s8.d05")
		_:
			return dialog("s8.d04")


func advance() -> void:
	## 手動逐步（互動切片）；auto_advance=false 時由 View 呼叫。
	if phase == Phase.DONE or phase == Phase.IDLE:
		return
	var order := [
		Phase.E01_ENTER, Phase.E02_WIND, Phase.E03_AMBIENT, Phase.E04_INTERACT,
		Phase.E05_SHADOW, Phase.E06_TO_BATTLE, Phase.B01_START, Phase.B02_COMBAT,
		Phase.B03_PART_UNLOCK, Phase.B05_PART_BROKEN, Phase.B06_ENEMY_DOWN,
		Phase.B07_END, Phase.D01_START, Phase.D02_SELECT, Phase.D03_UNSCREW,
		Phase.D04_EXTRACT, Phase.D06_COMPLETE,
	]
	var idx := order.find(phase)
	if idx < 0 or idx >= order.size() - 1:
		return
	_enter(order[idx + 1])


## 三相按鈕：往指定分組推進（已過則 noop；未到則連跳到該組入口）。
func goto_group(group: String) -> void:
	if phase == Phase.DONE:
		return
	var target := Phase.E01_ENTER
	match group:
		"explore":
			target = Phase.E01_ENTER
		"combat":
			target = Phase.B01_START
		"dismantle":
			target = Phase.D01_START
		_:
			return
	if phase >= target and phase_group() == group:
		# 已在該組：當一步 advance（B02 特判由 View 處理）
		if phase == Phase.B02_COMBAT:
			_run_combat_loop()
		else:
			advance()
		return
	if phase > target:
		return
	# 連跳到目標入口（保留中間扣點／狀態）
	var guard := 0
	while phase < target and phase != Phase.DONE and guard < 32:
		guard += 1
		if phase == Phase.B02_COMBAT:
			_run_combat_loop()
		else:
			advance()
		if last_error != "":
			return


func _run_combat_loop() -> void:
	if not _shown_b02_hint:
		_shown_b02_hint = true
		_emit_phase(dialog("s8.b02_hint"))
	else:
		_emit_phase("即時互毆（節奏預算）")
	# 目標：把本體壓到 unlock 門檻以下，再砸掉部位。
	var unlock_hp := int(ceil(float(enemy_max_hp) * wind.part_unlock_hp()))
	while enemy_hp > unlock_hp:
		if not _spend("B_strike"):
			return
		var dmg := 8
		enemy_hp = maxi(0, enemy_hp - dmg)
		_strike_count += 1
		_log("strike#%d enemy_hp=%d/%d wind=%d" % [_strike_count, enemy_hp, enemy_max_hp, wind.current])
		# 被擊不耗發條（B_takeHit=0）
		_spend("B_takeHit")
	_check_part_unlock()
	if not part_unlocked:
		last_error = "part did not unlock at PartUnlockHP"
		_finish(false)
		return
	# 無論手動／自動，解鎖後進入 B03（手動模式由 View 觸發本函式）
	_enter(Phase.B03_PART_UNLOCK)


func _check_part_unlock() -> void:
	var ratio := float(enemy_hp) / float(enemy_max_hp)
	if ratio <= wind.part_unlock_hp():
		part_unlocked = true


func _break_part() -> void:
	if not part_unlocked:
		last_error = "break before unlock"
		_finish(false)
		return
	while part_hp > 0:
		if not _spend("B_strike"):
			return
		var dmg := int(ceil(6.0 * wind.break_bonus()))
		part_hp = maxi(0, part_hp - dmg)
		_log("part hit hp=%d/%d (bonus×%.2f)" % [part_hp, part_max_hp, wind.break_bonus()])
	part_broken = true
	var drop_preview := wind.primary_drop()
	_log("broke gear_brass → candy chips (%s)" % drop_preview)
	part_break_fx.emit(drop_preview, "gear_brass")


func _spend(action_id: String) -> bool:
	if wind.try_spend(action_id):
		return true
	last_error = dialog("s8.err_stamina") + " (%s)" % action_id
	_emit_phase(last_error)
	_finish(false)
	return false


func _emit_phase(line: String) -> void:
	phase_changed.emit(phase_name(), line)


func _log(text: String) -> void:
	log_line.emit(text)


func _finish(ok: bool) -> void:
	phase = Phase.DONE
	var summary := "ok loot=%s wind=%d/%d strikes=%d part_broken=%s" % [
		str(loot), wind.current, wind.max_stamina, _strike_count, str(part_broken)
	]
	if not ok:
		summary = "FAIL: %s | %s" % [last_error, summary]
	finished.emit(ok, summary)


## 無頭／單元：一次跑完並回傳結果字典。
func run_to_completion() -> Dictionary:
	auto_advance = true
	setup()
	var ok_holder := {"ok": false, "summary": ""}
	finished.connect(func(ok: bool, summary: String) -> void:
		ok_holder["ok"] = ok
		ok_holder["summary"] = summary
	, CONNECT_ONE_SHOT)
	start()
	return {
		"ok": bool(ok_holder["ok"]),
		"summary": str(ok_holder["summary"]),
		"wind": wind.current,
		"max": wind.max_stamina,
		"loot": loot.duplicate(),
		"part_broken": part_broken,
		"part_unlocked": part_unlocked,
		"hud_style": wind.hud_style(),
		"forbids_blue_mana": wind.hud_forbids_blue_mana(),
		"dialog_e02": dialog("s8.e02_hud"),
		"dialog_b02": dialog("s8.b02_hint"),
	}
