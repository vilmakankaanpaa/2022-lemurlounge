# LemurLounge

This is a python program for a device built to play audio (music, sounds)
for lemurs in a zoo when they interact with it. The device is built with a
Raspberry Pi that is controlling three infrared sensors, a speaker,
a microhone, and a camera. The structure is tunnel-shaped with wooden base and
polycarbonate top as a roof, sized: W 44, H 53, L 60. Audio is turned on when
a lemur enters the structure, triggering the IR sensors.

In overview, the device continuously checks the readings of IR sensors, and
updates the audio accordingly. When a lemur is inside and audio is playing,
the device records the interaction with a camera and a speaker
(to ensure the audio is playing correctly), and logs details into a spreadsheet.

This version of the device is running completely offline because the internet
connection in the zoo was not sufficient. Previous releases use Google Drive and Sheets API.

![](/images/lemurlounge.jpg)
