import turtle
import time
import random
import math
import sys

width = 1000
height = 600
points = 0
gas = 250
gas_limit = 500
max_dist = math.sqrt((width/2 * width/2) + (height/2 * height/2))
max_garbage = 7
size = 5
k = 25
garbage_arr = []
filename = 'nian.gif'
dist_sun = 0

screen = turtle.Screen()
screen.title('VALHALLA: SPACE JUNK ELIMINATION GAME')
screen.bgcolor('black')
screen.setup(width=width, height=height)
screen.tracer(0)
screen.register_shape(filename)

#PLANETA
planet = turtle.Turtle()
planet.speed(0)
planet.shape('circle')
planet.penup()
planet.shapesize(stretch_wid=size, stretch_len=size)
planet.color('blue')
planet.goto(0,0)

#SOL
sun = turtle.Turtle()
sun.speed(0)
sun.shape('circle')
sun.penup()
sun.shapesize(stretch_wid=9, stretch_len=9)
sun.color('orange')
sun.goto(width/2 - 70, height/2 - 70)

#SCORE
score = turtle.Turtle()
score.speed(0)
score.shape('square')
score.color('white')
score.penup()
score.hideturtle()
score.goto(-width/2+5,height/2 - 75)
marcador = "Debris Collection: {} \nEnergy: {}".format(points, gas)
score.write(marcador, font=('Courier', 15, 'bold'))

#PLAYER
ship = turtle.Turtle()
ship.speed(0)
ship.penup()
ship.shape(filename)
ship.goto(-width/2 + 50,0)
ship.accel = 2
ship.step = 20
ship.d = 1000

#Asteroide 0
asteroid0 = turtle.Turtle()
asteroid0.speed(0)
asteroid0.penup()
asteroid0.shape('circle')
asteroid0.color('crimson')
asteroid0.r = 110
asteroid0.x = asteroid0.r
asteroid0.y = 0
asteroid0.goto(asteroid0.x,asteroid0.y)
asteroid0.vel = -1
asteroid0.delta = 5

#Asteroide 1
asteroid1 = turtle.Turtle()
asteroid1.speed(0)
asteroid1.penup()
asteroid1.shape('circle')
asteroid1.color('medium purple')
asteroid1.r = 165
asteroid1.x = -asteroid1.r
asteroid1.y = 0
asteroid1.goto(asteroid1.x,asteroid1.y)
asteroid1.vel = 1
asteroid1.delta = 10

#Asteroide 2
asteroid2 = turtle.Turtle()
asteroid2.speed(0)
asteroid2.penup()
asteroid2.shape('circle')
asteroid2.color('teal')
asteroid2.r = 225
asteroid2.x = 0
asteroid2.y = asteroid2.r
asteroid2.goto(asteroid2.x,asteroid2.y)
asteroid2.vel = 1
asteroid2.delta = 5


def create_garbage(x, y):
	if len(garbage_arr) < max_garbage:
		garbage = turtle.Turtle()
		garbage.speed(0)
		garbage.penup()
		garbage.shape('square')
		garbage.color('gray')
		garbage.goto(x+50,y)
		garbage_arr.append(garbage)


def gravity():
	dist_x = planet.xcor() - ship.xcor() 
	dist_y = planet.ycor() - ship.ycor()
	x_dir = 1
	y_dir = 1
	if dist_x < 0:
		x_dir = -1
	if dist_y < 0:
		y_dir = -1
	d = math.sqrt(dist_x*dist_x + dist_y*dist_y)
	ship.d = d
	force = k*size/d
	ship.accel += force 
	ship.setpos(ship.xcor()+ ship.accel*x_dir, ship.ycor()+ ship.accel*y_dir)

def check_garbage(arr):
	global points
	for garbage in arr:
		if ship.xcor() > garbage.xcor()-15 and ship.xcor() < garbage.xcor()+15:
			if ship.ycor() > garbage.ycor()-15 and ship.ycor() < garbage.ycor()+15:
				#collide and erase!
				garbage.hideturtle()
				arr.remove(garbage)
				points += 1

