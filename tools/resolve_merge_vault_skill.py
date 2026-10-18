#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

base_repo = "/opt/side/bravesoul-game"

# 1. Resolve clockwork_vault_dialog.gd
vault_path = f"{base_repo}/game/scripts/ui/clockwork_vault_dialog.gd"
with open(vault_path, "r", encoding="utf-8") as f:
    text = f.read()

c1_old = """<<<<<<< HEAD
signal wardrobe_requested()
signal go_wardrobe()
=======
signal skill_requested()
signal go_skill()
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c1_new = """signal wardrobe_requested()
signal go_wardrobe()
signal skill_requested()
signal go_skill()"""
text = text.replace(c1_old, c1_new)

if 'const COLOR_CORAL' not in text:
    text = text.replace('const COLOR_SKY        := Color("#38A0FF")  ## 天藍\n', 'const COLOR_SKY        := Color("#38A0FF")  ## 天藍\nconst COLOR_CORAL      := Color("#FF5E8A")  ## 珊瑚粉\n')

c2_old = """<<<<<<< HEAD
var _btn_go_wardrobe: Button
=======
var _btn_go_skill: Button
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c2_new = """var _btn_go_wardrobe: Button
var _btn_go_skill: Button"""
text = text.replace(c2_old, c2_new)

c3_old = """<<<<<<< HEAD
\t## 2. 彈窗主體卡片 (寬 920, 高 460, 置中)
\t_dialog_card = PanelContainer.new()
\t_dialog_card.name = "VaultCard"
\t_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
\t_dialog_card.custom_minimum_size = Vector2(920, 460)
\t_dialog_card.offset_left = -460
\t_dialog_card.offset_right = 460
=======
\t## 2. 彈窗主體卡片 (寬 890, 高 460, 置中)
\t_dialog_card = PanelContainer.new()
\t_dialog_card.name = "VaultCard"
\t_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
\t_dialog_card.custom_minimum_size = Vector2(890, 460)
\t_dialog_card.offset_left = -445
\t_dialog_card.offset_right = 445
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c3_new = """\t## 2. 彈窗主體卡片 (寬 1000, 高 460, 置中)
\t_dialog_card = PanelContainer.new()
\t_dialog_card.name = "VaultCard"
\t_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
\t_dialog_card.custom_minimum_size = Vector2(1000, 460)
\t_dialog_card.offset_left = -500
\t_dialog_card.offset_right = 500"""
text = text.replace(c3_old, c3_new)

c4_old = """<<<<<<< HEAD
\t## 底部操作按鈕：普通領取、雙倍領取、前往委託、前往鍛造、前往背包、前往戰力、前往商城與前往衣櫥 (高 52px, 熱區 >= 48px, 立體果凍厚底)
=======
\t## 底部操作按鈕：普通領取、雙倍領取、前往委託、前往鍛造、前往背包、前往戰力、前往商城與前往心法 (高 52px, 熱區 >= 48px, 立體果凍厚底)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c4_new = """\t## 底部操作按鈕：普通領取、雙倍領取、前往委託、前往鍛造、前往背包、前往戰力、前往商城、前往衣櫥與前往心法 (高 52px, 熱區 >= 48px, 立體果凍厚底)"""
text = text.replace(c4_old, c4_new)

c5_old = """<<<<<<< HEAD
\t_btn_claim.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_claim.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c5_new = """\t_btn_claim.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c5_old, c5_new)

c6_old = """<<<<<<< HEAD
\t_btn_double_claim.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_double_claim.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c6_new = """\t_btn_double_claim.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c6_old, c6_new)

c7_old = """<<<<<<< HEAD
\t_btn_go_windup.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_go_windup.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c7_new = """\t_btn_go_windup.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c7_old, c7_new)

c8_old = """<<<<<<< HEAD
\t_btn_go_forge.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_go_forge.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c8_new = """\t_btn_go_forge.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c8_old, c8_new)

c9_old = """<<<<<<< HEAD
\t_btn_go_inventory.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_go_inventory.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c9_new = """\t_btn_go_inventory.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c9_old, c9_new)

