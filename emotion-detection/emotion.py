import cv2
from deepface import DeepFace
import pygame
from collections import deque
import numpy as np
import time
from gtts import gTTS
import threading
import atexit
import os

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Define the sound files corresponding to each frequency
frequency_sound_files = {
    'theta': 'theta.mp3',  # For emotions like 'angry', 'fear'
    'alpha': 'alpha.mp3',  # For emotions like 'sad', 'disgust'
}

# Map emotions to frequencies
emotion_frequency_map = {
    'angry': 'theta',
    'fear': 'theta',
    'sad': 'alpha',
    'disgust': 'alpha',
}

# Define uplifting messages for negative emotions
uplifting_messages = {
    'angry': "Take a deep breath!",
    'disgust': "Stay positive!",
    'fear': "You're strong!",
    'sad': "Smile, it's a new day!"
}

# Define colors for emotions (BGR format)
emotion_colors = {
    'angry': (0, 0, 255),      # Red
    'disgust': (0, 128, 128),   # Teal
    'fear': (128, 0, 128),      # Purple
    'happy': (0, 255, 0),       # Green
    'sad': (255, 0, 0),         # Blue
    'surprise': (0, 255, 255),  # Yellow
    'neutral': (192, 192, 192)  # Gray
}

# Load the sounds into pygame
frequency_sounds = {}
for freq, file in frequency_sound_files.items():
    try:
        frequency_sounds[freq] = pygame.mixer.Sound(file)
    except pygame.error as e:
        print(f"Could not load sound for frequency {freq}: {e}")

# Pre-generate TTS audio files for the uplifting messages
tts_audio_files = {}
for emotion, message in uplifting_messages.items():
    filename = f"{emotion}_message.mp3"
    if not os.path.exists(filename):
        try:
            tts = gTTS(text=message, lang='en')
            tts.save(filename)
        except Exception as e:
            print(f"Error generating TTS for {emotion}: {e}")
    tts_audio_files[emotion] = filename

# Initialize variables
current_emotion = None
previous_emotion = None
current_confidence = None
detected_emotion = None
detected_confidence = 0
face_coords = None

# Emotion buffer for temporal smoothing
emotion_buffer = deque(maxlen=10)
emotion_consistency_threshold = 4

# Confidence threshold
confidence_threshold = 50  # Only consider emotions with confidence >= 50%

# List of possible emotions
emotion_list = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Initialize EMA variables
ema_alpha = 0.7  # Higher value for more responsiveness
emotion_emas = {emotion: 0.0 for emotion in emotion_list}

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Frame counter
frame_counter = 0
process_frame_rate = 5  # Process more frequently for better responsiveness

# Sound playback control
sound_channel = pygame.mixer.Channel(0)

# TTS thread control
tts_thread = None
tts_lock = threading.Lock()
tts_stop_event = threading.Event()

# Cooldown control for TTS messages
last_tts_time = 0
tts_cooldown = 5  # Seconds between TTS messages

# Cooldown control for emotion changes
last_emotion_change_time = 0
emotion_cooldown = 3  # Seconds between emotion changes

def speak_message(emotion):
    with tts_lock:
        try:
            filename = tts_audio_files.get(emotion)
            if filename and os.path.exists(filename):
                # Play the pre-generated audio
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                # Wait for playback or stop event
                while pygame.mixer.music.get_busy():
                    if tts_stop_event.is_set():
                        pygame.mixer.music.fadeout(1000)  # Fade out over 1 second
                        break
                    time.sleep(0.1)
                # Update last TTS time
                global last_tts_time
                last_tts_time = time.time()
            else:
                print(f"No TTS audio file for emotion: {emotion}")
        except Exception as e:
            print(f"Error in TTS playback: {e}")

# Register cleanup function
def cleanup():
    # Stop any existing TTS
    if tts_thread is not None and tts_thread.is_alive():
        tts_stop_event.set()
        tts_thread.join()
        tts_stop_event.clear()
    # Quit pygame mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    # Release video capture
    cap.release()
    cv2.destroyAllWindows()
    # Optionally, delete TTS audio files
    for filename in tts_audio_files.values():
        if os.path.exists(filename):
            os.remove(filename)

