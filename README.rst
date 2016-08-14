=================================================
FFCut: Cutting Video with FFMpeg for Human Beings
=================================================

FFMpeg is a great tool, but cutting several parts of a video with it can
become a complex task. This small script serves to help with it.

Install it from PyPI::

    pip install --user ffcut

.. note:: ``--user`` flag makes ``pip`` install it to ``~/.local/bin``.

Then use like::

    ~/.local/bin/ffcut -i file1.mp4 -s ..0:10 -s 0:30..+20 -s 1:30..2:30 -s 3:00.. -i file2.mp4 -s 5:00.. -o final.mp4

Here you first specify input files with ``-i``, then slices to take from each
file with ``-s`` using format ``[begin]..[end]`` (both parts being optional).

You can also merge two or more files in one::

    ~/.local/bin/ffcut -i file1.mp4 -i file2.mp4 -o result.mp4

Use ``--copy`` flag to avoid re-encoding (may cause problems with playback).

Use built-in help for more details::

    ~/.local/bin/ffcut -h
