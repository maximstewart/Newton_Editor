# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports


@dataclass
class Config:
    base_of_home: str                = ""
    hide_hidden_files: str           = "true"
    thumbnailer_path: str            = "ffmpegthumbnailer"
    blender_thumbnailer_path: str    = ""
    go_past_home: str                = "true"
    lock_folder: str                 = "false"
    locked_folders: list               = field(default_factory=lambda: [ "venv", "flasks" ])
    mplayer_options: str             = "-quiet -really-quiet -xy 1600 -geometry 50%:50%",
    music_app: str                   = "/opt/deadbeef/bin/deadbeef"
    media_app: str                   = "mpv"
    image_app: str                   = "mirage"
    office_app: str                  = "libreoffice"
    pdf_app: str                     = "evince"
    code_app: str                    = "atom"
    text_app: str                    = "leafpad"
    file_manager_app: str            = "solarfm"
    terminal_app: str                = "terminator"
    remux_folder_max_disk_usage: str = "8589934592"
    make_transparent: int            = 0
    main_window_x: int               = 721
    main_window_y: int               = 465
    main_window_min_width: int       = 720
    main_window_min_height: int      = 480
    main_window_width: int           = 800
    main_window_height: int          = 600
