#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

base_repo = "/opt/side/bravesoul-game"

locales = {
    "zh_TW": {
        "skill.btn_go_vault": "前往儲能庫"
    },
    "zh_CN": {
        "skill.btn_go_vault": "前往储能库"
    },
    "en": {
        "skill.btn_go_vault": "To Vault"
    },
    "ja": {
        "skill.btn_go_vault": "貯蔵庫へ"
    },
    "ko": {
        "skill.btn_go_vault": "저장고로 이동"
    },
    "es": {
        "skill.btn_go_vault": "Ir a Bóveda"
    }
}

base_i18n = f"{base_repo}/game/data/i18n"

def resolve_json(path, new_kvs):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
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

# Resolve docs/PROJECTS.json
proj_path = f"{base_repo}/docs/PROJECTS.json"
with open(proj_path, "r", encoding="utf-8") as f:
    pcontent = f.read()

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

print("All merge conflicts for skill-vault branch resolved successfully!")
