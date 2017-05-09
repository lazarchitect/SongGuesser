import pygame
from backEnd import *
from random import choice

#############################
#VARIABLES
#############################

#RGB colors for pygame to read
BLACK = (0,0,0)
WHITE = (255,255, 255)
#BLUE =  (66, 134, 244) #It's like a nice relaxing blue.
RED = 	(230, 20, 20)

pi = 3.141592653578
start = pi/2

ticks = pygame.time.get_ticks #because I dont want to type all that

#self-explanatory
# PlayerOneScore = 0
# PlayerTwoScore = 0

screen_x = 1000
screen_y = 700

###########################
#CUSTOM CLASSES
###########################
class WhiteButton():
	def __init__(self, text, left, top, width, height):
		
		self.pr = pygame.Rect(left, top, width, height)
		self.left = left
		self.top = top
		self.width = width
		self.height = height

		pic = pygame.image.load("WhiteButton.png")
		pic = pygame.transform.scale(pic, (width, height))

		screen.blit(pic, (left, top))

		#lets say its X pixels wide. how many characters of a font of  given size can that hold?
		#If theres more, just truncate it with an ellipsis.
		self.text = text
		font = pygame.font.SysFont("trebuchetms", 36)
		self.pgtext = font.render(text, 1, BLACK)

		right = left + width
		center = (left + right)/2
		stringLen = len(text)
		pixelShift = stringLen*8

		screen.blit(self.pgtext, (center - pixelShift, top))
		pygame.display.update(self.pr)


class GreenButton():
	def __init__(self, text, left, top, width, height):
		
		self.pr = pygame.Rect(left, top, width, height)

		pic = pygame.image.load("GreenButton.png")
		pic = pygame.transform.scale(pic, (width, height))

		screen.blit(pic, (left, top))

		#lets say its X pixels wide. how many characters of a font of  given size can that hold?
		#If theres more, just truncate it with an ellipsis.
		self.text = text
		font = pygame.font.SysFont("trebuchetms", 36)
		self.pgtext = font.render(text, 1, BLACK)

		right = left + width
		center = (left + right)/2
		stringLen = len(text)
		pixelShift = stringLen*8

		screen.blit(self.pgtext, (center - pixelShift, top))
		pygame.display.update(self.pr)

class RedButton():
	def __init__(self, text, left, top, width, height):
		
		self.pr = pygame.Rect(left, top, width, height)

		pic = pygame.image.load("RedButton.png")
		pic = pygame.transform.scale(pic, (width, height))

		screen.blit(pic, (left, top))

		#lets say its X pixels wide. how many characters of a font of  given size can that hold?
		#If theres more, just truncate it with an ellipsis.
		self.text = text
		font = pygame.font.SysFont("trebuchetms", 36)
		self.pgtext = font.render(text, 1, BLACK)

		right = left + width
		center = (left + right)/2
		stringLen = len(text)
		pixelShift = stringLen*8

		screen.blit(self.pgtext, (center - pixelShift, top))
		pygame.display.update(self.pr)		

class GrayButton():
	def __init__(self, text, left, top, width, height):
		
		self.pr = pygame.Rect(left, top, width, height)

		pic = pygame.image.load("GrayButton.png")
		pic = pygame.transform.scale(pic, (width, height))

		screen.blit(pic, (left, top))

		#lets say its X pixels wide. how many characters of a font of  given size can that hold?
		#If theres more, just truncate it with an ellipsis.
		self.text = text
		font = pygame.font.SysFont("trebuchetms", 36)
		self.pgtext = font.render(text, 1, BLACK)

		right = left + width
		center = (left + right)/2
		stringLen = len(text)
		pixelShift = stringLen*8

		screen.blit(self.pgtext, (center - pixelShift, top))
		pygame.display.update(self.pr)		

############################
#FUNCTIONS
############################

#wait for the given number of seconds. Can still quit.
def customSleep(sec):
	start_time = ticks()
	while(1):
		if(ticks() - start_time > sec*1000):
			return
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4):
				deleteFiles()
				exit()

