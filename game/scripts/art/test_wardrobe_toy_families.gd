extends SceneTree
## 衣櫥玩具家族與主角紙娃娃（任務書 §1 §2 §3 §6）
##   1. 衣櫥分頁只有四個玩具家族，順序固定
##   2. 從衣櫥走不到狐／獅／野豬：分頁、本體、卡片部件都不是毛皮種族
##   3. 舊種族 id 全部對得到新家族；舊毛皮存檔載入後改回兔子本體
##   4. 紙娃娃資料表剛好七層；兔子 512 圖層腳底對齊同一條基準線
##   5. 背後發條：8 格轉動幀，每 8 幀轉一格

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const PaperdollSelectDemo = preload("res://scripts/ui/paperdoll_select_demo.gd")
const ToyFamily = preload("res://scripts/art/toy_family.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const WindingKeyAnim = preload("res://scripts/art/winding_key_anim.gd")
const WindingKeyTicker = preload("res://scripts/art/winding_key_ticker.gd")

const EXPECTED_TABS := ["胡桃鉗兔", "八音盒", "錫兵", "旋轉木馬"]
const FUR := ["fox", "lion", "boar"]

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== test_wardrobe_toy_families ===")
	_check_family_table()
	_check_legacy_mapping()
	_check_save_normalize()
	_check_creation_hides_fur()
	_check_wardrobe()
	_check_seven_layers()
	_check_baseline()
	_check_key_frames()
	if _ok:
		print("WARDROBE_TOY_FAMILIES_OK")
		quit(0)
	else:
		print("WARDROBE_TOY_FAMILIES_FAIL")
		quit(1)


func _check_family_table() -> void:
	var names: Array = []
	for f in ToyFamily.FAMILIES:
		names.append(str(f.get("name_zh", "")))
	if names != EXPECTED_TABS:
		_fail("玩具家族順序不符：%s" % [names])
	for f in FUR:
		if not ToyFamily.is_fur_race(f):
			_fail("%s 應標成毛皮種族" % f)
		if ToyFamily.art_race_for(f) != "rabbit":
			_fail("%s 的本體應改回兔子，實際 %s" % [f, ToyFamily.art_race_for(f)])
	print("  ✓ 四個玩具家族：", names)


func _check_legacy_mapping() -> void:
	# 舊衣櫥／創角用過的每個種族 id 都要有對應家族
	var legacy_ids: Array = PaperdollSelectDemo.RACE_KEYS.duplicate()
	for opt in WardrobeDialog.RACE_FILTER_OPTIONS:
		legacy_ids.append(str(opt.get("id", "")))
	legacy_ids.append_array(FUR)
	for rid in legacy_ids:
		if not ToyFamily.LEGACY_RACE_TO_FAMILY.has(rid):
			_fail("舊種族 %s 沒有對應家族" % rid)
			continue
		var fam := ToyFamily.family_of(rid)
		if not ToyFamily.is_family(fam):
			_fail("舊種族 %s 對到不存在的家族 %s" % [rid, fam])
	var expect := {"rabbit": "nutcracker_rabbit", "fox": "music_box", "lion": "tin_soldier", "boar": "tin_soldier"}
	for rid in expect:
		if ToyFamily.family_of(rid) != expect[rid]:
			_fail("%s 應對到 %s，實際 %s" % [rid, expect[rid], ToyFamily.family_of(rid)])
	if ToyFamily.family_of("no_such_race") != ToyFamily.DEFAULT_FAMILY:
		_fail("未知 id 應回預設家族")
	for opt in WardrobeDialog.RACE_FILTER_OPTIONS:
		var rid := str(opt.get("id", ""))
		if rid in FUR or rid == "all":
			_fail("RACE_FILTER_OPTIONS 還留著 %s" % rid)
	print("  ✓ %d 個舊種族 id 都對得到家族" % legacy_ids.size())


func _check_save_normalize() -> void:
	var fur_ids := ToyFamily.fur_item_ids()
	for f in FUR:
		var d := {
			"player_race": f,
			"player_name": {"fox": "靈尾狐", "lion": "烈鬃獅", "boar": "鋼牙豕"}[f],
			"paperdoll_slots": {"race": f, "costume_id": "costume_nutcracker_guard"},
			"flags": {},
		}
		if not fur_ids.is_empty():
			d["paperdoll_slots"]["head_unit"] = fur_ids[0]
		var out := ToyFamily.normalize_legacy_save(d, fur_ids)
		if out["player_race"] != "rabbit":
			_fail("%s 存檔載入後本體應為 rabbit，實際 %s" % [f, out["player_race"]])
		if out["player_name"] != "小白":
			_fail("%s 存檔預設名字應改回小白，實際 %s" % [f, out["player_name"]])
		if out["flags"].get("wardrobe.family", "") != ToyFamily.family_of(f):
			_fail("%s 存檔家族旗標錯誤：%s" % [f, out["flags"]])
		if out["flags"].get("wardrobe.legacy_race", "") != f:
			_fail("%s 存檔沒有記下舊種族" % f)
		if out["paperdoll_slots"].get("race", "") != "rabbit":
			_fail("%s 存檔紙娃娃 race 應為 rabbit" % f)
		for v in out["paperdoll_slots"].values():
			if fur_ids.has(str(v)):
				_fail("%s 存檔仍留著毛皮專屬部件 %s" % [f, v])
	# 非毛皮存檔原樣不動；正規化可重複執行
	var keep := {"player_race": "macaque", "player_name": "靈爪猴", "paperdoll_slots": {"race": "macaque"}, "flags": {}}
	var keep_out := ToyFamily.normalize_legacy_save(keep.duplicate(true), fur_ids)
	if keep_out != keep:
		_fail("非毛皮存檔不該被改動：%s" % [keep_out])
	var twice := ToyFamily.normalize_legacy_save(ToyFamily.normalize_legacy_save({"player_race": "fox", "flags": {}}, fur_ids), fur_ids)
	if twice["player_race"] != "rabbit" or twice["flags"].get("wardrobe.family", "") != "music_box":
		_fail("正規化重複執行結果不穩定：%s" % [twice])
	# GameState.from_dict 實際走一次
	var gs: Node = root.get_node_or_null("GameState")
	if gs and gs.has_method("from_dict"):
		gs.call("from_dict", {"player_race": "lion", "player_name": "烈鬃獅", "paperdoll_slots": {"race": "lion"}, "flags": {}})
		if str(gs.get("player_race")) != "rabbit":
			_fail("GameState.from_dict 讀舊獅子存檔後 player_race=%s" % gs.get("player_race"))
		if str(gs.call("get_flag", "wardrobe.family", "")) != "tin_soldier":
			_fail("GameState.from_dict 沒寫入家族旗標")
		gs.call("reset_new_game", "rabbit")
	print("  ✓ 舊毛皮存檔改回兔子本體並記下家族")


func _check_creation_hides_fur() -> void:
	for f in FUR:
		if PaperdollSelectDemo.has_race_assets(f):
			_fail("創角畫面仍可選 %s" % f)
		if PaperdollSelectDemo.LAUNCH_RACES.has(f):
			_fail("LAUNCH_RACES 仍有 %s" % f)
	if not PaperdollSelectDemo.has_race_assets("rabbit"):
		_fail("兔子本體素材應該齊全")
	print("  ✓ 創角畫面不再出現狐／獅／野豬")


func _check_wardrobe() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
	var dlg = WardrobeDialog.new()
	root.add_child(dlg)

	var chip_ids: Array = dlg._filter_chips.keys()
	if chip_ids != ToyFamily.family_ids():
		_fail("衣櫥分頁應為四個家族，實際 %s" % [chip_ids])
	var chip_texts: Array = []
	for fid in chip_ids:
		chip_texts.append((dlg._filter_chips[fid] as Button).text)
	if chip_texts != EXPECTED_TABS:
		_fail("衣櫥分頁文字不符：%s" % [chip_texts])
	for f in FUR:
		if dlg._filter_chips.has(f):
			_fail("衣櫥仍有 %s 分頁" % f)
		if dlg.find_child("Chip_" + f, true, false) != null:
			_fail("衣櫥仍有 Chip_%s 節點" % f)

	var seen_counts := {}
	for fid in ToyFamily.family_ids() + FUR:
		if fid in FUR:
			dlg.set_race_filter(fid) # 舊呼叫：毛皮 id 只會切到對應家族
		else:
			(dlg._filter_chips[fid] as Button).pressed.emit()
		if ToyFamily.is_fur_race(dlg.current_race) or ToyFamily.is_fur_race(dlg.current_filter_race):
			_fail("切到 %s 後本體變成毛皮種族 %s" % [fid, dlg.current_race])
		if dlg.current_race != "rabbit":
			_fail("切到 %s 後本體應保持兔子，實際 %s" % [fid, dlg.current_race])
		if not ToyFamily.is_family(dlg.current_family):
			_fail("切到 %s 後分頁不是家族：%s" % [fid, dlg.current_family])
		if fid in FUR and dlg.current_family != ToyFamily.family_of(fid):
			_fail("舊 id %s 應切到 %s，實際 %s" % [fid, ToyFamily.family_of(fid), dlg.current_family])
		var total := 0
		for sid in dlg._displayed_items.keys():
			for item in dlg._displayed_items[sid]:
				total += 1
				var iid := str(item.get("id", ""))
				var irace := str(item.get("race_id", ""))
				if ToyFamily.is_fur_race(irace):
					_fail("[%s] %s 卡片 %s 來自毛皮種族 %s" % [fid, sid, iid, irace])
				if ToyFamily.fur_item_ids().has(iid):
					_fail("[%s] %s 卡片 %s 是毛皮專屬部件" % [fid, sid, iid])
				var fam := str(item.get("family", ""))
				if not fam.is_empty() and fam != dlg.current_family:
					_fail("[%s] %s 卡片 %s 屬於 %s 卻出現在 %s 分頁" % [fid, sid, iid, fam, dlg.current_family])
		if dlg._displayed_costumes.is_empty() or dlg._displayed_chassis.is_empty():
			_fail("[%s] 外裝或塗裝清單是空的" % fid)
		seen_counts[fid] = total
		# 卡片名稱不再帶種族前綴
		for sid in dlg._slot_cards.keys():
			for card in dlg._slot_cards[sid]:
				var lbl = (card as Node).find_child("NameLabel", true, false)
				if lbl is Label:
					for short in ["[狐]", "[獅]", "[野豬]"]:
						if short in (lbl as Label).text:
							_fail("卡片名稱仍帶 %s" % short)

	# 換裝存檔：本體寫兔子、家族寫旗標
	(dlg._filter_chips["tin_soldier"] as Button).pressed.emit()
	var sel: Dictionary = dlg.get_current_selections()
	if ToyFamily.is_fur_race(str(sel.get("race", ""))):
		_fail("目前選擇的本體是毛皮種族")
	if gs:
		var saved := {"family": ""}
		dlg.outfit_saved.connect(func(_r, _s): saved["family"] = str(gs.call("get_flag", "wardrobe.family", "")))
		dlg.confirm_selection() # 會順手 queue_free 衣櫥
		var saved_family: String = saved["family"]
		if str(gs.paperdoll_slots.get("race", "")) != "rabbit":
			_fail("換裝後 paperdoll_slots.race 應為 rabbit")
		if saved_family != "tin_soldier":
			_fail("換裝後家族旗標應為 tin_soldier，實際 %s" % saved_family)
	else:
		dlg.queue_free()
	print("  ✓ 衣櫥四分頁可切換，部件數：", seen_counts)


func _check_seven_layers() -> void:
	var canonical := ToyFamily.canonical_slot_ids()
	var expect := ["chassis", "head_unit", "optic_core", "costume", "back_curio", "weapon", "winding_key"]
	if canonical != expect:
		_fail("七層順序不符：%s" % [canonical])
	var spec_ids: Array = []
	for s in PaperdollRenderer.get_spec().get("slots_architecture", {}).get("slots", []):
		spec_ids.append(str(s.get("slot_id", "")))
	var a := spec_ids.duplicate()
	var b := canonical.duplicate()
	a.sort()
	b.sort()
	if a != b:
		_fail("紙娃娃資料表槽位應剛好七層 %s，實際 %s" % [b, a])
	var used: Array = []
	for e in PaperdollRenderer.get_sorted_slot_entries_512("rabbit", {}):
		used.append(str(e.get("slot_id", "")))
	for sid in used:
		if not canonical.has(sid):
			_fail("合成器用了七層以外的槽位 %s" % sid)
	var wslots: Array = []
	for d in WardrobeDialog.SEVEN_SLOTS:
		wslots.append(str(d.get("id", "")))
	wslots.sort()
	if wslots != b:
		_fail("衣櫥七槽與資料表不一致：%s" % [wslots])
	print("  ✓ 紙娃娃剛好七層：", canonical)


func _check_baseline() -> void:
	var base := ToyFamily.HERO_BASELINE_Y_512
	var dir := "res://assets/sprites/player/paperdoll/rabbit/"
	for paint in ["paint_ivory_stock", "paint_brass_gold", "paint_midnight_navy"]:
		var img := _img(dir + "chassis/%s_512.png" % paint)
		if img == null:
			_fail("缺少素體 %s" % paint)
			continue
		if img.get_width() != 512 or img.get_height() != 512:
			_fail("%s 不是 512 畫布" % paint)
		var bottom := _bottom_y(img)
		if absi(bottom - base) > 1:
			_fail("%s 腳底在 y=%d，基準線 %d" % [paint, bottom, base])
	for e in PaperdollRenderer.get_sorted_slot_entries_512("rabbit", {}):
		var p := str(e.get("texture_path", ""))
		if not p.ends_with("_512.png"):
			continue
		var img := _img(p)
		if img == null:
			continue
		if img.get_width() != 512 or img.get_height() != 512:
			_fail("%s 不是 512 畫布" % p)
		if _bottom_y(img) > base + 1:
			_fail("%s 超出腳底基準線（y=%d）" % [p, _bottom_y(img)])
	print("  ✓ 兔子 512 圖層腳底對齊 y=%d" % base)


func _check_key_frames() -> void:
	var frames := WindingKeyAnim.build_idle_key_frames_512("rabbit", {})
	if frames.size() != WindingKeyAnim.STEPS_PER_TURN:
		_fail("兔子鑰匙待機幀應為 8 張，實際 %d" % frames.size())
		return
	var key_rect := Rect2i(140, 256, 56, 80)
	var sigs := {}
	for f in frames:
		if f.get_width() != 512 or f.get_height() != 512:
			_fail("鑰匙幀不是 512 畫布")
		var crop := f.get_image().get_region(key_rect)
		sigs[hash(crop.get_data())] = true
	if sigs.size() < 6:
		_fail("鑰匙幀變化太少（%d 種）" % sigs.size())
	# 第 0 格與第 2 格（側面最窄）鑰匙可見像素要明顯不同 → 側面看得到在轉
	var a0 := _opaque_count(frames[0].get_image().get_region(key_rect))
	var a2 := _opaque_count(frames[2].get_image().get_region(key_rect))
	if a0 <= a2:
		_fail("鑰匙轉到側面時應變窄：%d vs %d" % [a0, a2])
	# 鑰匙以外的區域不受影響
	var outside := Rect2i(220, 300, 120, 150)
	if frames[0].get_image().get_region(outside).get_data() != frames[3].get_image().get_region(outside).get_data():
		_fail("鑰匙動畫改到了本體")

	# 節拍：每 8 幀進一格
	var rect := TextureRect.new()
	root.add_child(rect)
	rect.texture = PaperdollRenderer.build_composite_texture_512("rabbit", {})
	var t = WindingKeyTicker.new()
	rect.add_child(t)
	t.set_process(false)
	t.attach(rect, func(): return {"race": "rabbit", "sel": {}})
	t.set_process(false)
	var changed_at: Array = []
	for i in range(1, 25):
		if t.tick():
			changed_at.append(i)
	if changed_at != [8, 16, 24]:
		_fail("鑰匙應在第 8／16／24 幀轉一格，實際 %s" % [changed_at])
	if not frames.has(rect.texture):
		_fail("節拍器沒有把貼圖換成鑰匙幀")
	# 非待機（攻擊姿勢）時不碰貼圖
	var pose := ImageTexture.create_from_image(Image.create(300, 400, false, Image.FORMAT_RGBA8))
	rect.texture = pose
	for i in range(16):
		t.tick()
	if rect.texture != pose:
		_fail("姿勢貼圖被鑰匙節拍器蓋掉")
	rect.queue_free()
	print("  ✓ 鑰匙 8 格、每 8 幀轉一格（%d 種畫面）" % sigs.size())


func _img(path: String) -> Image:
	if ResourceLoader.exists(path):
		var t := load(path) as Texture2D
		if t:
			var i := t.get_image()
			if i.is_compressed():
				i.decompress()
			return i
	if FileAccess.file_exists(path):
		return Image.load_from_file(ProjectSettings.globalize_path(path))
	return null


func _bottom_y(img: Image) -> int:
	var used := img.get_used_rect()
	return used.position.y + used.size.y - 1


func _opaque_count(img: Image) -> int:
	var n := 0
	for y in range(img.get_height()):
		for x in range(img.get_width()):
			if img.get_pixel(x, y).a > 0.3:
				n += 1
	return n
