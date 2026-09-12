extends RefCounted
## 日循環：發條回復＋日限（對 Ken W8-K1）。

var config
var wind: int = 15
var wind_max: int = 15
var last_regen_unix: float = 0.0
var daily_soul_pulls: int = 0
var daily_sweeps: int = 0
var daily_ad_regen: int = 0
var day_key: String = ""  ## YYYY-MM-DD after resetHour


func setup(cfg, now_unix: float = -1.0) -> void:
	config = cfg
	wind_max = int(config.daily.get("WindStaminaMax", 15))
	wind = wind_max
	last_regen_unix = now_unix if now_unix >= 0.0 else Time.get_unix_time_from_system()
	_ensure_day(last_regen_unix)


func _ensure_day(now_unix: float) -> void:
	var reset_h: int = int(config.daily.get("resetHourLocal", 5))
	var dt := Time.get_datetime_dict_from_unix_time(int(now_unix))
	# 簡易日鍵：未過 resetHour 算前一天
	var day := int(dt.day)
	var month := int(dt.month)
	var year := int(dt.year)
	if int(dt.hour) < reset_h:
		day -= 1
	var key := "%04d-%02d-%02d" % [year, month, max(1, day)]
	if key != day_key:
		day_key = key
		daily_soul_pulls = 0
		daily_sweeps = 0
		daily_ad_regen = 0


func tick_regen(now_unix: float = -1.0) -> int:
	## 回傳本次回復量
	if now_unix < 0.0:
		now_unix = Time.get_unix_time_from_system()
	_ensure_day(now_unix)
	var regen: Dictionary = config.daily.get("regen", {}) as Dictionary
	var per_min: float = float(regen.get("perMinutes", 8))
	var amount: int = int(regen.get("amount", 1))
	var cap: int = int(regen.get("cap", wind_max))
	if per_min <= 0.0:
		return 0
	var elapsed: float = now_unix - last_regen_unix
	var steps: int = int(floor(elapsed / (per_min * 60.0)))
	if steps <= 0:
		return 0
	var gained: int = steps * amount
	var before := wind
	wind = mini(cap, wind + gained)
	last_regen_unix += float(steps) * per_min * 60.0
	return wind - before


func spend(amount: int) -> bool:
	tick_regen()
	if amount <= 0:
		return true
	if wind < amount:
		return false
	wind -= amount
	return true


func try_ad_regen() -> bool:
	tick_regen()
	var ad: Dictionary = config.daily.get("adRegen", {}) as Dictionary
	var lim: int = int(ad.get("dailyLimit", 5))
	var gain: int = int(ad.get("WindStamina", 3))
	if daily_ad_regen >= lim:
		return false
	daily_ad_regen += 1
	wind = mini(wind_max, wind + gain)
	return true


func can_soul_pull() -> bool:
	tick_regen()
	var caps: Dictionary = config.daily.get("dailyCap", {}) as Dictionary
	return daily_soul_pulls < int(caps.get("soulPull", 30))


func note_soul_pull() -> void:
	daily_soul_pulls += 1


func can_sweep() -> bool:
	tick_regen()
	var caps: Dictionary = config.daily.get("dailyCap", {}) as Dictionary
	return daily_sweeps < int(caps.get("sweep", 20))


func note_sweep() -> void:
	daily_sweeps += 1