#If the user wants to quit, let em.
def quitCheck():
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4):
			return True
	return False		
 
def deleteFiles():
	import os
	for x in os.listdir("Songs"):
		try:
			os.remove("Songs/"+x) #This causes an error if pygame played the song in question last. Solution unknown.
		except PermissionError:
			pass #Just leave the file. its ok.
	for x in os.listdir("Pics"):
		try:
			os.remove("Pics/"+x) 
		except PermissionError:
			pass #Don't think this will ever happen but better safe than sorry

def reveal(theyWereRight, currentPlayer, timeLeft, ButtonClicked, CorrectButton):
	#global PlayerOneScore, PlayerTwoScore
	answer = pygame.Rect(200, 600, 1000, 50)
	

	if theyWereRight:
		GreenButton(ButtonClicked.text, ButtonClicked.left, ButtonClicked.top, ButtonClicked.width, ButtonClicked.height)
	else:
		RedButton(ButtonClicked.text, ButtonClicked.left, ButtonClicked.top, ButtonClicked.width, ButtonClicked.height)
		GreenButton(CorrectButton.text, CorrectButton.left, CorrectButton.top, CorrectButton.width, CorrectButton.height)

	pygame.display.update()		

	points = timeLeft*10
	if theyWereRight == False:
		points = -(10 - timeLeft) * 10

	# if currentPlayer == 1:
	# 	PlayerOneScore += points
	# else:
	# 	PlayerTwoScore += points	

	pygame.mixer.stop()
	pygame.mixer.quit()
	customSleep(1)
	return points


