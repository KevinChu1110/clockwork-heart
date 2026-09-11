extends SceneTree
## Headless：驗證 W6-K3 紙娃娃組裝規則。
## 執行：godot --headless --path game -s res://scripts/systems/paper_doll_v2/test_paper_doll_v2.gd

const ConfigScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_config.gd")
const AssemblerScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_assembler.gd")


func _init() -> void:
	var ok := true
	var cfg = ConfigScript.new()
	if not cfg.load_from():
		print("PAPER_DOLL_V2_FAIL config")
		quit(1)
		return
	if not cfg.chest_binds_wind_stamina_glow():
		print("PAPER_DOLL_V2_FAIL chest_heart bind")
		ok = false
	if not cfg.back_key_always_on_back():
		print("PAPER_DOLL_V2_FAIL back_key rule")
		ok = false
	if cfg.mvp_weapon_class() != "one_hand":
		print("PAPER_DOLL_V2_FAIL mvp")
		ok = false

	var asm = AssemblerScript.new()
	if not asm.setup(cfg):
		print("PAPER_DOLL_V2_FAIL setup")
		quit(1)
		return

	# 副手不可非 empty
	if asm.equip("weapon_off", "shield_brass"):
		print("PAPER_DOLL_V2_FAIL weapon_off should reject")
		ok = false
	if str(asm.loadout.get("weapon_off", "")) != "empty":
		print("PAPER_DOLL_V2_FAIL weapon_off not empty")
		ok = false

	# 擋 two_hand
	if asm.set_weapon_class("two_hand"):
		print("PAPER_DOLL_V2_FAIL two_hand should reject")
		ok = false
	if asm.current_weapon_class != "one_hand":
		print("PAPER_DOLL_V2_FAIL weapon class drift")
		ok = false

	# 背鑰不可進主手
	if asm.equip("weapon_main", str(asm.loadout.get("back_key", "back_key_brass"))):
		print("PAPER_DOLL_V2_FAIL back_key in hand")
		ok = false

	asm.set_phase("explore")
	var pe := asm.composite_path_for_phase()
	asm.set_phase("battle")
	var pb := asm.composite_path_for_phase()
	asm.set_phase("dismantle")
	var pd := asm.composite_path_for_phase()
	if not (pe.ends_with("xiaobai_e03.png") and pb.ends_with("xiaobai_b02.png") and pd.ends_with("xiaobai_d02.png")):
		print("PAPER_DOLL_V2_FAIL composite map %s | %s | %s" % [pe, pb, pd])
		ok = false

	# 戰鬥相才見主手
	asm.set_phase("explore")
	if Array(asm.visible_slots_for_phase()).has("weapon_main"):
		print("PAPER_DOLL_V2_FAIL weapon on explore")
		ok = false
	asm.set_phase("battle")
	if not Array(asm.visible_slots_for_phase()).has("weapon_main"):
		print("PAPER_DOLL_V2_FAIL weapon missing on battle")
		ok = false
	if not Array(asm.visible_slots_for_phase()).has("back_key"):
		print("PAPER_DOLL_V2_FAIL back_key missing")
		ok = false

	if not asm.play_anim("one_hand_atk_1"):
		print("PAPER_DOLL_V2_FAIL atk1")
		ok = false

	# 資產存在
	for p in [pe, pb, pd]:
		if not FileAccess.file_exists(p):
			print("PAPER_DOLL_V2_FAIL missing asset %s" % p)
			ok = false

	print(JSON.stringify(asm.summary()))
	if ok:
		print("PAPER_DOLL_V2_SUCCESS")
		quit(0)
	else:
		print("PAPER_DOLL_V2_FAIL")
		quit(1)
