import pygame
import math



pygame.init()

WIDTH, HEIGHT = 800,700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Orbit Sim')


#colors
WHITE =  (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BROWN = (92,64,51)
ORANGE = (255,165,0)
BLUE = (0,0,255)
GREEN = (124,252,0)
RED = (136,8,8)
BRIGHT_RED = (238,75,43)

#text setup
Font = pygame.font.SysFont('comicsans', 12)
Font8 = pygame.font.SysFont('comicsans', 10)
text_distance = Font.render('In Kilometers', False, (BRIGHT_RED))
text_sun = Font.render('Sun', False, (BRIGHT_RED))
text_mercury = Font.render('Mercury', False, (BRIGHT_RED))
text_venus = Font.render('Venus', False, (BRIGHT_RED))
text_earth = Font.render('Earth', False, (BRIGHT_RED))
text_mars = Font.render('Mars', False, (BRIGHT_RED))
text_na = Font.render('N/A', False, (BRIGHT_RED))
text_sec = Font.render('1 Second', False, (BRIGHT_RED))
text_hour = Font.render('1 Hour', False, (BRIGHT_RED))
text_day = Font.render('1 Day', False, (BRIGHT_RED))

#time set rects
second_rect = pygame.Rect(100, 600, 200, 50)
hour_rect = pygame.Rect(300, 600, 200, 50)
day_rect = pygame.Rect(500, 600, 200, 50)


class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 120 / AU  # 1AU = 100 pixels

	global TIMESTEP
	TIMESTEP = 3600


	
	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0
		

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y =  self.y * self.SCALE + HEIGHT / 2 

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))
	
				

			

			pygame.draw.lines(win, WHITE, False, updated_points, 2)

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y


	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy 

		self.x_vel += total_fx / self.mass * TIMESTEP
		self.y_vel += total_fy / self.mass * TIMESTEP

		self.x += self.x_vel * TIMESTEP
		self.y += 200 + self.y_vel * TIMESTEP
		self.orbit.append((self.x, self.y))


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet(0, 0, 20, YELLOW, 1.98892 * 10**30)
	sun.sun = True

	earth = Planet(-1 * Planet.AU, 0, 11, BLUE, 5.9742 * 10**24)
	earth.y_vel = 29.783 * 1000 

	mars = Planet(-1.524 * Planet.AU, 0, 8, RED, 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000

	mercury = Planet(0.387 * Planet.AU, 0, 5, BROWN, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000

	venus = Planet(0.723 * Planet.AU, 0, 9, GREEN, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000
	

	planets = [sun, earth, mars, mercury, venus]

	while run:
		clock.tick(10)
		WIN.fill((0, 0, 0))
		mercury_venus_to_x = mercury.x - venus.x
		mercury_venus_to_y = mercury.y - venus.y
		mercury_venus_delta = math.sqrt(mercury_venus_to_x ** 2 + mercury_venus_to_y ** 2)

		mercury_earth_to_x = mercury.x - earth.x
		mercury_earth_to_y = mercury.y - earth.y
		mercury_earth_delta = math.sqrt(mercury_earth_to_x ** 2 + mercury_earth_to_y ** 2)

		mercury_mars_to_x = mercury.x - mars.x
		mercury_mars_to_y = mercury.y - mars.y
		mercury_mars_delta = math.sqrt(mercury_mars_to_x ** 2 + mercury_mars_to_y ** 2)

		venus_earth_to_x = venus.x - earth.x
		venus_earth_to_y = venus.y - earth.y
		venus_earth_delta = math.sqrt(venus_earth_to_x ** 2 + venus_earth_to_y ** 2)

		venus_mars_to_x = venus.x - mars.x
		venus_mars_to_y = venus.y - mars.y
		venus_mars_delta = math.sqrt(venus_mars_to_x ** 2 + venus_mars_to_y ** 2)
	
		earth_mars_to_x = earth.x - mars.x
		earth_mars_to_y = earth.y - mars.y
		earth_mars_delta = math.sqrt(earth_mars_to_x ** 2 + earth_mars_to_y ** 2)


		text_mercury_venus = Font8.render(f'{mercury_venus_delta}', False, (BRIGHT_RED))
		text_mercury_earth = Font8.render(f'{mercury_earth_delta}', False, (BRIGHT_RED))
		text_mercury_mars = Font8.render(f'{mercury_mars_delta}', False, (BRIGHT_RED))
		text_venus_earth = Font8.render(f'{venus_earth_delta}', False, (BRIGHT_RED))
		text_venus_mars = Font8.render(f'{venus_mars_delta}', False, (BRIGHT_RED))
		text_earth_mars = Font8.render(f'{earth_mars_delta}', False, (BRIGHT_RED))
		text_sun_mercury = Font8.render(f'{mercury.distance_to_sun}', False, (BRIGHT_RED))
		text_sun_venus = Font8.render(f'{venus.distance_to_sun}', False, (BRIGHT_RED))
		text_sun_earth = Font8.render(f'{earth.distance_to_sun}', False, (BRIGHT_RED))
		text_sun_mars = Font8.render(f'{mars.distance_to_sun}', False, (BRIGHT_RED))

		#box creation

 # x lines
		pygame.draw.line(WIN, BRIGHT_RED, (0,5), (725,5))
		pygame.draw.line(WIN, BRIGHT_RED, (0,30), (725,30))
		pygame.draw.line(WIN, BRIGHT_RED, (0,55), (725,55))
		pygame.draw.line(WIN, BRIGHT_RED, (0,80), (725,80))
		pygame.draw.line(WIN, BRIGHT_RED, (0,105), (725,105))
		pygame.draw.line(WIN, BRIGHT_RED, (0,130), (725,130))
		pygame.draw.line(WIN, BRIGHT_RED, (0,155), (725,155))

		# y lines
		pygame.draw.line(WIN, BRIGHT_RED, (100,5), (100,155))
		pygame.draw.line(WIN, BRIGHT_RED, (225,5), (225,155))
		pygame.draw.line(WIN, BRIGHT_RED, (350,5), (350,155))
		pygame.draw.line(WIN, BRIGHT_RED, (475,5), (475,155))
		pygame.draw.line(WIN, BRIGHT_RED, (600,5), (600,155))
		pygame.draw.line(WIN, BRIGHT_RED, (725,5), (725,155))

		# distance to Texts
		WIN.blit(text_distance, (10, 8))
		WIN.blit(text_sun, (37, 33))
		WIN.blit(text_mercury, (25, 58))
		WIN.blit(text_venus, (33, 83))
		WIN.blit(text_earth, (33, 108))
		WIN.blit(text_mars, (33, 133))	
		WIN.blit(text_sun, (150, 8))
		WIN.blit(text_mercury, (263, 8))
		WIN.blit(text_venus, (395, 8))
		WIN.blit(text_earth, (520, 8))
		WIN.blit(text_mars, (650, 8))
		WIN.blit(text_sun_mercury, (240, 37))
		WIN.blit(text_sun_venus, (365, 37))
		WIN.blit(text_sun_earth, (490, 37))
		WIN.blit(text_sun_mars, (610, 37))
		WIN.blit(text_na, (145, 33))
		WIN.blit(text_na, (275, 58))
		WIN.blit(text_na, (398, 83))
		WIN.blit(text_na, (525, 108))
		WIN.blit(text_na, (655, 133))
		WIN.blit(text_earth_mars, (615, 111))
		WIN.blit(text_earth_mars, (490, 136))
		WIN.blit(text_mercury_venus, (240, 86))
		WIN.blit(text_mercury_venus, (365, 61))
		WIN.blit(text_mercury_mars, (240, 136))
		WIN.blit(text_mercury_mars, (610, 61))
		WIN.blit(text_mercury_earth, (240, 111))
		WIN.blit(text_mercury_earth, (490, 61))
		WIN.blit(text_venus_earth, (490, 86))
		WIN.blit(text_venus_earth, (365, 111))
		WIN.blit(text_venus_mars, (615, 86))
		WIN.blit(text_venus_mars, (365, 136))
		WIN.blit(text_sun_mercury, (115, 60))
		WIN.blit(text_sun_venus, (115, 85))
		WIN.blit(text_sun_earth, (115, 110))
		WIN.blit(text_sun_mars, (114, 135))
		
		#time commands
		WIN.blit(text_sec, (180, 617))
		WIN.blit(text_hour, (380, 617))
		WIN.blit(text_day, (590, 617))
	
		
		 # x2 lines
		pygame.draw.line(WIN, BRIGHT_RED, (100,600), (700,600))
		pygame.draw.line(WIN, BRIGHT_RED, (100,650), (700,650))


		# y2 lines
		pygame.draw.line(WIN, BRIGHT_RED, (100,600), (100,650))
		pygame.draw.line(WIN, BRIGHT_RED, (300,600), (300,650))
		pygame.draw.line(WIN, BRIGHT_RED, (500,600), (500,650))
		pygame.draw.line(WIN, BRIGHT_RED, (700,600), (700,650))

		#time set
		global TIMESTEP
		if pygame.mouse.get_pressed()[0] == 1:
			pos = pygame.mouse.get_pos()
			print('clicked')
			if second_rect.collidepoint(pos):
				TIMESTEP = 1
			if hour_rect.collidepoint(pos):
				TIMESTEP = 3600
			if day_rect.collidepoint(pos):
				TIMESTEP = 3600 * 24

	

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			#update and draw planets and orbital trail

		for planet in planets:

			planet.update_position(planets)
			planet.draw(WIN)
			
	

		
		





			
		
    
		pygame.display.update()
		

	pygame.quit()


main()