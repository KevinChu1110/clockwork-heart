extends RefCounted
## 關卡：首通／掃蕩（對 Ken W8-K1 chapters）。

var config
var cleared: Dictionary = {}  ## ChapterId → true
var last_error: String = ""


func setup(cfg) -> void:
	config = cfg
	cleared.clear()


func is_cleared(chapter_id: String) -> bool:
	return bool(cleared.get(chapter_id, false))


func final_damage(atk: int, enhance_atk: int, enemy_def: int) -> int:
	# Max(1, ATK + EnhanceATK - DEF)
	return max(1, atk + enhance_atk - enemy_def)


func can_sweep(chapter_id: String, wind: int, daily_sweep_ok: bool) -> bool:
	var ch: Dictionary = config.chapter_def(chapter_id)
	if ch.is_empty():
		return false
	if not is_cleared(chapter_id):
		return false
	if not daily_sweep_ok:
		return false
	return wind >= int(ch.get("staminaEnter", 0))


func first_clear_reward(chapter_id: String) -> Dictionary:
	var ch: Dictionary = config.chapter_def(chapter_id)
	if ch.is_empty():
		return {}
	return ch.get("firstClear", {}) as Dictionary


func sweep_reward(chapter_id: String) -> Dictionary:
	var ch: Dictionary = config.chapter_def(chapter_id)
	if ch.is_empty():
		return {}
	return ch.get("sweep", {}) as Dictionary


func mark_cleared(chapter_id: String) -> void:
	cleared[chapter_id] = true
