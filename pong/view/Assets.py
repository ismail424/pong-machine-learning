# package pong.view

from abc import abstractmethod, ABC

import pygame.color
import pygame.image
import pygame.mixer


class Assets(ABC):
    """
       Defining all assets used by application
       Common assets and asset handling (for all themes) here
       For specific handling see classes in theme/

       *** Nothing to do here ***
    """

    IMAGE_DIR = "assets/img/"
    SOUND_DIR = "assets/sound/"

    # A Map to store which image belongs to which object
    object_image_map = {}

    # ------------ Handling Colors and Images ------------------------
    color_fg_text = pygame.color.THECOLORS['white']
    splash_file = "pong.png"

    left_paddle_img_file = "coolbluepaddle.png"
    right_paddle_img_file = "coolredpaddle.png"

    # -------------- Audio handling -----------------------------
    ball_hit_paddle_sound_file = "ballhitpaddle.wav"

    @classmethod
    @abstractmethod
    def get_background(cls):  # Implemented by subclasses
        raise NotImplementedError

    # -------------- Methods binding objects/classes to assets -----------------

    @classmethod
    def bind(cls, obj, image_file_name):
        i = cls.get_image(image_file_name)
        if i is not None:
            cls.object_image_map.update({obj: i})
        else:
            raise ValueError("Missing image: " + cls.IMAGE_DIR + image_file_name)

    # Get image to render
    @classmethod
    def get(cls, obj):
        i = cls.object_image_map.get(obj)  # Try to find bound object
        if i is None:
            return cls.get_for_type(type(obj))  # .. if fail, check if class bound
        return i  # possible None, will throw exception, OK!

    @classmethod
    def get_for_type(cls, clazz):
        return cls.object_image_map.get(clazz)

    # ---------- Helpers ------------------------
    @classmethod
    def get_image(cls, file_name):
        return pygame.image.load(cls.IMAGE_DIR + file_name)

    @classmethod
    def get_sound(cls, file_name):
        return pygame.mixer.Sound(cls.SOUND_DIR + file_name)

