extends SceneTree

func _initialize() -> void:
    var gs: Node = root.get_node_or_null("GameState")
    if gs:
        gs.call("reset_new_game", "macaque")
        print("player_race: ", gs.get("player_race"))
        print("paperdoll_slots: ", gs.get("paperdoll_slots"))
        print("equip_slots: ", gs.get("equip_slots"))
    quit(0)
