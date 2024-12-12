class Effects:
    def pitch_shift_up(self, file):
        pass

    def time_stretch(self, file):
        pass

    def reverse(self, track):
        pass


"""
Potential routes to take:
    1. Hard code this somehow. Not a very appealing option as it is labor
       intensive. Pitch shift and time stretch can be accomplished using
       Fast Fourier Transform
    2. **Librosa** - a package for music and audio analysis. Has time-stretch
       and pitch-shift functionality. Might be a little hard to play
       nice with Pydub, but I believe this is our best route
    3. pysndfx - we can do different effects using pysndfx, a wrapper for
       a package called SoX. It supports EQ, reverb, phaser, delay
    NOTE: Windows users may need to download ffmpeg for librosa to work
"""
