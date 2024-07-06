# easy-micropython-servo
A MicroPython library for controlling servos using the PWM and Timer modules.

## Features

- Supports current ESP32 boards such as ESP32-C3/C6, ESP8266, and other ESP boards
- Allows to control the speed of the servo
- Allows synchronous and asynchronous servo movements
- Dynamic timer management based on the board type
- Provides methods to stop and detach servos
- Includes a method to check if the servo has reached its goal angle

## Usage

### Importing the Library

```python
from easy-servo import Servo
```

### Initializing a Servo

```python
servo_pin_1 = 0  # Example pin for servo 1
servo_pin_2 = 1  # Example pin for servo 2

s1 = Servo(servo_pin_1, start=0, min_angle=0, max_angle=270, freq=50)
s2 = Servo(servo_pin_2, start=90, min_angle=0, max_angle=180, freq=50)
```

### Moving a Servo

#### Synchronous Movement

```python
s1.move(90)  # Move to 90 degrees
s2.move(45, speed=30)  # Move to 45 degrees at 30 degrees per second
```

#### Asynchronous Movement

```python
s1.move(180, speed=30, async_mode=True)  # Move to 180 degrees asynchronously
s2.move(45, speed=15, async_mode=True)  # Move to 45 degrees asynchronously

# Wait while the servos are moving asynchronously
import time
time.sleep(10)

# Check if the goal is reached
if s1.goal_reached():
    print("Servo 1 has reached its goal.")
if s2.goal_reached():
    print("Servo 2 has reached its goal.")
```

### Stopping a Servo

```python
s1.stop()
s2.stop()
```

### Detaching a Servo

```python
s1.detach()
s2.detach()
```

## API Reference

### `Servo` Class

#### `__init__(self, pin, start=0, *, min_angle=0, max_angle=180, freq=50, pulse_min=0.5, pulse_max=2.5)`

Initializes the servo object.

- `pin`: The pin to which the servo is connected.
- `start`: Starting angle of the servo.
- `min_angle`: Minimum angle of the servo in degrees.
- `max_angle`: Maximum angle of the servo in degrees.
- `freq`: PWM frequency.
- `pulse_min`: Minimum pulse width in milliseconds.
- `pulse_max`: Maximum pulse width in milliseconds.

#### `move(self, target_angle, speed=None, async_mode=False)`

Moves the servo to a specific angle.

- `target_angle`: Target angle.
- `speed`: Speed of movement in degrees per second.
- `async_mode`: `True` for asynchronous movement, `False` for synchronous movement.

#### `stop(self)`

Stops the servo movement and releases the timer.

#### `detach(self)`

Detaches the servo.

#### `goal_reached(self)`

Checks if the servo has reached its target angle.

- Returns `True` if the servo has reached its target angle, `False` otherwise.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
