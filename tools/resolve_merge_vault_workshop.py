#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

base_repo = "/opt/side/bravesoul-game"
base_i18n = f"{base_repo}/game/data/i18n"

locales = {
    "zh_TW": {
        "vault.btn_go_workshop": "前往工坊"
    },
    "zh_CN": {
        "vault.btn_go_workshop": "前往工坊"
    },
    "en": {
        "vault.btn_go_workshop": "To Workshop"
    },
    "ja": {
        "vault.btn_go_workshop": "工房へ"
    },
    "ko": {
        "vault.btn_go_workshop": "공방으로"
    },
    "es": {
        "vault.btn_go_workshop": "Al Taller"
    }
}

def resolve_json_file(file_path, new_kvs):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

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

    cleaned = "\n".join(out_lines)
    data = json.loads(cleaned)
    data.update(new_kvs)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Resolved {file_path}")

for loc, kvs in locales.items():
    resolve_json_file(f"{base_i18n}/{loc}.json", kvs)
    resolve_json_file(f"{base_i18n}/content/{loc}/ui.json", kvs)

print("All 12 i18n files resolved successfully!")
