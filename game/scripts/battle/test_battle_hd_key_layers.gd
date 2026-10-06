extends SceneTree
## 全新存檔戰鬥中鑰匙會轉（#48）：godot --headless -s res://scripts/battle/test_battle_hd_key_layers.gd
##
## 沒存過外觀時 player_body 退回展示立繪 HD。美術把它拆成身體／鑰匙兩層（#27），
## 這支守：
##   1. 待機時 player_body 換成身體層，後面有一張可見的 HdKeyLayer（show_behind_parent）
##   2. 鑰匙層樞軸在 HD 畫布 (512,970) 換算後的位置
##   3. 每 8 幀轉一格，至少看到 2 種不同的 scale.y；身體貼圖不變
##   4. 換成非待機姿勢時鑰匙層收起、不疊在動作圖上；回待機再出現

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _ok := true
var _frame := 0
var _step := 0
var _battle: Control = null
var _body: TextureRect = null
var _layer: TextureRect = null
var _scales: Dictionary = {}
var _body_tex: Texture2D = null
var _watch := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			var gs := root.get_node_or_null("GameState")
			if gs == null:
				_fail("GameState autoload 沒載起來")
				return _finish()
			gs.reset_new_game()  ## 全新存檔：不經創角、沒存過外觀
			var layers: Dictionary = SpriteDB.hero_showcase_hd_layers("rabbit")
			if layers.is_empty():
				_fail("讀不到 rabbit_idle_hd_body／_key（PR #45 的圖）")
				return _finish()
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			_battle.call("setup", "wolf")
			_body = _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
			_step = 1
		1:
			if _frame < 6:
				return false
			var layers: Dictionary = SpriteDB.hero_showcase_hd_layers("rabbit")
			if _body.texture != layers["body"]:
				_fail("新存檔待機時 player_body 應是身體層，實際：%s" % (_body.texture.resource_path if _body.texture else "null"))
				return _finish()
			_layer = _body.get_node_or_null("HdKeyLayer") as TextureRect
			if _layer == null or not _layer.visible or _layer.texture != layers["key"]:
				_fail("沒有可見的 HdKeyLayer（鑰匙層）")
				return _finish()
			if not _layer.show_behind_parent:
				_fail("鑰匙層要在身體後面（show_behind_parent）")
			print("  ok 新存檔待機：身體層＋後面一張鑰匙層")
			var dr: Rect2 = _battle.call("_body_drawn_rect", _body)
			var ts := _layer.texture.get_size()
			var want := dr.position + Vector2(512, 970) * (dr.size / ts)
			if _layer.pivot_offset.distance_to(want) > 0.5:
				_fail("鑰匙層樞軸應在 %s，實際 %s" % [want, _layer.pivot_offset])
			else:
				print("  ok 樞軸 (512,970) → %s" % _layer.pivot_offset)
			_body_tex = _body.texture
			_scales.clear()
			_watch = 0
			_step = 2
		2:
			_watch += 1
			_scales[snappedf(_layer.scale.y, 0.001)] = true
			if _body.texture != _body_tex:
				_fail("轉鑰匙時身體貼圖不該變")
				return _finish()
			if _watch < 40:
				return false
			if _scales.size() < 2:
				_fail("40 幀內鑰匙沒有轉（scale.y 只有 %s）" % str(_scales.keys()))
				return _finish()
			var ticker := _body.get_node_or_null("WindingKeyTicker")
			print("  ok 40 幀內鑰匙轉了 %d 格，看到 %d 種 scale.y：%s" % [
				int(ticker.get("steps_taken")) if ticker else -1, _scales.size(), str(_scales.keys())])
			_battle.call("_set_player_pose", "attack", true)
			if _layer.visible:
				_fail("攻擊姿勢時鑰匙層應收起")
			else:
				print("  ok 非待機姿勢收起鑰匙層")
			_battle.call("_set_player_pose", "idle")
			if not _layer.visible:
				_fail("回到待機時鑰匙層應再出現")
			else:
				print("  ok 回待機鑰匙層再出現")
			return _finish()
	return false


func _finish() -> bool:
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
	if _ok:
		print("BATTLE_HD_KEY_LAYERS_OK")
		quit(0)
	else:
		print("BATTLE_HD_KEY_LAYERS_FAIL")
		quit(1)
	return true
