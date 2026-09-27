extends SceneTree

func _initialize() -> void:
	var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
	print("Loaded EquipPanelScn: ", EquipPanelScn != null)
	quit(0)
