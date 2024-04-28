import csv
import re
import random
import os
import copy
from mido import Message, MidiFile, MidiTrack

global majmin, chordlist, chordList, keyList
majmin = ["c","c#","d","d#","e","f","f#","g","g#","a","a#","b"]

chordlist = ["i","ii","iii","iv","v","vi","vii"]

chordList = [1, 2, 3, 4, 5, 6,  7]

keyList = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "hb", "h",
           "c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "hb", "h"]

c = [36,48, 60, 72, 84]
db = [37,49, 61, 73, 85]
d = [38,50, 62, 74, 86]
eb = [39,51, 63, 75, 87]
e = [40,52, 64, 76, 88]
f = [41,53, 65, 77, 89]
gb = [42,54, 66, 78, 90]
g = [43,55, 67, 79, 91]
ab = [44,56, 68, 80, 92]
a = [45,57, 69, 81, 93]
hb = [46, 58, 70, 82, 94]
h = [47, 59, 71, 83, 95] 

buildings = [c, db, d, eb, e, f, gb, g, ab, a, hb, h,
             c, db, d, eb, e, f, gb, g, ab, a, hb, h]
             
def prog_builder(followers):
    """
    Takes in the available data for chords and use it to build a 2-4 chord progression based on the given data
    """

    checker = True
    while checker:

        # Create the list of probabilities 
        prob_list = []
        for i in range(len(followers)):
            pl_item = []
            for k in range(len(followers[i])):
                for j in followers[k]:
                    for l in range(int(j[1])):
                        pl_item.append(chordlist.index(j[0])+1)
            prob_list.append(pl_item)
        
        # Select starting chord
        start_ch = random.choice(chordList)
        
        #select number of chords that will be in prog
        ch_sel = random.randint(0,100)
        if ch_sel < 20:
            num_chords = 2
        elif ch_sel > 20 and ch_sel < 55:
            num_chords = 3
        else:
            num_chords = 4
        
        prog = []
        
        for chord in range(num_chords):
            
            # For the first chord, just add to prog
            if chord == 0:
                prog.append(start_ch)
                continue
            
            # For subsequent chords, choose next chord based on probability
            else:
                check = True
                while check:

                # The next chord added is based on the probability of the
                # Upcoming chord. It is selected randomly from the probability
                # list, with prog[chord-1] denoting the number of the chord 
                # and the next -1 denoting that chords index within the 
                # probability list

                    chord_check = random.choice(prob_list[int(prog[chord-1])-1])
                    prog.append(chord_check)
                    if len(prog) == 1:
                        break
                    elif (prog.count(chord_check) / len(prog)) > 0.76:
                        del prog[chord]
                    else:
                        check = False
                        
        # Make sure prog has 4 chords
        if len(prog) == 3:
            choices = ["first", "last"]
            x = random.choice(choices)
            if x == "first":
                prog.insert(0,prog[0])
            else:
                prog.append(prog[2])
        elif len(prog) == 2:
            prog.append(prog[0])
            prog.append(prog[1])
        
        # Make sure 4 chord maker did not create 3 of the same chord
        if prog.count(prog[1]) == 3 or prog.count(prog[0]) == 3:
            continue
        else:
            checker = False

    print("Progression:" ,prog)    
    return prog

def chord_builder(prog):

    # Select random key
    key = random.choice(keyList)

    # Determine which notes will be in the scale
    # Initialze scale starting with key root note
    scale = [key]
    
    # Add the 6 remaining notes to scale
    for i in range(6):
        if i != 2:
            try:
                key = keyList[keyList.index(key) + 2]
                scale.append(key)
            except IndexError:
                if key == "h":
                    key = "db"
                else:
                    key = "c"
                scale.append(key)
        else:
            try:
                key = keyList[keyList.index(key) + 1]
                scale.append(key)
            except IndexError:
                key = "c"
                scale.append(key)

    scale2 = scale * 2    
    #Get root note chords from scale
    roots = []
    [roots.append(scale[ch-1]) for ch in prog]   
    
    # Copy roots so roots2 has raw note data without added notes later
    roots2 = copy.deepcopy(roots)  
    all_ch = []

    # Add chord numbers
    for note in roots:
        this_ch = []
        for nute in keyList:
            if nute == note:
                x = buildings[keyList.index(nute)]
                this_ch.append(x[0])
                ind = scale2.index(nute)
                y = buildings[keyList.index(scale2[ind + 2])]
                this_ch.append(y[0])
                z = buildings[keyList.index(scale2[ind + 4])]
                this_ch.append(z[0]) 
                break
        all_ch.append(this_ch)
                        
    ch_types = ["4","6","7","2"]

    # Add logic for determining if extra notes are added
    for ch in roots:
        if random.randint(1,100) < 30:
            x = random.choice(ch_types)
            ch2 = ch + x
            roots[roots.index(ch)]  = ch2   
       
    # Add the extra notes        
    for num in ch_types:
        w = 0
        for ch in roots2:
            if num in roots[w]:
                frank = scale2[scale2.index(ch) + int(num) - 1]
                v = buildings[keyList.index(frank)]
                all_ch[w].append(v[0])
            w += 1
            
    # Create list of all chords by letter
    letters = []
    for subList in all_ch:
        this_chord=[]
        for num in subList:
            for note in buildings:
                if num in note[0:]:
                    let = keyList[buildings.index(note)]
                    this_chord.append(let)
                    break
        letters.append(this_chord)
    
    return all_ch, scale2

