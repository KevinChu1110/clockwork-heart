extends SceneTree

func _init() -> void:
    print("=== Testing SpriteDB.player_pose with fox race ===")
    GameState.player_race = "fox"
    
    var poses := ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    for p in poses:
        var tex: Texture2D = SpriteDB.player_pose(p)
        assert(tex != null, "Pose %s must not be null!" % p)
        var path: String = tex.resource_path
        print("Fox pose [%s] -> %s (size: %s)" % [p, path, tex.get_size()])
        assert("poses/fox/" in path, "Expected poses/fox/ in path, got: %s" % path)
        
    print("ALL FOX POSES LOADED CORRECTLY IN GODOT!")
    quit(0)
