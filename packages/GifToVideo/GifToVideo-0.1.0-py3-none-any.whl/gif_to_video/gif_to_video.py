#!/usr/bin/env python3

import os
import math
import shutil
import tempfile
import argparse
import python_print_tools.printer
from ffmpeg import FFmpeg
from ffmpeg.errors import FFmpegError, FFmpegFileNotFound, FFmpegUnsupportedCodec
from os.path import abspath, exists, join
from PIL import Image, GifImagePlugin, UnidentifiedImageError
from typing import List

def extract_frames_from_gif(gif_file:str, extract_dir:str) -> List[dict]:
    """
    Extracts all the individual frames from an animated GIF.
    Each frame is saved as a PNG image to a given directory.
    A list of dictionaries is returned containing file paths and duration for each frame.
    
    :param gif_file: Path to an animated GIF
    :type gif_file: str, required
    :param extract_dir: Directory to extract frames into
    :type extract_dir: str, required
    :return: List of frame dictionaries with "image" and "duration" fields
    :rtype: List[dict]
    """
    # Load the animated GIF
    try:
        GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS
        gif = Image.open(gif_file)
    except (FileNotFoundError, UnidentifiedImageError):
        # Return empty list if image is invalid
        return []
    # Run through each frame of the gif
    frame = 0
    frame_data = []
    while True:
        try:
            # Seek the next frame of the image
            gif.seek(frame)
            frame += 1
        except EOFError: break
        # Convert the frame to an RGBA image
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_image = abspath(join(abspath(temp_dir), "image.png"))
            gif.save(temp_image)
            rgba_image = Image.open(temp_image).convert("RGBA")
        # Save the frame as a .png image
        frame_file = abspath(join(abspath(extract_dir), f"{frame}.png"))
        rgba_image.save(frame_file)
        # Add frame data
        try:
            duration = gif.info["duration"]
        except KeyError: duration = 100
        frame_data.append({"image":frame_file, "duration":duration})
    # Return the frame data
    return frame_data

def create_video_frames(gif_frames:List[dict], background:str="#ffffff", scale:int=1) -> dict:
    """
    Resaves the given gif frames while padded if necessary to account for variable frame rate.
    Returns a dictionary containing the video framerate and directory in which the new frames are stored.
    
    :param gif_frames: Gif frame info as returned by extract_frames_from_gif
    :type gif_frames: List[dict], required
    :param background: Background color to use in place of transparency, defaults to "#ffffff"
    :type background: str, optional
    :param scale: Number of times to scale up the image, defaults to 1
    :type scale: int, optional
    :return: Dictionary with "framerate" and "directory" fields
    :rtype: dict
    """
    # Return None if the list of gif frames is invalid
    if gif_frames == []:
        return None
    # Get the standard duration of a single frame
    duration = gif_frames[0]["duration"]
    for i in range(1, len(gif_frames)):
        duration = math.gcd(duration, gif_frames[i]["duration"])
    if duration > 1000:
        duration = math.gcd(duration, 1000)
    raw_framerate = int(1000/duration)
    # Get the closest available framerate
    framerate = raw_framerate
    framerates = [1, 3, 6, 12, 25, 30, 50, 60]
    lowest_difference = 200000
    for f in framerates:
        current_difference = abs(raw_framerate - f)
        if current_difference < lowest_difference:
            framerate = f
            lowest_difference = current_difference
    # Save the video frames
    frame = 1
    frame_directory = abspath(join(gif_frames[0]["image"], os.pardir))
    for gif_frame in gif_frames:
        image = Image.open(gif_frame["image"])
        # Scale image, if necessary
        size = image.size
        if scale > 1:
            size = (size[0] * scale, size[1] * scale)
            image = image.resize(size, resample=Image.Resampling.NEAREST)
        # Add background color
        try:
            full_image = Image.new("RGB", size, background)
        except ValueError:
            full_image = Image.new("RGB", size, "#ffffff")
        full_image.paste(image, (0, 0, size[0], size[1]), image)
        # Save frames
        for i in range(0, int(gif_frame["duration"] / duration)):
            full_image.save(abspath(join(frame_directory, f"VID{frame}.png")))
            frame += 1
    # Return dictionary with framerate and directory info
    return {"directory":frame_directory, "framerate":framerate}

