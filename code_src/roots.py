import pathlib

ROOT = pathlib.Path(__file__).parent.parent  # Project root

SRC_ROOT = ROOT / "src"  # Where assets (images, ...) are

CACHE_ROOT = ROOT / "cache"  # Where cached files (as skins) are
if not CACHE_ROOT.exists():
    CACHE_ROOT.mkdir()

USER_ROOT = ROOT / "user"  # Where userdata (username, keymap, ...) is

SAVE_ROOT = ROOT / "saves"  # Where saves are
if not SAVE_ROOT.exists():
    SAVE_ROOT.mkdir()

TMP_ROOT = ROOT / "temp"  # Where temporary files are
if not TMP_ROOT.exists():
    TMP_ROOT.mkdir()
