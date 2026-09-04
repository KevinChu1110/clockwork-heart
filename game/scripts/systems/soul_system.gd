extends Node
## 戰魂／抽魂＝聚魂（原作招牌）。
## 葫蘆魂器綠→藍→紫→橙跳階；金幣＋每日免費；紫微十四主星。
## 見 docs/PRODUCT_BRIDGE.md §6；參考 bravesoul/engine/soul.py。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

## 紫微斗數十四主星（截圖證實）；數值映射到本作三圍
const STARS: Array[Dictionary] = [
	{"id": "紫微", "stat": "all", "label": "衡", "base": 1},
	{"id": "天機", "stat": "atk", "label": "機", "base": 2},
	{"id": "太陽", "stat": "atk", "label": "陽", "base": 3},
	{"id": "武曲", "stat": "atk", "label": "武", "base": 3},
	{"id": "天同", "stat": "hp", "label": "同", "base": 8},
	{"id": "廉貞", "stat": "atk", "label": "廉", "base": 2},
	{"id": "天府", "stat": "def", "label": "府", "base": 3},
	{"id": "太陰", "stat": "hp", "label": "陰", "base": 8},
	{"id": "貪狼", "stat": "hp", "label": "血", "base": 6},
	{"id": "巨門", "stat": "atk", "label": "巨", "base": 2},
	{"id": "天相", "stat": "def", "label": "相", "base": 3},
	{"id": "天梁", "stat": "def", "label": "防", "base": 2},
	{"id": "七殺", "stat": "atk", "label": "銳", "base": 2},
	{"id": "破軍", "stat": "atk", "label": "攻", "base": 2},
]

## 品質倍率（神＝頂級；大凶可賣／合成素材感）
const QUALITIES: Array[Dictionary] = [
	{"id": "大凶", "mult": 0.4, "weight": 0},
	{"id": "凡", "mult": 1.0, "weight": 0},
	{"id": "吉", "mult": 1.6, "weight": 0},
	{"id": "大吉", "mult": 2.3, "weight": 0},
	{"id": "稀世", "mult": 3.2, "weight": 0},
	{"id": "神", "mult": 4.5, "weight": 0},
]

## 葫蘆階（永不降級語意由「同色摔回綠」表現循環）
const VESSEL_LADDER: Array[String] = ["綠葫蘆", "藍葫蘆", "紫葫蘆", "橙葫蘆"]
## 金幣花費（較原作 200/500/1500/3000 略降，適配本作經濟；精神不變）
const VESSEL_COST := {"綠葫蘆": 80, "藍葫蘆": 200, "紫葫蘆": 500, "橙葫蘆": 1000}
## 同色 jackpot → 摔回綠
const VESSEL_MATCH := {"綠葫蘆": "吉", "藍葫蘆": "大吉", "紫葫蘆": "稀世", "橙葫蘆": "神"}
const VESSEL_UP := {"綠葫蘆": 0.30, "藍葫蘆": 0.20, "紫葫蘆": 0.10, "橙葫蘆": 0.0}
## 各階品質權重表
const VESSEL_QUALITY := {
	"綠葫蘆": {"大凶": 40, "凡": 35, "吉": 25},
	"藍葫蘆": {"凡": 30, "吉": 40, "大吉": 30},
	"紫葫蘆": {"吉": 30, "大吉": 40, "稀世": 30},
	"橙葫蘆": {"神": 100},
}

## 相容舊測試／UI：星屑代價常數保留為「建議持有星屑」顯示用，實際主代價是金幣
const RITUAL_COST := 0
const FUSE_COUNT := 3
## 凡～稀世：3 合 1 最高到 3 階。神品質＝原作「神魂」，聚俠網 2012：最高 10 級。
const FUSE_MAX_LEVEL := 3
const SHEN_MAX_LEVEL := 10

## ---- 養魂（原作：廢魂餵給要的魂升級，逐級翻倍；一鍵吸收）----
## 所有魂餵魂上限 10 級（原作）；3 合 1 仍在，當快速合併捷徑
const SOUL_MAX_LEVEL := 10
## 升 1 級所需魂經驗 = FEED_BASE_XP × 2^目前等級（原創補完，仿原作 960 起逐級翻倍的曲線）
const FEED_BASE_XP := 60
## 各品質當飼料的魂經驗（仿原作 藍=60、紫=120 的比例）
const FEED_VALUE := {"大凶": 15, "凡": 30, "吉": 60, "大吉": 120, "稀世": 240, "神": 500, "秘境": 240}

## ---- 虔誠度／戰魂碎片（原作官方機制：每次聚魂積虔誠度，滿 100 換 1 碎片）----
const PIETY_PER_DRAW := 10
const PIETY_PER_SHARD := 100
## 碎片兌換價（原創補完：仿原作 36 碎=1 紫魂的軟保底精神，適配本作經濟）
const SHARD_EXCHANGE := {"稀世": 6, "神": 15}