c10_old = """<<<<<<< HEAD
\t_btn_go_power_stat.custom_minimum_size = Vector2(105, 52)
=======
\t_btn_go_power_stat.custom_minimum_size = Vector2(102, 52)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c10_new = """\t_btn_go_power_stat.custom_minimum_size = Vector2(102, 52)"""
text = text.replace(c10_old, c10_new)

c11_old = """<<<<<<< HEAD
\t## 前往衣櫥快捷按鈕 (BtnGoWardrobe，高 52px、熱區 >= 48px、暖橘 #FFA010 底色、深藍紫描邊 #1F1A3A、厚底 5px、圓角 18px、字級 16px、零系統 Emoji)
\t_btn_go_wardrobe = Button.new()
\t_btn_go_wardrobe.name = "BtnGoWardrobe"
\t_btn_go_wardrobe.custom_minimum_size = Vector2(105, 52)
\t_btn_go_wardrobe.focus_mode = Control.FOCUS_NONE

\tvar wardrobe_sb := StyleBoxFlat.new()
\twardrobe_sb.bg_color = COLOR_ORANGE
\twardrobe_sb.border_color = COLOR_BORDER
\twardrobe_sb.set_border_width_all(2)
\twardrobe_sb.border_width_bottom = 5
\twardrobe_sb.set_corner_radius_all(18)
\tvar wardrobe_sb_h := wardrobe_sb.duplicate() as StyleBoxFlat
\twardrobe_sb_h.bg_color = Color("#FFB030")
\tvar wardrobe_sb_p := wardrobe_sb.duplicate() as StyleBoxFlat
\twardrobe_sb_p.border_width_bottom = 2
\t_btn_go_wardrobe.add_theme_stylebox_override("normal", wardrobe_sb)
\t_btn_go_wardrobe.add_theme_stylebox_override("hover", wardrobe_sb_h)
\t_btn_go_wardrobe.add_theme_stylebox_override("pressed", wardrobe_sb_p)
\t_btn_go_wardrobe.add_theme_color_override("font_color", COLOR_TEXT_DARK)
\t_btn_go_wardrobe.add_theme_font_size_override("font_size", 16)
\tif _cached_font:
\t\t_btn_go_wardrobe.add_theme_font_override("font", _cached_font)
\t_btn_go_wardrobe.pressed.connect(_on_go_wardrobe_pressed)
\tfoot_box.add_child(_btn_go_wardrobe)
=======
\t## 前往心法快捷按鈕 (BtnGoSkill，高 52px、熱區 >= 48px、珊瑚粉 #FF5E8A 底色、深藍紫描邊 #1F1A3A、厚底 5px、圓角 18px、字級 16px、零系統 Emoji)
\t_btn_go_skill = Button.new()
\t_btn_go_skill.name = "BtnGoSkill"
\t_btn_go_skill.custom_minimum_size = Vector2(102, 52)
\t_btn_go_skill.focus_mode = Control.FOCUS_NONE

