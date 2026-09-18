import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = '/opt/side/bravesoul-game'

cases = [
    {
        'title': 'Boar: viking_harness vs viking_ironclad',
        'src_128': 'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_harness.png',
        'new_512': 'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_harness_512.png',
        'ref_512': 'game/assets/sprites/player/paperdoll/boar/costume/costume_viking_ironclad_512.png',
    },
    {
        'title': 'Macaque: dawn_monk_tunic vs zen_striker',
        'src_128': 'game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png',
        'new_512': 'game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic_512.png',
        'ref_512': 'game/assets/sprites/player/paperdoll/macaque/costume/costume_zen_striker_512.png',
    },
    {
        'title': 'Fox: astral_cape vs astral_observer',
        'src_128': 'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_cape.png',
        'new_512': 'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_cape_512.png',
        'ref_512': 'game/assets/sprites/player/paperdoll/fox/costume/costume_astral_observer_512.png',
    }
]

def make_checkerboard(width, height, tile_size=16):
    bg = Image.new("RGBA", (width, height), (240, 240, 245, 255))
    draw = ImageDraw.Draw(bg)
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if ((x // tile_size) + (y // tile_size)) % 2 == 1:
                draw.rectangle([x, y, x + tile_size, y + tile_size], fill=(225, 225, 230, 255))
    return bg

def main():
    cell_w, cell_h = 300, 300
    gap = 20
    header_h = 60
    total_w = gap * 4 + cell_w * 3
    total_h = header_h + (cell_h + gap + 40) * len(cases) + gap

    sheet = Image.new("RGBA", (total_w, total_h), (30, 32, 40, 255))
    draw = ImageDraw.Draw(sheet)

    # Column titles
    draw.text((gap + 50, 20), "128px (Original, Lanczos scaled)", fill=(200, 200, 210, 255))
    draw.text((gap * 2 + cell_w + 50, 20), "512px NEW (Lanczos Output)", fill=(100, 220, 120, 255))
    draw.text((gap * 3 + cell_w * 2 + 50, 20), "512px Approved Reference", fill=(100, 180, 255, 255))

    for row_idx, c in enumerate(cases):
        row_y = header_h + row_idx * (cell_h + gap + 40)

        # Title
        draw.text((gap, row_y - 25), f"[{row_idx+1}] {c['title']}", fill=(255, 215, 0, 255))

        imgs = [
            (os.path.join(REPO_ROOT, c['src_128']), "Original 128"),
            (os.path.join(REPO_ROOT, c['new_512']), "New 512 (Lanczos)"),
            (os.path.join(REPO_ROOT, c['ref_512']), "Reference 512")
        ]

        for col_idx, (img_path, label) in enumerate(imgs):
            col_x = gap + col_idx * (cell_w + gap)
            bg = make_checkerboard(cell_w, cell_h)
            
            im = Image.open(img_path).convert("RGBA")
            im_resized = im.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            bg.paste(im_resized, (0, 0), im_resized)
            sheet.paste(bg, (col_x, row_y))

            # Border
            draw.rectangle([col_x, row_y, col_x + cell_w, row_y + cell_h], outline=(80, 85, 100, 255), width=2)

            # File info
            size_kb = os.path.getsize(img_path) / 1024.0
            colors = len(set(im.getdata()))
            info = f"{label}: {im.size[0]}x{im.size[1]} | {colors} colors | {size_kb:.1f} KB"
            print(f"Cell ({row_idx}, {col_idx}): {info}")
            draw.text((col_x, row_y + cell_h + 5), info, fill=(180, 190, 200, 255))

    out_p = os.path.join(REPO_ROOT, "proofs/comparison_512_review.png")
    sheet.save(out_p)
    print(f"Generated comparison sheet: {out_p}")

if __name__ == '__main__':
    main()
