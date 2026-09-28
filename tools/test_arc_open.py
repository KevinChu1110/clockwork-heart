#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import binary_fill_holes, label

# Test adjusting arc to not close loop with axe body
# Let's inspect where the loop closes
# If start is 315 and end is 45, or if start is 305 to 50
