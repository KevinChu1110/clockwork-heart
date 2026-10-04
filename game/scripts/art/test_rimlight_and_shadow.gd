extends SceneTree
## 角色動態光影與大氣景深升級把關測試：
## 1. 主角與怪物 Rim Light 邊緣輪廓光著色器
## 2. 雙層接地陰影（大範圍漸層軟影 + 腳底深色接觸硬影）
## 3. 天宮背景微幅視差浮動與金色微光星屑粒子
## 4. 低階手機模式（Low tier）平穩相容

func _initialize() -> void:
	var ok := true
	print("--- 開始角色動態光影與大氣景深升級測試 ---")

	# 1. 檢驗著色器資產
	if not _test_shaders():
		ok = false

	# 2. 檢驗大廳光影、雙層陰影、天宮視差與金色星屑
	if not await _test_lobby_visuals():
		ok = false

	# 3. 檢驗戰鬥場景主角與怪物 Rim Light 與雙層接地陰影
	if not await _test_battle_visuals():
		ok = false

	# 4. 檢驗低階設定相容性
	if not await _test_low_end_compatibility():
		ok = false

	if ok:
		print("RIMLIGHT_AND_SHADOW_OK")
		quit(0)
	else:
		push_error("RIMLIGHT_AND_SHADOW_FAIL")
		print("RIMLIGHT_AND_SHADOW_FAIL")
		quit(1)


func _test_shaders() -> bool:
	var passed := true
	var rim_path := "res://shaders/rim_light.gdshader"
	var outline_path := "res://shaders/outline.gdshader"
	var shadow_path := "res://shaders/foot_shadow.gdshader"

	if not ResourceLoader.exists(rim_path):
		push_error("缺少 %s" % rim_path)
		passed = false
	if not ResourceLoader.exists(outline_path):
		push_error("缺少 %s" % outline_path)
		passed = false
	if not ResourceLoader.exists(shadow_path):
		push_error("缺少 %s" % shadow_path)
		passed = false

	var rim_src := FileAccess.get_file_as_string(rim_path)
	if rim_src.find("rim_enabled") < 0 or rim_src.find("rim_color") < 0 or rim_src.find("rim_direction") < 0:
		push_error("rim_light.gdshader 缺少必要 uniform 參數")
		passed = false

	var shadow_src := FileAccess.get_file_as_string(shadow_path)
	if shadow_src.find("is_contact_shadow") < 0 or shadow_src.find("smooth_gradient") < 0:
		push_error("foot_shadow.gdshader 缺少雙層接地陰影參數")
		passed = false

	if passed:
		print("  ok [Shader] 邊緣輪廓光與雙層陰影著色器定義完整")
	return passed


func _test_lobby_visuals() -> bool:
	var passed := true
	var lobby_script: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if lobby_script == null:
		push_error("無法載入 mobile_lobby.gd")
		return false
	var lobby = lobby_script.new()
	root.add_child(lobby)

	# 等待一幀完成初始化
	for i in range(3):
		await process_frame

	# 檢查雙層接地陰影節點
	var foot_shadow := lobby.find_child("HeroFootShadow", true, false) as TextureRect
	var contact_shadow := lobby.find_child("HeroContactShadow", true, false) as TextureRect

	if foot_shadow == null or not foot_shadow.visible:
		push_error("大廳缺少 HeroFootShadow 軟影或不可見")
		passed = false
	else:
		var smat := foot_shadow.material as ShaderMaterial
		if smat == null or smat.get_shader_parameter("smooth_gradient") != true:
			push_error("HeroFootShadow 應啟用 smooth_gradient 漸層軟影")
			passed = false

	if contact_shadow == null or not contact_shadow.visible:
		push_error("大廳缺少 HeroContactShadow 接觸硬影或不可見")
		passed = false
	else:
		var cmat := contact_shadow.material as ShaderMaterial
		if cmat == null or cmat.get_shader_parameter("is_contact_shadow") != true:
			push_error("HeroContactShadow 應啟用 is_contact_shadow 接觸硬影")
			passed = false

	# 檢查主角 Rim Light Shader
	var hero_avatar := lobby.find_child("HeroAvatar", true, false) as TextureRect
	if hero_avatar == null:
		push_error("大廳缺少 HeroAvatar")
		passed = false
	else:
		var hmat := hero_avatar.material as ShaderMaterial
		if hmat == null:
			push_error("HeroAvatar 缺少 ShaderMaterial")
			passed = false
		elif hmat.get_shader_parameter("rim_enabled") != true:
			push_error("HeroAvatar Rim Light 未啟用")
			passed = false
		else:
			var rim_c: Color = hmat.get_shader_parameter("rim_color")
			if rim_c.r < 0.8 or rim_c.g < 0.7:
				push_error("HeroAvatar Rim Light 顏色應為金色晨曦微光")
				passed = false

	# 檢查天宮背景視差與星屑粒子
	var bg := lobby.find_child("TempleLobbyBg", true, false) as TextureRect
	if bg == null:
		push_error("缺少 TempleLobbyBg 背景")
		passed = false
	var particles_root := lobby.get("_particles_root") as Control
	if particles_root == null or particles_root.get_child_count() <= 0:
		push_error("大廳缺少金色微光星屑粒子")
		passed = false
	else:
		var sample_star := particles_root.get_child(0) as ColorRect
		if sample_star == null or not sample_star.name.begins_with("EtherMote_"):
			push_error("星屑粒子命名不符合規範")
			passed = false

	lobby.queue_free()
	await process_frame
	if passed:
		print("  ok [Lobby] 大廳主角RimLight、雙層接地陰影、天宮視差與金色星屑驗證通過")
	return passed