\tvar skill_sb := StyleBoxFlat.new()
\tskill_sb.bg_color = COLOR_CORAL
\tskill_sb.border_color = COLOR_BORDER
\tskill_sb.set_border_width_all(2)
\tskill_sb.border_width_bottom = 5
\tskill_sb.set_corner_radius_all(18)
\tvar skill_sb_h := skill_sb.duplicate() as StyleBoxFlat
\tskill_sb_h.bg_color = Color("#FF7A9F")
\tvar skill_sb_p := skill_sb.duplicate() as StyleBoxFlat
\tskill_sb_p.border_width_bottom = 2
\t_btn_go_skill.add_theme_stylebox_override("normal", skill_sb)
\t_btn_go_skill.add_theme_stylebox_override("hover", skill_sb_h)
\t_btn_go_skill.add_theme_stylebox_override("pressed", skill_sb_p)
\t_btn_go_skill.add_theme_color_override("font_color", COLOR_TEXT_DARK)
\t_btn_go_skill.add_theme_font_size_override("font_size", 16)
\tif _cached_font:
\t\t_btn_go_skill.add_theme_font_override("font", _cached_font)
\t_btn_go_skill.pressed.connect(_on_go_skill_pressed)
\tfoot_box.add_child(_btn_go_skill)
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c11_new = """\t## 前往衣櫥快捷按鈕 (BtnGoWardrobe，高 52px、熱區 >= 48px、暖橘 #FFA010 底色、深藍紫描邊 #1F1A3A、厚底 5px、圓角 18px、字級 16px、零系統 Emoji)
\t_btn_go_wardrobe = Button.new()
\t_btn_go_wardrobe.name = "BtnGoWardrobe"
\t_btn_go_wardrobe.custom_minimum_size = Vector2(102, 52)
\t_btn_go_wardrobe.focus_mode = Control.FOCUS_NONE

\tvar wardrobe_sb := StyleBoxFlat.new()
\twardrobe_sb.bg_color = COLOR_ORANGE
\twardrobe_sb.border_color = COLOR_BORDER
\twardrobe_sb.set_border_width_all(2)
\twardrobe_sb.border_width_bottom = 5
\twardrobe_sb.set_corner_radius_all(18)
\tvar wardrobe_sb_h := wardrobe_sb.duplicate() as StyleBoxFlat
\twardrobe_sb_h.bg_color = Color("#FFB030")
\tvar wardrobe_sb_p := wardrobe_sb.duplicate() as StyleBoxFlat
\twardrobe_sb_p.border_width_bottom = 2
\t_btn_go_wardrobe.add_theme_stylebox_override("normal", wardrobe_sb)
\t_btn_go_wardrobe.add_theme_stylebox_override("hover", wardrobe_sb_h)
\t_btn_go_wardrobe.add_theme_stylebox_override("pressed", wardrobe_sb_p)
\t_btn_go_wardrobe.add_theme_color_override("font_color", COLOR_TEXT_DARK)
\t_btn_go_wardrobe.add_theme_font_size_override("font_size", 16)
\tif _cached_font:
\t\t_btn_go_wardrobe.add_theme_font_override("font", _cached_font)
\t_btn_go_wardrobe.pressed.connect(_on_go_wardrobe_pressed)
\tfoot_box.add_child(_btn_go_wardrobe)

\t## 前往心法快捷按鈕 (BtnGoSkill，高 52px、熱區 >= 48px、珊瑚粉 #FF5E8A 底色、深藍紫描邊 #1F1A3A、厚底 5px、圓角 18px、字級 16px、零系統 Emoji)
\t_btn_go_skill = Button.new()
\t_btn_go_skill.name = "BtnGoSkill"
\t_btn_go_skill.custom_minimum_size = Vector2(102, 52)
\t_btn_go_skill.focus_mode = Control.FOCUS_NONE

\tvar skill_sb := StyleBoxFlat.new()
\tskill_sb.bg_color = COLOR_CORAL
\tskill_sb.border_color = COLOR_BORDER
\tskill_sb.set_border_width_all(2)
\tskill_sb.border_width_bottom = 5
\tskill_sb.set_corner_radius_all(18)
\tvar skill_sb_h := skill_sb.duplicate() as StyleBoxFlat
\tskill_sb_h.bg_color = Color("#FF7A9F")
\tvar skill_sb_p := skill_sb.duplicate() as StyleBoxFlat
\tskill_sb_p.border_width_bottom = 2
\t_btn_go_skill.add_theme_stylebox_override("normal", skill_sb)
\t_btn_go_skill.add_theme_stylebox_override("hover", skill_sb_h)
\t_btn_go_skill.add_theme_stylebox_override("pressed", skill_sb_p)
\t_btn_go_skill.add_theme_color_override("font_color", COLOR_TEXT_DARK)
\t_btn_go_skill.add_theme_font_size_override("font_size", 16)
\tif _cached_font:
\t\t_btn_go_skill.add_theme_font_override("font", _cached_font)
\t_btn_go_skill.pressed.connect(_on_go_skill_pressed)
\tfoot_box.add_child(_btn_go_skill)"""
text = text.replace(c11_old, c11_new)