#defines what happens for a song guess. (5 of these happen for each player each round, grand total of 30.)
def songGuess(playerNum, songNum, roundNum, points, otherPlayerScore, playerOneWins, playerTwoWins):

	while(1): #This loop simply gets a song. Not a game mechanic loop.
		try:
			index = random_index()
			jsonData = get_track_data(index)
			download_mp3(jsonData)
			break
		except TypeError: #if the song lacks an mp3 url
			pass
		except OSError: # if the song name has quotes in it...
			pass
		except ValueError: #if the song lacks a spotify link (I think)
			pass	
	song_name = jsonData["name"]
	song_ID = jsonData["id"]
	artist = jsonData["artists"][0]["name"]#[0]["name"] #come on spotify...
	artist_ID = jsonData["album"]["artists"][0]["id"]

	fakes = getOtherSongs(artist_ID, song_name)[:3]
	if len(fakes) < 3 or artist == "Kygo" or artist == "Auli'i Cravalho":
		return songGuess(playerNum, songNum, roundNum, points, otherPlayerScore, playerOneWins, playerTwoWins)
		 

	#Get Image of artist.
	verify = True
	try:
		download_pic(artist_ID)
	except IndexError:
		verify = False

	pic = None

	if verify == True:
		pic = pygame.image.load("Pics/"+artist+"Pic.png")
		pic = pygame.transform.scale(pic, (200, 200))

	while(1):
		screen.fill(WHITE)
		
		currentPlayer = font.render("Player "+str(playerNum)+"\'s Turn", 1, BLACK)
		screen.blit(currentPlayer, (1,1))
		currentScore = font.render("Your Score: "+str(points), 1, BLACK)
		screen.blit(currentScore, (1, 50))

		if playerNum == 2:
			enemyScore = font.render("Player 1's Score: "+str(otherPlayerScore), 1, RED)
			screen.blit(enemyScore, (1, 100))

		roundWins = font.render("Round Wins", 1, BLACK)
		p1w = font.render("Player 1: "+str(playerOneWins), 1, BLACK)
		p2w = font.render("Player 2: "+str(playerTwoWins), 1, BLACK)

		screen.blit(roundWins, (750, 1))
		screen.blit(p1w, (750, 50))
		screen.blit(p2w, (750, 100))

		artist_text = font.render(artist, 1, BLACK)
		
		if roundNum == 0:
			screen.blit(artist_text, (500-len(artist)*10, 300))

		if pic != None and roundNum < 2:
			screen.blit(pic, (402, 100))

		

		button_texts = ["~~~", "~~~", "~~~", "~~~"] #THESE ARE SUBJECT TO CHANGE

		BUTTON_TEXT = ""

		if len(song_name)>40:
			button_texts[randint(0,3)] = song_name[0:38] + "..."
			BUTTON_TEXT = song_name[0:38] + "..."
		else:
			button_texts[randint(0,3)] = song_name
			BUTTON_TEXT = song_name

		for fake in fakes:
			index = randint(0,3)
			while button_texts[index] != "~~~":
				index = randint(0,3)
			if len(fake)>40:
				fake = fake[0:38] + "..."
			button_texts[index] = fake	

		left = 50
		top1 = 400
		top2 = 460
		top3 = 520
		top4 = 580
		width = 850
		height = 40

		Button_A = WhiteButton(button_texts[0], left, top1, width, height)
		Button_B = WhiteButton(button_texts[1], left, top2, width, height)
		Button_C = WhiteButton(button_texts[2], left, top3, width, height)
		Button_D = WhiteButton(button_texts[3], left, top4, width, height)

		CorrectButton = None
		for i in [Button_A, Button_B, Button_C, Button_D]:
			if i.text == BUTTON_TEXT:
				CorrectButton = i

		Button_Skip = WhiteButton("Skip", 375, 640, 100, 40)

		pygame.display.update() #THIS IS THE LINE THAT UPDATES ALL THE "SEMI PERMANENT" BLITTED ELEMENTS FOR EACH SONG. AKA EVERYTHING EXCEPT TIME LEFT

		pygame.mixer.init()
		pygame.mixer.music.load("Songs/"+song_name+".mp3")
		pygame.mixer.music.play()
		start_time = ticks()
		
		while(1):
		
			curr_time = ticks()

			timeUpdateRect = pygame.Rect(1, 150, 400, 50)#left, top, width, height
			timeLeft = 10-int((curr_time - start_time)/1000)
			timeLeftString = font.render("Time Left: "+str(timeLeft), 1, BLACK)
			screen.fill(WHITE, timeUpdateRect)
			screen.blit(timeLeftString, (1, 150))
			pygame.display.update(timeUpdateRect)
		
			arcRect = pygame.Rect(1, 200, 200, 200)
			pygame.draw.rect(screen, WHITE, arcRect, 0) #this could be the problem
			pic = pygame.image.load("stopwatch.png")
			pic = pygame.transform.scale(pic, (200, 200))
			screen.blit(pic, (1, 200))
			# pygame.draw.circle(screen, BLACK, (101, 300), 100, 100)	
			pygame.draw.arc(screen, WHITE, arcRect, start, start + (start*(curr_time-start_time)/2500), 100)
			pygame.display.update(arcRect)

			if curr_time - start_time >= 10040:
				pygame.mixer.stop()
				pygame.mixer.quit()
				#THEY RAN OUT OF TIME!
				notif = font.render("You ran out of time!", 1, BLACK)
				screen.fill(WHITE, timeUpdateRect)
				screen.blit(notif, (1, 150))
				GreenButton(CorrectButton.text, CorrectButton.left, CorrectButton.top, CorrectButton.width, CorrectButton.height)
				pygame.display.update(timeUpdateRect)
				customSleep(1)
				return -30

			for event in pygame.event.get():
				
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4):
					deleteFiles()
					exit()

				if pygame.mouse.get_pressed()[0]:
					location = pygame.mouse.get_pos()
					#location is a tuple with X,Y integer coords

					if(50<=location[0]<=900 and 400<=location[1]<=440):
						return reveal(Button_A.text == BUTTON_TEXT, playerNum, timeLeft, Button_A, CorrectButton)

					elif(50<=location[0]<=900 and 460<=location[1]<=500):
						return reveal(Button_B.text == BUTTON_TEXT, playerNum, timeLeft, Button_B, CorrectButton)	

					elif(50<=location[0]<=900 and 520<=location[1]<=560):
						return reveal(Button_C.text == BUTTON_TEXT, playerNum, timeLeft, Button_C, CorrectButton)	

					elif(50<=location[0]<=900 and 580<=location[1]<=620):
						return reveal(Button_D.text == BUTTON_TEXT, playerNum, timeLeft, Button_D, CorrectButton)

					elif(375<=location[0]<=475 and 640<=location[1]<=680):
						#Skip button.
						GrayButton(Button_Skip.text, Button_Skip.left, Button_Skip.top, Button_Skip.width, Button_Skip.height)
						GreenButton(CorrectButton.text, CorrectButton.left, CorrectButton.top, CorrectButton.width, CorrectButton.height)
						pygame.display.update()
						pygame.mixer.stop()
						pygame.mixer.quit()
						customSleep(1)	
						return -10
		return 0
		

