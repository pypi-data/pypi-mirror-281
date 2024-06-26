#!/usr/bin/env python3

import os
import tempfile
import gif_to_video.gif_to_video as GTV
from os.path import abspath, basename, exists, join
from PIL import Image

TEST_DIRECTORY = abspath(join(abspath(join(abspath(__file__), os.pardir)), "test_files"))

def test_extract_frames_from_gif():
    """
    Tests the extract_frames_from_gif function
    """
    # Test extracting frames from gif with uniform duration
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "UniformDuration.gif"))
        frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        assert len(frames) == 5
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (0, 0, 0, 255)
        assert Image.open(frames[1]["image"]).getpixel((1,1)) == (255, 0, 0, 255)
        assert Image.open(frames[2]["image"]).getpixel((1,1)) == (0, 255, 0, 255)
        assert Image.open(frames[3]["image"]).getpixel((1,1)) == (0, 0, 255, 255)
        assert Image.open(frames[4]["image"]).getpixel((1,1)) == (255, 255, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert basename(frames[1]["image"]) == "2.png"
        assert basename(frames[2]["image"]) == "3.png"
        assert basename(frames[3]["image"]) == "4.png"
        assert basename(frames[4]["image"]) == "5.png"
        assert frames[0]["duration"] == 80
        assert frames[1]["duration"] == 80
        assert frames[2]["duration"] == 80
        assert frames[3]["duration"] == 80
        assert frames[4]["duration"] == 80
    # Test extracting frames from gif with variable durations
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "VariableDuration.gif"))
        frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        assert len(frames) == 3
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (255, 0, 0, 255)
        assert Image.open(frames[1]["image"]).getpixel((1,1)) == (0, 255, 0, 255)
        assert Image.open(frames[2]["image"]).getpixel((1,1)) == (0, 0, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert basename(frames[1]["image"]) == "2.png"
        assert basename(frames[2]["image"]) == "3.png"
        assert frames[0]["duration"] == 80
        assert frames[1]["duration"] == 1000
        assert frames[2]["duration"] == 160
    # Test extracting frames from gif with transparency
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "Transparency.gif"))
        frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        assert len(frames) == 4
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (255, 0, 0, 255)
        assert Image.open(frames[0]["image"]).getpixel((100,100)) == (255, 255, 255, 0)
        assert Image.open(frames[1]["image"]).getpixel((1,1)) == (255, 255, 255, 0)
        assert Image.open(frames[2]["image"]).getpixel((1,1)) == (0, 0, 255, 255)
        assert Image.open(frames[3]["image"]).getpixel((1,1)) == (255, 255, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert basename(frames[1]["image"]) == "2.png"
        assert basename(frames[2]["image"]) == "3.png"
        assert basename(frames[3]["image"]) == "4.png"
        assert frames[0]["duration"] == 30
        assert frames[1]["duration"] == 30
        assert frames[2]["duration"] == 30
        assert frames[3]["duration"] == 30
    # Test extracting frames from an optimized gif
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "Optimized.gif"))
        frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        assert len(frames) == 5
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (0, 0, 0, 255)
        assert Image.open(frames[1]["image"]).getpixel((1,1)) == (0, 0, 0, 255)
        assert Image.open(frames[1]["image"]).getpixel((190,1)) == (255, 0, 0, 255)
        assert Image.open(frames[2]["image"]).getpixel((1,1)) == (0, 255, 0, 255)
        assert Image.open(frames[2]["image"]).getpixel((100,1)) == (0, 0, 0, 255)
        assert Image.open(frames[2]["image"]).getpixel((190,1)) == (255, 0, 0, 255)
        assert Image.open(frames[3]["image"]).getpixel((100,1)) == (0, 0, 255, 255)
        assert Image.open(frames[4]["image"]).getpixel((1,1)) == (255, 255, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert basename(frames[1]["image"]) == "2.png"
        assert basename(frames[2]["image"]) == "3.png"
        assert basename(frames[3]["image"]) == "4.png"
        assert basename(frames[4]["image"]) == "5.png"
        assert frames[0]["duration"] == 100
        assert frames[1]["duration"] == 100
        assert frames[2]["duration"] == 100
        assert frames[3]["duration"] == 100
        assert frames[4]["duration"] == 100
    # Test extracting frames if there is only one frame
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "Static.gif"))
        frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        assert len(frames) == 1
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (0, 0, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert frames[0]["duration"] == 100
    with tempfile.TemporaryDirectory() as extract_dir:
        jpeg_file = abspath(join(TEST_DIRECTORY, "JPEG.jpg"))
        frames = GTV.extract_frames_from_gif(jpeg_file, abspath(extract_dir))
        assert len(frames) == 1
        assert Image.open(frames[0]["image"]).getpixel((1,1)) == (255, 255, 255, 255)
        assert basename(frames[0]["image"]) == "1.png"
        assert frames[0]["duration"] == 100
    # Test extracting frames if the given file is not a gif file
    with tempfile.TemporaryDirectory() as extract_dir:
        text_file = abspath(join(TEST_DIRECTORY, "Text.txt"))
        assert GTV.extract_frames_from_gif(text_file, abspath(extract_dir)) == []

def test_create_video_frames():
    """
    Tests the create_video_frames function.
    """
    # Test creating video frames based on variable duration gif frames
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "VariableDuration.gif"))
        gif_frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        info = GTV.create_video_frames(gif_frames)
        assert info["directory"] == extract_dir
        assert info["framerate"] == 25
        files = sorted(os.listdir(info["directory"]))
        assert len(files) == 34
        assert "VID1.png" in files
        assert "VID31.png" in files
        assert "VID32.png" not in files
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).size == (100, 100)
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).getpixel((1,1)) == (255, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID2.png"))).getpixel((1,1)) == (255, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID3.png"))).getpixel((1,1)) == (0, 255, 0)
        assert Image.open(abspath(join(extract_dir, "VID27.png"))).getpixel((1,1)) == (0, 255, 0)
        assert Image.open(abspath(join(extract_dir, "VID28.png"))).getpixel((1,1)) == (0, 0, 255)
        assert Image.open(abspath(join(extract_dir, "VID31.png"))).getpixel((1,1)) == (0, 0, 255)
    # Test creating video frames based on uniform duration gif frames
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "UniformDuration.gif"))
        gif_frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        info = GTV.create_video_frames(gif_frames)
        assert info["directory"] == extract_dir
        assert info["framerate"] == 12
        files = sorted(os.listdir(info["directory"]))        
        assert len(files) == 10
        assert "VID1.png" in files
        assert "VID2.png" in files
        assert "VID3.png" in files
        assert "VID4.png" in files
        assert "VID5.png" in files
        assert "VID6.png" not in files
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).size == (200, 200)
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).getpixel((1,1)) == (0, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID5.png"))).getpixel((1,1)) == (255, 255, 255)
    # Test with a long duration
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "Long.gif"))
        gif_frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        info = GTV.create_video_frames(gif_frames)
        assert info["directory"] == extract_dir
        assert info["framerate"] == 1
        files = sorted(os.listdir(info["directory"]))
        assert len(files) == 12
        assert "VID1.png" in files
        assert "VID2.png" in files
        assert "VID3.png" in files
        assert "VID8.png" in files
        assert "VID9.png" in files
        assert "VID10.png" in files
        assert "VID11.png" not in files
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).size == (200, 200)
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).getpixel((1,1)) == (0, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID5.png"))).getpixel((1,1)) == (0, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID6.png"))).getpixel((1,1)) == (255, 255, 255)
        assert Image.open(abspath(join(extract_dir, "VID10.png"))).getpixel((1,1)) == (255, 255, 255)
    # Test adding background and scaling image
    with tempfile.TemporaryDirectory() as extract_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "Transparency.gif"))
        gif_frames = GTV.extract_frames_from_gif(gif_file, abspath(extract_dir))
        info = GTV.create_video_frames(gif_frames, scale=3, background="#aa8080")
        assert info["directory"] == extract_dir
        assert info["framerate"] == 30
        files = sorted(os.listdir(info["directory"]))
        assert len(files) == 8
        assert "VID1.png" in files
        assert "VID2.png" in files
        assert "VID3.png" in files
        assert "VID4.png" in files
        assert "VID5.png" not in files
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).size == (600, 600)
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).getpixel((1,1)) == (255, 0, 0)
        assert Image.open(abspath(join(extract_dir, "VID1.png"))).getpixel((150, 150)) == (170, 128, 128)
        assert Image.open(abspath(join(extract_dir, "VID2.png"))).getpixel((1,1)) == (170, 128, 128)
        assert Image.open(abspath(join(extract_dir, "VID2.png"))).getpixel((150, 150)) == (0, 255, 0)
        assert Image.open(abspath(join(extract_dir, "VID3.png"))).getpixel((1,1)) == (0, 0, 255)
        assert Image.open(abspath(join(extract_dir, "VID4.png"))).getpixel((1,1)) == (255, 255, 255)
        # Test creating video frames if there are no source gif frames
        assert GTV.create_video_frames([]) is None

