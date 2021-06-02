from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongGame(Widget):
    ball = ObjectProperty(None)
    player_1 = ObjectProperty(None)
    player_2 = ObjectProperty(None)

    def place_players(self):
        self.player_1.center = self.center
        self.player_2.center = self.center
        self.player_2.orientation_x = -1

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(-45, 45))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:  # Left side, player 1
            self.player_1.center_y = touch.y
        if touch.x > self.width - self.width / 3:  # Right side, player 2
            self.player_2.center_y = touch.y

    def collision_handler(self):

        wall_collision_conditions = {  # Booleans
            'top': (self.ball.top > self.height) and (self.ball.velocity_y > 0),
            'bottom': (self.ball.y < 0) and (self.ball.velocity_y < 0),
            'right': (self.ball.right > self.width) and (self.ball.velocity_x > 0),
            'left': (self.ball.x < 0) and (self.ball.velocity_x < 0)
        }

        # Check and (if True) perform wall collisions
        if True in wall_collision_conditions.values():
            self.ball.collide_wall(wall_collision_conditions)

        # Check and (if True) perform paddle collisions
        else:  # Prevents double collision bugs
            self.ball.collide_paddle(self.player_1)
            self.ball.collide_paddle(self.player_2)

    def update(self, dt):
        self.ball.move()
        self.collision_handler()


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def teleport(self, new_pos, shift):
        pass

    def bounce_from_surface(self, surface_direction):
        # Bounces if moving opposite of intended bounce direction.
        if self.velocity_x * surface_direction[0] < 0:
            self.velocity_x *= -1
        if self.velocity_y * surface_direction[1] < 0:
            self.velocity_y *= -1

    def collide_wall(self, wall_collisions):
        wall_orientation = [0, 0]  # Enforces general direction after collision. [x, y]
        # Example directions: [1, 1] is positive x and y -> right and up.
        # [1, 1] is positive x and y -> right and up.
        # [0, -1] is zero x and negative y -> continue previous left/right, but move down.
        if wall_collisions['left']:
            wall_orientation[0] = 1  # Bounce to the right
        if wall_collisions['right']:
            wall_orientation[0] = -1  # Bounce to the left
        if wall_collisions['bottom']:
            wall_orientation[1] = 1  # Bounce up
        if wall_collisions['top']:
            wall_orientation[1] = -1  # Bounce down
        self.bounce_from_surface(wall_orientation)

    def collide_paddle(self, paddle):
        if self.collide_widget(paddle):

            # Give points to player for hitting the ball
            if self.velocity_x * paddle.orientation_x < 0:  # Prevents double counting a hit
                paddle.score += 1
            elif self.velocity_y * paddle.orientation_y < 0:  # For (hypothetical) top/bottom paddle
                paddle.score += 1

            # Speed up for each strike
            added_speed = 0.4  # 10% of starting speed (4.0 pixels per update)
            added_vector = Vector(self.velocity).normalize() * added_speed  # Aligns added speed to direction of travel
            self.velocity_x += added_vector.x
            self.velocity_y += added_vector.y

            # Bounce
            self.bounce_from_surface(paddle.orientation)

            # Deflect depending on where on the paddle it lands
            # pseudocode: deflection (counter-clockwise) proportional to f(h, o) = h/o, where:
            # h = height of impact from center of paddle
            # o = outgoing angle before deflection (also counter-clockwise)


class PongPaddle(Widget):
    # Orientation of the paddle. [1, 1] means right and up diagonally, [-1, 0] means left only.
    # Right side paddle is oriented to the left. [1, 0] (rightwards) orientation is default.
    orientation_x = NumericProperty(1)
    orientation_y = NumericProperty(0)
    orientation = ReferenceListProperty(orientation_x, orientation_y)

    score = NumericProperty(0)


class PongApp(App):
    def build(self):
        game = PongGame()

        game.place_players()
        game.serve_ball()

        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
