extends SceneTree

func _init():
    root.size = Vector2i(1280, 720)
    var win := root.get_window()
    if win: win.size = Vector2i(1280, 720)

var _frame = 0

func _process(delta):
    _frame += 1
    if _frame == 1:
        change_scene_to_file("res://scenes/main.tscn")
    elif _frame == 25:
        var main = current_scene
        var gs = root.get_node_or_null("GameState")
        if gs:
            gs.call("reset_new_game")
            gs.set("player_name", "小白")
            gs.set("player_race", "rabbit")
        main.call("_start_battle_raw", "road_bandit")
    elif _frame == 45:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        # Test 10 lines added
        for i in range(10):
            battle_node.call("_append_log", "Test message line %d" % i)
    elif _frame == 60:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        var log_label: RichTextLabel = battle_node.get_node_or_null("LogPanel/Log")
        var vbar = log_label.get_v_scroll_bar()
        print("After 10 lines - vbar value:", vbar.value, "max:", vbar.max_value, "page:", vbar.page)
        for i in range(log_label.get_line_count()):
            print("Line %d offset: %f" % [i, log_label.get_line_offset(i)])
        quit(0)
    return false
