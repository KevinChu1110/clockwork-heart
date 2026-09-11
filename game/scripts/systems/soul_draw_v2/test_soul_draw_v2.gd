extends SceneTree
## Headless：W7-K1b 四角色 loadout＋SoulDraw 池。
## godot --headless --path game -s res://scripts/systems/soul_draw_v2/test_soul_draw_v2.gd

const ConfigScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_config.gd")
const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const LoadoutScript := preload("res://scripts/systems/paper_doll_v2/character_loadout.gd")


func _init() -> void:
	var ok := true
	var cfg = ConfigScript.new()
	if not cfg.load_from():
		print("SOUL_DRAW_V2_FAIL config")
		quit(1)
		return
	if cfg.total_weight() != 100:
		print("SOUL_DRAW_V2_FAIL weight_sum=%d" % cfg.total_weight())
		ok = false
	for bad in ["tin_soldier", "gear_bear"]:
		if cfg.is_character_allowed(bad):
			print("SOUL_DRAW_V2_FAIL blocked leaked %s" % bad)
			ok = false
	for good in ["xiaobai", "lion", "fox", "pig"]:
		if not cfg.is_character_allowed(good):
			print("SOUL_DRAW_V2_FAIL missing %s" % good)
			ok = false

	var loadout = LoadoutScript.new()
	if not loadout.setup(cfg):
		print("SOUL_DRAW_V2_FAIL loadout")
		quit(1)
		return
	if loadout.select_character("tin_soldier"):
		print("SOUL_DRAW_V2_FAIL tin_soldier allowed")
		ok = false
	if not loadout.select_character("lion"):
		print("SOUL_DRAW_V2_FAIL lion select")
		ok = false
	if str(loadout.summary().get("outfitId", "")) != "outfit_brass_vest":
		print("SOUL_DRAW_V2_FAIL lion default outfit")
		ok = false

	# 資產存在
	for cid in ["xiaobai", "lion", "fox", "pig"]:
		var p: String = loadout.base_path(cid)
		if not FileAccess.file_exists(p):
			print("SOUL_DRAW_V2_FAIL missing base %s" % p)
			ok = false
	if not FileAccess.file_exists(loadout.outfit_atlas_path()):
		print("SOUL_DRAW_V2_FAIL missing atlas")
		ok = false

	var pool = PoolScript.new()
	if not pool.setup(cfg, 42):
		print("SOUL_DRAW_V2_FAIL pool")
		quit(1)
		return
	var seen_outfit := false
	var seen_part := false
	for i in 80:
		var drop: Dictionary = pool.pull()
		if not bool(drop.get("ok", false)):
			print("SOUL_DRAW_V2_FAIL pull")
			ok = false
			break
		var kind: String = str(drop.get("kind", ""))
		if kind == "outfit":
			seen_outfit = true
			loadout.apply_soul_drop(drop)
		elif kind == "part":
			seen_part = true
	if not seen_outfit or not seen_part:
		print("SOUL_DRAW_V2_FAIL pool coverage outfit=%s part=%s" % [seen_outfit, seen_part])
		ok = false

	# hard pity：連續非 outfit 達 hardPity 應強制 outfit
	var pool2 = PoolScript.new()
	pool2.setup(cfg, 7)
	pool2.pulls_since_outfit = 19
	var forced: Dictionary = pool2.pull()
	if str(forced.get("kind", "")) != "outfit" or not bool(forced.get("pityForced", false)):
		print("SOUL_DRAW_V2_FAIL hard pity %s" % str(forced))
		ok = false

	# alias：Alice 短名 → K1b
	if cfg.resolve_outfit_id("scarf_tunic") != "outfit_scarf_tunic":
		print("SOUL_DRAW_V2_FAIL alias scarf")
		ok = false
	if cfg.resolve_outfit_id("apron") != "outfit_worker_apron":
		print("SOUL_DRAW_V2_FAIL alias apron")
		ok = false
	if not loadout.unlock_outfit("scarf_tunic"):
		print("SOUL_DRAW_V2_FAIL unlock alias")
		ok = false
	var sample: Dictionary = pool.pull()
	if str(sample.get("toastKey", "")).find("soul.pull_") != 0 and str(sample.get("toastKey", "")).find("soul.pity_") != 0:
		print("SOUL_DRAW_V2_FAIL toastKey %s" % str(sample.get("toastKey", "")))
		ok = false

	# rabbit → xiaobai；junk_enamel_chip
	if cfg.resolve_character_id("rabbit") != "xiaobai":
		print("SOUL_DRAW_V2_FAIL rabbit alias")
		ok = false
	if not loadout.select_character("rabbit"):
		print("SOUL_DRAW_V2_FAIL select rabbit")
		ok = false
	if loadout.active_character_id != "xiaobai":
		print("SOUL_DRAW_V2_FAIL rabbit not canonical")
		ok = false
	if cfg.resolve_drop_id("junk_scrap") != "junk_enamel_chip":
		print("SOUL_DRAW_V2_FAIL junk alias")
		ok = false
	var junk_ok := false
	for e in cfg.loot_table:
		if typeof(e) == TYPE_DICTIONARY and str((e as Dictionary).get("DropId", "")) == "junk_enamel_chip":
			junk_ok = true
	if not junk_ok:
		print("SOUL_DRAW_V2_FAIL junk_enamel_chip missing")
		ok = false

	print(JSON.stringify({
		"loadout": loadout.summary(),
		"sampleForced": forced,
		"weight": cfg.total_weight(),
	}))
	if ok:
		print("SOUL_DRAW_V2_SUCCESS")
		quit(0)
	else:
		print("SOUL_DRAW_V2_FAIL")
		quit(1)