## 秘境專屬戰魂（唯一）：key = boss battle mode
const SECRET_RELICS: Dictionary = {
	"scar_lord": {
		"unique_flag": "soul.relic.scar_lord",
		"star": "疤焰",
		"quality": "秘境",
		"display": "疤焰心核",
		"atk": 9,
		"def": 2,
		"hp": 8,
		"lore": "黑焰疤主的傷口凝成的心核。刃上會殘一絲不肯散的熱。",
	},
	"mirror_wraith": {
		"unique_flag": "soul.relic.mirror_wraith",
		"star": "鏡影",
		"quality": "秘境",
		"display": "真影裂片",
		"atk": 5,
		"def": 6,
		"hp": 12,
		"lore": "鏡廊殘影碎裂時留下的真影。防的是「猶豫」。",
	},
	"wreck_captain": {
		"unique_flag": "soul.relic.wreck_captain",
		"star": "潮骨",
		"quality": "秘境",
		"display": "船長潮骨",
		"atk": 7,
		"def": 5,
		"hp": 20,
		"lore": "沉船船長影的龍骨碎片。像潮汐一樣穩、一樣重。",
	},
}


## 器階到魂槽的門檻。設計是 T1／T6／T11 各開一槽（PROGRESSION 2.2）。
##
## 這張表要跟鍛造的階數上限對得起來。曾經對不上：這裡寫 T11 開第三槽，
## 而鍛造在 T8 就擋下來 —— 第三個魂槽是一個玩家再怎麼玩都拿不到的獎勵。
## 不會報錯，玩家只會把武器練到頂、發現第三格還是灰的，以為自己漏了什麼。
## `test_progression.gd` 現在守著「每一個門檻都要鍛造得到」。
const SLOT_TIERS: Array[int] = [1, 6, 11]



## 玩家看得到的中文字面值一律包這支（以原文當 key，譯文在
## data/i18n/content/<locale>/ui.json）。務必包在格式化之前 ——
## `_t("A %d") % [n]` 查得到表，`_t("A %d" % [n])` 查不到。
static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func slot_count() -> int:
	var t: int = GameState.weapon_tier
	var n := 0
	for need in SLOT_TIERS:
		if t >= need:
			n += 1
	return n


func ensure_slots() -> void:
	var n: int = slot_count()
	while GameState.soul_slots.size() < n:
		GameState.soul_slots.append("")
	if GameState.soul_slots.size() > n:
		## 多出來的卸下回背包
		for i in range(n, GameState.soul_slots.size()):
			var sid: String = str(GameState.soul_slots[i])
			if sid != "":
				_set_soul_equipped(sid, false)
		GameState.soul_slots.resize(n)


func find_soul(sid: String) -> Dictionary:
	for s in GameState.souls:
		if str(s.get("id", "")) == sid:
			return s
	return {}


## 星曜與品質的 id 本身就是中文（"破軍"／"凡"），而且會寫進存檔、拿來跟
## STARS／QUALITIES 比對，所以 id 一律留原文，只在要顯示的時候查譯文。
func soul_word(id: String) -> String:
	return ContentLoc.text("soul", id)


func soul_display(s: Dictionary) -> String:
	if s.is_empty():
		return _t("（空）")
	if bool(s.get("relic", false)):
		var dn := str(s.get("display", s.get("star", "秘境魂")))
		var lv: int = int(s.get("level", 0))
		var lv_s := "" if lv <= 0 else "·%d" % lv
		return _t("秘·%s%s") % [soul_word(dn), lv_s]
	var q: String = str(s.get("quality", "凡"))
	var star: String = str(s.get("star", "？"))
	var lv2: int = int(s.get("level", 0))
	var lv_s2 := "" if lv2 <= 0 else "·%d" % lv2
	## 原作截圖：僅「神」品質加「神-」前綴
	if q == "神":
		return "%s%s%s" % [_t("神-"), soul_word(star), lv_s2]
	return "%s·%s%s" % [soul_word(q), soul_word(star), lv_s2]


func soul_bonus_line(s: Dictionary) -> String:
	if s.is_empty():
		return ""
	var b: Dictionary = calc_soul_bonus(s)
	var parts: PackedStringArray = []
	if int(b.get("atk", 0)) != 0:
		parts.append(_t("攻+%d") % int(b.get("atk", 0)))
	if int(b.get("def", 0)) != 0:
		parts.append(_t("防+%d") % int(b.get("def", 0)))
	if int(b.get("hp", 0)) != 0:
		parts.append(_t("血+%d") % int(b.get("hp", 0)))
	return " ".join(parts)


func calc_soul_bonus(s: Dictionary) -> Dictionary:
	## 秘境專屬：固定三圍（可再吃 level 微幅）
	if bool(s.get("relic", false)):
		var lv: int = int(s.get("level", 0))
		var scale := 1.0 + 0.12 * float(lv)
		return {
			"atk": maxi(1, int(round(float(s.get("atk_bonus", 0)) * scale))),
			"def": maxi(0, int(round(float(s.get("def_bonus", 0)) * scale))),
			"hp": maxi(0, int(round(float(s.get("hp_bonus", 0)) * scale))),
		}
	var star_id: String = str(s.get("star", "破軍"))
	var q_id: String = str(s.get("quality", "凡"))
	var lv2: int = int(s.get("level", 0))
	var star_def: Dictionary = {}
	for st in STARS:
		if str(st.get("id", "")) == star_id:
			star_def = st
			break
	if star_def.is_empty():
		star_def = STARS[0]
	var mult := 1.0
	for q in QUALITIES:
		if str(q.get("id", "")) == q_id:
			mult = float(q.get("mult", 1.0))
			break
	if q_id == "秘境":
		mult = 3.2
	var base: float = float(star_def.get("base", 1)) * mult * (1.0 + 0.15 * float(lv2))
	var val: int = maxi(1, int(round(base)))
	var stat: String = str(star_def.get("stat", "atk"))
	var out := {"atk": 0, "def": 0, "hp": 0}
	match stat:
		"atk":
			out["atk"] = val
			if star_id == "七殺":
				out["atk"] = val + 1
		"def":
			out["def"] = val
		"hp":
			out["hp"] = val
		"all":
			out["atk"] = val
			out["def"] = val
			out["hp"] = val * 3
	return out


