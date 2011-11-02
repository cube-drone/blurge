import abjad
import noise

class Note(object):
    def __init__(self, duration = 16):
        self.raw_pitch = 0.5
        self.duration = duration
    
    def set_duration( self, duration = -1 ):
        if duration != -1:
            return self.duration
        else:
            self.duration = duration
            return self 

    def abjad_note(self):
        return abjad.Note("c'" + self.duration)

class ChromaticPitchNote(Note):
    def __init__(self, number_of_chromatic_pitches, duration = 16):
        super( ChromaticPitchNote, self ).__init__(duration)
        self.pitches = number_of_chromatic_pitches

    def abjad_note(self):
        return abjad.Note( int(round(self.raw_pitch * self.pitches)), abjad.Duration(1, self.duration))

class ListOfNotes(noise.NoiseChoice):
    """ A note generated from a list of potential notes. """
    def __init__(self, list_of_notes = ["c"], duration = 16):
        super( ListOfNotes, self ).__init__( list_of_notes )
        self.duration = duration
    def abjad_note(self):
        note_string = self.choice() + str(self.duration) 
        return abjad.Note( note_string )

class CMajorDiatonic(ListOfNotes):
    def __init__(self, duration = 16):
        super( CMajorDiatonic, self ).__init__( ["c", "d", "e", "f", "g", "a", "b"], duration )

class CMajorDiatonicThreeOctaves(ListOfNotes):
    def __init__(self, duration = 16):
        super( CMajorDiatonicThreeOctaves, self ).__init__( \
                        ["c,", "d,", "e,", "f,", "g,", "a,", "b,", \
                        "c", "d", "e", "f", "g", "a", "b", \
                        "c'", "d'", "e'", "f'", "g'", "a'", "b'"],  duration )

class CWholeTone(ListOfNotes):
    def __init__(self, duration = 16):
        super( CWholeTone, self).__init__( ["c", "d", "e", "fs", "gs", "as", "c'"], duration )

class CPentatonic(ListOfNotes):
    def __init__(self, duration = 16):
        super( CPentatonic, self).__init__( ["c", "d", "e", "g", "a", "c'"], duration)