atexit.register(cleanup)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Error: Failed to capture image.")
        break

    # Preprocess frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    frame_counter += 1
    if frame_counter % process_frame_rate == 0:
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_coords = (x, y, w, h)
            face_roi = rgb_frame[y:y + h, x:x + w]

            # Perform emotion analysis
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            emotion_scores = result[0]['emotion']
            emotion_confidence = emotion_scores[emotion]

            detected_emotion = emotion
            detected_confidence = emotion_confidence

            # Only consider emotions with high confidence
            if emotion_confidence >= confidence_threshold:
                # Update EMA for each emotion
                for em in emotion_emas.keys():
                    if em == emotion:
                        emotion_emas[em] = (1 - ema_alpha) * emotion_emas[em] + ema_alpha * emotion_confidence
                    else:
                        emotion_emas[em] = (1 - ema_alpha) * emotion_emas[em]

                # Determine the emotion with the highest EMA
                most_common_emotion = max(emotion_emas, key=emotion_emas.get)
                current_confidence = emotion_emas[most_common_emotion]

                # Check if the emotion should be updated based on cooldown
                if most_common_emotion != current_emotion:
                    time_since_last_emotion_change = time.time() - last_emotion_change_time
                    if time_since_last_emotion_change >= emotion_cooldown:
                        previous_emotion = current_emotion
                        current_emotion = most_common_emotion
                        last_emotion_change_time = time.time()

                        # Play sound and TTS if emotion changes
                        if current_emotion != previous_emotion:
                            # Stop existing sound with fadeout
                            if sound_channel.get_busy():
                                sound_channel.fadeout(1000)  # Fade out over 1 second

                            # Check if the emotion is mapped to a frequency
                            if current_emotion in emotion_frequency_map:
                                frequency = emotion_frequency_map[current_emotion]
                                # Play the corresponding frequency sound
                                if frequency in frequency_sounds:
                                    sound_channel.play(frequency_sounds[frequency], loops=-1)
                                else:
                                    print(f"No sound file for frequency: {frequency}")

                                # Check cooldown before speaking message
                                time_since_last_tts = time.time() - last_tts_time
                                if time_since_last_tts >= tts_cooldown:
                                    # Stop any existing TTS
                                    if tts_thread is not None and tts_thread.is_alive():
                                        tts_stop_event.set()
                                        tts_thread.join()
                                        tts_stop_event.clear()

                                    # Start TTS in a new thread
                                    tts_thread = threading.Thread(target=speak_message, args=(current_emotion,))
                                    tts_thread.start()
                                else:
                                    print("TTS cooldown active. Message not spoken.")
                            else:
                                # Stop sound if not a target emotion
                                if sound_channel.get_busy():
                                    sound_channel.fadeout(1000)  # Fade out over 1 second
                                # Stop any existing TTS
                                if tts_thread is not None and tts_thread.is_alive():
                                    tts_stop_event.set()
                                    tts_thread.join()
                                    tts_stop_event.clear()
                    else:
                        # Keep the current emotion until cooldown passes
                        pass
                else:
                    # Update last emotion change time if the emotion remains the same
                    last_emotion_change_time = time.time()
        else:
            face_coords = None
            # Stop sound if no face is detected
            if sound_channel.get_busy():
                sound_channel.fadeout(1000)  # Fade out over 1 second
            # Stop any existing TTS
            if tts_thread is not None and tts_thread.is_alive():
                tts_stop_event.set()
                tts_thread.join()
                tts_stop_event.clear()

    # Draw annotations
    if face_coords is not None and current_emotion is not None:
        x, y, w, h = face_coords
        color = emotion_colors.get(current_emotion, (255, 255, 255))  # Default to white

        # Draw rectangle with the emotion color
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Display the emotion text with the same color
        cv2.putText(frame, f"{current_emotion} ({current_confidence:.2f}%)", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # If negative emotion, display uplifting message
        if current_emotion in emotion_frequency_map:
            message = uplifting_messages.get(current_emotion, "")
            if message:
                cv2.putText(frame, message, (x, y + h + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
    else:
        # Existing code for when no emotion is detected
        pass

    # Display the frame
    cv2.imshow('Real-time Emotion Detection with Frequency Audio and TTS', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Stop any playing sound
        if sound_channel.get_busy():
            sound_channel.fadeout(1000)  # Fade out over 1 second
        # Stop any existing TTS
        if tts_thread is not None and tts_thread.is_alive():
            tts_stop_event.set()
            tts_thread.join()
            tts_stop_event.clear()
        break

# Cleanup (will be handled by atexit)
