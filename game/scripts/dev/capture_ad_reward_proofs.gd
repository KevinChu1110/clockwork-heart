extends SceneTree
## 擷取獎勵型廣告（Mock）相關畫面截圖：
## godot --path game --headless -s res://scripts/dev/capture_ad_reward_proofs.gd

const EnergyLackDialogScript := preload("res://scripts/ui/energy_lack_dialog.gd")
const MockAdDialogScript := preload("res://scripts/ui/mock_ad_dialog.gd")
const BattleDefeatDialogScript := preload("res://scripts/battle/battle_defeat_dialog.gd")

var _frame: int = 0
var _out_dir: String = ""
var _current_dlg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	var en = root.get_node_or_null("EnergySystem")
	if gs:
		gs.reset_new_game()
		gs.energy = 2
	if en:
		en.refresh_ad_daily()


func _process(_delta: float) -> bool:
	_frame += 1

	if _frame == 2:
		# 1. 展示體力不足彈窗（觀看前：能量 2/15，剩餘 3/3 次）
		_current_dlg = EnergyLackDialogScript.new()
		root.add_child(_current_dlg)

	elif _frame == 4:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_ad_dialog_energy_before.png")
			img.save_png(p)
			print("SAVED_ENERGY_BEFORE: ", p)
		if _current_dlg:
			_current_dlg.queue_free()
			_current_dlg = null

	elif _frame == 6:
		# 2. 展示假讀秒占位廣告播放中
		_current_dlg = MockAdDialogScript.new()
		_current_dlg.setup("energy")
		root.add_child(_current_dlg)

	elif _frame == 8:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_ad_countdown_mock.png")
			img.save_png(p)
			print("SAVED_AD_COUNTDOWN: ", p)
		if _current_dlg:
			_current_dlg.queue_free()
			_current_dlg = null

	elif _frame == 10:
		# 3. 領取體力獎勵（+3 點體力），展示領取後狀態（能量 5/15，剩餘 2/3 次）
		var en = root.get_node_or_null("EnergySystem")
		if en:
			en.claim_ad_energy(3)
		_current_dlg = EnergyLackDialogScript.new()
		root.add_child(_current_dlg)

	elif _frame == 12:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_ad_dialog_energy_after.png")
			img.save_png(p)
			print("SAVED_ENERGY_AFTER: ", p)
		if _current_dlg:
			_current_dlg.queue_free()
			_current_dlg = null

	elif _frame == 14:
		# 4. 展示戰鬥失敗結算畫面（二次機會復活按鈕）
		_current_dlg = BattleDefeatDialogScript.new()
		root.add_child(_current_dlg)

	elif _frame == 16:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_ad_dialog_defeat.png")
			img.save_png(p)
			print("SAVED_DEFEAT_DIALOG: ", p)
		if _current_dlg:
			_current_dlg.queue_free()
			_current_dlg = null
		print("AD_REWARD_CAPTURE_OK")
		quit(0)

	return false
