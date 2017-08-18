from glob import glob
import os
import sys
import ntpath
from pydub import AudioSegment

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

IS_EMPTY = 'input directory empty create sub directories with mp3s inside'


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
            seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m" + '\n'
            sys.stdout.write(seq)
    else:
            sys.stdout.write(text)

def duration(segment):
    secs = len(segment)/1000
    mins = int(secs/60)
    sec = secs-mins*60
    if sec < 10:
        sec = '0{}'.format(sec)
    return "{}:{}".format(mins, sec)

def process_dirname_to_id3(_dir):
    # /artist - title[ - comment]/xxxx-dd.mp3
    name = _dir.split(os.sep)[1]
    n = name.split(' - ')
    artist = n[0]
    title = n[1]
    album = 'N21'
    comment = ''
    if len(n) > 2:
        comment = n[2]

    return dict(
        album=album,
        artist=artist,
        title=title,
        comment=comment
    )

def combine(input_dir_name = 'splitted', output_dir_name = 'combined'):
    input_dirs = sorted(glob(input_dir_name + "/*"))
    if not len(input_dirs):
        printc(IS_EMPTY, RED)
    for _dir in input_dirs:
        if not os.path.isdir(_dir):
            printc(IS_EMPTY, RED)
            break
        else:
            id3 = process_dirname_to_id3(_dir)
            printc(_dir+'/*.*', YELLOW)

            playlist = AudioSegment.silent(duration=500)
            i = 0

            # read the mp3 from the subdirectory
            for mp3_file in sorted(glob("{}/*.mp3".format(_dir))):
                song = AudioSegment.from_mp3(mp3_file)
                i += 1
                playlist = playlist.append(song)
                printc("   {} > {}".format(ntpath.basename(mp3_file), duration(song)), BLACK)

            # output/artist - title[ - comment].mp3
            if id3['comment']:
                output = "{}/{} - {} ({}).mp3".format(output_dir_name, id3['artist'], id3['title'], id3['comment'])
            else:
                output = "{}/{} - {}.mp3".format(output_dir_name, id3['artist'], id3['title'])

            # combine / output the current subdir files
            printc(output, GREEN)
            out_f = open(output, 'wb')
            playlist.export(out_f, format='mp3', tags=id3)

            # tell user the status
            printc('OK\n', GREEN)

combine()