func grant_secret_relic(boss_mode: String) -> Dictionary:
	## 回傳 {ok, soul?, msg, dust?}
	if not SECRET_RELICS.has(boss_mode):
		return {"ok": false, "msg": _t("沒有對應秘境魂器。")}
	var def: Dictionary = SECRET_RELICS[boss_mode]
	var flag := str(def.get("unique_flag", ""))
	if flag != "" and GameState.has_flag(flag):
		## 已有：補償星屑
		GameState.add_stardust(3)
		return {"ok": true, "duplicate": true, "dust": 3, "msg": _t("你已持有此秘境魂器。改獲星屑 3。")}
	var soul := {
		"id": "relic_%s_%d" % [boss_mode, Time.get_ticks_msec()],
		"star": str(def.get("star", "秘")),
		"quality": str(def.get("quality", "秘境")),
		"display": str(def.get("display", "秘境魂")),
		"level": 0,
		"equipped": false,
		"relic": true,
		"relic_key": boss_mode,
		"atk_bonus": int(def.get("atk", 0)),
		"def_bonus": int(def.get("def", 0)),
		"hp_bonus": int(def.get("hp", 0)),
		"lore": str(def.get("lore", "")),
	}
	GameState.souls.append(soul)
	if flag != "":
		GameState.set_flag(flag, true)
	## 至少開一槽
	if GameState.weapon_tier < 1:
		GameState.weapon_tier = 1
	ensure_slots()
	return {
		"ok": true,
		"duplicate": false,
		"soul": soul,
		"msg": _t("獲得秘境魂器【%s】！%s") % [soul_word(str(def.get("display", ""))), _t(str(def.get("lore", "")))],
	}


func total_equipped_bonus() -> Dictionary:
	ensure_slots()
	var total := {"atk": 0, "def": 0, "hp": 0}
	for sid in GameState.soul_slots:
		if str(sid) == "":
			continue
		var s: Dictionary = find_soul(str(sid))
		if s.is_empty():
			continue
		var b: Dictionary = calc_soul_bonus(s)
		total["atk"] = int(total["atk"]) + int(b.get("atk", 0))
		total["def"] = int(total["def"]) + int(b.get("def", 0))
		total["hp"] = int(total["hp"]) + int(b.get("hp", 0))
	return total


## 足跡權重：主線進度偏科
func _star_weights() -> Dictionary:
	var w: Dictionary = {}
	for st in STARS:
		w[str(st.get("id", ""))] = 14.0
	if GameState.has_flag("boss.leo_cleared"):
		w["破軍"] = float(w.get("破軍", 14)) + 25.0
		w["七殺"] = float(w.get("七殺", 14)) + 10.0
		w["太陽"] = float(w.get("太陽", 14)) + 8.0
	if GameState.has_flag("boss.white_fog_cleared"):
		w["紫微"] = float(w.get("紫微", 14)) + 15.0
		w["天機"] = float(w.get("天機", 14)) + 8.0
	if GameState.has_flag("boss.abo_cleared"):
		w["天梁"] = float(w.get("天梁", 14)) + 20.0
		w["天府"] = float(w.get("天府", 14)) + 10.0
	if GameState.has_flag("c0_care") or GameState.has_wheat_stalk or GameState.wheat_stalk_broken:
		w["天梁"] = float(w.get("天梁", 14)) + 12.0
		w["貪狼"] = float(w.get("貪狼", 14)) + 8.0
		w["天同"] = float(w.get("天同", 14)) + 6.0
	if GameState.has_flag("boss.shadowwind_cleared"):
		w["七殺"] = float(w.get("七殺", 14)) + 12.0
		w["天機"] = float(w.get("天機", 14)) + 8.0
	if GameState.has_flag("boss.stonefist_cleared"):
		w["貪狼"] = float(w.get("貪狼", 14)) + 12.0
		w["武曲"] = float(w.get("武曲", 14)) + 8.0
	return w


func _pick_weighted(items: Array, key: String = "weight") -> Dictionary:
	var total := 0.0
	for it in items:
		total += float(it.get(key, 0))
	if total <= 0.0:
		return items[0] if not items.is_empty() else {}
	var r := randf() * total
	var acc := 0.0
	for it in items:
		acc += float(it.get(key, 0))
		if r <= acc:
			return it
	return items[items.size() - 1]


func today_key() -> String:
	var dt := Time.get_datetime_dict_from_system()
	return "%04d-%02d-%02d" % [int(dt.get("year", 2026)), int(dt.get("month", 1)), int(dt.get("day", 1))]


func ensure_daily_free() -> void:
	var day := today_key()
	if GameState.soul_free_day != day:
		GameState.soul_free_day = day
		GameState.soul_free_draws = 1


func as_vessel(v: String) -> String:
	if v in VESSEL_LADDER:
		return v
	return "綠葫蘆"


