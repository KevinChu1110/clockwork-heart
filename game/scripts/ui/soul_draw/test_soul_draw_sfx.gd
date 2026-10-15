extends SceneTree
## #91：抽魂流程音效。
## 1. 五個框色各播自己的檔（AudioManager 實際播出的 stream 路徑），金／彩不跟紫共用。
## 2. 實際掉落（白／藍／紫）走對應的檔；十連只播一聲、取最高框。
## 3. 演出開始播 summon；跳過會收掉 summon，不再加聲音。
## 4. 每個時刻 AudioManager 同時在響 ≤2 聲（按抽＋召喚、跳過後翻卡、十連結算）。

const Sfx := preload("res://scripts/ui/soul_draw/soul_draw_sfx.gd")
const ResultCard := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const TenPull := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")
const SummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const SFX_DIR := "res://assets/audio/sfx/"
const EXPECT := {
	"white": "reveal_white", "blue": "reveal_blue", "purple": "reveal_purple",
	"gold": "reveal_gold", "rainbow": "reveal_rainbow",
}
## 各框色的 volume_db（照 game/assets/audio/MANIFEST.md 抽魂翻卡表）
const EXPECT_DB := {"white": -5.0, "blue": 0.0, "purple": 0.0, "gold": 0.0, "rainbow": 0.0}

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _process(_d: float) -> bool:
	_frame += 1
	if _frame < 3:
		return false
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager autoload missing")
	else:
		am.call("set_muted", false)
		_run(am)
	print("TEST_SOUL_DRAW_SFX_OK" if _ok else "TEST_SOUL_DRAW_SFX_FAIL")
	quit(0 if _ok else 1)
	return true


func _stop_all(am: Node) -> void:
	for p in am.get("_pool"):
		(p as AudioStreamPlayer).stop()


## 現在在響的 SFX 檔名（不含副檔名）
func _playing(am: Node) -> Array[String]:
	var out: Array[String] = []
	for p in am.get("_pool"):
		var ap := p as AudioStreamPlayer
		if ap.playing and ap.stream:
			out.append(ap.stream.resource_path.get_file().get_basename())
	return out


func _cap(am: Node, label: String) -> void:
	var now := _playing(am)
	if now.size() > 2:
		_fail("%s：同時 %d 聲 %s，超過 2" % [label, now.size(), str(now)])
	else:
		print("  ok %s：同時 %d 聲 %s" % [label, now.size(), str(now)])


func _run(am: Node) -> void:
	var streams: Dictionary = am.get("_streams")
	# 0. 檔案都有載入，而且五個 key 是五個不同的檔
	var paths := {}
	for f in EXPECT:
		var key: String = EXPECT[f]
		if not streams.has(key):
			_fail("AudioManager 沒載入 %s（SFX 清單沒加？）" % key)
			continue
		paths[f] = (streams[key] as AudioStream).resource_path
	if not streams.has("summon"):
		_fail("AudioManager 沒載入 summon")
	if paths.size() == 5:
		var uniq := {}
		for f in paths:
			uniq[paths[f]] = true
		if uniq.size() != 5:
			_fail("五個框色的翻卡檔有重複：%s" % str(paths))

	# 1. 五個框色：AudioManager 實際播出的檔
	for f in EXPECT:
		_stop_all(am)
		Sfx.calls.clear()
		Sfx.play_reveal_frame(f)
		var now := _playing(am)
		if now != [EXPECT[f]]:
			_fail("[%s] 翻卡應只播 %s，實際在響 %s" % [f, EXPECT[f], str(now)])
		var sfx_db: float = float(am.get("_sfx_db"))
		for p in am.get("_pool"):
			var ap := p as AudioStreamPlayer
			if ap.playing and ap.stream and ap.stream.resource_path.get_file().get_basename() == EXPECT[f]:
				var got := ap.volume_db - sfx_db
				if not is_equal_approx(got, float(EXPECT_DB[f])):
					_fail("[%s] %s 音量應為 %+.1f dB，實際 %+.1f dB" % [f, EXPECT[f], EXPECT_DB[f], got])
	if _ok:
		print("  ok 五個框色各播自己的檔與音量 %s %s" % [str(EXPECT.values()), str(EXPECT_DB.values())])

	# 2. 實際掉落 → 對應框色的檔
	var card: Control = ResultCard.new()
	root.add_child(card)
	var drops := {
		"white": {"kind": "junk", "DropId": "junk_enamel_chip"},
		"blue": {"kind": "part", "DropId": "drop_spring_coil"},
		"purple": {"kind": "outfit", "DropId": "outfit_cream"},
	}
	for f in drops:
		_stop_all(am)
		card.call("show_drop", drops[f])
		var now := _playing(am)
		if now != [EXPECT[f]]:
			_fail("[%s] 單抽翻卡應播 %s，實際 %s" % [f, EXPECT[f], str(now)])
	print("  ok 單抽翻卡：白／藍／紫掉落播 reveal_white／reveal_blue／reveal_purple")

	# 3. 十連：只播一聲、取最高框
	var ten: Control = TenPull.new()
	root.add_child(ten)
	var ten_drops: Array[Dictionary] = []
	for i in 9:
		ten_drops.append(drops["blue"])
	ten_drops.append(drops["purple"])
	_stop_all(am)
	Sfx.calls.clear()
	ten.call("show_drops", ten_drops)
	var now10 := _playing(am)
	if now10 != ["reveal_purple"]:
		_fail("十連（含紫）結算應只播 reveal_purple 一聲，實際 %s" % str(now10))
	else:
		print("  ok 十連結算只播最高框一聲：%s" % str(now10))

	# 4. 演出：按抽＋summon ≤2；跳過收掉 summon；跳過後翻卡 ≤2
	var fx: Control = SummonFx.new()
	root.add_child(fx)
	_stop_all(am)
	Sfx.calls.clear()
	Sfx.play_pull()
	fx.call("play_summon", true, func(): pass)
	if not _playing(am).has("summon"):
		_fail("召喚開始應播 summon，實際 %s" % str(_playing(am)))
	_cap(am, "按抽＋召喚開始")
	fx.call("skip")
	if _playing(am).has("summon"):
		_fail("跳過後 summon 還在響（殘響）")
	var played_after := Sfx.calls.filter(func(c): return not str(c[0]).begins_with("stop:") and c[0] != "summon" and c[0] != "ui")
	if not played_after.is_empty():
		_fail("跳過演出不該補播聲音：%s" % str(played_after))
	Sfx.play_reveal_frame("rainbow")
	_cap(am, "跳過後立刻出彩框")
	if _ok:
		print("  ok 召喚播 summon，跳過收掉 summon、不留殘響")

	# 5. 按抽：play_pull 走 play_ui
	am.set("last_sfx", "")
	Sfx.play_pull()
	if str(am.get("last_sfx")) != "ui":
		_fail("按抽應播 ui，last_sfx=%s" % str(am.get("last_sfx")))
	_stop_all(am)
