from moviepy import VideoFileClip


videoClip = VideoFileClip("video/Comp1.mp4")
videoClip.write_gif("video/Comp1.gif")