extends SceneTree
## Mobile renderer profile 把關：godot --headless -s res://scripts/systems/test_renderer_profile.gd
##
## 驗：桌面／Web = gl_compatibility；手機 = mobile；features 不再謊稱 Forward Plus。


func _initialize() -> void:
	var ok := true
	var desktop := str(ProjectSettings.get_setting("rendering/renderer/rendering_method"))
	var mobile := str(ProjectSettings.get_setting("rendering/renderer/rendering_method.mobile"))
	var web := str(ProjectSettings.get_setting("rendering/renderer/rendering_method.web"))
	var features: PackedStringArray = ProjectSettings.get_setting("application/config/features")
	var feat_str := ",".join(features)

	if desktop != "gl_compatibility":
		push_error("desktop rendering_method 應為 gl_compatibility，得 %s" % desktop)
		ok = false
	else:
		print("desktop renderer OK: ", desktop)

	if mobile != "mobile":
		push_error("mobile rendering_method 應為 mobile，得 %s" % mobile)
		ok = false
	else:
		print("mobile renderer OK: ", mobile)

	if web != "gl_compatibility":
		push_error("web rendering_method 應為 gl_compatibility，得 %s" % web)
		ok = false
	else:
		print("web renderer OK: ", web)

	if "Forward Plus" in features:
		push_error("config/features 仍寫 Forward Plus（與實際 renderer 不符）：%s" % feat_str)
		ok = false
	if not ("GL Compatibility" in features):
		push_error("config/features 應含 GL Compatibility，得 %s" % feat_str)
		ok = false
	else:
		print("features OK: ", feat_str)

	print(
		"runtime rendering_method=",
		RenderingServer.get_current_rendering_method(),
		" os=",
		OS.get_name()
	)

	if ok:
		print("RENDERER_PROFILE_OK")
		quit(0)
	else:
		print("RENDERER_PROFILE_FAIL")
		quit(1)
