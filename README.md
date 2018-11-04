# Unrecognizable

A quick hack for recognizing faces.

![Logo](/data/unrecognizable.png)

For instruction on face, see [here](https://github.com/iitzco/faced.git)

Dependencies:

* python 3.6
* dlib

Check `requirements.txt` for other dependencies

# How to run recognition on video:

In the root directory, place

* `video.mp4`: Video to run the recognition on
* `image.jpg`: Face or even portrait of the person to be detected

Setup the environment with all depencies and run `python video.py`

# How to run recognition on webcam with you own image:

Place your image in the root directory and edit the image filename inside `webcam.py` and edit your name inside the file as well. You can detect multiple people in one frame as well, just check for the array inside the code and you would know :)

Run `python webcam.py` and boom!
