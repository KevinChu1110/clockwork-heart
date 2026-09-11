extends SceneTree

func _initialize() -> void:
    var base := ProjectSettings.globalize_path("res://")
    var gs: Node = root.get_node_or_null("GameState")
    if gs:
        gs.call("reset_new_game")
        gs.set("player_race", "macaque")
        gs.set("paperdoll_slots", {
            "race": "macaque",
            "costume": "costume_dawn_monk_tunic",
            "chassis": "paint_ivory_stock",
            "weapon": "wpn_spring_claws"
        })
    var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
    var battle: Control = b_scn.instantiate()
    root.add_child(battle)
    battle.call("setup", "wolf")
    
    var pb: TextureRect = battle.get_node("BattleField/PlayerTeam/PlayerSlot/PlayerBody")
    if pb and pb.texture:
        var img := pb.texture.get_image()
        if img:
            img.save_png("/tmp/dump_player_body.png")
            print("Successfully dumped player_body texture: size=", img.get_size())
            
    # Also check if there are child nodes under PlayerSlot or PlayerBody!
    var slot: Node = battle.get_node("BattleField/PlayerTeam/PlayerSlot")
    for child in slot.get_children():
        print("Child of PlayerSlot:", child.name, "type:", child.get_class(), "visible:", child.visible if "visible" in child else "N/A")
        if child is TextureRect and child.texture:
            print("  Texture:", child.texture.resource_path)
            
    quit(0)
