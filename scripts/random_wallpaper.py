import glob

import argparse
import root_path
import random
import os
import time
import signal
import sys
import dataclasses

# Registry SIGINT handler to gracefully handle shutdown.
signal.signal(signal.SIGINT, lambda _, __: exit(0))

parser = argparse.ArgumentParser(
    description="Random wallpaper picker",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-i",
    "--interval",
    help="Interval in seconds that wallpaper should switch.",
    default=0,
    type=int,
)


@dataclasses.dataclass
class Args:
    interval: int


args = Args(**vars(parser.parse_args()))


WALLPAPER_DIR = root_path.get_root_path() + "/wallpapers"
EXTENSIONS = [".png", ".jpg"]


def get_random_wallpaper() -> str:
    image_paths: list[str] = []
    for extension in EXTENSIONS:
        # Search for images in wallpaper subdirectories.
        image_paths.extend(glob.glob(f"{WALLPAPER_DIR}/**/*{extension}"))
        # Search for images in wallpaper directory.
        image_paths.extend(glob.glob(f"{WALLPAPER_DIR}/*{extension}"))
    return random.choice(image_paths)


def format_cmd(image_path: str) -> str:
    return f"feh --bg-fill {image_path}"


prev_image_path = None
while True:
    curr_image_path = get_random_wallpaper()
    # Ensure image is different than previous one.
    while curr_image_path == prev_image_path:
        curr_image_path = get_random_wallpaper()
    prev_image_path = curr_image_path
    cmd = format_cmd(curr_image_path)
    code = os.system(cmd)
    # Exit if command failed or process is not long running.
    if code != 0:
        print(f"set wallpaper '{cmd}' failed with code: {code}", file=sys.stderr)
        exit(code)
    if args.interval == 0:
        exit(code)

    time.sleep(args.interval)
