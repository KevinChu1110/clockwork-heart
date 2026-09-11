extends SceneTree

func _init():
    root.size = Vector2i(1280, 720)
    var win := root.get_window()
    if win: win.size = Vector2i(1280, 720)

var _frame = 0

func _align_log(rtl: RichTextLabel) -> void:
    var vbar := rtl.get_v_scroll_bar()
    if vbar == null: return
    var cur := vbar.value
    var count := rtl.get_line_count()
    for i in range(count):
        var off := rtl.get_line_offset(i)
        if off >= cur - 1.0:
            vbar.value = off
            print("Snapped vbar from", cur, "to line", i, "offset", off)
            break

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
        battle_node.call("_append_log", "[color=#fc0]部位破壞！【右腕重刃】打破擊暈！[/color]")
        battle_node.call("_append_log", "[color=#f52]怒氣滿 · 暴怒！（5 秒攻速與傷害提升）[/color]")
        battle_node.call("_append_log", "[color=#fa6]王者斬要擋，擋住就能反擊 · 火圈亮起後按 J 跳開[/color]")
    elif _frame == 55:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        var log_label: RichTextLabel = battle_node.get_node_or_null("LogPanel/Log")
        _align_log(log_label)
    elif _frame == 60:
        var img := root.get_viewport().get_texture().get_image()
        img.save_png("/tmp/test_snapped.png")
        quit(0)
    return false
