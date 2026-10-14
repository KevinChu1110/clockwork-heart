#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve JSON conflicts in i18n and docs/PROJECTS.json during git merge."""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

lock_file = os.path.join(REPO, ".git", "index.lock")
if os.path.exists(lock_file):
    try:
        os.remove(lock_file)
        print("Removed stale index.lock")
    except Exception as e:
        print(f"Could not remove lock: {e}")

def get_git_content(path, stage):
    # stage: 1=base, 2=ours (HEAD), 3=theirs (MERGE_HEAD)
    res = subprocess.run(["git", "-C", REPO, "show", f":{stage}:{path}"], capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except Exception as e:
            print(f"Error parsing stage {stage} for {path}: {e}")
            return None
    return None

def resolve_i18n_files():
    locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
    paths = []
    for loc in locales:
        paths.append(f"game/data/i18n/{loc}.json")
        paths.append(f"game/data/i18n/content/{loc}/ui.json")

    resolved = []
    for p in paths:
        full_p = os.path.join(REPO, p)
        ours = get_git_content(p, 2)
        theirs = get_git_content(p, 3)
        if ours is not None and theirs is not None:
            merged = dict(ours)
            merged.update(theirs)
            with open(full_p, "w", encoding="utf-8") as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)
                f.write("\n")
            resolved.append(p)
            print(f"Resolved i18n: {p}")
        elif os.path.exists(full_p):
            content = open(full_p, "r", encoding="utf-8").read()
            if "<<<<<<<" in content:
                print(f"Warning: {p} still has conflict markers and stage content was missing")
    return resolved

def resolve_projects_json():
    p = "docs/PROJECTS.json"
    full_p = os.path.join(REPO, p)
    ours = get_git_content(p, 2)
    theirs = get_git_content(p, 3)
    if ours is not None and theirs is not None:
        merged = dict(ours)
        items_by_id = {}
        for it in ours.get("items", []):
            items_by_id[it["id"]] = it
        for it in theirs.get("items", []):
            if it["id"] not in items_by_id:
                items_by_id[it["id"]] = it
            else:
                status_order = {"草稿": 0, "開發中": 1, "測試中": 2, "已上線": 3}
                our_st = items_by_id[it["id"]].get("status", "草稿")
                their_st = it.get("status", "草稿")
                if status_order.get(their_st, 0) >= status_order.get(our_st, 0):
                    items_by_id[it["id"]].update(it)

        new_items = []
        seen = set()
        for it in ours.get("items", []):
            new_items.append(items_by_id[it["id"]])
            seen.add(it["id"])
        for it in theirs.get("items", []):
            if it["id"] not in seen:
                new_items.append(items_by_id[it["id"]])
                seen.add(it["id"])

        merged["items"] = new_items
        with open(full_p, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"Resolved {p}")
        return [p]
    return []

if __name__ == "__main__":
    to_add = []
    to_add.extend(resolve_i18n_files())
    to_add.extend(resolve_projects_json())
    if to_add:
        subprocess.run(["git", "-C", REPO, "add"] + to_add, check=True)
        print("Git add completed for all resolved files.")