func vessel_cost(vessel: String = "") -> int:
	var v := as_vessel(vessel if vessel != "" else GameState.soul_vessel)
	return int(VESSEL_COST.get(v, 80))


func ritual_cost_gold() -> int:
	ensure_daily_free()
	if GameState.soul_free_draws > 0:
		return 0
	return vessel_cost()


func can_ritual() -> bool:
	ensure_daily_free()
	if GameState.soul_free_draws > 0:
		return true
	return GameState.gold >= vessel_cost()


## 原作聚魂有 ×10。花費以「當下葫蘆階 × 付費次數」估；抽的過程中若升階，
## 實際可能多扣一點，錢不夠就停，不預扣頂階。
func ritual_batch_gold_estimate(n: int = 10) -> int:
	ensure_daily_free()
	var paid: int = maxi(0, n - GameState.soul_free_draws)
	return paid * vessel_cost()


func can_ritual_batch(n: int = 10) -> bool:
	ensure_daily_free()
	if n <= 0:
		return false
	if GameState.soul_free_draws >= n:
		return true
	return GameState.gold >= ritual_batch_gold_estimate(n)


func vessel_ladder_bbcode() -> String:
	var cur := as_vessel(GameState.soul_vessel)
	var bits: PackedStringArray = []
	for v in VESSEL_LADDER:
		if v == cur:
			bits.append("[b]%s[/b]" % v)
		else:
			bits.append(v)
	return " → ".join(bits)


## 聚魂殿足跡連線文案（加權星曜；品質仍看葫蘆階）
func ritual_footprint_line() -> String:
	var parts: PackedStringArray = []
	if GameState.has_flag("boss.leo_cleared"):
		parts.append(_t("騎士域·勇／攻"))
	if GameState.has_flag("boss.white_fog_cleared"):
		parts.append(_t("霧痕·衡"))
	if GameState.has_flag("boss.abo_cleared"):
		parts.append(_t("拳山·防"))
	if GameState.has_flag("c0_care") or GameState.has_wheat_stalk or GameState.wheat_stalk_broken:
		parts.append(_t("麥稈·梁／血"))
	if GameState.has_flag("boss.shadowwind_cleared"):
		parts.append(_t("林風·銳"))
	if GameState.has_flag("boss.stonefist_cleared"):
		parts.append(_t("岸岩·血"))
	if parts.is_empty():
		return _t("魂器仍樸——但你的腳步已經在畫線。")
	return _t("足跡偏向：%s。") % " · ".join(parts)


func _roll_quality_for_vessel(vessel: String) -> String:
	var table: Dictionary = VESSEL_QUALITY.get(as_vessel(vessel), VESSEL_QUALITY["綠葫蘆"])
	var items: Array = []
	for q in table.keys():
		items.append({"id": str(q), "weight": float(table[q])})
	var pick: Dictionary = _pick_weighted(items)
	return str(pick.get("id", "凡"))


func _next_vessel_after(vessel: String, quality: String) -> Dictionary:
	## 回傳 {next, climbed, reset}
	var v := as_vessel(vessel)
	var match_q := str(VESSEL_MATCH.get(v, ""))
	if quality == match_q:
		return {"next": "綠葫蘆", "climbed": false, "reset": true}
	var idx := VESSEL_LADDER.find(v)
	if idx < 0:
		idx = 0
	var top := VESSEL_LADDER.size() - 1
	var up := float(VESSEL_UP.get(v, 0.0))
	if idx < top and randf() < up:
		return {"next": VESSEL_LADDER[idx + 1], "climbed": true, "reset": false}
	return {"next": v, "climbed": false, "reset": false}


func ritual(quiet: bool = false) -> Dictionary:
	## 抽魂／聚魂：品質看葫蘆階；星曜受足跡加權；耗免費或金幣
	if not can_ritual():
		return {}
	ensure_daily_free()
	var vessel := as_vessel(GameState.soul_vessel)
	var used_free := false
	if GameState.soul_free_draws > 0:
		GameState.soul_free_draws -= 1
		used_free = true
	else:
		var cost := vessel_cost(vessel)
		if GameState.gold < cost:
			return {}
		GameState.add_gold(-cost)
	var quality := _roll_quality_for_vessel(vessel)
	var soul := {
		"id": "soul_%d_%d" % [Time.get_ticks_msec(), randi() % 10000],
		"star": _roll_star(),
		"quality": quality,
		"level": 0,
		"equipped": false,
	}
	var nv: Dictionary = _next_vessel_after(vessel, quality)
	GameState.soul_vessel = str(nv.get("next", vessel))
	GameState.souls.append(soul)
	## 原作：每次聚魂積虔誠度，滿 100 產 1 個戰魂碎片
	var shard_got := _add_piety(PIETY_PER_DRAW)
	if not quiet:
		_ritual_success_hooks(soul, vessel, used_free, nv, shard_got)
	return soul


## 星曜抽選（足跡加權；足跡未覆蓋的星也有底權重）——抽魂與碎片兌換共用
func _roll_star() -> String:
	var sw: Dictionary = _star_weights()
	var star_items: Array = []
	for k in sw.keys():
		star_items.append({"id": k, "weight": sw[k]})
	for st in STARS:
		var sid := str(st.get("id", ""))
		if not sw.has(sid):
			star_items.append({"id": sid, "weight": 12.0})
	var star_pick: Dictionary = _pick_weighted(star_items)
	return str(star_pick.get("id", "破軍"))


