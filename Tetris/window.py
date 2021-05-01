import arcade
from grid import Grid
from enum import Enum, auto
import sys


# A játék állapotai.
class States(Enum):
    PAUSE = auto()
    PLAYING = auto()
    LOST = auto()


class TetrisWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.center_window()
        self.grid = Grid()
        self.timer = 0
        self.state = States.PLAYING
        self.down_key_held = False

    def on_draw(self):
        arcade.start_render()
        self.grid.draw_all()

        # Szövegek megjelnítése az ablak jobb oldali részében.
        arcade.draw_text("Cleared rows:", 832, 840, arcade.color.AERO_BLUE, 20)
        arcade.draw_text(str(self.grid.cleared_rows), 896, 800, arcade.color.AERO_BLUE, 25)
        arcade.draw_text("Next letter:", 832, 600, arcade.color.AERO_BLUE, 20)
        arcade.draw_text("Press P to pause", 852, 80, arcade.color.AERO_BLUE, 15)
        arcade.draw_text("Press ESC to exit", 852, 40, arcade.color.AERO_BLUE, 15)

        # Pause valamint a Game Over szövegek.
        if self.state == States.PAUSE:
            arcade.draw_text("Game paused", 256, 480, arcade.color.YELLOW, 40)
        elif self.state == States.LOST:
            arcade.draw_rectangle_filled(256 + 128, 480 + 10, 512, 140, arcade.color.YANKEES_BLUE)
            arcade.draw_text("Game Over!", 256, 480, arcade.color.YELLOW, 40)
            arcade.draw_text("Press Space to restart", 256 + 48, 440, arcade.color.AERO_BLUE, 15)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP and self.state == States.PLAYING:
            """ Másoljuk át a main_grid adatait a test_grid-be. """
            self.grid.grid_copy(self.grid.main_grid, self.grid.test_grid)
            """ Forgassuk el a betűt a main_grid-en. """
            self.grid.rotate_letter()
            """ Ellenőrizzük, hogy nem e lett felülírva a fal, vagy a megálapodott betűk."""
            if not self.grid.check_grids():
                """ Ha felülírtunk valamit, akkor visszamásoljuk az adatokat a test_grid-ből a main_grid-be."""
                self.grid.grid_copy(self.grid.test_grid, self.grid.main_grid)

        elif symbol == arcade.key.LEFT and self.state == States.PLAYING:
            self.grid.move_left()
        elif symbol == arcade.key.RIGHT and self.state == States.PLAYING:
            self.grid.move_right()
        elif symbol == arcade.key.DOWN and self.state == States.PLAYING:
            self.down_key_held = True
        elif symbol == arcade.key.SPACE and self.state == States.LOST:
            self.grid.restart()
            self.state = States.PLAYING
        elif symbol == arcade.key.ESCAPE:
            sys.exit()
        elif symbol == arcade.key.P:
            if self.state == States.PLAYING:
                self.state = States.PAUSE
            else:
                self.state = States.PLAYING

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.DOWN and self.state == States.PLAYING:
            self.down_key_held = False

    def on_update(self, dt):
        if self.state == States.PLAYING:
            self.timer += dt
            if self.down_key_held and self.timer >= 0.05:
                self.grid.move_down()
                self.timer = 0
            else:
                if self.timer >= 0.5:
                    self.grid.move_down()
                    self.timer = 0

        if self.grid.game_over:
            self.state = States.LOST


win = TetrisWindow(1024, 960, "Tetris game")
arcade.run()
