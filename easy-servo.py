from machine import Pin, PWM, Timer
import time
import os

class Servo:
    _timer_list = []
    _timer_usage = []
    _initialized = False

    def __init__(self, pin, start=0, *, min_angle=0, max_angle=180, freq=50, pulse_min=0.5, pulse_max=2.5):
        """
        Initializes the servo object.

        :param pin: The pin to which the servo is connected.
        :param start: Starting angle of the servo.
        :param min_angle: Minimum angle of the servo in degrees.
        :param max_angle: Maximum angle of the servo in degrees.
        :param freq: PWM frequency.
        :param pulse_min: Minimum pulse width in milliseconds.
        :param pulse_max: Maximum pulse width in milliseconds.
        """
        self._servo = PWM(Pin(pin))
        self._servo.freq(freq)
        self._pulse_min = pulse_min  # Minimum pulse width in milliseconds for 0 degrees
        self._pulse_max = pulse_max  # Maximum pulse width in milliseconds for 180 degrees
        self._freq = freq  # Frequency in Hertz (pulse period in milliseconds)
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._current_angle = start
        self._servo.duty(self._angle_to_duty(self._current_angle))
        self._target_angle = self._current_angle
        self._step = 0
        self._step_delay = 0.1
        self._timer = None  # Timer will be initialized only when needed
        self._timer_index = None
        if not Servo._initialized:
            self._initialize_timers()

    def move(self, target_angle, speed=None, async_mode=False):
        """
        Moves the servo to a specific angle.

        :param target_angle: Target angle.
        :param speed: Speed of movement in degrees per second.
        :param async_mode: True for asynchronous movement, False for synchronous movement.
        """
        if not self._min_angle <= target_angle <= self._max_angle:
            raise ValueError(f"Target angle must be between {self._min_angle} and {self._max_angle}.")
        
        if speed is None:
            self._servo.duty(self._angle_to_duty(angle))
            self._target_angle = angle
            self._current_angle = angle
        else:
            self._step_delay = 1.0 / speed
            self._target_angle = target_angle

            if self._current_angle < self._target_angle:
                self._step = 1
            else:
                self._step = -1
            
            if async_mode:
                if self._timer is None:
                    self._timer_index = self._get_free_timer()
                    self._timer = Timer(self._timer_list[self._timer_index])
                self._timer.init(period=int(self._step_delay * 1000), mode=Timer.PERIODIC, callback=self._update_angle)
            else:
                while self._current_angle != self._target_angle:
                    self._update_angle(None)
                    time.sleep(self._step_delay)
                
    def goal_reached(self):
        """
        Checks if the servo has reached its target angle.

        :return: True if the servo has reached its target angle, False otherwise.
        """
        return self._current_angle == self._target_angle
    
    def stop(self):
        """
        Stops the servo movement and releases the timer.
        """
        if self._timer:
            self._timer.deinit()
            Servo._timer_usage[self._timer_index] = False
            self._timer = None
        self._servo.duty(0)

    def detach(self):
        """
        Detaches the servo.
        """
        self._servo.deinit()

    def _angle_to_duty(self, angle):
        """
        Converts the angle to duty cycle.

        :param angle: The angle in degrees.
        :return: The duty cycle.
        """
        pulse_width = self._pulse_min + (angle / self._max_angle) * (self._pulse_max - self._pulse_min)
        duty_cycle = int((pulse_width * self._freq / 1000) * 1023)
        return duty_cycle
    
    def _update_angle(self, t):
        """
        Moves the servo step by step to the target angle.

        :param t: Timer callback parameter (not used).
        """
        if self._current_angle != self._target_angle:
            self._current_angle += self._step
            duty = self._angle_to_duty(self._current_angle)
            self._servo.duty(duty)
        else:
            if t:
                self.stop()

    @classmethod
    def _initialize_timers(cls):
        """
        Initializes the timer management based on the ESP model.
        """
        model = os.uname().machine
        if 'ESP32C' in model:
            cls._timer_list = [0, 2]  # ESP32-C3/6 have 2 timers (0 and 2)
        elif 'ESP8266' in model:
            cls._timer_list = [0, 1]  # ESP8266 has 2 timers
        elif 'ESP32' in model:
            cls._timer_list = [0, 1, 2, 3]  # Default to 4 timers for ESP32
        elif 'Nano' in model:
            cls._timer_list = [0, 1, 2]  # Default to 4 timers for ESP32
        else:
            cls._timer_list = [0]  # Default to 1 timer for other boards
        cls._timer_usage = [False] * len(cls._timer_list)
        cls._initialized = True

    @classmethod
    def _get_free_timer(cls):
        """
        Returns a free timer index.

        :return: A free timer index.
        :raises RuntimeError: If no free timers are available.
        """
        for index, in_use in enumerate(cls._timer_usage):
            if not in_use:
                cls._timer_usage[index] = True
                return index
        raise RuntimeError("No free timers available")

