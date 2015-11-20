
Code for the HU/Adapt version of Shanghai Lectures exercises.

Inspired by EmbedIT kit by Dorit Assaf and Rolf Pfeifer [1] and built on top of "Demo of Arduino control with a Python GUI program" by Robin2 [2].

*Running*
 1. Load ArduinoGUICode onto arduino (using a Nano here)
 2. Optional: Disable Arduino auto-reset on serial connect: stty -F /dev/ttyUSB0 -hupcl or some other method [3]
 3. run python arduinoGUIthread.py -d /dev/ttyUSB0

[1] http://www.iiis.org/CDs2011/CD2011SCI/EISTA_2011/PapersPdf/EA065NR.pdf
[2] http://forum.arduino.cc/index.php?topic=271097.0
[3] http://playground.arduino.cc/Main/DisablingAutoResetOnSerialConnection

