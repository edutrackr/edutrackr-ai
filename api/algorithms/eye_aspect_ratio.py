import numpy as np


def __mid_line_distance(p1 ,p2, p3, p4):
    """
    Compute the euclidean distance between the midpoints of the two sets of points.
    """
    p5 = np.array([int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)])
    p6 = np.array([int((p3[0] + p4[0])/2), int((p3[1] + p4[1])/2)])
    return np.linalg.norm(p5 - p6)


def original_ear(eye_landmarks: np.ndarray) -> float:
    """
    Compute the eye aspect ratio (EAR) given the eye landmarks (original version).
    """

    if len(eye_landmarks) != 6:
        raise ValueError("The eye landmarks must have 6 points.")

    # Extract the coordinates of each eye landmark
    P1, P2, P3, P4, P5, P6 = eye_landmarks # Each point is an integer tuple (x, y)

    # Calculate the euclidean distance between the vertical points of the eye
    A = np.linalg.norm(P2 - P6)
    B = np.linalg.norm(P3 - P5)
    # Calculate the euclidean distance between the horizontal points of the eye
    C = np.linalg.norm(P1 - P4)

    # Calculate the eye aspect ratio (EAR)
    ear = (A + B) / (2.0 * C)
    return float(ear)


def optimized_ear(eye_landmarks: np.ndarray) -> float:
    """
    Compute the eye aspect ratio (EAR) given the eye landmarks (optimized version).
    """

    if len(eye_landmarks) != 6:
        raise ValueError("The eye landmarks must have 6 points.")

    # Compute the euclidean distances
    B = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
    A = __mid_line_distance(
        eye_landmarks[1],
        eye_landmarks[2],
        eye_landmarks[5],
        eye_landmarks[4]
    )

    # Use the euclidean distance to compute the aspect ratio
    ear = float(A / B)
    return ear
