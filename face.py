import cv2
import face_recognition
import pickle
import os

# File to store registered faces
FACE_DATA_FILE = "registered_faces.pkl"

# Function to capture a face encoding
def capture_face_encoding():
    """Capture a face encoding from the webcam."""
    video_capture = cv2.VideoCapture(0)
    print("Position your face in front of the camera...")

    face_encoding = None
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]  # Convert from BGR to RGB for face_recognition

        # Detect face and encode
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]
            print("Face captured.")
            break

        # Display the resulting image
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return face_encoding

# Function to save face data
def save_face_data(face_data):
    """Save face data to a file."""
    with open(FACE_DATA_FILE, "wb") as f:
        pickle.dump(face_data, f)
    print("Face data saved.")

# Function to load face data
def load_face_data():
    """Load face data from a file."""
    if os.path.exists(FACE_DATA_FILE):
        with open(FACE_DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# Function to register a new face
def register_face(name):
    """Register a new face with a name."""
    print(f"Registering face for {name}...")
    face_encoding = capture_face_encoding()
    if face_encoding is None:
        print("Failed to capture face.")
        return

    # Load existing face data
    face_data = load_face_data()
    face_data[name] = face_encoding
    save_face_data(face_data)
    print(f"Face registered for {name}.")

# Function to authenticate a face
def authenticate_face():
    """Authenticate a face by matching with stored face data."""
    print("Authenticating face. Please look at the camera...")
    face_encoding_to_check = capture_face_encoding()
    if face_encoding_to_check is None:
        print("Failed to capture face.")
        return

    # Load registered faces
    face_data = load_face_data()
    if not face_data:
        print("No registered faces found.")
        return

    # Check if the captured face matches any registered face
    for name, face_encoding in face_data.items():
        match = face_recognition.compare_faces([face_encoding], face_encoding_to_check, tolerance=0.6)
        if match[0]:
            print(f"Authentication successful! Hello, {name}.")
            return

    print("Authentication failed. Face not recognized.")

# Main Program
def main():
    while True:
        print("\nFace Scanner System")
        print("1. Register Face")
        print("2. Authenticate Face")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")
        if choice == '1':
            name = input("Enter name for registration: ")
            register_face(name)
        elif choice == '2':
            authenticate_face()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