func piety() -> int:
	return int(GameState.get_flag("soul.piety", 0))


func shards() -> int:
	return int(GameState.get_flag("soul.shards", 0))


## 累積虔誠度；回傳這次產出的碎片數
func _add_piety(n: int) -> int:
	var p := piety() + n
	var got := int(p / PIETY_PER_SHARD)
	GameState.set_flag("soul.piety", p % PIETY_PER_SHARD)
	if got > 0:
		GameState.set_flag("soul.shards", shards() + got)
	return got


## 碎片兌換戰魂（軟保底）：品質指定、星曜隨足跡機率
func exchange_shards(quality: String) -> Dictionary:
	var cost := int(SHARD_EXCHANGE.get(quality, 0))
	if cost <= 0:
		return {"ok": false, "msg": _t("這個品質不開放兌換。")}
	if shards() < cost:
		return {"ok": false, "msg": _t("戰魂碎片不足（需 %d）。") % cost}
	GameState.set_flag("soul.shards", shards() - cost)
	var soul := {
		"id": "soul_%d_%d" % [Time.get_ticks_msec(), randi() % 10000],
		"star": _roll_star(),
		"quality": quality,
		"level": 0,
		"equipped": false,
	}
	GameState.souls.append(soul)
	SaveManager.save_game()
	if AudioManager and AudioManager.has_method("play_ritual_success"):
		AudioManager.play_ritual_success()
	return {"ok": true, "soul": soul, "msg": _t("碎片凝魂：%s（%s）") % [soul_display(soul), soul_bonus_line(soul)]}


## ---- 養魂 ----


func feed_xp_needed(level: int) -> int:
	return FEED_BASE_XP * int(pow(2.0, clampi(level, 0, SOUL_MAX_LEVEL - 1)))


## 把 food_ids 這些魂吃掉，經驗餵進 target；逐級進位到 SOUL_MAX_LEVEL
func absorb(target_id: String, food_ids: Array) -> Dictionary:
	var target: Dictionary = find_soul(target_id)
	if target.is_empty():
		return {"ok": false, "msg": _t("找不到要餵的戰魂。")}
	if int(target.get("level", 0)) >= SOUL_MAX_LEVEL:
		return {"ok": false, "msg": _t("已是 10 級，吃不下了。")}
	var gained := 0
	var eaten := 0
	for fid in food_ids:
		var sid := str(fid)
		if sid == target_id:
			continue
		var f: Dictionary = find_soul(sid)
		if f.is_empty() or bool(f.get("equipped", false)) or bool(f.get("relic", false)):
			continue
		gained += int(FEED_VALUE.get(str(f.get("quality", "凡")), 30))
		eaten += 1
		for i in GameState.souls.size():
			if str((GameState.souls[i] as Dictionary).get("id", "")) == sid:
				GameState.souls.remove_at(i)
				break
	if eaten == 0:
		return {"ok": false, "msg": _t("沒有可吸收的魂（入槽與秘境魂不能當飼料）。")}
	var xp := int(target.get("feed_xp", 0)) + gained
	var lv := int(target.get("level", 0))
	var ups := 0
	while lv < SOUL_MAX_LEVEL and xp >= feed_xp_needed(lv):
		xp -= feed_xp_needed(lv)
		lv += 1
		ups += 1
	for i in GameState.souls.size():
		var s: Dictionary = GameState.souls[i]
		if str(s.get("id", "")) == target_id:
			s["feed_xp"] = xp
			s["level"] = lv
			GameState.souls[i] = s
			break
	SaveManager.save_game()
	var msg := _t("吸收 %d 顆魂 · 魂經驗+%d") % [eaten, gained]
	if ups > 0:
		msg += _t(" · 升至 %d 級！") % lv
	return {"ok": true, "eaten": eaten, "xp": gained, "level": lv, "ups": ups, "msg": msg}


## 一鍵吸收（原作）：把所有未入槽的大凶／凡 廢魂餵給最強的一顆
func absorb_junk_auto() -> Dictionary:
	var best_id := ""
	var best_score := -1.0
	var junk: Array = []
	for s in GameState.souls:
		var q := str(s.get("quality", "凡"))
		var sid := str(s.get("id", ""))
		if not bool(s.get("equipped", false)) and not bool(s.get("relic", false)) and q in ["大凶", "凡"]:
			junk.append(sid)
		var mult := 1.0
		for qd in QUALITIES:
			if str(qd.get("id", "")) == q:
				mult = float(qd.get("mult", 1.0))
				break
		var score := mult * 100.0 + float(int(s.get("level", 0)))
		if score > best_score:
			best_score = score
			best_id = sid
	## 最強那顆自己是廢魂時，別把它吃掉
	junk.erase(best_id)
	if best_id == "" or junk.is_empty():
		return {"ok": false, "msg": _t("沒有可吸收的廢魂（大凶／凡）。")}
	return absorb(best_id, junk)


func ritual_batch(n: int = 10) -> Array:
	## 連續抽魂；每抽吃當下葫蘆階（會跳階）。錢不夠就停。
	var out: Array = []
	for _i in n:
		if not can_ritual():
			break
		var s: Dictionary = ritual(true)
		if s.is_empty():
			break
		out.append(s)
	if not out.is_empty() and AudioManager and AudioManager.has_method("play_ritual_success"):
		AudioManager.play_ritual_success()
	return out


