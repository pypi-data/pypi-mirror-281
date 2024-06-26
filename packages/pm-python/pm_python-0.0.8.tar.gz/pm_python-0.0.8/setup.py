import sys
import os
import logging

from setuptools import setup, Command, Extension

from Cython.Distutils import build_ext


if sys.platform == "win32":
    print("Found Win32 platform")
    setup(
        ext_modules=[
            Extension(
                "pyportmidi._pyportmidi",
                [os.path.join("src", "pyportmidi", "_pyportmidi.pyx")],
                library_dirs=["../Release"],
                libraries=["portmidi", "winmm"],
                include_dirs=["../porttime"],
                extra_compile_args=["/DWIN32"],
            )  # needed by portmidi.h
        ]
    )
elif sys.platform == "darwin":
    print("Found darwin (OS X) platform")
    library_dirs = ["/usr/local/lib"]
    include_dirs = ["/usr/local/include"]
    setup(
        ext_modules=[
            Extension(
                "pyportmidi._pyportmidi",
                [os.path.join("src", "pyportmidi", "_pyportmidi.pyx")],
                library_dirs=library_dirs,
                include_dirs=include_dirs,
                libraries=["portmidi"],
                extra_link_args=[
                    "-framework",
                    "CoreFoundation",
                    "-framework",
                    "CoreMIDI",
                    "-framework",
                    "CoreAudio",
                ],
            )
        ]
    )
else:
    print("Assuming Linux platform")
    setup(
        ext_modules=[
            Extension(
                "pyportmidi._pyportmidi",
                [os.path.join("src", "pyportmidi", "_pyportmidi.pyx")],
                library_dirs=["./linux"],
                libraries=["portmidi", "asound", "pthread"],
            )
        ]
    )
