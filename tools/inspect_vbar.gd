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
    elif _frame == 55:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        var log_label: RichTextLabel = battle_node.get_node_or_null("LogPanel/Log")
        battle_node.call("_append_log", "[color=#fc0]部位破壞！【右腕重刃】打破擊暈！[/color]")
        battle_node.call("_append_log", "[color=#f52]怒氣滿 · 暴怒！（5 秒攻速與傷害提升）[/color]")
        battle_node.call("_append_log", "[color=#fa6]王者斬要擋，擋住就能反擊 · 火圈亮起後按 J 跳開[/color]")
    elif _frame == 65:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        var log_panel = battle_node.get_node_or_null("LogPanel")
        var log_label: RichTextLabel = battle_node.get_node_or_null("LogPanel/Log")
        var vbar = log_label.get_v_scroll_bar()
        print("VScrollBar value:", vbar.value)
        print("VScrollBar max:", vbar.max_value)
        print("VScrollBar page:", vbar.page)
        print("log_label content_height:", log_label.get_content_height())
        print("log_label visible lines:", log_label.get_visible_line_count())
        print("log_label total lines:", log_label.get_line_count())
        quit(0)
    return false