#This function occurs for a player's turn, AKA their 5 songs in a given round.
def playerTurn(playerNum, roundNum, otherPlayerScore, playerOneWins, playerTwoWins):
	
	screen.fill(WHITE)

	hereWeGo = font.render("", 1, BLACK)

	if playerNum == 2:
		hereWeGo = font.render("Player 1\'s score: "+str(otherPlayerScore), 1, BLACK)
		screen.blit(hereWeGo, (300, 350))

	getReady = font.render("Player "+str(playerNum)+", Get Ready.", 1, BLACK)
	screen.blit(getReady, (300, 300))
	pygame.display.update()
	customSleep(3)

	screen.fill(WHITE)
	pygame.display.update()

	points = 0

	for songNum in range(5):
		points += songGuess(playerNum, songNum, roundNum, points, otherPlayerScore, playerOneWins, playerTwoWins)

	return points

######################################################
#STUFF THAT ACTUALLY HAPPENS
######################################################

pygame.init()
font = pygame.font.SysFont("trebuchetms", 40)

screen = pygame.display.set_mode((screen_x, screen_y))
# pygame.display.set_caption("What's That Song?", "None") #ignore that second thing
screen.fill(WHITE)

playerOneWins = 0
playerTwoWins = 0

for rounds in range(3):
	PlayerOnePoints = playerTurn(1, rounds, -34, playerOneWins, playerTwoWins) 
	#PLAYER ONE'S POINTS MATTER AT NO POINT DURING THE GAME. 
	#IF THE NUMBER -34 SHOWS UP ANYWHERE... THATS BAD MMKAY
	PlayerTwoPoints = playerTurn(2, rounds, PlayerOnePoints, playerOneWins, playerTwoWins)

	if PlayerOnePoints > PlayerTwoPoints:
		playerOneWins+=1
		screen.fill(WHITE)
		screen.blit(font.render("Player One wins the round!", 1, BLACK), (300,300))
		pygame.display.update()
		customSleep(3)
		screen.fill(WHITE)
		pygame.display.update()

	elif PlayerTwoPoints > PlayerOnePoints:
		playerTwoWins+=1
		screen.fill(WHITE)
		screen.blit(font.render("Player Two wins the round!", 1, BLACK), (300,300))
		pygame.display.update()
		customSleep(3)
		screen.fill(WHITE)
		pygame.display.update()

	else: #a tie		
		pass #idk what to do here

	if (playerOneWins == 2 and playerTwoWins == 0) or (playerTwoWins == 2 and playerOneWins == 0):
		break 	

#The game has ended. display the results.
screen.fill(WHITE)
WhiteButton("Quit", 360, 360, 100, 40)

if(playerTwoWins == playerOneWins):
	final = font.render("It's a tie!", 1, BLACK)
	screen.blit(final, (300,300))

else:	
	WhoWon = "One" if playerOneWins>playerTwoWins else "Two"
	final = font.render("Player " + WhoWon +" Wins!", 1, BLACK)
	screen.blit(final, (300,300))

pygame.display.update()

while(1):
	if pygame.mouse.get_pressed()[0]:
		location = pygame.mouse.get_pos()
		if(360<=location[0]<=460 and 360<=location[1]<=400):
			exit()

	if quitCheck():
		deleteFiles()
		exit()
