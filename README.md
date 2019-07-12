# retro-frame
WS2812B based LED-frame to display images, animations, sprites and more.
Code is written in Python and is intended to run on a Raspberry Pi. The defaul display size is 16x16 pixels. Can easily be changed through global variables to support other sizes.

This project is largely inspired by the <https://github.com/stahlfabrik/RibbaPi> project written by @stahlfabrik.

# Supported sources
The following sources are currently supported by the application:
- Images
- Animations
- Sprite Sheets
- Videos

## Images
Support for locally stored images. Images are resized from their original size to selected display size.

## Animations
Gifs are loaded during startup from a local directory. Animations are resized to fit selected display size.
Random animations from Giphy.com is also supported.

## Sprite Sheets
Limited support. Requires a bit more information in order to read properly (number of frames, start position of X and Y etc.)

## Videos
Support for local videos or directly from YouTube (never have the He-Man intro looked so good!). OpenCV is used to load frames and rescale them to fit the selected display size. Frame rate is read from the source to run the playback in proper speed.

# Simulated Hardware
PyGame is used to easily develop the logic and don't rely on the HW for all the testing. This have proven to be very successful and reduces the overall development time. 
