import turtle
import time
import random
import math
import sys
from playsound import playsound

width = 1000
height = 600
points = 0
gas = 150
gas_limit = 500
max_dist = math.sqrt((width/2 * width/2) + (height/2 * height/2))
max_garbage = 15
size = 5
k = 35
garbage_arr = []
filename = 'tomar.gif'
file2 = 'earth.gif'
file3 = 'sun.gif'
file4 = 'sat1.gif'
dist_sun = 1000
tomar = False

screen = turtle.Screen()
screen.title('VALHALLA: SPACE JUNK ELIMINATION GAME')
screen.bgcolor('black')
screen.setup(width=width, height=height)
screen.tracer(0)
screen.register_shape(filename)
screen.register_shape(file2)
screen.register_shape(file3)
screen.register_shape(file4)
#PLANETA
planet = turtle.Turtle()
planet.speed(0)
planet.shape(file2)
planet.penup()
planet.goto(0,0)
#SOL
sun = turtle.Turtle()
sun.speed(0)
sun.shape(file3)
sun.penup()
sun.goto(width/2 - 50, height/2 - 50)
#SCORE [][][][][][][][][][][][][][][] 
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
#ship.shape('square')
ship.color('green')
ship.goto(-width/2 + 50,0)
ship.accel = 2
ship.step = 20
ship.d = 1000
ship.rot = 10
#Asteroide 0
asteroid0 = turtle.Turtle()
asteroid0.speed(0)
asteroid0.penup()
asteroid0.shape(file4)
asteroid0.r = 110
asteroid0.x = asteroid0.r
asteroid0.y = 0
asteroid0.goto(asteroid0.x,asteroid0.y)
asteroid0.vel = -1
asteroid0.delta = 10
#Asteroide 1
asteroid1 = turtle.Turtle()
asteroid1.speed(0)
asteroid1.penup()
asteroid1.shape(file4)
asteroid1.r = 165
asteroid1.x = -asteroid1.r
asteroid1.y = 0
asteroid1.goto(asteroid1.x,asteroid1.y)
asteroid1.vel = 1
asteroid1.delta = 5
#Asteroide 2
asteroid2 = turtle.Turtle()
asteroid2.speed(0)
asteroid2.penup()
asteroid2.shape(file4)
asteroid2.r = 225
asteroid2.x = 0
asteroid2.y = asteroid2.r
asteroid2.goto(asteroid2.x,asteroid2.y)
asteroid2.vel = 1
asteroid2.delta = 1

def create_garbage(x, y):
	if len(garbage_arr) < max_garbage:
		garbage = turtle.Turtle()
		garbage.speed(0)
		garbage.penup()
		garbage.shape('square')
		garbage.color('gray')
		garbage.goto(x,y)
		garbage.dx = random.randint(-10,10)
		garbage.dy = random.randint(-10,10)
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
	global max_garbage
	for garbage in arr:
		if ship.xcor() > garbage.xcor()-15 and ship.xcor() < garbage.xcor()+15:
			if ship.ycor() > garbage.ycor()-15 and ship.ycor() < garbage.ycor()+15:
				#collide and erase!
				garbage.hideturtle()
				arr.remove(garbage)
				points += 1
				if points % 5 == 0:
					max_garbage -= 1
					if max_garbage <= 3:
						win()
					arr[len(arr)-1].hideturtle()
					arr.pop()
					score.clear()
					score.goto(100-width/4,0)
					score.write("LEVEL {}".format(math.ceil(points/5)+1), font=('Courier', 42, 'bold'))
					playsound('bip2.wav')
					time.sleep(1.5)

def move_trash(arr):
	for item in arr:
		x = item.xcor()+item.dx
		y = item.ycor()+item.dy
		if (x<=-width/2+10 or x>=width/2-10):
			item.dx = item.dx*-1
		if (y<=-height/2+10 or y>=height/2-10):
			item.dy = item.dy*-1
		item.setpos(x, y)

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

