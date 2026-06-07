import sys
from config import CARLA_EGG

sys.path.append(CARLA_EGG)

import carla


class CarlaManager:

    def __init__(self, host, port):

        self.client = carla.Client(host, port)
        self.client.set_timeout(10.0)

        self.world = self.client.get_world()

        self.actors = []

    def spawn_vehicle(self):

        blueprint_library = self.world.get_blueprint_library()

        vehicle_bp = blueprint_library.filter(
            "vehicle.tesla.model3"
        )[0]

        import random

        spawn_point = random.choice(
            self.world.get_map().get_spawn_points()
        )

        vehicle = self.world.spawn_actor(
            vehicle_bp,
            spawn_point
        )

        vehicle.set_autopilot(True)

        self.actors.append(vehicle)

        return vehicle
    
    def destroy_all(self):

        for actor in self.actors:

            actor.destroy()

        self.actors.clear()