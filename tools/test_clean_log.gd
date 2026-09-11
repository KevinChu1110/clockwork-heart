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
        var log_panel = battle_node.get_node_or_null("LogPanel")
        var log_label: RichTextLabel = battle_node.get_node_or_null("LogPanel/Log")
        
        # Increase content_margin_top on LogPanel
        var sb = log_panel.get_theme_stylebox("panel") as StyleBoxFlat
        sb.content_margin_top = 14
        sb.content_margin_bottom = 10
        sb.content_margin_left = 18
        sb.content_margin_right = 18
        
        # Clear and put 4 lines
        log_label.clear()
        log_label.append_text("[b][color=#1F1A3A]右側拇指：攻擊／技能／換武／鎖定／暫停／逃離。[/color][/b]\n")
        log_label.append_text("[b][color=#1F1A3A]敵手筋骨結實（防爆高）——爆擊難進，斧鎚硬砸最實在。[/color][/b]\n")
        log_label.append_text("[b][color=#A85A00]部位破壞！【右腕重刃】打破擊暈！[/color][/b]\n")
        log_label.append_text("[b][color=#C22B55]怒氣滿 · 暴怒！（5 秒攻速與傷害提升）[/color][/b]\n")
        log_label.append_text("[b][color=#A85A00]王者斬要擋，擋住就能反擊 · 火圈亮起後按 J 跳開[/color][/b]\n")
    elif _frame == 55:
        var img := root.get_viewport().get_texture().get_image()
        img.save_png("/tmp/test_clean_log.png")
        print("Saved clean log image.")
        quit(0)
    return false
