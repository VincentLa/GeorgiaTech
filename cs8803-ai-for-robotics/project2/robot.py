import math
import random

PI = math.pi


def compute_distance(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.sqrt(dx**2 + dy**2)


def compute_bearing(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.atan2(dy, dx)


def truncate_angle(t):
    return ((t+PI) % (2*PI)) - PI

class Robot:
    def __init__(self, x=0.0, y=0.0, bearing=0.0, max_distance=1.0, max_steering=PI/4):
        self.x = x
        self.y = y
        self.bearing = bearing
        self.max_distance = max_distance
        self.max_steering = max_steering

    def set_noise(self, steering_noise, distance_noise, measurement_noise):
        self.steering_noise = float(steering_noise)
        self.distance_noise = float(distance_noise)
        self.measurement_noise = float(measurement_noise)

    # move the robot
    def move(self, steering, distance, noise=False):
        if noise:
            steering += random.uniform(-0.01, 0.01)
            distance *= random.uniform(0.99, 1.01)

        steering = max(-self.max_steering, steering)
        steering = min(self.max_steering, steering)
        distance = max(0, distance)
        distance = min(self.max_distance, distance)

        self.bearing = truncate_angle(self.bearing + float(steering))
        self.x += distance * math.cos(self.bearing)
        self.y += distance * math.sin(self.bearing)

    def measure_distance_and_bearing_to(self, point, noise=False):
        
        current_position = (self.x, self.y)

        distance_to_point = compute_distance(current_position, point)
        bearing_to_point = compute_bearing(current_position, point)

        if noise:
            distance_sigma = 0.05*distance_to_point
            bearing_sigma = 0.02*distance_to_point

            distance_noise = random.gauss(0, distance_sigma)
            bearing_noise = random.gauss(0, bearing_sigma)
        else:
            distance_noise = 0
            bearing_noise = 0

        measured_distance = distance_to_point + distance_noise
        measured_bearing = truncate_angle(bearing_to_point - self.bearing + bearing_noise)

        return measured_distance, measured_bearing

    # find the next point without updating the robot's position
    def find_next_point(self, steering, distance):

        steering = max(-self.max_steering, steering)
        steering = min(self.max_steering, steering)
        distance = max(0, distance)
        distance = min(self.max_distance, distance)

        bearing = truncate_angle(self.bearing + float(steering))
        x = self.x + (distance * math.cos(bearing))
        y = self.y + (distance * math.sin(bearing))

        return x, y

    def __repr__(self):
        """This allows us to print a robot's position"""
        return '[%.5f, %.5f]' % (self.x, self.y)
