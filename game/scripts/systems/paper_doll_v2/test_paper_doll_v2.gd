extends SceneTree
## Headless：驗證 W6-K3 紙娃娃單幀組裝。
## 執行：godot --headless --path game -s res://scripts/systems/paper_doll_v2/test_paper_doll_v2.gd

const ConfigScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_config.gd")
const AssemblerScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_assembler.gd")
const FramesScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_frames.gd")


func _init() -> void:
	var ok := true
	var cfg = ConfigScript.new()
	if not cfg.load_from():
		print("PAPER_DOLL_V2_FAIL config")
		quit(1)
		return

	var asm = AssemblerScript.new()
	if not asm.setup(cfg):
		print("PAPER_DOLL_V2_FAIL setup")
		quit(1)
		return

	if asm.equip("weapon_off", "shield_brass"):
		print("PAPER_DOLL_V2_FAIL weapon_off should reject")
		ok = false
	if str(asm.loadout.get("weapon_off", "")) != "empty":
		print("PAPER_DOLL_V2_FAIL weapon_off not empty")
		ok = false
	if asm.set_weapon_class("two_hand"):
		print("PAPER_DOLL_V2_FAIL two_hand should reject")
		ok = false

	asm.set_phase("explore")
	var pe: String = asm.frame_path_for_current()
	asm.set_phase("battle")
	var pb: String = asm.frame_path_for_current()
	asm.set_phase("dismantle")
	var pd: String = asm.frame_path_for_current()
	if not pe.ends_with("explore_walk.png"):
		print("PAPER_DOLL_V2_FAIL explore frame %s" % pe)
		ok = false
	if not pb.ends_with("oh_ready.png"):
		print("PAPER_DOLL_V2_FAIL ready frame %s" % pb)
		ok = false
	if not pd.ends_with("dismantle_pull.png"):
		print("PAPER_DOLL_V2_FAIL dismantle frame %s" % pd)
		ok = false

	asm.set_phase("battle")
	if not asm.play_anim("one_hand_atk_1"):
		print("PAPER_DOLL_V2_FAIL atk1")
		ok = false
	var atk: String = asm.frame_path_for_current()
	if not atk.ends_with("oh_atk_1.png"):
		print("PAPER_DOLL_V2_FAIL atk1 frame %s" % atk)
		ok = false

	# 裝備單幀存在
	for sid in ["outfit", "helmet", "weapon_main"]:
		var sp: String = asm.slot_texture_path(sid)
		if sp == "" or not FileAccess.file_exists(sp):
			print("PAPER_DOLL_V2_FAIL slot frame %s -> %s" % [sid, sp])
			ok = false

	for path in [pe, pb, pd, atk]:
		if not FileAccess.file_exists(path):
			print("PAPER_DOLL_V2_FAIL missing %s" % path)
			ok = false

	# strip 不得再當主路徑
	if "oh_anim_strip" in pe or "oh_anim_strip" in pb:
		print("PAPER_DOLL_V2_FAIL strip still primary")
		ok = false

	print(JSON.stringify(asm.summary()))
	if ok:
		print("PAPER_DOLL_V2_SUCCESS")
		quit(0)
	else:
		print("PAPER_DOLL_V2_FAIL")
		quit(1)
