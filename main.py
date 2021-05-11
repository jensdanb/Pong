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

    def update(self, dt):
        self.ball.move()

        # Ball-Wall collision
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # Ball-Paddle collision
        self.player_1.bounce_ball(self.ball)
        self.player_2.bounce_ball(self.ball)


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos

    def teleport(self, new_pos, shift):
        pass


class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            added_speed = 0.4   # Pixels per update. 10% of starting speed
            added_vector = list(Vector(vx, vy).normalize() * added_speed)
            ball.velocity_x += added_vector[0]
            ball.velocity_y += added_vector[1]

            ball.velocity_x *= -1


class PongApp(App):
    def build(self):
        game = PongGame()
        game.place_players()

        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
