extends SceneTree

func _initialize() -> void:
    var gs: Node = root.get_node_or_null("GameState")
    if gs:
        gs.set("player_race", "macaque")
    var tex = SpriteDB.player_pose("attack", "macaque")
    print("SpriteDB.player_pose('attack', 'macaque'): ", tex)
    if tex:
        print("  resource_path: ", tex.resource_path)
    var tex_idle = SpriteDB.player_pose("idle", "macaque")
    print("SpriteDB.player_pose('idle', 'macaque'): ", tex_idle)
    if tex_idle:
        print("  resource_path: ", tex_idle.resource_path)
    quit(0)