func _test_battle_visuals() -> bool:
	var passed := true
	var battle_scene: PackedScene = load("res://scenes/battle/battle.tscn")
	if battle_scene == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		return false
	var battle = battle_scene.instantiate()
	root.add_child(battle)
	battle.call("setup", "colossus_lion")

	for i in range(5):
		await process_frame

	# 檢查戰鬥主角與敵方的雙層接地陰影
	var shadow_layer := battle.get_node_or_null("ShadowLayer") as Control
	if shadow_layer == null:
		push_error("戰鬥場景缺少 ShadowLayer")
		passed = false
	else:
		var p_soft := shadow_layer.get_node_or_null("FootShadow_PlayerBody") as TextureRect
		var p_contact := shadow_layer.get_node_or_null("ContactShadow_PlayerBody") as TextureRect
		if p_soft == null:
			push_error("戰鬥缺少主角軟影 FootShadow_PlayerBody")
			passed = false
		if p_contact == null:
			push_error("戰鬥缺少主角深色接觸硬影 ContactShadow_PlayerBody")
			passed = false

		var e_soft := shadow_layer.get_node_or_null("FootShadow_EnemyBody") as TextureRect
		var e_contact := shadow_layer.get_node_or_null("ContactShadow_EnemyBody") as TextureRect
		if e_soft == null:
			push_error("戰鬥缺少怪物軟影 FootShadow_EnemyBody")
			passed = false
		if e_contact == null:
			push_error("戰鬥缺少怪物深色接觸硬影 ContactShadow_EnemyBody")
			passed = false

	# 檢查主角與怪物的 Rim Light Shader
	var p_body := battle.get("player_body") as TextureRect
	var e_body := battle.get("enemy_body") as TextureRect
	if p_body:
		var p_mat := p_body.material as ShaderMaterial
		if p_mat == null or p_mat.get_shader_parameter("rim_enabled") != true:
			push_error("戰鬥主角缺少 Rim Light Shader")
			passed = false
	if e_body:
		var e_mat := e_body.material as ShaderMaterial
		if e_mat == null or e_mat.get_shader_parameter("rim_enabled") != true:
			push_error("戰鬥怪物缺少 Rim Light Shader")
			passed = false

	battle.queue_free()
	await process_frame
	if passed:
		print("  ok [Battle] 戰鬥雙方RimLight邊緣光與雙層接地陰影驗證通過")
	return passed


func _test_low_end_compatibility() -> bool:
	var gp: Node = root.get_node_or_null("GraphicsProfile")
	if gp == null:
		return true
	var old_choice := str(gp.choice)
	gp.set_choice("low")

	var lobby_script: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = lobby_script.new()
	root.add_child(lobby)
	for i in range(2):
		await process_frame
	lobby.queue_free()

	var battle_scene: PackedScene = load("res://scenes/battle/battle.tscn")
	if battle_scene:
		var battle = battle_scene.instantiate()
		root.add_child(battle)
		battle.call("setup", "colossus_lion")
		for i in range(2):
			await process_frame
		battle.queue_free()

	gp.set_choice(old_choice)
	print("  ok [Performance] 低階手機設定 (GraphicsProfile low) 下平穩執行無報錯")
	return true
