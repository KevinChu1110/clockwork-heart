extends Node
## 待機發條節拍器：掛在顯示主角的 TextureRect 底下，每 8 幀把貼圖換成下一格鑰匙轉動幀。
## 主角在做其他動作（攻擊、受擊…）時，宿主讓 idle_check 回 false，這裡就不碰貼圖。
## 只接手 512 紙娃娃合成圖；沒存過外觀時用的手繪展示立繪（鑰匙畫死在圖上）維持靜態。
##
##   var t = WindingKeyTicker.new()
##   rect.add_child(t)
##   t.attach(rect, func(): return {"race": "rabbit", "sel": {...}}, func(): return is_idle)
##
## sel_provider 省略時讀 GameState.paperdoll_slots；idle_check 省略時永遠視為待機。

const WindingKeyAnim = preload("res://scripts/art/winding_key_anim.gd")
const ToyFamily = preload("res://scripts/art/toy_family.gd")

var target: Control = null
var sel_provider: Callable = Callable()
var idle_check: Callable = Callable()
var frame_count := 0
var step := 0
var steps_taken := 0
var _frames: Array[Texture2D] = []
var _frames_key := ""


func attach(rect: Control, provider: Callable = Callable(), is_idle: Callable = Callable()) -> void:
	target = rect
	sel_provider = provider
	idle_check = is_idle
	frame_count = 0
	set_process(true)


func _process(_delta: float) -> void:
	tick()


## 推進一幀；剛好滿 8 幀時換下一格。回傳這幀有沒有換格。
func tick() -> bool:
	frame_count += 1
	if frame_count % WindingKeyAnim.FRAMES_PER_STEP != 0:
		return false
	return advance_step()


## 直接進一格（大廳點擊等互動也可以呼叫）
func advance_step() -> bool:
	if target == null or not is_instance_valid(target) or not ("texture" in target):
		return false
	if idle_check.is_valid() and not bool(idle_check.call()):
		return false
	var cur: Texture2D = target.get("texture") as Texture2D
	if cur == null:
		return false
	var frames := current_frames()
	if frames.size() != WindingKeyAnim.STEPS_PER_TURN:
		return false
	# 只接手紙娃娃 512 合成圖（或自己的幀）；手繪展示立繪的鑰匙是畫死的，不硬換成合成圖
	if not frames.has(cur) and not is_paperdoll_canvas(cur):
		return false
	step = (step + 1) % WindingKeyAnim.STEPS_PER_TURN
	steps_taken += 1
	target.set("texture", frames[step])
	return true


static func is_paperdoll_canvas(t: Texture2D) -> bool:
	return t != null and t.get_width() == WindingKeyAnim.CANVAS and t.get_height() == WindingKeyAnim.CANVAS


func current_frames() -> Array[Texture2D]:
	var info := _current_info()
	var race: String = str(info.get("race", ToyFamily.HERO_ART_RACE))
	var sel: Dictionary = info.get("sel", {})
	var key := "%s:%s" % [race, JSON.stringify(sel)]
	if key != _frames_key:
		_frames_key = key
		_frames = WindingKeyAnim.build_idle_key_frames_512(race, sel)
	return _frames


func _current_info() -> Dictionary:
	if sel_provider.is_valid():
		var v: Variant = sel_provider.call()
		if v is Dictionary:
			return v
	var race := ToyFamily.HERO_ART_RACE
	var sel: Dictionary = {}
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if "player_race" in gs:
				# 跟宿主畫的本體一致（SpriteDB 讀原值），不另外換本體，免得把別族合成圖換成兔子幀
				var raw := str(gs.get("player_race")).strip_edges().to_lower()
				race = raw if not raw.is_empty() else ToyFamily.HERO_ART_RACE
			if "paperdoll_slots" in gs and gs.get("paperdoll_slots") is Dictionary:
				sel = (gs.get("paperdoll_slots") as Dictionary).duplicate()
	if not sel.has("costume") and sel.has("costume_id"):
		sel["costume"] = sel["costume_id"]
	if not sel.has("chassis") and sel.has("paint_id"):
		sel["chassis"] = sel["paint_id"]
	sel.erase("race")
	return {"race": race, "sel": sel}
