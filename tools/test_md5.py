import hashlib

s = "res://assets/sprites/player/paperdoll/lion/costume/costume_steam_artisan.png"
print("MD5:", hashlib.md5(s.encode('utf-8')).hexdigest())

s2 = "res://assets/sprites/player/paperdoll/lion/chassis/paint_midnight_navy.png"
print("MD5:", hashlib.md5(s2.encode('utf-8')).hexdigest())
