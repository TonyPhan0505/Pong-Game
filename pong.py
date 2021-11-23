import pygame

# define function "main" where a screen is created and the Game class is called.
def main():

	pygame.init()
	screen = pygame.display.set_mode((600,500))  # Create screen of width 600 and height 500
	pygame.display.set_caption("Pong")  # The screen window's title is set to "Pong"

	game = Game(screen)
	game.play()  # Call method play in the Game class to initiate the game.
	pygame.quit()

class Game:
	# Initialize essential objects of the game
	def __init__(self, screen):

		self.screen = screen
		self.continue_game = True
		self.bg_color = pygame.Color("black")
		self.game_clock = pygame.time.Clock()  # Initiate a clock in the game to count how much time has passed.
		self.FPS = 40  # Set the number of frames to pass in a second.
		self.close_clicked = False
		self.width = 600
		self.height = 500

		self.left_paddle_pos = [95, 250]
		self.left_paddle = Paddle(self.left_paddle_pos, self.screen)
		self.q_pressed = False  # Initialize an indicator to indicate whether the key "q" is pressed or not. Initially, it's False.
		self.a_pressed = False  # Initalize an indicator to indicate whether the key "a" is pressed ot not. Initially, it's False.
		self.left_score = 0  # The initial score of the left player is 0
		self.right_paddle_pos = [500, 250]
		self.right_paddle = Paddle(self.right_paddle_pos, self.screen)

		# Initialize the indicators to indicate whether the keys "p" and "l" are pressed
		self.p_pressed = False
		self.l_pressed = False

		self.right_score = 0  # The inital score of the right player is also 0

		self.ball = ball(self.screen, self.left_paddle_pos, self.right_paddle_pos)  # Create the pong ball using the ball class

	def handle_events(self):
		for event in pygame.event.get():  # Get all events inputted in the game

			if event.type == pygame.QUIT:  # If the player indicates they want to close the game window by hitting the X icon.
				self.close_clicked = True

			# IF a key on the keyboard is noticed to be pressed, set it's indicator to True
			elif event.type == pygame.KEYDOWN:

				if event.key == pygame.K_q:
					self.q_pressed = True  
				if event.key == pygame.K_a:
					self.a_pressed = True
				if event.key == pygame.K_p:
					self.p_pressed = True
				if event.key == pygame.K_l:
					self.l_pressed = True	
			
			# If a key on the keyboard is noticed to be released from pressing, set the corresponding indicator to False
			elif event.type == pygame.KEYUP:

				if event.key == pygame.K_q:
					self.q_pressed = False
				if event.key == pygame.K_a:
					self.a_pressed = False
				if event.key == pygame.K_p:
					self.p_pressed = False
				if event.key == pygame.K_l:
					self.l_pressed = False	
	
	# define method update to to set when to move what object
	def update(self):
		# If no winner has been found (no player has obtained 11 scores), keep the ball moving
		if self.left_score < 11 and self.right_score < 11:	
			self.ball.move()

		# If the indicator of the key "q" is True, move the left paddle up as long as it hasn't collided with the top edge of the screen window.
			if self.q_pressed and (self.left_paddle_pos[1] - 10 >= 0):
				self.left_paddle.move_up()

			# If the indicator of the key "a" is True, move the left paddle down as long as it hasn't collided with the bottom edge of the screen window.
			elif self.a_pressed and (self.left_paddle_pos[1] + 60 <= self.height):
				self.left_paddle.move_down()
		
			# If the indicator of the key "p" is True, move the right paddle up as long as it hasn't collided with the top edge of the screen window.
			if self.p_pressed and (self.right_paddle_pos[1] - 10 >= 0):
				self.right_paddle.move_up()
		
			# If the indicator of the key "l" is True, move the right paddle down as long as it hasn't collided with the bottom edge of the screen window.
			elif self.l_pressed and (self.right_paddle_pos[1] + 60 <= self.height):
				self.right_paddle.move_down()

	# Define method show_score to display text that tells the scores of the players onto the screen.
	def show_score(self):
		
		# If the ball collides with the wall behind the left player, the right player gets a point
		if self.ball.collide_with_left_edge():
			self.right_score += 1

		# If the ball collides with the wall behind the right player, the left player gets a point
		if self.ball.collide_with_right_edge():
			self.left_score += 1

		# Set color and font to the text
		text_color = pygame.Color("WHITE")
		text_font = pygame.font.SysFont("Times New Roman", 30, bold = True, italic = False)
		
		# Render and display the text of the score of the left player
		left_score_string = str(self.left_score)
		left_text_image = text_font.render(left_score_string, True, text_color)
		left_score_pos = (20, 10)
		self.screen.blit(left_text_image, left_score_pos)

		# Render and display the text of the score of the right player
		right_score_string = str(self.right_score)
		right_text_image = text_font.render(right_score_string, True, text_color)
		right_score_pos = (560,10)
		self.screen.blit(right_text_image, right_score_pos)

	# Define method draw to display all objects onto the screen
	def draw(self):
		
		self.screen.fill(self.bg_color)  # Remove the traces of the ball after it moves to new coordinates on the screen
		self.left_paddle.draw()
		self.right_paddle.draw()
		self.ball.draw()
		self.show_score()
		pygame.display.flip()  # Show all objects onto the screen

	# Define method play to set when to execute what during the game
	def play(self):
		# As long as the human player hasn't clicked the X icon to close the screen window
		while not self.close_clicked:
			self.handle_events()
			if self.continue_game:  # Only if the conditions in the method decide_continue below are not satisfied
				self.draw()
				self.update()
				self.decide_continue()
			self.game_clock.tick(self.FPS)  # Set 30 frames to pass a second

	# Define method decide_continue to set the conditions by which the game must come to an end
	def decide_continue(self):
		# If a player is found to have obtained 11 scores
		if self.left_score == 11 or self.right_score == 11:
			self.continue_game = False

