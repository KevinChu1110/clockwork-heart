#!/usr/bin/env python3
import hashlib

p = "res://assets/sprites/player/poses/walrus/attack.png"
print("MD5 of res_path:", hashlib.md5(p.encode("utf-8")).hexdigest())

p_toucan = "res://assets/sprites/player/poses/toucan/attack.png"
print("MD5 of toucan res_path:", hashlib.md5(p_toucan.encode("utf-8")).hexdigest())
