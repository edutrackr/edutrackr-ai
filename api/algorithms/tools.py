import cv2
from cv2 import VideoCapture


def new_video_size(video: VideoCapture):
    """
    Determine the new optimal width and height of the video based on its aspect ratio.
    """

    # Get the video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Determine the aspect ratio of the frame
    aspect_ratio = width / height

    # Set the new width and height
    if aspect_ratio == 4/3:
        # Medium resolution
        # new_width = 600
        # new_height = 450
        
        # Low resolution
        new_width = 480
        new_height = 360
    elif aspect_ratio == 16/9:
        # Medium resolution
        # new_width = 640
        # new_height = 360

        # Low resolution
        new_width = 480
        new_height = 270
    else:
        # Medium resolution
        # new_width = 600
        # new_height = 450

        # Low resolution
        new_width = 480
        new_height = 360

    return new_width, new_height
