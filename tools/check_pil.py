try:
    import PIL
    from PIL import Image, ImageDraw
    print("PIL is available, version:", PIL.__version__)
except ImportError as e:
    print("PIL not available:", e)
