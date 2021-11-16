#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <ostream>

using namespace std;
#include "song.h"

//This constructor uses the given string to 
//initialize the pitch, octave, and duration of this note.
Note::Note(const string str){

    for (int i = 0; i < str.length(); i++){
        switch (str[i])
        {
                //Pitch case
                case 'C':
                    if(str[i+1] == '#')
                        pitch = Db;
                    else
                        pitch = C;
                    break;
                case 'D':
                    if(str[i+1] == '#')
                        pitch = Eb;
                    else if (str[i+1] == 'b' )
                        pitch = Db;
                    else
                        pitch = D;
                    break;
                case 'E':
                    if (str[i+1] == 'b' )
                        pitch = Eb;
                    else
                        pitch = E;
                    break;
                case 'F':
                    if(str[i+1] == '#')
                        pitch = Gb;
                    else
                        pitch = F;
                    break;
                case 'G':
                    if(str[i+1] == '#')
                        pitch = Ab;
                    else if (str[i+1] == 'b')
                        pitch = Gb;
                    else
                        pitch = G;
                    break;
                case 'A':
                    if(str[i+1] == '#')
                        pitch = Bb;
                    else if (str[i+1] == 'b')
                        pitch = Ab;
                    else
                        pitch = A;
                    break;
                case 'B':
                    if(str[i+1] == 'b')
                        pitch = Bb;
                    else
                        pitch = B;
                    break;
                case 'R': pitch = REST; break;

                //Octave case
                case '0': octave = 0; break;
                case '1': octave = 1; break;
                case '2': octave = 2; break;
                case '3': octave = 3; break;
                case '4': octave = 4; break;
                case '5': octave = 5; break;
                case '6': octave = 6; break;
                case '7': octave = 7; break;
                
                //Duration case
                case 'q': duration = 1; break;
                case 'h': duration = 2; break;
                case 'w': duration = 4; break;
                case 'e': duration = 0.5; break;
                case 's': duration = 0.25;break;
        }
            //multiplie duration to 1.5 if the note ends with '.'
            if(str[i+1] == '.')
                duration *= 1.5;
    }
}

//This constructor takes in a line of the input file 
//(the first argument) and uses it to initialize a vector of Notes. 
Voice::Voice(const string& str, double vol, instrument_t instr){
    istringstream iss(str);
    string s1;
    while (iss >> s1){
        Note note(s1);
        addNote(note);
    }
    setInstrument(ORGAN);
    setVolume(1000.0);
}

//Constructor opens the file with the given name and reads in 
//the tempo and note information to initialize the song
Song::Song(const string& file){

    ifstream in (file);
    string s, s1, s2;
    int lineN = 1;
    unsigned int temp;

    //read line 1 to tempo variable
    if (lineN == 1){
        getline(in,s1);
        istringstream iss(s1);
        iss >> temp; 
        setTempo(temp);
        lineN++;
    }

    while(getline(in,s)){
        Voice v(s);
        addVoice(v);
    }
    in.close();
}

//prints the given note to out, in the same format as it is stored in the file
ostream& operator<<(ostream& out, const Note& n){
    //Convert the the enum postion to its 
    string p;
    if (n.getPitch() == 0) p = "C";
    else if (n.getPitch() == 1) p = "Dd";
    else if (n.getPitch() == 2) p = "D";
    else if (n.getPitch() == 3) p = "Eb";
    else if (n.getPitch() == 4) p = "E";
    else if (n.getPitch() == 5) p = "F";
    else if (n.getPitch() == 6) p = "Gb";
    else if (n.getPitch() == 7) p = "G";
    else if (n.getPitch() == 8) p = "Ab";
    else if (n.getPitch() == 9) p = "A";
    else if (n.getPitch() == 10) p = "Bb";
    else if (n.getPitch() == 11) p = "B";
    else if (n.getPitch() == 12) p = "R";
    //Convert the duration to its associated letter
    string dur;
    if (n.getDuration() == 1) dur = "q";
    else if (n.getDuration() == 1.5) dur = "q.";
    else if (n.getDuration() == 2) dur = "h";
    else if (n.getDuration() == 3) dur = "h.";
    else if (n.getDuration() == 4) dur = "w";
    else if (n.getDuration() == 6) dur = "w.";
    else if (n.getDuration() == 0.5) dur = "e";
    else if (n.getDuration() == 0.75) dur = "e.";
    else if (n.getDuration() == 0.25) dur = "s";
    else if (n.getDuration() == 0.375) dur = "s.";

    out << p << n.getOctave() << dur;
    return out;
}

//prints all of the Notes in the given Voice to out, separated by spaces.
ostream& operator<<(ostream& out, const Voice& v){
    for(int i = 0; i < v.getNotes().size(); i++){
        out << v.getNotes()[i] << ' ' ;
    }
    return out;
}


//prints to out the tempo on a line, followed by each Voice in the Song, one per line
ostream& operator<<(ostream& out, const Song& s){
    out << s.getTempo() << endl;
    for (int i = 0; i < s.getVoices().size(); i++){
        out << s.getVoices()[i] << endl;
    }
    return out;
}
