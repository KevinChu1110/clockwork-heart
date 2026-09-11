class_name S8SmokeFlow
extends RefCounted
## Wave-2 §8 煙測流程：探索 → 戰鬥 → 拆一部位。
## 對齊 Bingo W2_B1_S8_SMOKE_SCRIPT.md；數值對齊 Ken W2-K1。
## 刻意極薄：不拉整包 RPG／main.gd，專供 Mac 可開切片與無頭證明。

signal phase_changed(phase: String, line: String)
signal log_line(text: String)
signal finished(ok: bool, summary: String)

const DIALOG := {
	"s8.e01": "……背上一緊。有人上了發條？",
	"s8.e03": "齒輪……還在轉。",
	"s8.e04": "黃色的……黃銅？",
	"s8.e05": "那邊也在響。",
	"s8.b01": "別擋住路。",
	"s8.b03": "接縫開了！",
	"s8.b05": "下來！",
	"s8.b07": "還能走。",
	"s8.d01": "一顆一顆來。",
	"s8.d03": "……轉開。",
	"s8.d04": "黃銅齒輪，收好。",
	"s8.d05": "……亮了一下。",
	"s8.d06": "發條還沒停。",
	"s8.err_stamina": "發條轉不動了。",
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


func setup() -> void:
	wind = WindStamina.new()
	wind.load_defaults()
	wind.reset_scene()
	enemy_max_hp = 40
	enemy_hp = enemy_max_hp
	part_max_hp = maxi(4, int(float(enemy_max_hp) * wind.part_hp_ratio()))
	part_hp = part_max_hp
	part_unlocked = false
	part_broken = false
	loot.clear()
	last_error = ""
	_strike_count = 0
	phase = Phase.IDLE


func dialog(key: String) -> String:
	return str(DIALOG.get(key, key))


func phase_name() -> String:
	return Phase.keys()[phase]


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
			_emit_phase("（系統）發條 −%d" % wind.cost_of("E02_exploreTick"))
			_log("WindStamina → %d/%d" % [wind.current, wind.max_stamina])
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
			_log("combat enter cost; WindStamina → %d/%d" % [wind.current, wind.max_stamina])
			if auto_advance:
				_enter(Phase.B02_COMBAT)
		Phase.B02_COMBAT:
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
			_log("dismantle enter; WindStamina → %d/%d" % [wind.current, wind.max_stamina])
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
			_emit_phase(dialog("s8.d04"))
			_log("loot +%s (%s)" % [drop_id, wind.drop_display_name(drop_id)])
			if auto_advance:
				_enter(Phase.D06_COMPLETE)
		Phase.D06_COMPLETE:
			_emit_phase(dialog("s8.d06"))
			_finish(true)
		_:
			pass


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


func _run_combat_loop() -> void:
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
	_log("broke gear_brass")


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
	}
