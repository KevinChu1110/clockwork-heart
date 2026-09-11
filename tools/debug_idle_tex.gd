extends SceneTree

func _initialize() -> void:
    var gs: Node = root.get_node_or_null("GameState")
    if gs:
        gs.call("reset_new_game")
        gs.set("player_race", "macaque")
    
    var slots = {
        "race": "macaque",
        "costume": "costume_dawn_monk_tunic",
        "chassis": "paint_ivory_stock",
        "weapon": "wpn_spring_claws"
    }
    
    var tex: Texture2D = SpriteDB.player_equipped_idle("macaque", slots)
    print("player_equipped_idle result:")
    print("  Type:", tex.get_class() if tex else "null")
    if tex:
        print("  Resource path:", tex.resource_path)
        print("  Size:", tex.get_size())
        var img := tex.get_image()
        if img:
            img.save_png("/tmp/debug_equipped_idle_macaque.png")
            print("  Saved /tmp/debug_equipped_idle_macaque.png")
            
    var fb = SpriteDB.player_pose("idle", "macaque")
    print("player_pose('idle', 'macaque'):")
    print("  Resource path:", fb.resource_path if fb else "null")
    
    quit(0)
