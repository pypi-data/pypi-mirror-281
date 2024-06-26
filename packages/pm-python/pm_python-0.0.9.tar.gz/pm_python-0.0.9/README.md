# pm-python - Python wrappings for PortMidi

Originally created by John Harrison, harrison@media.mit.edu

Modified by Roger B. Dannenberg, Nov 2009, 2021, with contributions by anonymous

I, Aaron Krister Johnson <akjmicro@gmail.com>, am volunteering to maintain
and modernize this code.

My fork of the repo, the basis of this package, lives at https://github.com/akjmicro/pm_python

pm-python
---------

pm-python is a Python wrapper for PortMidi. PortMidi is a cross-platform
C library for realtime MIDI control. Using pm-python, you can send and
receive MIDI data in realtime from Python.

Besides using pm-python to communicate to synthesizers and the
like, it is possible to use pm-python as a way to send MIDI messages
between software packages on the same computer. For example, Using
pm-python and MIDI-YOKE on a Windows machine, it is possible to send
realtime MIDI messages between programs on the same computer using
loopback virtual MIDI ports.

pm-python works with Python 3.x and may also work with Python 2.6

Example usage
-------------

>>> from pyportmidi import *
>>> pm_init()
>>> pm_show_all_devices()
DEVNUM: 0 | ALSA Midi Through Port-0 - OUTPUT 
DEVNUM: 1 | ALSA Midi Through Port-0 - INPUT 
DEVNUM: 2 | ALSA VirMIDI 1-0 - OUTPUT 
DEVNUM: 3 | ALSA VirMIDI 1-0 - INPUT 
DEVNUM: 4 | ALSA VirMIDI 1-1 - OUTPUT 
DEVNUM: 5 | ALSA VirMIDI 1-1 - INPUT 
DEVNUM: 6 | ALSA VirMIDI 1-2 - OUTPUT 
DEVNUM: 7 | ALSA VirMIDI 1-2 - INPUT 
DEVNUM: 8 | ALSA VirMIDI 1-3 - OUTPUT 
DEVNUM: 9 | ALSA VirMIDI 1-3 - INPUT 
>>> out = PmOutput(2)
>>> out.note_on(60, 100)
>>> out.note_off(60)
>>> pm_quit()

There remain certain possible bugs relating to closing the actual
PmInput/PmOutput objects with `.close()`. As I know the solution,
I'll push a fix.

For questions/concerns, contact me at akjmicro@gmail.com

