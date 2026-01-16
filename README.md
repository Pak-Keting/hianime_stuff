# hianime_stuff

Just my personal beginner project.  
Any requests to this repository will not be accepted. Please fork it instead if you wanted to make a change.

ffmpeg command to merge all the ts segments:
```bash
ffmpeg -fflags +genpts -i local.m3u8 -c copy -avoid_negative_ts make_zero $FILENAME
```


## Usage

### listEp.py
```bash
python listEp.py <title_id>
```

`title_id`: Accept a link or the title id directly.  
Eg. `https://hianime.to/watch/vinland-saga-2nd-season-18239` as a whole link, or just the title_id `18239`.

It would return the following:
```
EP01    EPISODE_LINK
EP02    EPISODE_LINK
EP03    EPISODE_LINK
...
```

----------------------------------
### downloader.py
```bash
python downloader.py <episode_link> [-q <quality_format>]
```
`episode_link`: Hianime episode link that have the episode id.  
Eg. `https://hianime.to/watch/vinland-saga-2nd-season-18239?ep=97120`, where `?ep=` is presented


`-q`, `--quality`: Takes number 1 to 3. Default is set to 2.
* `-q 1`: Highest (1080p)
* `-q 2`: Medium  (720p)
* `-q 3`: Lowest

As for now, I didn't make it able to accept just the episode id, I'll probably implement it later *(or never)*.

This would download english subtitle, and download the sub version for the show (option to choose dub, or change the subtitle language aren't presented at the moment).  
It would download all the segments, generate localized m3u8, merge all the segments with ffmpeg, and delete all the segments and local m3u8 if all the segments are merged successfully.

At the end, you'll ended up with EPxx.mp4 and EPxx.vtt. Careful though, since the implementation aren't that robust, this project is pretty messy.

----------------------------------
### search.py
```bash
python search.py <search_query>
```
`search_query`: Stuff that you want to search for

**Example:**
```bash
$ python search.py "overlord season 2"
```
It would return the following:
```
Overlord Movie 2: Shikkoku no Eiyuu  https://hianime.to/watch/overlord-the-dark-hero-1086
Overlord: Ple Ple Pleiades           https://hianime.to/watch/overlord-ple-ple-pleiades-3543
Overlord Movie 1: Fushisha no Ou     https://hianime.to/watch/overlord-movie-1-the-undead-king-1190
Overlord                             https://hianime.to/watch/overlord-552
Overlord IV                          https://hianime.to/watch/overlord-iv-18075
```


----------------------------------
### getInfo.py
***...TO BE CONTINUED...***