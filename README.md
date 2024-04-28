To use:

1). Clone the repo

2). Install requirements with "pip install -r requirements.txt" 

    Alternatively, just do "pip install mido" since this is the only non built in dependency
    
3). Run the program to generate a new MIDI file!

===== NOTE =====

The program was built within a Windows environment, and the opening and playing of the MIDI file at the end is done using Window's default
media player (Windows Media Player) with its default sound (a low quality piano). Occaisionally, the notes are not rendered
properly and it sounds like a chord is only playing one note, when there are actually 3+ notes that should be playing. Visualization of a MIDI
file is provided on the last page of the report, and also here: 

![alt text](https://i.imgur.com/Kiwhbyd.png)


I am not sure how the program will behave on a Mac. Line 372 in the program: "os.startfile(midi_write(note_locs))" is what is responsible for the playback,
and I am not sure if Mac has a default playback program like Windows. 
