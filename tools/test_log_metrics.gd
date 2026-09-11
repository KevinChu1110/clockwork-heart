extends SceneTree

func _init():
    root.size = Vector2i(1280, 720)
    var win := root.get_window()
    if win: win.size = Vector2i(1280, 720)

var _frame = 0

func _process(delta):
    _frame += 1
    if _frame == 1:
        # Load main and battle
        change_scene_to_file("res://scenes/main.tscn")
    elif _frame == 25:
        var main = current_scene
        var gs = root.get_node_or_null("GameState")
        if gs:
            gs.call("reset_new_game")
            gs.set("player_name", "小白")
            gs.set("player_race", "rabbit")
        main.call("_start_battle_raw", "road_bandit")
    elif _frame == 55:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        var log_panel = battle_node.get_node_or_null("LogPanel")
        var log_label = battle_node.get_node_or_null("LogPanel/Log")
        print("LogPanel:", log_panel)
        print("LogLabel:", log_label)
        if log_panel and log_label:
            var sb = log_panel.get_theme_stylebox("panel")
            print("sb content_margin_top:", sb.content_margin_top)
            print("sb content_margin_bottom:", sb.content_margin_bottom)
            print("log_panel clip_contents:", log_panel.clip_contents)
            print("log_label clip_contents:", log_label.clip_contents)
            print("log_label size:", log_label.size)
            print("log_label position:", log_label.position)
            print("log_panel size:", log_panel.size)
            print("log_panel position:", log_panel.position)
        quit(0)
    return false
