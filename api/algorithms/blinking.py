import dlib
import cv2
import numpy as np
from numpy.linalg import norm
from api.common.utils.video import get_video_metadata
from config import AIConfig
from decimal import Decimal

# Initialize dlib's face detector and face landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(AIConfig.Blinking.SHAPE_PREDICTOR_PATH)

def __mid_line_distance(p1 ,p2, p3, p4):
    """Compute the euclidean distance between the midpoints of the two sets of points"""
    p5 = np.array([int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)])
    p6 = np.array([int((p3[0] + p4[0])/2), int((p3[1] + p4[1])/2)])

    return norm(p5 - p6)

def __eye_aspect_ratio(landmarks, eye_range):
    """
    Compute the eye aspect ratio (EAR) given the eye landmarks.
    """

    # Get the eye coordinates
    eye = np.array(
        [np.array([landmarks.part(i).x, landmarks.part(i).y]) for i in eye_range]
    )
    # compute the euclidean distances
    B = norm(eye[0] - eye[3])
    A = __mid_line_distance(eye[1], eye[2], eye[5], eye[4])
    # Use the euclidean distance to compute the aspect ratio
    ear = A / B
    return ear

def analyze_blinks(
    video_path: str,
    blink_threshold=0.2,
    discarded_frames="auto" # Number of frames to discard in a second
):
    # Iniatialize the video capture object
    video = cv2.VideoCapture(video_path)

    # Get the video properties
    video_metadata = get_video_metadata(video_path)

    # Validate the number of frames to discard
    # TODO: Add to constants
    if discarded_frames == "auto":
        discarded_frames_rate = 0.1 # Sample rate should not be higher than 10% of FPS to avoid loosing analysis quality
        discarded_frames = int(video_metadata.avg_fps * discarded_frames_rate)
        #print(discarded_frames)

    eye_closed = False
    blinks = 0
    sample_count = 0
    while video.isOpened():

        # Read each frame from the video
        is_processing, frame = video.read()

        if not is_processing:
            break

        # Validate frames sampling interval
        if sample_count < discarded_frames:
            sample_count += 1
            continue
        else:
            sample_count = 0

        # Resize the frame and convert it to grayscale
        frame = cv2.resize(frame, (video_metadata.optimal_width, video_metadata.optimal_height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = detector(gray, 0)

        # Loop over the face detections
        for rect in rects:
            landmarks = predictor(gray, rect)

            # Use the coordinates of each eye to compute the eye aspect ratio.
            left_aspect_ratio = __eye_aspect_ratio(landmarks, range(42, 48))
            right_aspect_ratio = __eye_aspect_ratio(landmarks, range(36, 42))
            ear = (left_aspect_ratio + right_aspect_ratio) / 2.0 # Eye Aspect Ratio

            # If the eye aspect ratio is below the blink threshold, set the eye_closed flag to True.
            if ear < blink_threshold:
                eye_closed = True

            # If the eye aspect ratio is above the blink threshold and 
            # the eye_closed flag is True, increment the number of blinks.
            elif ear >= blink_threshold and eye_closed:
                blinks += 1
                eye_closed = False

    video.release()

    blink_rate = blinks / video_metadata.duration # In blinks per second
    formated_blink_rate=Decimal(f"{blink_rate:.3f}")
    formated_duration=Decimal(f"{video_metadata.duration:.2f}")
    return blinks, formated_duration, formated_blink_rate
