# ezdl
just another yt-dlp wrapper for even more simplicity with rich styling and loading animations.

![](https://i.imgur.com/yLlcVOA.png)

#### Dependencies
[Python](https://www.python.org/downloads/)
## Installation
You can install ezdl using pip:

```pwsh
pip install nrdrch-ezdl
```
## usage examples:
- Download a Youtube video (this will Ignore the rest of the playlist by default)
```pwsh
ezdl video https://youtu.be/dQw4w9WgXcQ
```
- just the audio
```
ezdl audio https://youtu.be/dQw4w9WgXcQ
```
- Download the whole playlist if the link leads to a playlist
```
ezdl video https://youtu.be/dQw4w9WgXcQ?list=PLE0hg-LdSfycrpTtMImPSqFLle4yYNzWD wp
```
- just the audio but the whole playlist
```
ezdl audio https://youtu.be/dQw4w9WgXcQ?list=PLE0hg-LdSfycrpTtMImPSqFLle4yYNzWD wp
```
- open locations by their name (settings, audio or video)
```
ezdl open settings
```