c12_old = """<<<<<<< HEAD
\tif _btn_go_wardrobe:
\t\t_btn_go_wardrobe.text = _get_go_wardrobe_text()


func _get_go_wardrobe_text() -> String:
\tvar t := Loc.t("vault.btn_go_wardrobe")
\tif t == "vault.btn_go_wardrobe" or t.is_empty():
\t\tt = Loc.t("vault.go_wardrobe")
\tif t == "vault.go_wardrobe" or t.is_empty():
\t\tt = "前往衣櫥"
\treturn t
=======
\tif _btn_go_skill:
\t\t_btn_go_skill.text = Loc.t("vault.btn_go_skill")
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c12_new = """\tif _btn_go_wardrobe:
\t\t_btn_go_wardrobe.text = _get_go_wardrobe_text()
\tif _btn_go_skill:
\t\t_btn_go_skill.text = Loc.t("vault.btn_go_skill")


func _get_go_wardrobe_text() -> String:
\tvar t := Loc.t("vault.btn_go_wardrobe")
\tif t == "vault.btn_go_wardrobe" or t.is_empty():
\t\tt = Loc.t("vault.go_wardrobe")
\tif t == "vault.go_wardrobe" or t.is_empty():
\t\tt = "前往衣櫥"
\treturn t"""
text = text.replace(c12_old, c12_new)

c13_old = """<<<<<<< HEAD
\t## 更新前往衣櫥按鈕狀態
\tif _btn_go_wardrobe:
\t\t_btn_go_wardrobe.text = _get_go_wardrobe_text()
\t\t_btn_go_wardrobe.disabled = false
=======
\t## 更新前往心法按鈕狀態
\tif _btn_go_skill:
\t\t_btn_go_skill.text = Loc.t("vault.btn_go_skill")
\t\t_btn_go_skill.disabled = false
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c13_new = """\t## 更新前往衣櫥按鈕狀態
\tif _btn_go_wardrobe:
\t\t_btn_go_wardrobe.text = _get_go_wardrobe_text()
\t\t_btn_go_wardrobe.disabled = false

\t## 更新前往心法按鈕狀態
\tif _btn_go_skill:
\t\t_btn_go_skill.text = Loc.t("vault.btn_go_skill")
\t\t_btn_go_skill.disabled = false"""
text = text.replace(c13_old, c13_new)