class Paddle:
	
	# Initialize essential properties to create a rectangular paddle
	def __init__(self, pos, screen):
		self.screen = screen
		self.pos = pos
		self.width = 10
		self.height = 50
		self.color = pygame.Color("white")

	def move_up(self):
		self.pos[1] -= 10  # Each time it moves up, it moves up the screen by 10 units

	def move_down(self):
		self.pos[1] += 10 # Each time it moves down, it moves down the screen by 10 units

	# define function draw to render a rectangle display it onto the screen
	def draw(self):
		self.shape = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
		pygame.draw.rect(self.screen, self.color, self.shape)

class ball:
	
	# Initialize essential properties to create a movable circular ball
	def __init__(self, screen, left_paddle_pos, right_paddle_pos):
		self.screen = screen
		self.color = "blue"
		self.radius = 15
		self.pos = [300, 250]
		self.velocity = [9,6]
		self.left_paddle_pos = left_paddle_pos
		self.right_paddle_pos = right_paddle_pos
		self.width = 600
		self.height = 500

	def collide_with_left_edge(self):

		# If the center of the ball is not at least it's radius away from the left edge of the screen, it means the very left point of the ball has passed over
		# left edge of the screen.
		if self.pos[0] <= self.radius:
			return True
		return False

	def collide_with_right_edge(self):

		# If the center of the ball is not at least it's radius away from the right edge of the screen, it means the very right point of the ball has passed over
		# the right edge of the screen.
		if self.pos[0] + self.radius >= self.width:
			return True
		return False

	def collide_with_top_edge(self):

		# If the center of the ball is not at least it's radius away from the top edge of the screen, it means the very top point of the ball has passed over
		# the top edge of the screen.
		if self.pos[1] < self.radius:
			return True
		return False

	def collide_with_bottom_edge(self):

		# If the center of the ball is not at least it's radius away from the bottom edge of the screen, it means the very bottom point of the ball has passed over
		# the bottom edge of the screen
		if self.pos[1] + self.radius > self.height:
			return True
		return False

	def collide_with_left_paddle(self):

		# If the very left point of the ball touches or passes over the right edge of the left paddle, the ball is on the left of the left paddle and the ball is within the vertical range of the paddle:
		if (self.pos[0] - self.radius <= self.left_paddle_pos[0] + 5) and (self.velocity[0]<0) and (self.pos[1] - self.radius <= self.left_paddle_pos[1] + 25) and (self.pos[1] + self.radius >= self.left_paddle_pos[1] - 25):
			return True
		return False	

	def collide_with_right_paddle(self):

		# If the very right point of the ball touches or passes over the left edge of the right paddle, the ball is on the right of the right paddle and the ball is wihtin the vertical range of the right paddle
		if (self.pos[0] + self.radius >= self.right_paddle_pos[0] - 5) and (self.velocity[0]>0) and (self.pos[1] - self.radius <= self.right_paddle_pos[1] + 25) and (self.pos[1] + self.radius >= self.right_paddle_pos[1] - 25):
			return True
		return False

	def move(self):

		# If the ball touches or passes over the left edge of the screen or the right edge of the left paddle, make the ball move right
		if self.collide_with_left_edge() or self.collide_with_left_paddle():
			self.velocity[0] = -self.velocity[0]

		# If the ball touches or passes over the top edge of the screen, make the ball move down
		elif self.collide_with_top_edge():
			self.velocity[1] = -self.velocity[1]

		# If the ball touches or passes over the right edge of the screen or the left edge of the right paddle, make the ball move left
		elif self.collide_with_right_edge() or self.collide_with_right_paddle():
			self.velocity[0] = - self.velocity[0]

		# If the ball touches or passes over the bottom edge of the screen, make the ball move up
		elif self.collide_with_bottom_edge():

			self.velocity[1] = -self.velocity[1]

		# Update the x and y coordinates of the ball to place it on a new position on the screen
		for index in range(0,2):
			self.pos[index] += self.velocity[index]

	# define method draw to display the ball onto the screen
	def draw(self):

		pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

# Call the main function to call the Game class and the play method in it to start the game.
main()