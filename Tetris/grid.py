import arcade
import letters
from copy import deepcopy

""" Minden betű a rács 1-es sor, és 4-es oszlopában kezd. """
START_X = 4
START_Y = 1

""" Ezek fogják tartalmazni az aktív betű x (oszlop), y (sor) pozícióját a rácson. """
current_x = START_X
current_y = START_Y


class Grid:
    def __init__(self):
        """ A Grid osztály tulajdonságai / tagsági változói. """
        self.width = 12
        self.height = 15
        self.line_color = arcade.make_transparent_color(arcade.color.WHITE, 25)
        self.main_grid = self.create()
        self.test_grid = deepcopy(self.main_grid)
        self.active_letter = letters.choose_random_letter()
        self.next_letter = None
        self.copy_letter_to_grid()
        self.letter_rotation = 1
        self.game_over = False
        self.cleared_rows = 0

    def restart(self):
        """ Újraindítja a játékot, visszaállít mindent az induló értékre. """
        global current_x, current_y
        current_x = START_X
        current_y = START_Y
        self.clear_grid(True)
        self.active_letter = letters.choose_random_letter()
        self.next_letter = None
        self.letter_rotation = 1
        self.copy_letter_to_grid()
        self.game_over = False
        self.cleared_rows = 0

    def grid_copy(self, from_grid, to_grid):
        """ Másolja az adatokat az egyik rácsból (from_grid) a másikba (to_grid). Gyorsabb mint a deepcopy függvény."""
        for y in range(self.height):
            for x in range(self.width):
                to_grid[y][x] = from_grid[y][x]

    def check_grids(self):
        """ Ellenőrzi, hogy nem e írtuk felül a falakat vagy a megállapodott betűket."""
        for y in range(self.height):
            for x in range(self.width):
                if self.test_grid[y][x] == 8 and self.get_cell(x, y) != 8:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 11 and self.get_cell(x, y) != 11:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 12 and self.get_cell(x, y) != 12:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 13 and self.get_cell(x, y) != 13:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 14 and self.get_cell(x, y) != 14:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 15 and self.get_cell(x, y) != 15:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 16 and self.get_cell(x, y) != 16:
                    self.letter_rotation -= 1
                    return False
                elif self.test_grid[y][x] == 17 and self.get_cell(x, y) != 17:
                    self.letter_rotation -= 1
                    return False
        return True

    def move_right(self):
        """ Jobbra mozgatja azokat a cellákat melyeknek 1-es értékük van. """
        global current_x
        breaker = False
        for x in range(self.width - 1, -1, -1):
            if breaker:
                break
            for y in range(self.height):
                if self.get_cell(x, y) == 1:
                    if self.try_move(x + 1, y):
                        self.set_cell(x, y, 0)
                        self.set_cell(x + 1, y, 1)
                    else:
                        breaker = True
                        break
        if not breaker:
            current_x += 1

    def move_left(self):
        """ Balra mozgatja azokat a cellákat melyeknek 1-es értékük van. """
        global current_x
        breaker = False
        for x in range(self.width):
            if breaker:
                break
            for y in range(self.height):
                if self.get_cell(x, y) == 1:
                    if self.try_move(x - 1, y):
                        self.set_cell(x, y, 0)
                        self.set_cell(x - 1, y, 1)
                    else:
                        breaker = True
                        break
        if not breaker:
            current_x -= 1

    def can_whole_letter_move_down(self):
        """ Megnézi, hogy az egész betű egyben tud e mozogni lefelé. """
        letter_can_move = []
        for y in range(self.height-1, -1, -1):
            for x in range(self.width):
                if self.get_cell(x, y) == 1:
                    if self.get_cell(x, y + 1) == 0 or self.get_cell(x, y + 1) == 1:
                        letter_can_move.append(True)
                    else:
                        letter_can_move.append(False)
        return letter_can_move[0] and letter_can_move[1] and letter_can_move[2] and letter_can_move[3]

    def move_down(self):
        """ Ha nem tud az egész betű egyben mozdulni lefelé, akkor settle, clear és return. """
        if not self.can_whole_letter_move_down():
            self.settle_letter()
            self.clear_full_rows()
            return

        """ Lefelé mozgatja azokat a cellákat melyeknek 1-es értékük van. """
        global current_y
        breaker = False
        for y in range(self.height-1, -1, -1):
            if breaker:
                break
            for x in range(self.width):
                if self.get_cell(x, y) == 1:
                    if self.try_move(x, y + 1):
                        self.set_cell(x, y, 0)
                        self.set_cell(x, y + 1, 1)
                    else:
                        breaker = True
                        # self.settle_letter()
                        break

        if not breaker:
            current_y += 1

    def clear_full_rows(self):
        """ Törli a full sorokat. """
        y = self.height - 1
        while y > 0:
            counter = 0
            for x in range(self.width):
                if self.get_cell(x, y) != 8 and self.get_cell(x, y) > 10:
                    counter += 1
            if counter == 10:
                """ Amikor a counter egyenlő tízzel, akkor van full sorunk."""
                # print(f"full row: {y}")
                for yy in range(y, 1, -1):
                    for xx in range(self.width):
                        if self.get_cell(xx, yy) != 8:
                            cell_above = self.get_cell(xx, yy - 1)
                            self.set_cell(xx, yy, cell_above)
                            self.set_cell(xx, yy - 1, 0)

                self.cleared_rows += 1
                y = self.height - 1
            y -= 1

    def try_move(self, x, y):
        """ Megnézi, hogy tudunk e mozdulni. Ha igen akkor True-t ad vissza, ha nem, akkor False-t ad vissza. """
        if self.get_cell(x, y) != 0:
            return False
        return True

    def rotate_letter(self):
        """ Forgatja az épp aktív betűt avagy Tetronimo-t. """
        self.clear_grid()
        self.letter_rotation += 1
        if self.letter_rotation > self.active_letter["num_rotations"]:
            self.letter_rotation = 1
        rot = self.active_letter[self.letter_rotation]
        for y in range(len(rot)):
            for x in range(len(rot[y])):
                if rot[y][x] == 1 and self.is_within_bounds(x + current_x):
                    self.set_cell(x + current_x, y + current_y, 1)

    def is_within_bounds(self, x):
        """ True vagy False értéket add vissza: True ha x 0 és 11 között van, egyébként meg False."""
        return x >= 0 and x < self.width

    def clear_grid(self, all_cell=False):
        """ Mindenütt törli a rácsot (nullára állítja) ahol nem 8-as (fal), vagy meg álapodott betű van. """
        for y in range(self.height):
            for x in range(self.width):
                if all_cell:
                    if self.get_cell(x, y) != 8:
                        self.set_cell(x, y, 0)
                else:
                    if self.get_cell(x, y) not in [8, 11, 12, 13, 14, 15, 16, 17]:
                        self.set_cell(x, y, 0)

    def copy_letter_to_grid(self):
        """ Bemásolja a rácsba az aktív betűt avagy Tetronimo-t. """
        rot = self.active_letter[1]
        for y in range(len(rot)):
            for x in range(len(rot[y])):
                if rot[y][x] == 1:
                    if self.get_cell(x + START_X, y + START_Y) == 0:
                        self.set_cell(x + START_X, y + START_Y, 1)
                    else:
                        """ Ha már nem tudja bemásolni az aktív betűt, akkor vége a játéknak. """
                        self.game_over = True

        self.next_letter = letters.choose_random_letter()

    def settle_letter(self):
        """ A betűk megállapodásáért felelős metódus. """
        global current_x, current_y
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) == 1:
                    self.set_cell(x, y, self.active_letter["settled_letter"])
        current_x = START_X
        current_y = START_Y
        self.active_letter = self.next_letter
        self.letter_rotation = 1
        self.copy_letter_to_grid()

    def draw_all(self):
        """ A egész rácsot megrajzolja. Így az ablak (window) on_draw metódusában csak ezt a metódust kell meghívni. """
        self.draw_grid_lines()
        self.draw_shapes()
        self.draw_next_letter()

    def draw_next_letter(self):
        """ Megrajzolja az ablak jobb középső oldalán a következő betűt. """
        for y in range(len(self.next_letter[1])):
            for x in range(len(self.next_letter[1][y])):
                if self.next_letter[1][y][x] == 1:
                    square_x = x * 64 + 32 + 800
                    square_y = (960 - 512) - y * 64 + 32
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, self.next_letter["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)

    def draw_shapes(self):
        """ Itt rajzoljuk meg a falakat, valamint a betűket avagy a Tetronimo-kat. """
        # arcade.draw_rectangle_filled(0+32, (960 - 64) - 0 * 64 + 32, 64, 64, arcade.color.WHITE)
        # arcade.draw_rectangle_filled(0+32, (960 - 64) - 1 * 64 + 32, 64, 64, arcade.color.WHITE)
        # arcade.draw_rectangle_filled(0+32, (960 - 64) - 2 * 64 + 32, 64, 64, arcade.color.WHITE)
        for y in range(self.height):
            for x in range(self.width):
                square_x = x * 64 + 32
                square_y = (960 - 64) - y * 64 + 32
                if self.get_cell(x, y) == 8:  # Walls - Falak
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, arcade.color.WHITE)
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 1:  # Active letters - Aktív betűk
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, self.active_letter["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)

                # megálpodott betűk
                elif self.get_cell(x, y) == 11:  # settled T
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_T["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 12:  # settled I
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_I["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 13:  # settled O
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_O["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 14:  # settled Z
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_Z["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 15:  # settled S
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_S["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 16:  # settled L
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_L["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)
                elif self.get_cell(x, y) == 17:  # settled J
                    arcade.draw_rectangle_filled(square_x, square_y, 64, 64, letters.letter_J["color"])
                    arcade.draw_rectangle_outline(square_x, square_y, 64, 64, arcade.color.AMAZON, border_width=2)

    def draw_grid_lines(self):
        """ Megrajzolja a Rács (Grid) vonalakat. """
        # Vertikális vonalak
        for x in range(self.width):
            arcade.draw_lines([[x * 64, 0], [x * 64, 960]], self.line_color, 1)
        # Horizontális vonalak
        for y in range(self.height):
            arcade.draw_lines([[0, y * 64], [768, y * 64]], self.line_color, 1)

    def get_cell(self, x, y):
        """ Visszadja az x, y pozícióban levő cella értékét. """
        return self.main_grid[y][x]

    def set_cell(self, x, y, value):
        """ A megadott x, y pozícióban beállítja egy cella értékét. """
        self.main_grid[y][x] = value

    def create(self):
        """ Létrehozza a Rács (Grid) struktúrát, mint 2 dimenziós python listát. """
        grid = []
        for y in range(self.height):
            grid.append([])
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == self.height - 1:
                    grid[y].append(8)
                else:
                    grid[y].append(0)
        return grid


# Arra az esetre ha ezt a python fájlt (grid.py) közvetlenül akarjuk futtatni.
if __name__ == "__main__":
    from pprint import pprint
    g = Grid()
    pprint(g.main_grid)
