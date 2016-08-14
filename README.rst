=================================================
FFCut: Cutting Video with FFMpeg for Human Beings
=================================================

FFMpeg is a great tool, but cutting several parts of a video with it can
become a complex task. This small script serves to help with it.

Install it from PyPI::

    pip install --user ffcut

.. note:: ``--user`` flag makes ``pip`` install it to ``~/.local/bin``.

Then use like::

    ~/.local/bin/ffcut -i file1.mp4 -t ..0:10 -t 0:30..+20 -t 1:30..2:30 -t 3:00.. -i file2.mp4 -t 5:00.. -o final.mp4

Use built-in help for more details::

    ~/.local/bin/ffcut -h

Use ``--copy`` flag to avoid reencoding (may cause problems with playback).
