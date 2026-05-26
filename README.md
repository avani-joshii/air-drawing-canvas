# air-drawing-canvas
A computer vision project built using Python, OpenCV, and MediaPipe that allows users to draw in the air using hand tracking.

## Key features:
- Real-time hand tracking using MediaPipe's 21-point landmark model
- Dual-hand control scheme for simultaneous color selection and drawing
- Left hand finger count controls brush color (4 colors + white)
- Right hand gestures control drawing (1 finger), brush thickness (2 fingers), and erase mode (fist)
- Smooth stroke rendering by connecting positional data between frames
- Semi-transparent webcam overlay so you can see your hand while drawing

## Technologies Used
- Python (3.11.9)
- OpenCV
- MediaPipe (0.10.9)
- NumPy
