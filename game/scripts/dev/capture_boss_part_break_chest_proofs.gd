extends SceneTree
## 實機 Framebuffer 截圖存證腳本：Boss 部位破壞掉落金色發條寶箱動效與機芯浮字提示
## 依據 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點三規範

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const BattleUnit := preload("res://scripts/battle/battle_unit.gd")

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _out_dir := "res://proofs/t_d514fe7c"
var _os_out_dir := ""


func _initialize() -> void:
	print("=== 開始執行 capture_boss_part_break_chest_proofs ===")
	_os_out_dir = ProjectSettings.globalize_path(_out_dir)
	DirAccess.make_dir_recursive_absolute(_os_out_dir)
	_step = 1
	_wait = 0


func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		push_error("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		push_error("get_image is null for %s" % filename)
		return
	var p := _os_out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
	else:
		push_error("save_png failed code=%d for %s" % [err, p])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 1. 載入戰鬥場景 Leo
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			_step = 2
			_wait = 0
		2:
			if _wait == 2:
				_battle.call("setup", "leo")
			if _wait == 6:
				_save_viewport("proof_01_battle_before_break.png", "Leo 部位破壞前戰鬥狀態")
				# 觸發部位破壞
				var break_data := {
					"boss_id": "leo",
					"part_id": "helm",
					"part_name": "獅衛重盔",
					"raw_name": "獅衛重盔",
					"staggered": true,
					"material": "knight_shard",
					"qty": 1,
					"hp": 200,
					"max_hp": 400,
				}
				_battle.call("_on_event", "part_broken", break_data)
				_step = 3
				_wait = 0
		3:
			# 破壞第 10 幀：寶箱彈跳躍起 (Pop Arc) 與金色流光粒子噴發
			if _wait == 10:
				_save_viewport("proof_02_battle_part_break_chest_bounce.png", "部位破壞瞬間寶箱彈起與金色流光")
			# 破壞第 26 幀：寶箱著地、軟陰影擴張、機芯浮字提示【機殼裝甲】彈出
			elif _wait == 26:
				_save_viewport("proof_03_battle_part_break_chest_landed_core_prompt.png", "寶箱落地彈跳與機芯提示浮字")
				if is_instance_valid(_battle):
					_battle.queue_free()
				_step = 4
				_wait = 0
		4:
			# 2. 測試巨偶戰鬥 (Colossus Lion)
			if _wait < 3:
				return false
			var b_scn_colossus: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn_colossus.instantiate()
			root.add_child(_battle)
			_step = 5
			_wait = 0
		5:
			if _wait == 2:
				_battle.call("setup", "colossus_lion")
			if _wait == 6:
				# 破壞巨偶溢能尖角 -> 鎖定發條發電機
				var break_colossus := {
					"boss_id": "colossus_lion",
					"part_id": "spike",
					"part_name": "溢能尖角",
					"raw_name": "溢能尖角",
					"staggered": true,
					"material": "iron_scrap",
					"qty": 1,
					"hp": 500,
					"max_hp": 1000,
				}
				_battle.call("_on_event", "part_broken", break_colossus)
			elif _wait == 26:
				_save_viewport("proof_04_battle_colossus_part_break_chest.png", "巨偶部位破壞寶箱掉落與發條發電機機芯提示")
				if is_instance_valid(_battle):
					_battle.queue_free()
				_step = 6
				_wait = 0
		6:
			print("=== capture_boss_part_break_chest_proofs 完成 ===")
			quit(0)
			return false
	return false
