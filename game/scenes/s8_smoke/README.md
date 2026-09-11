# §8 Wave-2 Mac smoke slice

Playable thin slice: **explore → combat → dismantle one part** with Ken **W2-K1 WindStamina** + chest-glow HUD (no blue mana bar).

## Open on Mac (Godot 4.7)

1. Install [Godot 4.7 stable](https://godotengine.org/download) (same minor as `project.godot` features `4.7`).
2. Open project: `game/project.godot` (File → Import / Open).
3. Open scene `scenes/s8_smoke/s8_smoke.tscn` and press **F6** (run current scene).
4. Controls: Space / click = step · **H** = auto-run · Esc = quit.

Headless proof (Linux CI / Frank box):

```bash
godot --path game --headless -s res://scripts/systems/standard_scene_s8/test_s8_smoke.gd
# expect: S8_SMOKE_SUCCESS
```

## Export zip

`export_presets.cfg` preset **macOS** → `../dist/macos/ClockworkHeart.zip`.  
Requires Godot 4.7 macOS export templates. If templates are missing on the build box, use the editor path above.

## Art debt (placeholders only)

- `assets/sprites/s8_smoke/e03_explore.png`
- `assets/sprites/s8_smoke/b02_combat.png` (B02 propeller/key)
- `assets/sprites/s8_smoke/d02_dismantle.png` (D02 key-in-hand)

## Delivered on Frank box

- Headless: `S8_SMOKE_SUCCESS` via `test_s8_smoke.gd`
- Mac zip (after installing 4.7 templates): `dist/macos/ClockworkHeart.zip`
- Note: exported zip launches **main scene** (full game). For the thin §8 slice on Mac, prefer opening `game/project.godot` → run `scenes/s8_smoke/s8_smoke.tscn` (F6).
