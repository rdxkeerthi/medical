import mediapipe as mp
import cv2

class MediaPipeTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        return results

    def get_landmark(self, results, landmark_index):
        if results.multi_face_landmarks:
            return results.multi_face_landmarks[0].landmark[landmark_index]
        return None

    def draw_landmarks(self, frame, landmarks):
        mp_drawing = mp.solutions.drawing_utils
        if landmarks.multi_face_landmarks:
            for face_landmarks in landmarks.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp.solutions.face_mesh.FACEMESH_CONTOURS
                )
        return frame