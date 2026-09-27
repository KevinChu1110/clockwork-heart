extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

func _init() -> void:
    var gs: Node = root.get_node_or_null("GameState")
    if gs:
        gs.set("player_race", "hedgehog")
        gs.set("paperdoll_slots", {})
    
    var lobby = MobileLobby.new()
    root.add_child(lobby)
    
    # Wait one frame for ready
    await process_frame
    
    var vp: Viewport = root.get_viewport()
    vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    await process_frame
    await process_frame
    
    var hero_avatar = lobby.get("_hero_avatar") as TextureRect
    if hero_avatar:
        print("Hero avatar global rect:", hero_avatar.get_global_rect())
        var tex = hero_avatar.texture
        print("Texture path:", tex.resource_path if tex else "null")
        print("Texture size:", tex.get_size() if tex else Vector2.ZERO)
    
    quit()