def move_trash(arr):
	for item in arr:
		item.setpos(item.xcor()+random.randrange(-25,25), item.ycor()+random.randrange(-25,25))

def move_asteroids(asteroid):
	asteroid.x = asteroid.x + asteroid.vel*asteroid.delta
	rad2 = asteroid.r * asteroid.r
	asteroid.y = asteroid.vel * math.sqrt(rad2 - (asteroid.x*asteroid.x))
	if asteroid.x == asteroid.r or asteroid.x == -asteroid.r:
		asteroid.vel = asteroid.vel * -1
	asteroid.setpos(asteroid.x, asteroid.y)

def up():
	global gas
	if gas > 0:
		ship.accel = 1
		ship.sety(ship.ycor()+ship.step)
		gas -= 1

def down():
	global gas
	if gas > 0:
		ship.accel = 1
		ship.sety(ship.ycor()-ship.step)
		gas -= 1

def right():
	global gas
	if gas > 0:
		ship.accel = 1
		ship.setx(ship.xcor()+ship.step)
		gas -= 1

def left():
	global gas
	if gas > 0:
		ship.accel = 1
		ship.setx(ship.xcor()-ship.step)
		gas -= 1

def gameover():
	score.clear()
	score.goto(100-width/4,0)
	score.write("GAME OVER", font=('Courier', 40, 'bold'))
	time.sleep(2)
	sys.exit()


screen.listen()
screen.onkeypress(up, 'Up')
screen.onkeypress(down, 'Down')
screen.onkeypress(right, 'Right')
screen.onkeypress(left, 'Left')

while True:
	move_asteroids(asteroid0)
	move_asteroids(asteroid1)
	move_asteroids(asteroid2)
	#Colisiones con los asteroides
	if ship.xcor() > asteroid1.xcor()-5 and ship.xcor() < asteroid1.xcor()+5:
		if ship.ycor() > asteroid1.ycor()-5 and ship.ycor() < asteroid1.ycor()+5:
			#choco con asteroide1
			gameover()
	if ship.xcor() > asteroid2.xcor()-5 and ship.xcor() < asteroid2.xcor()+5:
		if ship.ycor() > asteroid2.ycor()-5 and ship.ycor() < asteroid2.ycor()+5:
			#choco con asteroide2
			gameover()
	if ship.xcor() > asteroid0.xcor()-5 and ship.xcor() < asteroid0.xcor()+5:
		if ship.ycor() > asteroid0.ycor()-5 and ship.ycor() < asteroid0.ycor()+5:
			#choco con asteroide0
			gameover()

	#Colision con el planeta
	if ship.d < 50 : #choco
		gameover()

	x = random.randint(0,width/2)
	y = random.randint(0,height/2)
	prob = random.randint(0,100)
	if prob > 85: #agregar una basura espacial
		create_garbage(x, y)
	elif prob > 70:
		create_garbage(-x,y)
	elif prob > 50:
		create_garbage(x,-y)
	elif prob > 35:
		create_garbage(-x,-y)

	move_trash(garbage_arr)

	#solar panel
	if (ship.xcor()>sun.xcor()-100 and ship.xcor()<sun.xcor()+100) and (ship.ycor()>sun.ycor()-100 and ship.ycor()<sun.ycor()+100):
		if gas < gas_limit:
			gas += 5

	#collect garbage
	check_garbage(garbage_arr)

	dist_sun = math.ceil(math.sqrt((sun.xcor()-ship.xcor())**2 + (sun.ycor()-ship.ycor())**2)/ship.step)-5

	gravity()
	score.clear()
	marcador = "Debris Collection: {} \nEnergy: {} \nTrip to Sun: {}".format(points, gas, dist_sun)
	score.write(marcador, font=('Courier', 15, 'bold'))
	time.sleep(0.08)
	screen.update()