def test_create_video_from_images():
    """
    Tests the create_video_from_images function.
    """
    # Test creating a video
    with tempfile.TemporaryDirectory() as temp_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "UniformDuration.gif"))
        gif_frames = GTV.extract_frames_from_gif(gif_file, temp_dir)
        info = GTV.create_video_frames(gif_frames)
        short_file = abspath(join(temp_dir, "short.mp4"))
        long_file = abspath(join(temp_dir, "long.mp4"))
        assert GTV.create_video_from_images(info["directory"], info["framerate"], short_file)
        assert GTV.create_video_from_images(info["directory"], info["framerate"], long_file, loop=20)
        assert os.stat(short_file).st_size < os.stat(long_file).st_size
        # Test using an invalid codec
        invalid_file = abspath(join(temp_dir, "invalid.mp4"))
        long_file = abspath(join(temp_dir, "long.mp4"))
        assert not GTV.create_video_from_images(info["directory"], info["framerate"], invalid_file, codec="zxzxzx")
        # Test using an invalid directory
        assert not GTV.create_video_from_images("/non/existant", info["framerate"], invalid_file)
        assert not GTV.create_video_from_images(None, info["framerate"], invalid_file)
        # Test using an invalid framerate
        assert not GTV.create_video_from_images(info["directory"], 0, invalid_file)
        assert not GTV.create_video_from_images(info["directory"], -1, invalid_file)
        assert not GTV.create_video_from_images(info["directory"], None, invalid_file)
        # Test using an invalid output file
        assert not GTV.create_video_from_images(info["directory"], info["framerate"], "/non/existant/thing.mp4")
        assert not GTV.create_video_from_images(info["directory"], info["framerate"], None)

