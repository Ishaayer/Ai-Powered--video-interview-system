from pathlib import Path
from typing import Any

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class VisionService:
    """
    Computer vision service for AI interview monitoring.

    The model is loaded once and reused for all frames.
    """

    def __init__(self):
        model_path = Path("models/face_landmarker.task")

        if not model_path.exists():
            raise FileNotFoundError(
                f"MediaPipe model not found: {model_path}"
            )

        base_options = python.BaseOptions(
            model_asset_path=str(model_path)
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=3,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.landmarker = (
            vision.FaceLandmarker.create_from_options(
                options
            )
        )

    def process_frame(
        self,
        frame: np.ndarray,
    ) -> dict[str, Any]:

        height, width = frame.shape[:2]

        # OpenCV BGR -> RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.landmarker.detect(image)

        face_count = len(result.face_landmarks)

        response = {
            "face_present": face_count > 0,
            "face_count": face_count,
            "faces": [],
            "video_quality": self._video_quality(frame),
        }

        for landmarks in result.face_landmarks:

            bbox = self._get_bbox(
                landmarks,
                width,
                height
            )

            yaw, pitch, roll = (
                self._estimate_head_pose(
                    landmarks,
                    width,
                    height
                )
            )

            gaze = self._estimate_gaze(
                landmarks,
                width,
                height
            )

            looking_away = (
                abs(yaw) > 25
                or abs(pitch) > 20
            )

            face_data = {
                "bbox": bbox,
                "head_pose": {
                    "yaw": round(yaw, 2),
                    "pitch": round(pitch, 2),
                    "roll": round(roll, 2),
                },
                "gaze": gaze,
                "looking_away": looking_away,
            }

            response["faces"].append(
                face_data
            )

        # Convenience values for primary candidate
        if response["faces"]:

            primary = response["faces"][0]

            response["head_pose"] = (
                primary["head_pose"]
            )

            response["gaze"] = primary["gaze"]

            response["looking_away"] = (
                primary["looking_away"]
            )

        else:

            response["head_pose"] = {
                "yaw": 0,
                "pitch": 0,
                "roll": 0,
            }

            response["gaze"] = "unknown"
            response["looking_away"] = False

        response["multiple_faces"] = (
            face_count > 1
        )

        return response

    def _get_bbox(
        self,
        landmarks,
        width: int,
        height: int,
    ):

        xs = [
            max(0, min(1, lm.x)) * width
            for lm in landmarks
        ]

        ys = [
            max(0, min(1, lm.y)) * height
            for lm in landmarks
        ]

        x1 = int(min(xs))
        y1 = int(min(ys))
        x2 = int(max(xs))
        y2 = int(max(ys))

        return {
            "x": x1,
            "y": y1,
            "width": max(0, x2 - x1),
            "height": max(0, y2 - y1),
        }

    def _point(
        self,
        landmarks,
        index,
        width,
        height,
    ):

        if index >= len(landmarks):
            return None

        landmark = landmarks[index]

        return (
            landmark.x * width,
            landmark.y * height
        )

    def _estimate_head_pose(
        self,
        landmarks,
        width,
        height,
    ):

        # MediaPipe facial landmark indices

        nose = self._point(
            landmarks,
            1,
            width,
            height
        )

        chin = self._point(
            landmarks,
            152,
            width,
            height
        )

        left_eye = self._point(
            landmarks,
            33,
            width,
            height
        )

        right_eye = self._point(
            landmarks,
            263,
            width,
            height
        )

        forehead = self._point(
            landmarks,
            10,
            width,
            height
        )

        if any(
            value is None
            for value in [
                nose,
                chin,
                left_eye,
                right_eye,
                forehead,
            ]
        ):
            return 0.0, 0.0, 0.0

        eye_center_x = (
            left_eye[0] +
            right_eye[0]
        ) / 2

        eye_center_y = (
            left_eye[1] +
            right_eye[1]
        ) / 2

        eye_distance = abs(
            right_eye[0] -
            left_eye[0]
        )

        if eye_distance < 1:
            return 0.0, 0.0, 0.0

        # Approximate yaw
        nose_offset_x = (
            nose[0] -
            eye_center_x
        )

        yaw = (
            nose_offset_x /
            eye_distance
        ) * 60

        # Approximate pitch
        face_height = abs(
            chin[1] -
            forehead[1]
        )

        if face_height < 1:
            pitch = 0.0
        else:

            nose_vertical_position = (
                nose[1] -
                forehead[1]
            )

            expected_position = (
                face_height * 0.55
            )

            pitch = (
                (
                    nose_vertical_position -
                    expected_position
                )
                / face_height
            ) * 70

        # Roll
        dx = (
            right_eye[0] -
            left_eye[0]
        )

        dy = (
            right_eye[1] -
            left_eye[1]
        )

        roll = float(
            np.degrees(
                np.arctan2(dy, dx)
            )
        )

        return (
            float(yaw),
            float(pitch),
            float(roll)
        )

    def _estimate_gaze(
        self,
        landmarks,
        width,
        height,
    ):

        left_outer = self._point(
            landmarks, 33, width, height
        )

        left_inner = self._point(
            landmarks, 133, width, height
        )

        right_inner = self._point(
            landmarks, 362, width, height
        )

        right_outer = self._point(
            landmarks, 263, width, height
        )

        left_iris = self._point(
            landmarks, 468, width, height
        )

        right_iris = self._point(
            landmarks, 473, width, height
        )

        if any(
            point is None
            for point in [
                left_outer,
                left_inner,
                right_inner,
                right_outer,
                left_iris,
                right_iris,
            ]
        ):
            return "unknown"

        left_min = min(
            left_outer[0],
            left_inner[0]
        )

        left_max = max(
            left_outer[0],
            left_inner[0]
        )

        right_min = min(
            right_inner[0],
            right_outer[0]
        )

        right_max = max(
            right_inner[0],
            right_outer[0]
        )

        left_ratio = (
            left_iris[0] - left_min
        ) / max(
            1,
            left_max - left_min
        )

        right_ratio = (
            right_iris[0] - right_min
        ) / max(
            1,
            right_max - right_min
        )

        ratio = (
            left_ratio +
            right_ratio
        ) / 2

        if ratio < 0.30:
            return "left"

        if ratio > 0.70:
            return "right"

        return "center"

    def _video_quality(
        self,
        frame: np.ndarray,
    ):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        brightness = float(
            np.mean(gray)
        )

        blur_score = float(
            cv2.Laplacian(
                gray,
                cv2.CV_64F
            ).var()
        )

        if brightness < 35:
            brightness_status = "too_dark"

        elif brightness > 225:
            brightness_status = "too_bright"

        else:
            brightness_status = "good"

        if blur_score < 40:
            blur_status = "blurry"

        else:
            blur_status = "good"

        return {
            "brightness": round(
                brightness,
                2
            ),
            "blur_score": round(
                blur_score,
                2
            ),
            "brightness_status": (
                brightness_status
            ),
            "blur_status": blur_status,
        }

    def close(self):

        self.landmarker.close()