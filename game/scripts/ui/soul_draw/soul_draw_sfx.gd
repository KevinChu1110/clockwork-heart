extends RefCounted
## 抽魂流程音效（#91）。只走 AudioManager 既有 API（play / play_ui）。
## - reveal 系列只用在抽魂翻卡（brief §5）；五個框色各播自己的檔（reveal_<色>）。
## - 每個時刻最多 2 聲（#16 的兩聲上限）：開場 ui＋summon，翻卡只播 1 個檔。
## - 十連一次只播一聲 reveal（取最高框），不疊十聲。

const Catalog := preload("res://scripts/ui/soul_draw/soul_draw_card_catalog.gd")

## 框色 → 翻卡音效 [key, volume_db]（PR #99 的分級檔；每張只播一個檔、只佔 1 個 voice）
## 五個框色各有自己的檔（白 reveal_white，#99 76dc7f32），金和彩不再跟紫共用。
const REVEAL_BY_FRAME := {
	"white": ["reveal_white", 0.0],
	"blue": ["reveal_blue", 0.0],
	"purple": ["reveal_purple", 0.0],
	"gold": ["reveal_gold", 0.0],
	"rainbow": ["reveal_rainbow", 0.0],
}
## 由低到高（十連結算取最高那張）
const FRAME_ORDER: Array[String] = ["white", "blue", "purple", "gold", "rainbow"]

## 測試用：最近播過的 [key, pitch, db]
static var calls: Array = []


static func _am() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("AudioManager")
	return null


static func _play(key: String, pitch: float = 1.0, db: float = 0.0) -> void:
	calls.append([key, pitch, db])
	var am := _am()
	if am and am.has_method("play"):
		am.call("play", key, pitch, db)


## 按下單抽／十連
static func play_pull() -> void:
	calls.append(["ui", 1.0, -2.0])
	var am := _am()
	if am and am.has_method("play_ui"):
		am.call("play_ui")


## 召喚演出開始：summon（發條上緊＋彈簧放開，PR #99）
static func play_summon_start(_is_ten: bool) -> void:
	_play("summon")


## 跳過演出：收掉還在響的 summon（0.95 秒），翻卡音才不會疊在殘響上
static func stop_summon() -> void:
	calls.append(["stop:summon", 1.0, 0.0])
	var am := _am()
	if am and am.has_method("stop_sfx"):
		am.call("stop_sfx", "summon")


static func frame_for_drop(drop: Dictionary) -> String:
	var key := Catalog.frame_key_for_drop(Catalog.normalize_drop(drop))
	return key if REVEAL_BY_FRAME.has(key) else "blue"


## 翻卡／結果卡出現
static func play_reveal_frame(frame: String) -> void:
	var cfg: Array = REVEAL_BY_FRAME.get(frame, REVEAL_BY_FRAME["blue"])
	_play(str(cfg[0]), 1.0, float(cfg[1]))


static func play_reveal_for_drop(drop: Dictionary) -> void:
	play_reveal_frame(frame_for_drop(drop))


## 十連結算：只播一次，取最高框
static func play_reveal_for_drops(drops: Array) -> void:
	var best := 0
	for d in drops:
		if d is Dictionary:
			best = maxi(best, FRAME_ORDER.find(frame_for_drop(d)))
	play_reveal_frame(FRAME_ORDER[best])
