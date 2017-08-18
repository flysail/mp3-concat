from glob import glob
import os
import sys
from pydub import AudioSegment

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def printc(text, colour=WHITE):
    if has_colours:
            seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m" + "\n"
            sys.stdout.write(seq)
    else:
            sys.stdout.write(text)

def time(segment):
    secs = len(segment)/1000
    mins = int(secs/60)
    sec = secs-mins*60
    if sec < 10:
        sec = '0{}'.format(sec)
    return "{}:{}".format(mins, sec)


def combine():
    input_dirs = sorted(glob("mp3s/*"))
    if not len(input_dirs):
        printc('mp3s/ directory empty create directories with mp3s there', RED)
    for _dir in input_dirs:
        # mp3s/artist - title[ - comment]/xxxx-dd.mp3
        name = _dir.split(os.sep)[1]
        n = name.split(' - ')
        artist = n[0]
        title = n[1]
        album = 'N21'
        comment = ''
        if len(n) > 2:
            comment = n[2]

        id3 = dict(
            album=album,
            artist=artist,
            title=title,
            comment=comment
        )

        printc('mp3s/'+_dir, YELLOW)

        playlist = AudioSegment.silent(duration=500)

        i = 0
        for mp3_file in sorted(glob("{}/*.mp3".format(_dir))):
            song = AudioSegment.from_mp3(mp3_file)
            cut = song
            i += 1
            playlist = playlist.append(cut)
            printc("   {} > {} > {}".format(mp3_file, time(song), time(cut)), BLACK)
        # output/artist - title[ - comment].mp3
        if comment:
            output = "output/{} - {} ({}).mp3".format(artist, title, comment)
        else:
            output = "output/{} - {}.mp3".format(artist, title)

        out_f = open(output, 'wb')
        playlist.export(out_f, format='mp3', tags=id3)

        printc(output, GREEN)

combine()
