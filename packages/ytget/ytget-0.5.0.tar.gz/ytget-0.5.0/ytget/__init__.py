"""
-----------------|-----------|-----------------
-----------------|---YTGet---|-----------------
-----------------|-----------|-----------------

( Easily get data and download youtube videos )
(    Focused on speed and simplicity.         )

"""
__title__ = "ytget"
__description__ = "Easily get data and download youtube videos. Focused on speed and simplicity."
__url__ = "https://github.com/Coskon/ytget"
__author__ = "Cosk"
__license__ = "MIT"
__version__ = "0.5.0"
__all__ = ["Video", "Search", "Playlist", "Fetch", "Download", "GenericExtractor", "console", "exceptions", "out_colors", "utils"]

from ytget.__main__ import Video, Search, Playlist, Fetch, Download, GenericExtractor

from . import console
from . import exceptions
from . import out_colors
from . import utils
