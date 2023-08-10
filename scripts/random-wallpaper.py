import glob

import root_path
import random
import os

wallpaper_dir = root_path.get_root_path() + "/wallpapers"
extensions = [".png", ".jpg"]

image_paths: list[str] = []
for extension in extensions:
    # Search for images in wallpaper subdirectories.
    image_paths.extend(glob.glob(f"{wallpaper_dir}/**/*{extension}"))
    # Search for images in wallpaper directory.
    image_paths.extend(glob.glob(f"{wallpaper_dir}/*{extension}"))

image_path = random.choice(
    image_paths,
)

code = os.system(f"feh --bg-fill {image_path}")
exit(code)