def thrust():
	global gas
	if gas > 0:
		ship.accel = 1
		ship.forward(ship.step)
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

def gameover(v):
	score.clear()
	score.goto(50-width/3,-50)
	score.write("GAME OVER\n{}".format(v), font=('Courier', 50, 'bold'))
	time.sleep(3)
	sys.exit()

def rotR():
	angle = ship.heading()
	#print(angle)
	ship.ht()
	ship.setheading(angle+ship.rot)
	ship.st()

def rotL():
	angle = ship.heading()
	#print(angle)
	ship.ht()
	ship.setheading(angle-ship.rot)
	ship.st()

def win():
	score.clear()
	score.goto(25-width/3,height/4 - 250)
	score.write("The estimated population of\nparticles between 1 to 10 cm\nareapproximately 500,000\nNASA is very thankful\nfor your services!!!", font=('Courier', 30, 'bold'))
	playsound('win.wav')
	time.sleep(5)
	sys.exit()

def init():
	global tomar
	tomar = not tomar

screen.listen()
screen.onkeypress(up, 'Up')
screen.onkeypress(down, 'Down')
screen.onkeypress(right, 'Right')
screen.onkeypress(left, 'Left')
screen.onkeypress(init, 'space')
screen.onkeypress(rotR, "a")
screen.onkeypress(rotL, "d")
screen.onkeypress(thrust, "w")

while True:
	if tomar:
		move_asteroids(asteroid0)
		move_asteroids(asteroid1)
		move_asteroids(asteroid2)
		#Colisiones con los asteroides
		arr = ['Calipso', 'Cloudsat', 'Glory']
		num = random.randint(0,2)
		if ship.xcor() > asteroid1.xcor()-8 and ship.xcor() < asteroid1.xcor()+8:
			if ship.ycor() > asteroid1.ycor()-8 and ship.ycor() < asteroid1.ycor()+8:
				#choco con asteroide1
				gameover("You crashed with\n" + arr[num])
		if ship.xcor() > asteroid2.xcor()-8 and ship.xcor() < asteroid2.xcor()+8:
			if ship.ycor() > asteroid2.ycor()-8 and ship.ycor() < asteroid2.ycor()+8:
				#choco con asteroide2
				gameover("You crashed with\n" + arr[num])
		if ship.xcor() > asteroid0.xcor()-8 and ship.xcor() < asteroid0.xcor()+8:
			if ship.ycor() > asteroid0.ycor()-8 and ship.ycor() < asteroid0.ycor()+8:
				#choco con asteroide0
				gameover("You crashed with\n" + arr[num])
		#Colision con el planeta
		if ship.d < 85: #choco
			gameover("")
		x = random.randint(0,width/2 - 30)
		y = random.randint(0,height/2 -30)
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
		dist_sun = math.ceil(math.sqrt((sun.xcor()-ship.xcor())**2 + (sun.ycor()-ship.ycor())**2)/ship.step)-5
		#solar panel
		if dist_sun <= 2:
			gameover("")
		elif dist_sun <= 4:
			score.color('dark orange')
			if gas < gas_limit:
				gas += 3
		elif dist_sun <= 7:
			score.color('forest green')
			if gas < gas_limit:
				gas += 1
		elif gas < 50:
			score.color('red')
		else:
			score.color('white')
		#collect garbage
		check_garbage(garbage_arr)
		gas_to_rect = ""
		for x in range(0,gas,50):
			gas_to_rect = gas_to_rect + "[]"
		gravity()
		score.clear()
		score.goto(-width/2+5,height/2 - 75)
		marcador = "Debris Collection: {} \nEnergy: {} \nTrip to Sun: {}".format(points, gas_to_rect, dist_sun)
		score.write(marcador, font=('Courier', 15, 'bold'))
	else:
		score.clear()
		score.color('white')
		score.goto(25-width/3,0)
		score.write("The space need you!\nPress your SpaceBar", font=('Courier', 38, 'bold'))
	time.sleep(0.08)
	screen.update()
