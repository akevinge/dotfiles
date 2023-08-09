import argparse
import dataclasses
import os
import pathlib
import root
import shutil
import tempfile

home_path = pathlib.Path.home()

parser = argparse.ArgumentParser(
    description="Creates symlinks between dotfiles and targets",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-c",
    "--config",
    default=f"{home_path}/.config",
    help="Specify .config folder for symlinks from dotfiles/config",
)
parser.add_argument(
    "-b",
    "--bin",
    default=f"{home_path}/.local/bin",
    help="Specify .bin folder for symlinks from dotfiles/bin",
)
parser.add_argument(
    "-w",
    "--wallpapers",
    default=f"{home_path}/pictures/wallpapers",
    help="Specify wallpapers folder for symlinks from dotfiles/wallpapers",
)


args = vars(parser.parse_args())


@dataclasses.dataclass
class SymlinkTargetPaths:
    config: str
    bin: str
    wallpapers: str


@dataclasses.dataclass()
class SymlinkSourcePaths:
    root: str = root.get_root_path()
    config: str = root + "/config"
    config_entries: list[str] = dataclasses.field(init=False)
    bin: str = root + "/bin"
    bin_entries: list[str] = dataclasses.field(init=False)
    wallpapers: str = root + "/wallpapers"

    def __post_init__(self):
        self.config_entries = [
            pathlib.PurePath(f.path).name for f in os.scandir(self.config)
        ]
        self.bin_entries = [
            pathlib.PurePath(f.path).name for f in os.scandir(self.config)
        ]


@dataclasses.dataclass
class SafeSymlink:
    src: str
    dst: str
    tmp_dir: str = dataclasses.field(init=False)
    are_files: bool = dataclasses.field(init=False)

    def __post_init__(self):
        if not (self._would_be_dir(self.src) == self._would_be_dir(self.dst)):
            raise ValueError(
                f"{self.src} and {self.dst } must either be both directories or files."
            )

        self.tmp_dir = tempfile.mkdtemp(f"_dotfiles")
        self.are_files = os.path.isfile(self.src)
        self.dst_exists = os.path.exists(self.dst)

    def _would_be_dir(self, path: str) -> bool:
        _, extension = os.path.splitext(path)
        return extension == ""

    def mksymlink(self):
        self._backup_dst_to_tmp()
        try:
            os.symlink(
                self.src,
                self.dst,
                target_is_directory=(not self.are_files),
            )
        except Exception as error:
            print(f"Failed to create symlink: {error}")
            self._restore_tmp_to_dist()

    def _backup_dst_to_tmp(self):
        if self.dst_exists:
            print(f"Attempting to move {self.dst} to {self.tmp_dir}.")
            shutil.move(self.dst, self.tmp_dir)

    def _restore_tmp_to_dist(self):
        if self.dst_exists:
            print(f"Attempting to restore {self.dst}.")
            shutil.move(self.tmp_dir, self.dst)


target_paths = SymlinkTargetPaths(**args)
source_paths = SymlinkSourcePaths()


for entry in source_paths.config_entries:
    src = f"{source_paths.config}/{entry}"
    dst = f"{target_paths.config}/{entry}"
    SafeSymlink(src, dst).mksymlink()
