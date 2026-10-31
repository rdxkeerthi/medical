import cv2
import mediapipe as mp

class FacialTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1)
        self.landmarks = None

    def start_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Error: Could not open the webcam.")

        print("Facial tracker initialized.")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process the frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.landmarks = [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark]

            cv2.imshow("Facial Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_landmarks(self):
        return self.landmarks