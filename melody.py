import abjad
import random
import copy
from note import *
from rhythm import * 

class SimpleLineMelody(object):

    def __init__(self, line):
        self.line = line 
   
    def append_note(self, note):
        self.line.append( note )

    def append_line(self, line):
        self.line.extend( line )

    def generate(self):
        # We have a line containing notes. 
        self.score = abjad.Score([])
        staff = abjad.Staff([])

        for note in self.line:
            staff.append( note.abjad_note() )
        
        self.score.append( staff )

    def show(self):
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(self.score)
        lilypond_file.score_block.append(abjad.lilypondfiletools.MIDIBlock() )
        layout_block = abjad.lilypondfiletools.LayoutBlock()
        layout_block.is_formatted_when_empty = True
        lilypond_file.score_block.append(layout_block)
        
        abjad.show( lilypond_file) 

class SimpleRhythmMelody(SimpleLineMelody):
    
    def __init__(self, line, rhythm):
        self.line = line
        self.rhythm = rhythm
        self.rhythm_queue = []

    def __beat(self):
        if( self.rhythm_queue == [] ):
            self.rhythm_queue = self.rhythm.duration_map()
        return self.rhythm_queue.pop()

    def generate(self):
        self.score = abjad.Score([])
        staff = abjad.Staff([])
        
        for note in self.line:
            note.set_duration( self.__beat() )
            abj_note = note.abjad_note()
            staff.append( abj_note )
        
        self.score.append( staff )

class Chorus(SimpleLineMelody):
    def __init__ (self, rhythm, noteclass, randomness_factor):
        self.__rhythm = rhythm
        self.__note = noteclass
        self.__randomness = randomness_factor
        self.duration_map = []
        self.notes = []

    def generate_raw_melody(self):
        self.duration_map = self.__rhythm.duration_map()
        self.notes = [copy.deepcopy( self.__note ) for i in range( 0, len(self.duration_map) )]
        noise.line_noise( self.notes, 'noise', self.__randomness )  

    def add( self, chorus ):
        self.duration_map.extend( chorus.duration_map )
        self.notes.extend( chorus.notes ) 

    def generate_score(self):
        # We have a line containing notes. 
        self.score = abjad.Score([])
        staff = abjad.Staff([])

        for i in range( 0, len(self.duration_map )):
            duration = self.duration_map[i]
            note = self.notes[i]
            note.duration = duration
            staff.append( note.abjad_note() )
        
        self.score.append( staff )

class ComplexChorus(object):
    def __init__(self, chorus, number_of_chorals, length, randomness_factor):
        self.chorals = [ copy.deepcopy( chorus ) for i in range( 0, number_of_chorals ) ]
        self.__length = length
        self.__randomness = randomness_factor
        self.chorus = chorus 

    def generate_raw_melody(self):
        for chorus in self.chorals:
            chorus.generate_raw_melody()
        self.chunks = [ noise.NoiseChoice(self.chorals, 0.5) for i in range( 0, self.__length ) ] 
        noise.line_noise( self.chunks, 'noise', self.__randomness )

        for chunk in self.chunks:
            chorus = chunk.choice()
            self.chorus.add( chunk.choice() )

    def generate_score(self):
        self.chorus.generate_score()

    def show(self):
        self.chorus.show()

def __test_simple_line_melody():
    notes = [CWholeTone() for i in range(0, 20) ]
    noise.line_noise( notes, 'raw_pitch', 0.5 ) 
    melody = SimpleLineMelody(notes)
    melody.generate()
    melody.show()

def __test_simple_rhythm_melody():
    # Refactor so that a note and a duration are unified before processing. 
    notes = [CMajorDiatonic() for i in range(0, 12) ]
    noise.line_noise( notes, 'raw_pitch', 0.5 ) 
    
    melody = SimpleRhythmMelody(notes, RandomSplitRhythm( 0.95, 0.8 ))

    melody.generate()
    melody.show()

def __test_chorus():
    chorus = Chorus( RandomSplitRhythm( 0.95, 0.8), CPentatonic(), 0.3 ) 
    chorus.generate_raw_melody()
    chorus.generate_score()
    chorus.show()

def __test_complex_chorus():
    rhythm = RandomSplitRhythm (0.95, 0.8)
    chorus = Chorus( rhythm, CPentatonic(), 0.5 ) 
    complex_chorus = ComplexChorus( chorus, 8, 12, 0.6)
    complex_chorus.generate_raw_melody()
    complex_chorus.generate_score()
    complex_chorus.show()

if __name__ == "__main__":
    import noise
    
    #__test_simple_line_melody() 
    #__test_simple_rhythm_melody()
    __test_complex_chorus()
