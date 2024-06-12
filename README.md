# FFmpeg GUI Wrapper

This project provides a simple graphical user interface (GUI) wrapper for FFmpeg, designed to make basic video editing tasks accessible for users with minimal technical experience. The application allows users to increase the audio volume of a video file, cut the video from a specified start time, and perform test runs that process only the first 60 seconds of the video.

![image](https://github.com/alexeygrigorev/ffmpeg-gui/assets/875246/ed08b8e9-84d2-4f02-9e14-924f5209ec11)


## Prerequisites

- Python 3.11
- Pipenv
- FFmpeg


## Installation

To set up the project environment:

Run `pipenv install` to set up the virtual environment and install dependencies.


Make sure that `ffmpeg.exe` is available in the project directory.

```bash
wget https://github.com/alexeygrigorev/ffmpeg-gui/releases/download/ffmpeg/ffmpeg.exe
```

## Using the Application

To start the application:

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run `pipenv shell` to activate the virtual environment.
4. Execute `python ffmpeg_gui.py` to launch the GUI.

The GUI allows you to select a video file, set the volume increase in dB, specify the cut start time in seconds, and optionally select a "Test Run" mode that processes only the first 60 seconds of the video.

## Building the Executable

The project includes a Makefile for building the application into a standalone executable using PyInstaller. The steps are as follows:

1. Ensure you are in the virtual environment (`pipenv shell`).
2. Run `make build` to build it (check `build.sh` for detail).

This will generate an executable in the `dist` directory which can be run on any Windows system without the need to install Python or other dependencies.

## Notes

- The executable requires `ffmpeg.exe` to be in the same directory or in the system's PATH.
- Ensure that all paths and filenames do not contain spaces or special characters as they may affect the execution of FFmpeg commands.
