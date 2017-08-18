# mp3-concat
simple python script for combining splitted mp3 files

### requirements
* pydub

### installing
* create vitualenv, install requirements

### running

* create directories in the mp3s/ in the following format `artist - track - comment/files[1..99].mp3`
* run the script `python combine.py`
* output will contain the concatenated mp3s `output/artist - track - comment.mp3`