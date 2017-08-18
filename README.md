# mp3-concat
simple python script for combining splitted mp3 files

### requirements
* pydub

### installing
* create vitualenv, install requirements

### running

* create directories in the splitted/ in the following format `artist - track - comment/files[1..99].mp3`
* run the script `python combine.py`
* `combined` will contain the concatenated mp3s like `artist - track - comment.mp3`