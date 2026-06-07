import carla
import numpy as np

from config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    FOV,
    CAMERA_X,
    CAMERA_Z
)


class CameraManager:

    def __init__(self, world, vehicle):

        self.world = world
        self.vehicle = vehicle

        self.camera = None
        self.latest_frame = None

    def spawn_camera(self):

        blueprint_library = self.world.get_blueprint_library()

        camera_bp = blueprint_library.find(
            "sensor.camera.rgb"
        )

        camera_bp.set_attribute(
            "image_size_x",
            str(IMAGE_WIDTH)
        )

        camera_bp.set_attribute(
            "image_size_y",
            str(IMAGE_HEIGHT)
        )

        camera_bp.set_attribute(
            "fov",
            str(FOV)
        )

        transform = carla.Transform(
            carla.Location(
                x=CAMERA_X,
                z=CAMERA_Z
            )
        )

        self.camera = self.world.spawn_actor(
            camera_bp,
            transform,
            attach_to=self.vehicle
        )

        self.camera.listen(
            lambda image: self.process_image(image)
        )

    def process_image(self, image):

        array = np.frombuffer(
            image.raw_data,
            dtype=np.uint8
        )

        array = array.reshape(
            (
                image.height,
                image.width,
                4
            )
        )

        self.latest_frame = array[:, :, :3]

    def get_frame(self):

        return self.latest_frame
    
    def destroy(self):

        if self.camera:

            self.camera.destroy()