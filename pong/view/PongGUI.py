# package pong.view
import pygame
from pong.event.EventBus import EventBus
from pong.event.EventHandler import EventHandler
from pong.event.ModelEvent import ModelEvent
from pong.model import *
from pong.model.Config import *
from pong.model.Entity import Entity
from pong.model.Pong import Pong
from pong.view.theme.Cool import Cool
from pong.view.theme.Duckie import Duckie
from typing import Tuple
import time

class PongGUI:
    """
    The GUI for the Pong game (except the menu).
    No application logic here just GUI and event handling.

    Run this to run the game.

    See: https://en.wikipedia.org/wiki/Pong
    """
    running = False    # Is game running?
    stop_game = False  # Should game stop?
    assets = None # Assets for the game
    
    # ------- Keyboard handling ----------------------------------

    @classmethod
    def key_pressed(cls, event):
        """Handles the pygame.KEYDOWN event."""
        # Pausing the game but listening for escape key
        if event.key == pygame.K_ESCAPE:
            if cls.running:
                cls.pause_game()
            else:
                cls.running = True
        elif event.key == pygame.K_n:
            cls.new_game() 
            
        # Stop events if game is not running
        if not cls.running:
            return
        
        # -- Handle other keys --
        # Right player up
        if event.key == pygame.K_UP:
            Pong.right_paddle.accelerate(0, -PADDLE_SPEED)
        # Right player down
        elif event.key == pygame.K_DOWN:
            Pong.right_paddle.accelerate(0, PADDLE_SPEED)
        # Left player up
        elif event.key == pygame.K_q:
            Pong.left_paddle.accelerate(0, -PADDLE_SPEED)
        # Left player down
        elif event.key == pygame.K_a:
            Pong.left_paddle.accelerate(0, PADDLE_SPEED)

    @classmethod
    def key_released(cls, event):
        """Handles the pygame.KEYUP event."""
        if not cls.running:
            return

        # TODO: Do not set speed to 0 if acceleration is in opposite direction of released key
        # Right player halt up
        if event.key == pygame.K_UP:
            Pong.right_paddle.accelerate(0, 0)
        # Right player halt down
        elif event.key == pygame.K_DOWN:
            Pong.right_paddle.accelerate(0, 0)
        # Left player halt up
        elif event.key == pygame.K_q:
            Pong.left_paddle.accelerate(0, 0)
        # Left player halt down
        elif event.key == pygame.K_a:
            Pong.left_paddle.accelerate(0, 0)

    # -------- Event handling (events sent from model to GUI) ------------

    # It listens for events from the model, and when it hears one, it does something.
    class ModelEventHandler(EventHandler):
        def on_model_event(self, evt: ModelEvent):
            if evt.event_type == ModelEvent.EventType.BALL_HIT_PADDLE:
                filename = PongGUI.assets.ball_hit_paddle_sound_file
                PongGUI.assets.get_sound(filename).play()
            elif evt.event_type == ModelEvent.EventType.BALL_HIT_WALL_CEILING:
                # TODO Optional
                pass

    # ################## Nothing to do below ############################


    # ---------- View handling ------------------------------

    @classmethod
    def draw_entity(cls, entity: Entity):
        """Draws an entity on the screen."""
        image = cls.assets.get(entity)
        image = pygame.transform.scale(image, (entity.get_width(), entity.get_height()))
        cls.screen.blit(image, (entity.get_x(), entity.get_y()))        

    @classmethod
    def reset_screen(cls):
        """Clears the screen and draws the background."""
        # Clear screen
        cls.screen.fill((0, 0, 0))
        # Draw Background
        background_pic = pygame.transform.scale( cls.assets.get_background(), (GAME_WIDTH, GAME_HEIGHT))
        cls.screen.blit(background_pic, (0, 0))

    @classmethod
    def draw_scoreboard(cls):
        """Draws the scoreboard on the screen."""
        text = f"P1: {Pong.get_points_left()}, P2: {Pong.get_points_right()}"
        cls.__display_text(text, 22, (255,255,255), (GAME_WIDTH/2, 20), (0,0,0))

    @classmethod
    def __display_text(
        cls,
        text: str,
        size: int,
        color: Tuple[int, int, int],
        position: Tuple[int, int] = None,
        fill: Tuple[int, int, int] = None,
    ):
        """Displays given text in the center of the screen."""
        position = (GAME_WIDTH/2, GAME_HEIGHT/2) if position == None else position

        text = cls.__create_text_element(text, size, color)
        text_rect = text.get_rect(center=position)
        if fill != None:
            temp_surface = pygame.Surface(text.get_size())
            temp_surface.fill(fill)
            temp_surface.blit(text, (0,0))
            cls.screen.blit(temp_surface, text_rect)
        else:
            cls.screen.blit(text, text_rect)
        pygame.display.flip()

    @classmethod 
    def __create_text_element(cls, text: str, size: int, color: Tuple[int, int, int]):
        font = pygame.font.Font(None, size)
        final_text = font.render(text, True, color)
        return final_text

    @classmethod
    def render(cls):
        """Renders the View."""
        # Reset Screen and draw background
        cls.reset_screen()
        # Draw entities
        for entity in Pong.entities:
            cls.draw_entity(entity)

        # Draw scoreboard
        cls.draw_scoreboard()
        player_won = Pong.get_winner()
        if player_won:
            cls.win_screen(player_won)

        # Update screen
        pygame.display.flip()
       
    @classmethod
    def new_game(cls):
        """Starts a new game."""
        Pong.reset_points()
        Pong.load_entities()
        cls.running = True

    @classmethod
    def kill_game(cls):
        """Stops the game."""
        cls.stop_game = True
        cls.running = False
         
    @classmethod
    def pause_game(cls):
        """Pauses the game."""
        cls.running = False
        cls.__display_text("Paused", 50, (255, 255, 255))
        
    @classmethod
    def win_screen(cls, player_side: int):
        """Displays the winner screen."""
        # Allows a player to win the game
        cls.screen.fill((0, 0, 0))
        # Draw win message
        cls.__display_text(f"Player {player_side} wins!", 55, (255, 255, 255))
        cls.running = False

    # ---------- Game loop ----------------
        
    @classmethod
    def init_pygame(cls):
        """Initializes Pygame properties."""
        pygame.init()
        pygame.display.set_caption("Pong")
        cls.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        cls.clock = pygame.time.Clock()

    @classmethod
    def run(cls):
        """Loads and runs the game."""
        # Start Game
        cls.running = True
        cls.init_pygame()
        # Load assets
        cls.assets = Cool()
        Pong.load_entities()
        # Initialize model
        EventBus.register(cls.ModelEventHandler())

        # Main game loop
        while not cls.stop_game:
            # Handle events
            cls.handle_events()
            if cls.running:
                # Update model
                Pong.update(time.time())
                # Render
                cls.render()
            # Tick
            cls.clock.tick(60)
        pygame.quit()

    @classmethod
    def handle_events(cls):
        """Handles all Pygame Events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.kill_game()
            elif event.type == pygame.KEYDOWN:
                cls.key_pressed(event)
            elif event.type == pygame.KEYUP:
                cls.key_released(event)