c14_old = """<<<<<<< HEAD
func _on_go_wardrobe_pressed() -> void:
\tvar am: Node = null
\tif Engine.get_main_loop() is SceneTree:
\t\tam = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
\tif am and am.has_method("play_ui"):
\t\tam.call("play_ui")
\twardrobe_requested.emit()
\tgo_wardrobe.emit()
\tvar p := get_parent()
\tif p != null and p.has_method("open_wardrobe"):
\t\tp.call("open_wardrobe")
\telif p != null and p.has_method("open_wardrobe_dialog"):
\t\tp.call("open_wardrobe_dialog")
=======
func _on_go_skill_pressed() -> void:
\tskill_requested.emit()
\tgo_skill.emit()
\tvar p := get_parent()
\tif p != null and p.has_method("open_skill_dialog"):
\t\tp.call("open_skill_dialog")
\telif p != null and p.has_method("open_skill"):
\t\tp.call("open_skill")
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f
\telse:
\t\tvar loop := Engine.get_main_loop()
\t\tif loop is SceneTree and (loop as SceneTree).root != null:
\t\t\tvar ml: Node = (loop as SceneTree).root.get_node_or_null("MobileLobby")
<<<<<<< HEAD
\t\t\tif ml and ml.has_method("open_wardrobe"):
\t\t\t\tml.call("open_wardrobe")
\t\t\telif ml and ml.has_method("open_wardrobe_dialog"):
\t\t\t\tml.call("open_wardrobe_dialog")
=======
\t\t\tif ml and ml.has_method("open_skill_dialog"):
\t\t\t\tml.call("open_skill_dialog")
\t\t\telif ml and ml.has_method("open_skill"):
\t\t\t\tml.call("open_skill")
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f
\tclosed.emit()
\tqueue_free()"""
c14_new = """func _on_go_wardrobe_pressed() -> void:
\tvar am: Node = null
\tif Engine.get_main_loop() is SceneTree:
\t\tam = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
\tif am and am.has_method("play_ui"):
\t\tam.call("play_ui")
\twardrobe_requested.emit()
\tgo_wardrobe.emit()
\tvar p := get_parent()
\tif p != null and p.has_method("open_wardrobe"):
\t\tp.call("open_wardrobe")
\telif p != null and p.has_method("open_wardrobe_dialog"):
\t\tp.call("open_wardrobe_dialog")
\telse:
\t\tvar loop := Engine.get_main_loop()
\t\tif loop is SceneTree and (loop as SceneTree).root != null:
\t\t\tvar ml: Node = (loop as SceneTree).root.get_node_or_null("MobileLobby")
\t\t\tif ml and ml.has_method("open_wardrobe"):
\t\t\t\tml.call("open_wardrobe")
\t\t\telif ml and ml.has_method("open_wardrobe_dialog"):
\t\t\t\tml.call("open_wardrobe_dialog")
\tclosed.emit()
\tqueue_free()


func _on_go_skill_pressed() -> void:
\tskill_requested.emit()
\tgo_skill.emit()
\tvar p := get_parent()
\tif p != null and p.has_method("open_skill_dialog"):
\t\tp.call("open_skill_dialog")
\telif p != null and p.has_method("open_skill"):
\t\tp.call("open_skill")
\telse:
\t\tvar loop := Engine.get_main_loop()
\t\tif loop is SceneTree and (loop as SceneTree).root != null:
\t\t\tvar ml: Node = (loop as SceneTree).root.get_node_or_null("MobileLobby")
\t\t\tif ml and ml.has_method("open_skill_dialog"):
\t\t\t\tml.call("open_skill_dialog")
\t\t\telif ml and ml.has_method("open_skill"):
\t\t\t\tml.call("open_skill")
\tclosed.emit()
\tqueue_free()"""
text = text.replace(c14_old, c14_new)

c15_old = """<<<<<<< HEAD
func get_go_wardrobe_button() -> Button:
\treturn _btn_go_wardrobe


func get_wardrobe_button() -> Button:
\treturn _btn_go_wardrobe
=======
func get_go_skill_button() -> Button:
\treturn _btn_go_skill


func get_skill_button() -> Button:
\treturn _btn_go_skill
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
c15_new = """func get_go_wardrobe_button() -> Button:
\treturn _btn_go_wardrobe


func get_wardrobe_button() -> Button:
\treturn _btn_go_wardrobe


func get_go_skill_button() -> Button:
\treturn _btn_go_skill


