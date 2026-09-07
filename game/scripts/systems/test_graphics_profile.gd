extends SceneTree
## Low / Mid / High 繪圖 profile 把關：godot --headless -s res://scripts/systems/test_graphics_profile.gd
##
## 驗：三檔可讀可存、Low 真的關掉高成本項、High 不砍開發機、縮小 viewport 模擬低階。


func _initialize() -> void:
	var gp: Node = root.get_node_or_null("GraphicsProfile")
	if gp == null:
		push_error("GraphicsProfile autoload 缺失")
		print("GRAPHICS_PROFILE_FAIL")
		quit(1)
		return

	var ok := true
	var saved_choice := str(gp.choice)

	## 1) 三檔規格真的差得出來
	var low: Dictionary = gp.spec("low")
	var mid: Dictionary = gp.spec("mid")
	var high: Dictionary = gp.spec("high")
	if bool(low.get("shadows", true)) or bool(low.get("particles", true)) or bool(low.get("vfx", true)):
		push_error("Low 應關掉陰影／粒子／裝飾特效，得 %s" % str(low))
		ok = false
	if float(low.get("render_scale", 1.0)) >= float(mid.get("render_scale", 1.0)):
		push_error("Low render_scale 應 < Mid")
		ok = false
	if float(mid.get("render_scale", 1.0)) >= float(high.get("render_scale", 1.0)):
		push_error("Mid render_scale 應 < High")
		ok = false
	if not bool(high.get("shadows", false)) or not bool(high.get("particles", false)) or not bool(high.get("vfx", false)):
		push_error("High 應接近現況：陰影／粒子／特效全開，得 %s" % str(high))
		ok = false
	if int(gp.cost_score("low")) >= int(gp.cost_score("mid")) or int(gp.cost_score("mid")) >= int(gp.cost_score("high")):
		push_error("cost_score 應 Low < Mid < High，得 %d %d %d" % [
			int(gp.cost_score("low")), int(gp.cost_score("mid")), int(gp.cost_score("high"))
		])
		ok = false
	else:
		print("tier specs OK: low=", low.get("render_scale"), " mid=", mid.get("render_scale"), " high=", high.get("render_scale"))

	## 2) 可切、可存、可讀
	gp.set_choice("low")
	if str(gp.choice) != "low" or str(gp.applied) != "low" or gp.shadows_enabled() or gp.particles_enabled() or gp.vfx_enabled():
		push_error("set_choice(low) 後 applied/開關不符 choice=%s applied=%s shadows=%s" % [
			gp.choice, gp.applied, gp.shadows_enabled()
		])
		ok = false
	if gp.particle_count(14) != 0:
		push_error("Low particle_count(14) 應為 0，得 %d" % gp.particle_count(14))
		ok = false

	var f := FileAccess.open(gp.PATH, FileAccess.READ)
	if f == null:
		push_error("存檔讀不到 %s" % gp.PATH)
		ok = false
	else:
		var data = JSON.parse_string(f.get_as_text())
		if typeof(data) != TYPE_DICTIONARY or str(data.get("choice", "")) != "low":
			push_error("存檔 choice 應為 low，得 %s" % str(data))
			ok = false
		else:
			print("save/load OK: ", data)

	gp.load_settings()
	if str(gp.choice) != "low":
		push_error("load_settings 後 choice 應仍為 low，得 %s" % gp.choice)
		ok = false

	gp.set_choice("mid")
	if str(gp.applied) != "mid" or not gp.shadows_enabled() or gp.particle_count(14) != 7:
		push_error("Mid 應開陰影且粒子減半（14→7），applied=%s count=%d" % [gp.applied, gp.particle_count(14)])
		ok = false
	else:
		print("mid OK: particle_count 14→", gp.particle_count(14))

	gp.set_choice("high")
	if str(gp.applied) != "high" or not gp.shadows_enabled() or not gp.vfx_enabled() or gp.particle_count(14) != 14:
		push_error("High 應全開，applied=%s count=%d" % [gp.applied, gp.particle_count(14)])
		ok = false
	else:
		print("high OK: shadows/vfx on, particles full")

	## 3) auto 在桌面不得落到 Low（不砍開發機）
	gp.set_choice("auto")
	var detected := str(gp.detect_device_tier())
	var osn := OS.get_name()
	if osn in ["Windows", "Linux", "macOS", "FreeBSD", "Web"] and detected != "high":
		push_error("桌面 auto 應 detect=high，得 %s os=%s" % [detected, osn])
		ok = false
	if str(gp.applied) != detected:
		push_error("auto applied 應等於 detect_device_tier，applied=%s detect=%s" % [gp.applied, detected])
		ok = false
	else:
		print("auto/desktop OK: os=", osn, " detect=", detected, " applied=", gp.applied)

	## 4) 低階模擬：縮小 viewport + 讀 GLES／compatibility renderer
	var win := root.get_window()
	var old_size := Vector2i.ZERO
	if win != null:
		old_size = win.size
		win.size = Vector2i(640, 360)
	gp.set_choice("low")
	gp.apply()
	var method := str(RenderingServer.get_current_rendering_method())
	var scale_size := Vector2i.ZERO
	if win != null:
		scale_size = win.content_scale_size
	print("low-end sim: window=", old_size, "→", win.size if win else Vector2i.ZERO,
		" content_scale_size=", scale_size,
		" applied_content_size=", gp.applied_content_size,
		" render_scale=", gp.applied_scale,
		" method=", method,
		" os=", osn)
	if gp.applied_content_size != Vector2i(640, 360) or float(gp.applied_scale) != 0.5:
		push_error("Low 應落到 640×360 / scale 0.5，得 size=%s scale=%s" % [str(gp.applied_content_size), gp.applied_scale])
		ok = false
	if win != null and win.size.x > 0 and scale_size != Vector2i(640, 360):
		push_error("有視窗時 Low 應把 content_scale_size 設成 640×360，得 %s" % str(scale_size))
		ok = false
	if method == "":
		push_error("RenderingServer.get_current_rendering_method 空的")
		ok = false
	## 本機預設 gl_compatibility（GLES-class）。headless 視窗常是 0×0，所以用 applied_content_size 當解析度證據。
	print("low-end sim notes: shadows=", gp.shadows_enabled(), " particles=", gp.particles_enabled(), " vfx=", gp.vfx_enabled())

	gp.set_choice("high")
	gp.apply()
	if gp.applied_content_size != Vector2i(1280, 720) or float(gp.applied_scale) != 1.0:
		push_error("High 應還原 1280×720 / scale 1.0，得 size=%s scale=%s" % [str(gp.applied_content_size), gp.applied_scale])
		ok = false
	if win != null:
		win.size = old_size

	## 還原玩家 preference，避免污染 user://
	gp.set_choice(saved_choice if saved_choice in ["auto", "low", "mid", "high"] else "auto")

	if ok:
		print("GRAPHICS_PROFILE_OK")
		quit(0)
	else:
		print("GRAPHICS_PROFILE_FAIL")
		quit(1)
