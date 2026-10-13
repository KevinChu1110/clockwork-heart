extends SceneTree

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: Control = null
var _frame: int = 0

func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")
	gs.level = 20

	var w_sword := {
		"uid": "w_live_sword", "base_id": "sword", "name": "晨曦長劍", "line": "sword",
		"slot": "weapon", "tier": 1, "quality": "rare", "quality_label": "上品",
		"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 2.0, "crit_dmg": 5.0}
	}
	var w_spear := {
		"uid": "w_live_spear", "base_id": "spear", "name": "破浪長槍", "line": "spear",
		"slot": "weapon", "tier": 1, "quality": "uncommon", "quality_label": "良品",
		"rolled": {"atk": 12, "def": 2, "hp": 0, "crit": 1.0, "crit_dmg": 0.0}
	}
	var w_fist := {
		"uid": "w_live_fist", "base_id": "fist", "name": "熔火鐵拳", "line": "fist",
		"slot": "weapon", "tier": 1, "quality": "epic", "quality_label": "秘寶",
		"rolled": {"atk": 20, "def": 0, "hp": 10, "crit": 3.0, "crit_dmg": 10.0}
	}

	gs.equip_worn["w_live_sword"] = w_sword
	gs.equip_worn["w_live_spear"] = w_spear
	gs.equip_worn["w_live_fist"] = w_fist
	gs.weapon_loadout = ["w_live_sword", "w_live_spear", "w_live_fist"]
	gs.weapon_loadout_active = 0
	gs.equip_slots["weapon"] = "w_live_sword"

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
	_lobby.select_weapon_slot(1) # 選中副手長槍展示即時切換與暖橘選中態
	_lobby.refresh_weapon_slots()

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 2:
		_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
		_lobby.select_weapon_slot(1) # 選中副手長槍展示即時切換與暖橘選中態
		_lobby.refresh_weapon_slots()
	elif _frame == 10:
		var vp := root.get_viewport()
		var img := vp.get_texture().get_image()
		if img:
			var dir := DirAccess.open("res://")
			if not dir.dir_exists("proofs"):
				dir.make_dir("proofs")
			var p := "/opt/side/bravesoul-game/proofs/proof_lobby_weapon_loadout_live.png"
			img.save_png(p)
			print("CAPTURE_SAVED: ", p)
		quit(0)
	return false
