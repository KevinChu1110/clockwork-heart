extends SceneTree

var _shop = null
var _wait = 0

func _initialize() -> void:
	var ShopClass = load("res://scripts/ui/shop_dialog.gd")
	_shop = ShopClass.new()
	root.add_child(_shop)

func _process(_delta: float) -> bool:
	_wait += 1
	if _wait == 2:
		print("Children of shop:")
		_print_tree(_shop, 0)
		quit(0)
	return false

func _print_tree(node: Node, depth: int) -> void:
	var indent = ""
	for i in range(depth):
		indent += "  "
	var text_info = ""
	if node is Label:
		text_info = " text='%s'" % (node as Label).text
	elif node is Button:
		text_info = " btn_text='%s'" % (node as Button).text
	print("%s- %s (%s)%s" % [indent, node.name, node.get_class(), text_info])
	for child in node.get_children():
		_print_tree(child, depth + 1)