def test_create_video_from_gif():
    """
    Tests the create_video_from_gif function.
    """
     # Test creating a video
    with tempfile.TemporaryDirectory() as temp_dir:
        gif_file = abspath(join(TEST_DIRECTORY, "UniformDuration.gif"))
        small_file = abspath(join(temp_dir, "short.mp4"))
        large_file = abspath(join(temp_dir, "long.mp4"))
        assert GTV.create_video_from_gif(gif_file, small_file)
        assert GTV.create_video_from_gif(gif_file, large_file, scale=3)
        assert os.stat(small_file).st_size < os.stat(large_file).st_size
        # Test using invalid GIF file
        invalid_file = abspath(join(temp_dir, "invalid.mp4"))
        assert not GTV.create_video_from_gif("/non/existant/", invalid_file)
        assert not GTV.create_video_from_gif(None, invalid_file)
        # Test using invalid output file
        assert not GTV.create_video_from_gif(gif_file, "/non/existant/aaa.mp4")
        assert not GTV.create_video_from_gif(gif_file, None)
        # Test using invalid loop number
        assert GTV.create_video_from_gif(gif_file, large_file, loop=-1)
        assert not GTV.create_video_from_gif(gif_file, large_file, loop=None)
        # Test using invalid background
        assert GTV.create_video_from_gif(gif_file, invalid_file, background="ljsflkj")
        assert GTV.create_video_from_gif(gif_file, invalid_file, background=None)
