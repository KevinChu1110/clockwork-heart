import os
from PIL import Image

REPO_ROOT = '/opt/side/bravesoul-game'

targets = [
    (
        'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_harness.png',
        'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_harness_512.png',
        'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_ironclad_512.png'
    ),
    (
        'game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png',
        'game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic_512.png',
        'game/assets/sprites/player/paperdoll/macaque/costume/costume_zen_striker_512.png'
    ),
    (
        'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_cape.png',
        'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_cape_512.png',
        'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_observer_512.png'
    ),
]

def analyze_image(path):
    im = Image.open(path)
    colors = len(set(im.convert("RGBA").getdata()))
    size = os.path.getsize(path)
    return im, colors, size

def main():
    for src_rel, dst_rel, ref_rel in targets:
        src_p = os.path.join(REPO_ROOT, src_rel)
        dst_p = os.path.join(REPO_ROOT, dst_rel)
        ref_p = os.path.join(REPO_ROOT, ref_rel)

        im_src, c_src, s_src = analyze_image(src_p)
        print(f"\nSRC: {src_rel} ({im_src.size}, {c_src} colors, {s_src} bytes)")

        # Resize with LANCZOS
        im_lanczos = im_src.convert("RGBA").resize((512, 512), resample=Image.Resampling.LANCZOS)
        
        # Save to dst_p
        im_lanczos.save(dst_p, format="PNG", optimize=True)

        im_new, c_new, s_new = analyze_image(dst_p)
        print(f"NEW LANCZOS 512: {dst_rel} ({im_new.size}, {c_new} colors, {s_new} bytes)")

        im_ref, c_ref, s_ref = analyze_image(ref_p)
        print(f"REF 512: {ref_rel} ({im_ref.size}, {c_ref} colors, {s_ref} bytes)")

if __name__ == '__main__':
    main()
