# Single-player Pong

Hobby project built on Python 3.9.5 and Kivy 2.0.0, the only intended use is learning to use Kivy and to play with vector math.

Coolest feature is how the ball bounce direction from the paddle changes with where it strikes on the paddle. The intuitive approach of adding/subtracting degrees depending on the strike location works when the ball approaches close to head on, but breaks down at sharper angles. Instead, a hidden paddle surface is created, rotated slightly towards the strike location, and the ball bounces on this surface. Bounce direction therefore work as if the paddle was concave, bounces appear 'natural' and cannot do weird things like reflecting through the paddle. 
