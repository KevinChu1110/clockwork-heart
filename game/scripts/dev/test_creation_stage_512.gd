extends SceneTree

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

func _initialize() -> void:
	print("=== 測試開局選族中央舞台 512 渲染狀態 ===")
	var demo = DemoScene.instantiate()
	demo.creation_mode = true
	root.add_child(demo)

	var races = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant"]
	for r in races:
		demo.call("select_race", r)
		var is_512 = demo.call("is_stage_512")
		var tex = demo.call("get_stage_texture")
		var sz = tex.get_size() if tex else Vector2.ZERO
		var sprite = demo.call("get_stage_sprite_512")
		var filter = sprite.texture_filter if sprite else -1
		print("Race: %-8s | is_stage_512: %-5s | size: %-12s | filter: %d (2=LINEAR)" % [r, str(is_512), str(sz), filter])

	print("\n--- 測試換外裝／塗裝即時重合成 ---")
	# 兔族切換外裝 (0: nutcracker 512, 1: steam_artisan (LANCZOS), 2: royal_parade (LANCZOS), 3: none 512)
	demo.call("select_race", "rabbit")
	print("[Rabbit default 0]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")

	demo.call("_on_costume_next_pressed") # 1: steam_artisan
	print("[Rabbit costume 1]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")

	demo.call("_on_costume_next_pressed") # 2: royal_parade
	print("[Rabbit costume 2]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")

	demo.call("_on_costume_next_pressed") # 3: none
	print("[Rabbit costume 3 (none)]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")

	# 鶴族切換外裝 (0: zephyr_robe (LANCZOS), 1: sky_hunter (LANCZOS), 2: none 512)
	demo.call("select_race", "crane")
	print("\n[Crane default 0]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")
	demo.call("_on_costume_next_pressed") # 1: sky_hunter
	print("[Crane costume 1]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")
	demo.call("_on_costume_next_pressed") # 2: none (裸機素體)
	print("[Crane costume 2 (none)]: is_512=", demo.call("is_stage_512"), " size=", demo.call("get_stage_texture").get_size() if demo.call("get_stage_texture") else "null")

	demo.queue_free()
	print("\nCREATION_STAGE_512_OK")
	quit(0)
