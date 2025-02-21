# Face Direction Detection for Multi-Monitor Setup

This Python project uses OpenCV and MediaPipe to detect a user's face direction and move the cursor to the appropriate monitor based on nose position calibration. It allows seamless navigation across multiple displays by tracking head movements.

## Features

- Uses **OpenCV** for image processing.
- Implements **MediaPipe Face Mesh** for facial landmark detection.
- Tracks **nose position** for head movement detection.
- Supports **multi-monitor setups** for cursor navigation.
- Moves the cursor to the correct display based on calibration.

## Requirements

Make sure you have Python(3.10) installed along with the following dependencies:

```sh
pip install opencv-python mediapipe pyautogui
```

## Usage

1. Run the script:
   ```sh
   python script.py
   ```
2. Enter the number of displays when prompted.
3. Look at each display and press Enter when instructed to calibrate.
4. Once calibration is complete, the program will track head movements and move the cursor accordingly.
5. Press `q` to exit the program.

## How It Works

- The script initializes a webcam and detects the **nose landmark** using **MediaPipe Face Mesh**.
- During calibration, the nose position for each monitor is stored.
- In real-time, the script detects if the user's nose position matches a calibrated position and moves the cursor to the corresponding monitor.

## Known Issues

- Works best with **good lighting** and a **clear camera view**.
- Accuracy may vary depending on **camera resolution** and **face position**.

## Future Improvements

- Improve accuracy using **machine learning models**.
- Add support for **custom sensitivity adjustments**.
- Implement **gesture-based actions**.

## License

This project is open-source and free to use.

## Author

Chirag Gavande

