# YWP
YWP is a library to simplify the Python language for beginners while adding some features that are not found in other libraries

## Installation

You can install YWP using pip:

```bash
pip install YWP
```

### Usage

```python
from YWP import play_audio(pro_path, mp3_audio_file)
from YWP import stop_recording()
from YWP import create_file(name) :
    name : the name of the file
    body : show in cmd with input
from YWP import open_file(filepath)
from YWP import open_website(url)
from YWP import shutdown():
    Support to:
        1- Windows
        2- linux
        3- MacOS
from YWP import record_audio(filename='recorder.wav')
from YWP import transcribe_audio(filename='recorder.wav')
from YWP import text_to_speech(text, filename="tts.mp3", language='en')
from YWP import play_sound(filename='tts.mp3')
from YWP import restart():
    Support to:
        Windows only
from YWP import log_off():
    Support to:
        Windows only
from YWP import hibernate():
    Support to:
        Windows only
from YWP import play_audio_online(pro_path, mp3_file_link) :
    pro_path : any program can run online audio like AIMP
from YWP import token_information(data, type='binance') :
    Supported Types Now:
        1- binance
        2- etherum
        3- geckoterminal
    data required:
        1- binance (token)
        2- etherum (token)
        3- geckoterminal (pool)
from YWP import route_flask(location, returnValue)
from YWP import run(check=False, debug=True, host="0.0.0.0", port="8000")
from YWP import AI():
    train(jsonfile="intents.json", picklefile="data.pickle", h5file="model.h5")
    process(message="", picklefile="data.pickle", h5file="model.h5", jsonfile="intents.json", sleeptime=0)
    json_creator(jsonfile="intents.json", tag="", patterns=[], responses=[])
from YWP import basic_video_creator(image_folder="images/", animation_choice="None", frame_rate=25, video_name="output", video_type=".mp4", video_platform="Youtube", image_time=5):
    Available Platforms:
        1- Youtube
        2- Tiktok
        3- Instagram
        4- Facebook
    Available Animations:
        1- FadeIn
        2- FadeOut
        3- Rotate
        4- FlipHorizontal
        5- FlipVertical
        6- None
from YWP import endecrypt:
    aes_encrypt(file_path="", password="")
    aes_decrypt(file_path="", password="")
    blowfish_encrypt(file_path="", password="")
    blowfish_decrypt(file_path="", password="")
    base64_encrypt(file_path="")
    base64_decrypt(file_path="")
    hex_encrypt(file_path="")
    hex_decrypt(file_path="")
from YWP import Libraries:
    init_creator(filesave="__init__.py", filename="", function_class="")
    basic_setup_file_creator(filename="setup.py", folder_name="", readme_name="README.md", library_name="", library_version="", libraries_required=[], description="", creator_name="", creator_email="")
    upload_file_creator(filename="upload_libarary", pypi_api="", platform="windows"):
        Available Platforms:
            1- Windows
            2- Linux
        Available Write Platform:
            1- windows
            2- linux
```

#### LICENSE

MIT License

```javascript
Copyright (c) [2024] ["Ammar Elkhateeb"]
```

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