## 抽魂成功：sfx + 日誌
func _ritual_success_hooks(soul: Dictionary, from_vessel: String = "", used_free: bool = false, nv: Dictionary = {}, shard_got: int = 0) -> void:
	if AudioManager and AudioManager.has_method("play_ritual_success"):
		AudioManager.play_ritual_success()
	var tree := Engine.get_main_loop()
	if not (tree is SceneTree) or (tree as SceneTree).root == null:
		return
	var gl: Node = (tree as SceneTree).root.get_node_or_null("GameLog")
	if gl != null and gl.has_method("system"):
		var extra := ""
		if bool(nv.get("reset", false)):
			extra = _t("（同色頂階——魂器摔回綠葫蘆）")
		elif bool(nv.get("climbed", false)):
			extra = _t("（魂器升至 %s）") % str(nv.get("next", ""))
		var pay := _t("免費") if used_free else _t("%d 金") % vessel_cost(from_vessel)
		if shard_got > 0:
			extra += _t("（虔誠滿百——戰魂碎片+%d）") % shard_got
		gl.call("system", _t("抽魂凝出 %s（%s）｜%s｜%s%s") % [
			soul_display(soul), soul_bonus_line(soul), from_vessel, pay, extra
		])


func unequip_all_of(sid: String) -> void:
	ensure_slots()
	for i in GameState.soul_slots.size():
		if str(GameState.soul_slots[i]) == sid:
			GameState.soul_slots[i] = ""
	_set_soul_equipped(sid, false)


func _set_soul_equipped(sid: String, eq: bool) -> void:
	for i in GameState.souls.size():
		var s: Dictionary = GameState.souls[i]
		if str(s.get("id", "")) == sid:
			s["equipped"] = eq
			GameState.souls[i] = s
			return


func slot_soul(slot: int) -> Dictionary:
	ensure_slots()
	if slot < 0 or slot >= GameState.soul_slots.size():
		return {}
	return find_soul(str(GameState.soul_slots[slot]))


func compare_embed(sid: String, slot: int) -> Dictionary:
	## 新魂相對該槽現況的三圍差（空槽＝從 0 起算）
	var incoming: Dictionary = find_soul(sid)
	var cur: Dictionary = slot_soul(slot)
	var nb: Dictionary = calc_soul_bonus(incoming) if not incoming.is_empty() else {"atk": 0, "def": 0, "hp": 0}
	var ob: Dictionary = calc_soul_bonus(cur) if not cur.is_empty() else {"atk": 0, "def": 0, "hp": 0}
	var da: int = int(nb.get("atk", 0)) - int(ob.get("atk", 0))
	var dd: int = int(nb.get("def", 0)) - int(ob.get("def", 0))
	var dh: int = int(nb.get("hp", 0)) - int(ob.get("hp", 0))
	var bits: PackedStringArray = []
	if da > 0:
		bits.append(_t("攻+%d") % da)
	elif da < 0:
		bits.append(_t("攻%d") % da)
	if dd > 0:
		bits.append(_t("防+%d") % dd)
	elif dd < 0:
		bits.append(_t("防%d") % dd)
	if dh > 0:
		bits.append(_t("血+%d") % dh)
	elif dh < 0:
		bits.append(_t("血%d") % dh)
	var delta := "＝" if bits.is_empty() else " ".join(bits)
	var cur_name := soul_display(cur) if not cur.is_empty() else _t("（空）")
	return {
		"atk": da, "def": dd, "hp": dh,
		"line": _t("槽%d：%s → %s（%s）") % [slot + 1, cur_name, soul_display(incoming), delta],
	}


func equip_soul(sid: String, slot: int) -> String:
	## 回傳錯誤訊息；空字串＝成功
	ensure_slots()
	if slot < 0 or slot >= GameState.soul_slots.size():
		return _t("沒有這個魂槽。")
	var s: Dictionary = find_soul(sid)
	if s.is_empty():
		return _t("找不到這顆戰魂。")
	if bool(s.get("equipped", false)):
		unequip_all_of(sid)
	## 槽上原魂卸下
	var old: String = str(GameState.soul_slots[slot])
	if old != "":
		_set_soul_equipped(old, false)
	GameState.soul_slots[slot] = sid
	_set_soul_equipped(sid, true)
	return ""


func unequip_slot(slot: int) -> void:
	ensure_slots()
	if slot < 0 or slot >= GameState.soul_slots.size():
		return
	var sid: String = str(GameState.soul_slots[slot])
	if sid != "":
		_set_soul_equipped(sid, false)
	GameState.soul_slots[slot] = ""


func bag_souls() -> Array:
	## 未裝備
	var out: Array = []
	for s in GameState.souls:
		if not bool(s.get("equipped", false)):
			out.append(s)
	return out


func fuse_max_level(quality: String) -> int:
	if quality == "神":
		return SHEN_MAX_LEVEL
	return FUSE_MAX_LEVEL


func can_fuse(star: String, quality: String, level: int) -> bool:
	var cap := fuse_max_level(quality)
	if level + 1 > cap:
		return false
	var n := 0
	for s in bag_souls():
		if str(s.get("star", "")) == star \
				and str(s.get("quality", "")) == quality \
				and int(s.get("level", 0)) == level:
			n += 1
	return n >= FUSE_COUNT


