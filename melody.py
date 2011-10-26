import abjad

class Note(object):
    def __init__(self):
        self.raw_pitch = 0.5
    def abjad_note(self):
        return abjad.Note("c'4")

class ChromaticPitchNote(Note):
    def __init__(self, number_of_chromatic_pitches):
        self.raw_pitch = 0.5
        self.pitches = number_of_chromatic_pitches
    def abjad_note(self):
        return abjad.Note( int(round(self.raw_pitch * self.pitches)), abjad.Duration(1,4))

class SimpleLineMelody(object):

    def __init__(self, line):
        # We have a line containing notes. 
        self.score = abjad.Score([])
        staff = abjad.Staff([])

        for note in line:
            staff.append( note.abjad_note() )
        
        self.score.append( staff )
    
    def show(self):
        abjad.show(self.score)

if __name__ == "__main__":
   
    import noise
    
    notes = [ChromaticPitchNote(36) for i in range(0, 60) ]
    noise.line_noise( notes, 'raw_pitch', 0.3 ) 
    melody = SimpleLineMelody(notes)
    melody.show()