func get_skill_button() -> Button:
\treturn _btn_go_skill"""
text = text.replace(c15_old, c15_new)

with open(vault_path, "w", encoding="utf-8") as f:
    f.write(text)

# 2. Resolve mobile_lobby.gd
lobby_path = f"{base_repo}/game/scripts/ui/mobile_lobby.gd"
with open(lobby_path, "r", encoding="utf-8") as f:
    ltext = f.read()

l1_old = """<<<<<<< HEAD
\tif dlg.has_signal("wardrobe_requested"):
\t\tdlg.wardrobe_requested.connect(func():
\t\t\topen_wardrobe()
\t\t)
\tif dlg.has_signal("go_wardrobe"):
\t\tdlg.go_wardrobe.connect(func():
\t\t\topen_wardrobe()
=======
\tif dlg.has_signal("skill_requested"):
\t\tdlg.skill_requested.connect(func():
\t\t\topen_skill_dialog()
\t\t)
\tif dlg.has_signal("go_skill"):
\t\tdlg.go_skill.connect(func():
\t\t\topen_skill_dialog()
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
l1_new = """\tif dlg.has_signal("wardrobe_requested"):
\t\tdlg.wardrobe_requested.connect(func():
\t\t\topen_wardrobe()
\t\t)
\tif dlg.has_signal("go_wardrobe"):
\t\tdlg.go_wardrobe.connect(func():
\t\t\topen_wardrobe()
\t\t)
\tif dlg.has_signal("skill_requested"):
\t\tdlg.skill_requested.connect(func():
\t\t\topen_skill_dialog()
\t\t)
\tif dlg.has_signal("go_skill"):
\t\tdlg.go_skill.connect(func():
\t\t\topen_skill_dialog()"""
ltext = ltext.replace(l1_old, l1_new)

l2_old = """<<<<<<< HEAD
\t\tvar has_wardrobe: bool = get_node_or_null("WardrobeDialog") != null
\t\tif _equip_schematic and is_instance_valid(_equip_schematic) and not has_forge and not has_inv and not has_power and not has_windup and not has_shop and not has_wardrobe:
=======
\t\tvar has_skill: bool = get_node_or_null("SkillDialog") != null
\t\tif _equip_schematic and is_instance_valid(_equip_schematic) and not has_forge and not has_inv and not has_power and not has_windup and not has_shop and not has_skill:
>>>>>>> origin/agent/20261018-vault-skill-shortcut-t_64581b7f"""
l2_new = """\t\tvar has_wardrobe: bool = get_node_or_null("WardrobeDialog") != null
\t\tvar has_skill: bool = get_node_or_null("SkillDialog") != null
\t\tif _equip_schematic and is_instance_valid(_equip_schematic) and not has_forge and not has_inv and not has_power and not has_windup and not has_shop and not has_wardrobe and not has_skill:"""
ltext = ltext.replace(l2_old, l2_new)

with open(lobby_path, "w", encoding="utf-8") as f:
    f.write(ltext)

# 3. Resolve 12 i18n JSON files
locales = {
    "zh_TW": {
        "vault.btn_go_skill": "前往心法"
    },
    "zh_CN": {
        "vault.btn_go_skill": "前往心法"
    },
    "en": {
        "vault.btn_go_skill": "To Skills"
    },
    "ja": {
        "vault.btn_go_skill": "心法へ"
    },
    "ko": {
        "vault.btn_go_skill": "심법으로"
    },
    "es": {
        "vault.btn_go_skill": "A Habilidades"
    }
}

base_i18n = f"{base_repo}/game/data/i18n"

def resolve_json(path, new_kvs):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # If conflict markers in content, extract HEAD part
    if "<<<<<<< HEAD" in content:
        lines = content.splitlines()
        out_lines = []
        in_conflict = False
        in_head = False
        for line in lines:
            if line.startswith("<<<<<<< HEAD"):
                in_conflict = True
                in_head = True
                continue
            elif line.startswith("======="):
                in_head = False
                continue
            elif line.startswith(">>>>>>>"):
                in_conflict = False
                continue
            if not in_conflict:
                out_lines.append(line)
            elif in_head:
                out_lines.append(line)
        cleaned_json = "\n".join(out_lines)
        d = json.loads(cleaned_json)
    else:
        d = json.loads(content)
    d.update(new_kvs)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")

for loc, kvs in locales.items():
    resolve_json(f"{base_i18n}/{loc}.json", kvs)
    resolve_json(f"{base_i18n}/content/{loc}/ui.json", kvs)

# 4. Resolve docs/PROJECTS.json
proj_path = f"{base_repo}/docs/PROJECTS.json"
with open(proj_path, "r", encoding="utf-8") as f:
    pcontent = f.read()

# Extract HEAD part of PROJECTS.json
if "<<<<<<< HEAD" in pcontent:
    lines = pcontent.splitlines()
    out_lines = []
    in_conflict = False
    in_head = False
    for line in lines:
        if line.startswith("<<<<<<< HEAD"):
            in_conflict = True
            in_head = True
            continue
        elif line.startswith("======="):
            in_head = False
            continue
        elif line.startswith(">>>>>>>"):
            in_conflict = False
            continue
        if not in_conflict:
            out_lines.append(line)
        elif in_head:
            out_lines.append(line)
    p_data = json.loads("\n".join(out_lines))
else:
    p_data = json.loads(pcontent)

with open(proj_path, "w", encoding="utf-8") as f:
    json.dump(p_data, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("All merge conflicts for vault-skill branch resolved successfully!")
