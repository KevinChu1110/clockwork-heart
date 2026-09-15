extends Node
## 天宮鐵匠鍛造系統 (ForgeSystem)
## 統一管理鍛造階數上限、升階費用、成功率判定與連敗保底邏輯。
## Autoload：ForgeSystem

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

## 鍛造階數上限（T1～T11）
const FORGE_MAX_TIER := 11
const MAX_TIER := FORGE_MAX_TIER

## 升階價倍率（隨階數增加：升階價 = 這個數 × 目前階數）
const FORGE_COST_PER_TIER := 40
const COST_PER_TIER := FORGE_COST_PER_TIER

const MAX_FAIL_STREAK := 3


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## 升階費用計算
func forge_cost() -> int:
	return FORGE_COST_PER_TIER * maxi(1, GameState.weapon_tier)


## 基礎成功率隨階下降（最低 0.45）
func forge_rate_base() -> float:
	return maxf(0.45, 0.80 - 0.03 * float(GameState.weapon_tier - 1))


## 執行鍛造升階判定
## 回傳 Dictionary 包含 ok, code, tier, atk, used_scrap, cost, fail_streak 等結果
func try_forge() -> Dictionary:
	if GameState.weapon_tier >= FORGE_MAX_TIER:
		return {"ok": false, "code": "tier_max"}

	var cost := forge_cost()
	if GameState.gold < cost:
		return {"ok": false, "code": "no_gold", "cost": cost}

	GameState.add_gold(-cost)

	var forge_rate := forge_rate_base()
	if GameState.has_flag("meta.forge_debt_bonus"):
		forge_rate = 0.88
	if GameState.path_style in ["hammer", "crystal"]:
		forge_rate = minf(0.95, forge_rate + 0.08)

	## 消耗 1 鐵屑可提高成功率
	var used_scrap := false
	if InventorySystem.has_item("iron_scrap", 1):
		InventorySystem.remove_item("iron_scrap", 1)
		forge_rate = minf(0.96, forge_rate + 0.12)
		used_scrap = true

	var ok := randf() < forge_rate or GameState.forge_fail_streak >= 3
	QuestSystem.track_day("craft", 1)

	if ok:
		GameState.weapon_tier += 1
		GameState.forge_fail_streak = 0
		var forged_atk := _apply_forge_atk_gain(2)
		if AudioManager.has_method("play_craft_success"):
			AudioManager.play_craft_success()
		SaveManager.save_game()
		return {
			"ok": true,
			"code": "success",
			"tier": GameState.weapon_tier,
			"atk": forged_atk,
			"used_scrap": used_scrap,
			"cost": cost
		}
	else:
		GameState.forge_fail_streak += 1
		if GameState.forge_fail_streak >= 3:
			## W4 釘釘摔錘（連敗 3 次 · 主線可截圖記憶點）
			GameState.forge_fail_streak = 0
			GameState.hp = mini(GameState.max_hp, GameState.hp + 15)
			if AudioManager.has_method("play"):
				AudioManager.play("break", 0.92, -2.0)
			SaveManager.save_game()
			return {
				"ok": false,
				"code": "pity_break",
				"used_scrap": used_scrap,
				"cost": cost
			}
		else:
			SaveManager.save_game()
			return {
				"ok": false,
				"code": "failed",
				"fail_streak": GameState.forge_fail_streak,
				"used_scrap": used_scrap,
				"cost": cost
			}


func _apply_forge_atk_gain(atk_gain: int = 2) -> int:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var es: Node = (tree as SceneTree).root.get_node_or_null("EquipmentSystem")
		if es and es.has_method("forge_active_weapon"):
			var res: Dictionary = es.call("forge_active_weapon", atk_gain, GameState.weapon_tier)
			return int(res.get("atk", GameState.weapon_atk))

	## Fallback: 直接更新 equip_worn 與 legacy mirror
	var wuid := str(GameState.equip_slots.get("weapon", "")) if GameState.equip_slots != null else ""
	if wuid != "" and GameState.equip_worn != null and GameState.equip_worn.has(wuid):
		var w: Dictionary = (GameState.equip_worn[wuid] as Dictionary).duplicate(true)
		var r: Dictionary = (w.get("rolled", {}) as Dictionary).duplicate(true)
		r["atk"] = int(r.get("atk", 0)) + atk_gain
		w["rolled"] = r
		w["tier"] = GameState.weapon_tier
		GameState.equip_worn[wuid] = w
		GameState.weapon_atk = int(r["atk"])
		return GameState.weapon_atk

	GameState.weapon_atk += atk_gain
	return GameState.weapon_atk

