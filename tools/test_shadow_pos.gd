extends SceneTree

func _init() -> void:
    var root_node = Control.new()
    root_node.size = Vector2(1280, 720)
    root.add_child(root_node)

    var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
    var battle: Control = b_scn.instantiate()
    root_node.add_child(battle)
    battle.call("setup", "wolf")
    
    var pb: TextureRect = battle.get_node("Arena/PlayerSlot/PlayerBody")
    var layer: Control = battle.get_node("ShadowLayer")
    var sh: TextureRect = layer.get_node("FootShadow_PlayerBody")
    
    print("Initial (scale 1.0):")
    print("  pb.global_position: ", pb.global_position)
    print("  sh.global_position: ", sh.global_position)
    print("  sh.size: ", sh.size)
    print("  sh.visible: ", sh.visible)
    
    battle.pivot_offset = Vector2(300, 360)
    battle.scale = Vector2(2.1, 2.1)
    
    print("After scale 2.1:")
    print("  pb.global_position: ", pb.global_position)
    print("  sh.global_position: ", sh.global_position)
    print("  sh.size: ", sh.size)
    
    quit(0)
