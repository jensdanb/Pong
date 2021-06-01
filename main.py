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

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(-45, 45))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:  # Left side, player 1
            self.player_1.center_y = touch.y
        if touch.x > self.width - self.width / 3:  # Right side, player 2
            self.player_2.center_y = touch.y

    def check_collisions(self):
        new_direction = [0, 0]  # Enforces general direction after collision. [x, y]
        # Example directions: [1, 1] is positive x and y -> right and up.
        # [1, 1] is positive x and y -> right and up.
        # [0, -1] is zero x and negative y -> continue previous left/right, but move down.
        wall_collisions = {  # Booleans
            'top': (self.ball.top > self.height) and (self.ball.velocity_y > 0),
            'bottom': (self.ball.y < 0) and (self.ball.velocity_y < 0),
            'right': (self.ball.right > self.width) and (self.ball.velocity_x > 0),
            'left': (self.ball.x < 0) and (self.ball.velocity_x < 0)
        }

        if True in wall_collisions.values():
            if wall_collisions['left']:
                new_direction[0] = 1  # Bounce to the right
            if wall_collisions['right']:
                new_direction[0] = -1  # Bounce to the left
            if wall_collisions['bottom']:
                new_direction[1] = 1  # Bounce up
            if wall_collisions['top']:
                new_direction[1] = -1  # Bounce down

            self.ball.bounce_in_direction(new_direction)

        else:
            self.ball.bounce_on_paddle(self.player_1, [1, 0])
            self.ball.bounce_on_paddle(self.player_2, [-1, 0])

    def update(self, dt):
        self.ball.move()
        self.check_collisions()


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def teleport(self, new_pos, shift):
        pass

    def bounce_in_direction(self, bounce_direction):
        # Bounces if moving opposite of intended bounce direction.
        if self.velocity_x * bounce_direction[0] < 0:
            self.velocity_x *= -1
        if self.velocity_y * bounce_direction[1] < 0:
            self.velocity_y *= -1

    def bounce_on_paddle(self, paddle, bounce_direction):
        if self.collide_widget(paddle):
            added_speed = 0.4   # Pixels per update. 10% of starting speed
            added_vector = Vector(self.velocity).normalize() * added_speed
            self.velocity_x += added_vector.x
            self.velocity_y += added_vector.y

            self.bounce_in_direction(bounce_direction)
            # self.velocity_x *= -1

            paddle.score += 1


class PongPaddle(Widget):
    bounce_direction = NumericProperty(1)

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
