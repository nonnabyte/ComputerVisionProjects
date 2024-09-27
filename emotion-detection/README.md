# Real-time Emotion Detection and Uplifting Feedback System

![Emotion Detection](assets/emotion_detection_screenshot.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Concept and Inspiration](#concept-and-inspiration)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)
- [License](#license)

## Introduction

The **Real-time Emotion Detection and Uplifting Feedback System** is a Python-based application that leverages facial emotion recognition to provide users with immediate and supportive feedback. By analyzing facial expressions through a webcam, the system detects emotions and responds with corresponding audio cues and uplifting messages to enhance user well-being.

## Features

- **Real-time Emotion Detection**: Utilizes DeepFace to analyze facial expressions and determine the dominant emotion.
- **Visual Feedback**: Displays detected emotions with colored annotations on the video feed.
- **Audio Feedback**:
  - Plays frequency-specific background sounds (e.g., theta for anger and fear, alpha for sadness and disgust).
  - Provides uplifting verbal messages using Google Text-to-Speech (gTTS) to encourage positive emotions.
- **Emotion Stabilization**: Implements cooldown periods to prevent rapid fluctuations in emotion detection.
- **Smooth Audio Transitions**: Incorporates fade-out effects for audio to ensure a pleasant auditory experience.
- **Resource Management**: Ensures proper cleanup of audio resources and handles threading gracefully to prevent resource leaks.

## Concept and Inspiration

In today's fast-paced world, managing emotions effectively is crucial for mental well-being. The inspiration behind this project stems from the desire to create a tool that not only recognizes and acknowledges a user's current emotional state but also provides immediate, supportive feedback to help uplift and stabilize their mood.

By integrating facial emotion recognition with audio-visual feedback, the system aims to offer a seamless and non-intrusive way for individuals to become more aware of their emotions and receive encouragement in real-time. This can be particularly beneficial in settings like remote work, online education, or personal self-awareness practices.

## Installation

### Prerequisites

- **Python 3.6 or higher**: Ensure that Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
- **Webcam**: A functional webcam connected to your computer.

### Clone the Repository

```bash
git clone https://github.com/yourusername/emotion-detection-feedback.git
cd emotion-detection-feedback
```

### Install Dependencies

It's recommended to use a virtual environment to manage dependencies.

1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages**
   ```bash
   pip install opencv-python deepface pygame numpy gTTS
   ```

### Prepare Audio Files

Ensure that the frequency sound files (`theta.mp3` and `alpha.mp3`) are placed in the project directory. You can use royalty-free sound clips corresponding to the specified frequencies.

## Usage

1. **Run the Application**

   ```bash
   python emotion_detection.py
   ```

2. **Interact with the System**

   - **Emotion Detection**: The webcam will activate, and the system will begin analyzing your facial expressions in real-time.
   - **Visual Feedback**: Detected emotions will be displayed on the video feed with colored rectangles and labels.
   - **Audio Feedback**:
     - Frequency-specific sounds will play based on the detected emotion.
     - Uplifting messages will be spoken to encourage positive emotions.

3. **Exit the Application**

   - Press the **'q'** key on your keyboard to gracefully exit the application.

## Configuration

You can adjust various parameters within the `emotion_detection.py` script to tailor the application's behavior to your preferences.

### Parameters to Adjust

- **Confidence Threshold**: Determines the minimum confidence score required to consider an emotion detection valid.

  ```python
  confidence_threshold = 50  # Percentage
  ```

- **Cooldown Periods**:
  - **Emotion Change Cooldown**: Time (in seconds) before allowing another emotion change.

    ```python
    emotion_cooldown = 3  # Seconds between emotion changes
    ```

  - **TTS Cooldown**: Time (in seconds) before allowing another TTS message.

    ```python
    tts_cooldown = 5  # Seconds between TTS messages
    ```

- **Fade-Out Duration**: Duration (in milliseconds) for audio fade-out effects.

  ```python
  sound_channel.fadeout(1000)  # 1 second
  pygame.mixer.music.fadeout(1000)  # 1 second
  ```

- **Emotion Colors**: Customize the BGR color codes for different emotions.

  ```python
  emotion_colors = {
      'angry': (0, 0, 255),      # Red
      'disgust': (0, 128, 128),  # Teal
      'fear': (128, 0, 128),     # Purple
      'happy': (0, 255, 0),      # Green
      'sad': (255, 0, 0),        # Blue
      'surprise': (0, 255, 255), # Yellow
      'neutral': (192, 192, 192) # Gray
  }
  ```

## Dependencies

The project relies on several Python libraries. Below is a list of primary dependencies:

- **OpenCV (`opencv-python`)**: For video capture and image processing.
- **DeepFace (`deepface`)**: For facial emotion recognition.
- **Pygame (`pygame`)**: For audio playback.
- **NumPy (`numpy`)**: For numerical operations.
- **Google Text-to-Speech (`gTTS`)**: For generating spoken messages.
- **Threading and System Modules**: For managing concurrent operations and system interactions.

### Installing Dependencies

All dependencies can be installed using `pip`:

```bash
pip install opencv-python deepface pygame numpy gTTS
```

## Future Improvements

While the current system provides a solid foundation for emotion detection and uplifting feedback, several enhancements can be considered to improve its functionality and user experience:

1. **Enhanced Emotion Recognition**:
   - **Model Fine-Tuning**: Retrain or fine-tune the DeepFace model with a more diverse dataset to improve accuracy across different demographics and expressions.
   - **Alternative Libraries**: Explore other emotion detection libraries like FER or custom-trained models for better performance.

2. **User Interface Enhancements**:
   - **Graphical User Interface (GUI)**: Develop a more user-friendly GUI using libraries like Tkinter or PyQt for better interaction.
   - **Mobile Integration**: Adapt the system for mobile devices using frameworks like Kivy.

3. **Advanced Audio Feedback**:
   - **Dynamic Soundscapes**: Incorporate more varied and dynamic soundscapes that adapt based on the intensity of the detected emotion.
   - **Voice Customization**: Allow users to select different voices or languages for the TTS messages.

4. **Logging and Analytics**:
   - **Emotion Tracking**: Implement logging to track and visualize emotion trends over time.
   - **User Feedback**: Collect user feedback to continuously improve emotion detection accuracy and feedback relevance.

5. **Performance Optimization**:
   - **Real-time Processing**: Optimize the processing pipeline to reduce latency and ensure smooth real-time performance.
   - **Resource Management**: Further enhance resource cleanup and management to prevent potential memory leaks or performance degradation.

6. **Privacy and Security**:
   - **Data Protection**: Implement measures to ensure that captured facial data is not stored or misused.
   - **User Consent**: Ensure that users are informed and consent to the use of their facial data for emotion detection.

7. **Multi-user Support**:
   - **Multiple Faces**: Extend the system to handle multiple faces simultaneously, providing individualized feedback.

8. **Customization and Extensibility**:
   - **Custom Messages**: Allow users to input their own uplifting messages.
   - **Emotion Mapping**: Enable users to map different emotions to specific audio cues and messages.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Disclaimer**: This application uses facial recognition and emotion detection technologies. Ensure that you comply with all relevant laws and regulations regarding privacy and data protection. Obtain informed consent from all users before capturing and analyzing their facial data.

---

## Acknowledgements

- [DeepFace](https://github.com/serengil/deepface) - A lightweight face recognition and facial attribute analysis framework.
- [gTTS](https://github.com/pndurette/gTTS) - A Python library and CLI tool to interface with Google Translate's text-to-speech API.
- [Pygame](https://www.pygame.org/news) - A set of Python modules designed for writing video games.
- [OpenCV](https://opencv.org/) - An open-source computer vision and machine learning software library.

---

## Contact

For any questions, suggestions, or contributions, please open an issue or submit a pull request on the [GitHub repository](https://github.com/yourusername/emotion-detection-feedback).