def load_csv(file:str) -> csv.reader:
    csv_file = open(file, "r")
    data = csv.reader(csv_file)
    next(data)
    
    return data
    
def maj_chord_data(data):

    """
    Determines what major chord is most likely to come next for songs from the given artist
    """

    all_maj_prog = []
    
    
    for line in data:
        
        # Extract progression 
        regex = r"\w+|\w+\w+|\w+\w+\w+"
        match = re.findall(regex, line[4])
        all_maj_prog.append(match)
        
    # For each chord, create a list of chords that follow it
    # Index 0 of all_follower_chords is all chords that follow the i chord
    # Index 1 is for ii chord, etc
    all_follower_chords = []
    for chord in chordlist:
        this_chord_followers = []
        for prog in all_maj_prog:
            for item in prog:
                if (chord == item):
                    try:
                        this_chord_followers.append(prog[prog.index(chord)+1])
                    except IndexError:
                        continue
        all_follower_chords.append(this_chord_followers)
        
    ret_list = []
    this_dict = {}
    
    for item in all_follower_chords:
        this_dict = this_dict.clear()
        this_dict = {}
        for chord in chordlist:
            try:
                this_dict[chord] = "{:0.0f}".format(item.count(chord)/len(item) * 100)
            except ZeroDivisionError:
                this_dict[chord] = 0

        this_dict = list(this_dict.items())
        sd = sorted(this_dict, key = lambda scale_dict:this_dict[1], reverse = True)
        ret_list.append(sd)
    return ret_list

def min_chord_data(data):
    """
    Determines what minor chord is most likely to come next for songs from the given artist
    """

    all_min_prog = []
    for line in data:
        
        regex = r"\w+|\w+\w+|\w+\w+\w+"
        match = re.findall(regex, line[5])
        all_min_prog.append(match)
        
    all_follower_chords = []
    for chord in chordlist:
        this_chord_followers = []
        for prog in all_min_prog:
            for item in prog:
                if (chord == item):
                    try:
                        this_chord_followers.append(prog[prog.index(chord)+1])
                    except IndexError:
                        continue
        all_follower_chords.append(this_chord_followers)
        
    ret_lis = []
    this_dict = {}
    
    for item in all_follower_chords:
        this_dic = this_dict.clear()
        this_dic = {}
        for chord in chordlist:
            try:
                this_dic[chord] = "{:0.0f}".format(item.count(chord)/len(item) * 100)
            except ZeroDivisionError:
                this_dic[chord] = 0

        this_dic = list(this_dic.items())
        sd = sorted(this_dic, key = lambda scale_dict:this_dic[1], reverse = True)
        ret_lis.append(sd)
    return ret_lis

def normalize_notes(notes):
    """
    Ensures notes are not too close or too low
    """

    for i in range(len(notes)):
        for j in range(len(notes[i])):
            while notes[i][j]<50:
                notes[i][j]+=12
        notes[i] = sorted(notes[i])

    for i in range(len(notes)):
        for j in range(len(notes[i])):
            try:
                if notes[i][j] - notes[i][j]-1 < 3:
                    notes[i][j]+=12 
            except:
                pass
    return notes

def midi_write(note_locs):

    """
    Writes the midi file based on the base notes of the generated chords.
    """
    
    outfile = MidiFile(type = 2)
    t1 = MidiTrack()
    t2 = MidiTrack()
    t3 = MidiTrack()
    t4 = MidiTrack()
    outfile.tracks.append(t1)
    outfile.tracks.append(t2)
    outfile.tracks.append(t3)
    outfile.tracks.append(t4)

    # Write the midi information
    for i in range(4):
            t1.append(Message('note_on', note=note_locs[i][0], velocity=100, time=0))
            t1.append(Message('note_off', note=note_locs[i][0], velocity=100, time=1540))
            t2.append(Message('note_on', note=note_locs[i][1], velocity=100, time=0))
            t2.append(Message('note_off', note=note_locs[i][1], velocity=100, time=1540))
            t3.append(Message('note_on', note=note_locs[i][2], velocity=100, time=0))
            t3.append(Message('note_off', note=note_locs[i][2], velocity=100, time=1540))
            try:
                t4.append(Message('note_on', note=note_locs[i][3], velocity=100, time=0))
                t4.append(Message('note_off', note=note_locs[i][3], velocity=100, time=1540))
            except:
                t4.append(Message('note_on', note=note_locs[i][0], velocity=0, time=0))
                t4.append(Message('note_off', note=note_locs[i][0], velocity=0, time=1540))
    
    file = "generated_midi.mid"
    outfile.save(file)
    
    return file

def main():

    file = "JuiceWrldData.csv"
    data = load_csv(file)
    data2 = load_csv(file)

    minor = min_chord_data(data)
    maj = maj_chord_data(data2)

    if random.random() > 0.5:
        chords = maj
    else:
        chords = minor

    prog = prog_builder(chords)

    midi_note_locs_unsorted, scale_notes = chord_builder(prog)
    note_locs = normalize_notes(midi_note_locs_unsorted)

    try:
        os.startfile(midi_write(note_locs))
    except:
        print("Error playing back MIDI file...")

if __name__ == "__main__":
    main()
