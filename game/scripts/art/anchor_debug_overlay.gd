class_name AnchorDebugOverlay
extends Control
## 錨點與骨骼階層視覺化覆蓋層
## 繪製 Character.wz 骨骼連線與 neck/navel/hand/brow/back_key 錨點圓點與標籤

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")

@export var paperdoll_path: NodePath = ^"../DollContainer/MaplePaperdoll"
var _paperdoll: Node2D = null


func _ready() -> void:
	z_index = 100
	z_as_relative = false
	if not paperdoll_path.is_empty():
		_paperdoll = get_node_or_null(paperdoll_path) as Node2D


func _draw() -> void:
	if _paperdoll == null:
		return

	# 取得 5 大核心錨點（及可能具備的 tail 尾巴錨點）的世界座標 (轉為本 Control 區域座標)
	var anchors: Dictionary = {
		"neck": _get_anchor_pos(_paperdoll.node_neck),
		"brow": _get_anchor_pos(_paperdoll.node_brow),
		"navel": _get_anchor_pos(_paperdoll.node_navel),
		"hand": _get_anchor_pos(_paperdoll.node_hand),
		"back_key": _get_anchor_pos(_paperdoll.node_back_key)
	}

	# 骨骼連接線 (深藍紫描邊帶金色核心線)
	var bones: Array = [
		["neck", "brow", Color(0.2, 0.8, 1.0, 0.85)],       # 頸到眉
		["neck", "navel", Color(0.3, 0.85, 0.4, 0.85)],     # 頸到臍 (軀幹脊椎)
		["navel", "hand", Color(1.0, 0.65, 0.1, 0.85)],     # 臍到手 (持握手臂)
		["navel", "back_key", Color(1.0, 0.35, 0.5, 0.85)], # 臍到背鑰 (動力傳動軸)
	]

	# 若當前種族具備 tail 尾巴錨點（如烈金雄獅）
	if is_instance_valid(_paperdoll.node_tail):
		var anchors_dict: Dictionary = _paperdoll._spec.get("anchors", {})
		if anchors_dict.has("tail"):
			anchors["tail"] = _get_anchor_pos(_paperdoll.node_tail)
			bones.append(["navel", "tail", Color(0.75, 0.45, 1.0, 0.85)])

	for bone in bones:
		var p1: Vector2 = anchors[bone[0]]
		var p2: Vector2 = anchors[bone[1]]
		var col: Color = bone[2]
		# 底線深紫描邊
		draw_line(p1, p2, Color(0.12, 0.10, 0.23, 0.9), 5.0, true)
		# 頂線鮮豔多巴胺色
		draw_line(p1, p2, col, 2.5, true)

	# 繪製錨點端點圓與標示
	var default_font := ThemeDB.fallback_font
	for aname in anchors.keys():
		var pt: Vector2 = anchors[aname]
		var col: Color = Color(1.0, 0.82, 0.16) # 金黃
		if aname == "brow":
			col = Color(0.2, 0.85, 1.0) # 天藍
		elif aname == "back_key":
			col = Color(1.0, 0.35, 0.55) # 珊瑚粉
		elif aname == "hand":
			col = Color(1.0, 0.6, 0.1) # 暖橘
		elif aname == "tail":
			col = Color(0.75, 0.45, 1.0) # 紫晶尾部錨點

		# 外圈深色陰影
		draw_circle(pt, 7.0, Color(0.12, 0.10, 0.23, 0.9))
		# 內圈實心亮點
		draw_circle(pt, 4.5, col)
		draw_circle(pt, 2.0, Color.WHITE)

		# 繪製錨點文字名稱標籤
		var label_str: String = aname.to_upper()
		draw_string(default_font, pt + Vector2(10, 4), label_str, HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color(0.12, 0.10, 0.23, 1.0))
		draw_string(default_font, pt + Vector2(9, 3), label_str, HORIZONTAL_ALIGNMENT_LEFT, -1, 14, col)


func _get_anchor_pos(node: Node2D) -> Vector2:
	if node == null:
		return Vector2.ZERO
	return get_global_transform().affine_inverse() * node.global_position