func fuse(star: String, quality: String, level: int) -> Dictionary:
	if not can_fuse(star, quality, level):
		return {}
	var removed := 0
	var keep: Array = []
	for s in GameState.souls:
		if removed < FUSE_COUNT \
				and not bool(s.get("equipped", false)) \
				and str(s.get("star", "")) == star \
				and str(s.get("quality", "")) == quality \
				and int(s.get("level", 0)) == level:
			removed += 1
			continue
		keep.append(s)
	GameState.souls = keep
	var soul := {
		"id": "soul_%d_%d" % [Time.get_ticks_msec(), randi() % 10000],
		"star": star,
		"quality": quality,
		"level": level + 1,
		"equipped": false,
	}
	GameState.souls.append(soul)
	return soul


func grant_starter_soul() -> Dictionary:
	## C1 教學：凡·破軍
	var soul := {
		"id": "soul_starter_pojun",
		"star": "破軍",
		"quality": "凡",
		"level": 0,
		"equipped": false,
	}
	## 避免重複
	if find_soul(soul["id"]).is_empty():
		GameState.souls.append(soul)
	ensure_slots()
	if slot_count() >= 1 and str(GameState.soul_slots[0] if GameState.soul_slots.size() > 0 else "") == "":
		equip_soul(str(soul["id"]), 0)
	return soul


func panel_status_bbcode() -> String:
	ensure_slots()
	ensure_daily_free()
	var bonus: Dictionary = total_equipped_bonus()
	var lines: PackedStringArray = []
	lines.append(_t("[b]聚魂殿 · 戰魂[/b]"))
	lines.append(_t("神魂＝神品質戰魂（神-星名）。最高 10 級。"))
	lines.append(_t("魂器：%s") % vessel_ladder_bbcode())
	var cost := ritual_cost_gold()
	if cost <= 0:
		lines.append(_t("今日免費抽魂尚餘 %d 次｜金幣 %d｜星屑 %d") % [
			GameState.soul_free_draws, GameState.gold, GameState.stardust
		])
	else:
		lines.append(_t("下次抽魂：%d 金｜金幣 %d｜星屑 %d") % [
			cost, GameState.gold, GameState.stardust
		])
	lines.append(_t("虔誠度 %d/100 · 戰魂碎片 %d（稀世 6 片 · 神 15 片）") % [piety(), shards()])
	lines.append(_t("武器：%s  T%d · 魂槽 %d") % [GameState.weapon_display(), GameState.weapon_tier, slot_count()])
	lines.append(_t("入魂加成：攻+%d  防+%d  血+%d") % [
		int(bonus.get("atk", 0)), int(bonus.get("def", 0)), int(bonus.get("hp", 0))
	])
	lines.append("")
	lines.append(_t("[b]已入魂[/b]"))
	if slot_count() <= 0:
		lines.append(_t("（器階不足，尚無魂槽。先找釘釘養器。）"))
	else:
		for i in GameState.soul_slots.size():
			var sid: String = str(GameState.soul_slots[i])
			if sid == "":
				lines.append(_t("  槽%d：空") % (i + 1))
			else:
				var s: Dictionary = find_soul(sid)
				lines.append(_t("  槽%d：%s（%s）") % [i + 1, soul_display(s), soul_bonus_line(s)])
	lines.append("")
	lines.append(_t("[b]背包戰魂[/b]"))
	var bag: Array = bag_souls()
	if bag.is_empty():
		lines.append(_t("  （空）"))
	else:
		for s in bag:
			lines.append("  · %s  %s" % [soul_display(s), soul_bonus_line(s)])
	return "\n".join(lines)


## ---- 星盤調查（周天十四主星盤點）----
func quality_mult(q: String) -> float:
	for qd in QUALITIES:
		if str(qd.get("id", "")) == q:
			return float(qd.get("mult", 1.0))
	if q == "秘境":
		return 3.2
	return 1.0


func stat_inclination_name(stat: String) -> String:
	match stat:
		"all":
			return _t("全能均衡")
		"atk":
			return _t("攻擊偏向")
		"def":
			return _t("防禦偏向")
		"hp":
			return _t("氣血偏向")
		_:
			return stat