def create_video_from_images(image_directory:str, framerate:int, video_file:str,
            codec:str="h264", quality:int=17, loop:int=0) -> bool:
    """
    Creates a video based on a formatted group of frames saved as individual images.
    Images should be in the format created by create_video_frames.

    :param image_directory: Directory in which frames are stored
    :type image_directory: str, required
    :param framerate: Framerate of the video
    :type framerate: int, required
    :param video_file: Path of the video file to create
    :type video_file: str, required
    :param codec: Codec to use for encoding video, defaults to "h264"
    :type codec: str, optional
    :param quality: Quality to render the video, defaults to 17
    :type int: int, optional
    :param loop: How many times to loop the video, defaults to 0
    :type loop: int, optional
    :return: Whether the video was rendered correctly
    :rtype: bool
    """
    try:
        template = abspath(join(image_directory, "VID"))
        real_loop = loop
        if real_loop < 0:
            real_loop == 0
        ff = (FFmpeg().input(f"{template}%d.png", {"framerate":framerate, "stream_loop":real_loop})
                .output(video_file, {"codec:v":codec, "r":framerate}, crf=quality))
        ff.execute()
        return exists(abspath(video_file))
    except (FFmpegError, FFmpegFileNotFound, FFmpegUnsupportedCodec, TypeError):
        return False

def create_video_from_gif(gif_file:str, video_file:str,
        scale:int=1, background:str="#ffffff", loop:int=0) -> bool:
    """
    Creates a video based on an animated GIF.

    :param gif_file: GIF file to use as the video input
    :type gif_file: str, required
    :param video_file: Path of the video file to create
    :type video_file: str, required
    :param scale: Number of times to scale up the image, defaults to 1
    :type scale: int, optional
    :param background: Background color to use in place of transparency, defaults to "#ffffff"
    :type background: str, optional
    :param loop: How many times to loop the video, defaults to 0
    :type loop: int, optional
    :return: Whether the video was rendered correctly
    :rtype: bool
    """
    with tempfile.TemporaryDirectory() as extract_dir:
        try:
            # Create video frames from the gif file
            gif_frames = extract_frames_from_gif(abspath(gif_file), extract_dir)
            info = create_video_frames(gif_frames, background=background, scale=scale)
        except TypeError:
            return False
        # Encode the video
        codecs = ["h264", "libx264"]
        for codec in codecs:
            try:
                if create_video_from_images(info["directory"], info["framerate"],
                        abspath(video_file), codec=codec, loop=loop):
                    return True
            except TypeError: pass
    return False

def main():
    """
    Sets up the parser for the user to find errors in metadata.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "GIF",
            help="GIF file to convert into video",
            type=str)
    parser.add_argument(
            "OUTPUT",
            help="Video File",
            type=str)
    parser.add_argument(
            "-b",
            "--background",
            nargs="?",
            default="#ffffff",
            type=str,
            help="Background color in place of transparency")
    parser.add_argument(
            "-s",
            "--scale",
            nargs="?",
            default=1,
            type=int,
            help="Number of times to scale the image")
    parser.add_argument(
            "-l",
            "--loop",
            nargs="?",
            default=0,
            type=int,
            help="Number of times to loop the video")
    args = parser.parse_args()
    # Check that paths are valid
    gif_file = abspath(args.GIF)
    video_file = abspath(args.OUTPUT)
    # Create the video
    background = args.background
    if create_video_from_gif(gif_file, video_file,
            scale=args.scale, background=f"#{background}", loop=args.loop):
        python_print_tools.printer.color_print(video_file, "green")
    else:
        python_print_tools.printer.color_print("Video Rendering Failed", "red")