func survey_astrolabe() -> Dictionary:
	ensure_slots()
	var star_map: Dictionary = {}
	for st in STARS:
		var sid := str(st.get("id", ""))
		var stat_type := str(st.get("stat", "atk"))
		star_map[sid] = {
			"id": sid,
			"name": soul_word(sid),
			"stat": stat_type,
			"stat_name": stat_inclination_name(stat_type),
			"base": int(st.get("base", 1)),
			"label": str(st.get("label", "")),
			"is_lit": false,
			"count": 0,
			"equipped_count": 0,
			"bag_count": 0,
			"highest_quality": "",
			"highest_score": -1.0,
			"max_level": 0,
			"best_soul": {},
		}

	for s in GameState.souls:
		if typeof(s) != TYPE_DICTIONARY:
			continue
		var star_id := str(s.get("star", ""))
		if not star_map.has(star_id):
			continue
		var entry: Dictionary = star_map[star_id]
		entry["is_lit"] = true
		entry["count"] += 1
		var sid := str(s.get("id", ""))
		var is_eq := bool(s.get("equipped", false))
		if not is_eq and sid != "":
			is_eq = sid in GameState.soul_slots
		if is_eq:
			entry["equipped_count"] += 1
		else:
			entry["bag_count"] += 1

		var q := str(s.get("quality", "凡"))
		var lv := int(s.get("level", 0))
		var score := quality_mult(q) * 100.0 + float(lv)
		if score > float(entry["highest_score"]):
			entry["highest_quality"] = q
			entry["highest_score"] = score
			entry["max_level"] = lv
			entry["best_soul"] = s

	var lit_count := 0
	var stat_lit := {"all": 0, "atk": 0, "def": 0, "hp": 0}
	var stat_totals := {"all": 0, "atk": 0, "def": 0, "hp": 0}
	var stars_list: Array[Dictionary] = []
	for st in STARS:
		var sid := str(st.get("id", ""))
		var entry: Dictionary = star_map.get(sid, {})
		stars_list.append(entry)
		var st_type := str(entry.get("stat", "atk"))
		stat_totals[st_type] = int(stat_totals.get(st_type, 0)) + 1
		if bool(entry.get("is_lit", false)):
			lit_count += 1
			stat_lit[st_type] = int(stat_lit.get(st_type, 0)) + 1

	var relics: Array[Dictionary] = []
	for s in GameState.souls:
		if typeof(s) == TYPE_DICTIONARY and bool(s.get("relic", false)):
			relics.append(s)

	return {
		"stars": stars_list,
		"star_map": star_map,
		"lit_count": lit_count,
		"total_stars": STARS.size(),
		"stat_lit": stat_lit,
		"stat_totals": stat_totals,
		"total_souls": GameState.souls.size(),
		"equipped_bonus": total_equipped_bonus(),
		"relics": relics,
	}


func astrolabe_status_bbcode() -> String:
	var survey := survey_astrolabe()
	var lines: PackedStringArray = []
	lines.append(_t("[b]聚魂殿 · 周天星盤[/b]"))
	lines.append(_t("[color=#a0a8c0]「星盤偏了一角，像在等傭兵團最弱的那個。」[/color]"))
	lines.append("")

	var lit: int = int(survey.get("lit_count", 0))
	var tot: int = int(survey.get("total_stars", 14))
	var s_cnt: int = int(survey.get("total_souls", 0))
	var eq_cnt := 0
	for sid in GameState.soul_slots:
		if str(sid) != "":
			eq_cnt += 1
	var bag_cnt: int = maxi(0, s_cnt - eq_cnt)

	lines.append(_t("星盤點亮：%d / %d 主星 · 持有戰魂 %d 顆（入魂 %d，背包 %d）") % [
		lit, tot, s_cnt, eq_cnt, bag_cnt
	])

	var bonus: Dictionary = survey.get("equipped_bonus", {})
	lines.append(_t("入魂加成：攻+%d  防+%d  血+%d") % [
		int(bonus.get("atk", 0)), int(bonus.get("def", 0)), int(bonus.get("hp", 0))
	])
	lines.append("")

	var stat_lit: Dictionary = survey.get("stat_lit", {})
	var stat_tot: Dictionary = survey.get("stat_totals", {})
	lines.append(_t("[b]數值傾向分布[/b]"))
	lines.append(_t("  全能均衡：%d / %d 星點亮（紫微）") % [
		int(stat_lit.get("all", 0)), int(stat_tot.get("all", 1))
	])
	lines.append(_t("  攻擊偏向：%d / %d 星點亮（天機、太陽、武曲、廉貞、巨門、七殺、破軍）") % [
		int(stat_lit.get("atk", 0)), int(stat_tot.get("atk", 7))
	])
	lines.append(_t("  防禦偏向：%d / %d 星點亮（天府、天相、天梁）") % [
		int(stat_lit.get("def", 0)), int(stat_tot.get("def", 3))
	])
	lines.append(_t("  氣血偏向：%d / %d 星點亮（天同、太陰、貪狼）") % [
		int(stat_lit.get("hp", 0)), int(stat_tot.get("hp", 3))
	])
	lines.append("")

	lines.append(_t("[b]紫微十四主星盤點[/b]"))
	var stars: Array = survey.get("stars", [])
	for st in stars:
		var sid := str(st.get("id", ""))
		var sname := str(st.get("name", sid))
		var is_lit := bool(st.get("is_lit", false))
		var stat_name := str(st.get("stat_name", ""))
		var count := int(st.get("count", 0))
		var best_soul: Dictionary = st.get("best_soul", {})

		var lit_tag := _t("[已點亮]") if is_lit else _t("[未點亮]")
		var lit_color := "#ffd028" if is_lit else "#7a7890"
		var line := "  [color=%s]%s[/color] [b]%s[/b] · %s" % [lit_color, lit_tag, sname, stat_name]
		if is_lit:
			var best_desc := soul_display(best_soul)
			var bonus_desc := soul_bonus_line(best_soul)
			line += _t("（持有 %d 顆 · 最高 %s %s）") % [count, best_desc, bonus_desc]
		else:
			line += _t("（未感應）")
		lines.append(line)

	var relics: Array = survey.get("relics", [])
	if not relics.is_empty():
		lines.append("")
		lines.append(_t("[b]秘境異曜[/b]"))
		for r in relics:
			lines.append("  [color=#4ed86a]%s[/color] · %s" % [soul_display(r), soul_bonus_line(r)])

	return "\n".join(lines)
