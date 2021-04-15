import pygame,random,sys

pygame.init()

class Win:
	def __init__(self):
		self.w,self.h=800,600
		self.screen=pygame.display.set_mode([self.w,self.h])
		pygame.display.set_caption("Game of Life by John Conway")
		self.clock=pygame.time.Clock()
		self.done=False
		self.pause=False
		self.credit=False

class Square:
	def __init__(self):
		self.size=10
		self.list=[]
		self.list2=[]
		self.neighbours=0
		self.delay=10
		self.generation=0
		self.colour=(255,255,255)

	def create(self,x,y):
		self.list.append((x*10,y*10,self.size,self.size))

	def remove(self,x,y):
		self.list.remove((x*10,y*10,self.size,self.size))
	

class Mouse:
	def __init__(self):
		self.left_pressed=False
		self.cursor_string=[]
		self.multiplier=0

	'''for i in range(300):
		create(random.randint(0,w/10),random.randint(0,h/10))'''

	def update_cursor(self,square):
		self.cursor_string=[]
		lines=square.size
		self.multiplier=1
		while lines%8!=0:
			if lines>=8*self.multiplier and lines<8*(self.multiplier+1):
				lines=8*self.multiplier
			else:
				self.multiplier+=1
		print(lines)
		for y in range(lines):
			current_line=""
			for x in range(lines):
				if y<=square.size-1:
					if y==0 or y==square.size-1:
						current_line+="w"
					else:
						if x>0 and x<lines-1:
							current_line+="o"
						else:
							current_line+="w"
				else:
					current_line+=" "
			self.cursor_string.append(current_line)
		cursor = pygame.cursors.compile(self.cursor_string, black='b', white='w', xor='o')
		pygame.mouse.set_cursor((lines, lines), (int(square.size/2), int(square.size/2)), *cursor)



def main():
	win=Win()
	square=Square()
	mouse=Mouse()



	mouse.update_cursor(square)

	bg_colour=(0,0,0)
	grid_colour=(30,30,30)
	text_colour=(255,255,255)

	font,font2 = pygame.font.Font("data/app850.fon", 60),pygame.font.Font("data/app850.fon", 40)

	while not win.done:	

		for e in pygame.event.get():
			if e.type==pygame.QUIT:
				win.done=True

			if e.type==pygame.KEYDOWN:
				if e.key==pygame.K_SPACE:
					if not win.pause:
						win.pause=True
					else:
						win.pause=False

				if e.key==pygame.K_ESCAPE:
					win=Win()
					square=Square()
					mouse=Mouse()


				if e.key==pygame.K_TAB:
					win.credit=True

				if e.key==pygame.K_1 or e.key==pygame.K_KP1:
					if bg_colour==(0,0,0):
						bg_colour,grid_colour,square.colour,text_colour=(255,255,255),(225,225,255),(0,0,0),(0,0,0)
					else:
						bg_colour,grid_colour,square.colour,text_colour=(0,0,0),(30,30,30),(255,255,255),(255,255,255)

			if e.type==pygame.KEYUP:
				if e.key==pygame.K_TAB:
					win.credit=False


		square.list2=square.list.copy()

		if pygame.mouse.get_pressed()[0] and not mouse.left_pressed:
			mouse_x,mouse_y=pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
			if (int((mouse_x/square.size))*square.size,int((mouse_y/square.size))*square.size,square.size,square.size) in square.list2:
				square.remove(int(mouse_x/square.size),int(mouse_y/square.size))
			else:
				square.create(int(mouse_x/square.size),int(mouse_y/square.size))
			mouse.left_pressed=True
		if not pygame.mouse.get_pressed()[0]:
			mouse.left_pressed=False


		if square.delay<=0 and not win.pause:
			#print(len(square.list))

			for x in range(int(win.w/square.size)):
				for y in range(int(win.h/square.size)):
					change_grid_x=[-1,1,0,0,-1,1,-1,1]
					change_grid_y=[0,0,-1,1,-1,-1,1,1]

					for l in range(len(change_grid_x)):
						pos=((x+change_grid_x[l])*square.size,(y+change_grid_y[l])*square.size,square.size,square.size)
						if pos in square.list2:
							square.neighbours+=1

					#print(square.neighbours)

					if (x*square.size,y*square.size,square.size,square.size) in square.list2:
						if square.neighbours!=2 and square.neighbours!=3:
							square.remove(x,y)

					else:
						if square.neighbours==3:
							square.create(x,y)

					square.neighbours=0

			square.delay=10
			square.generation+=1

		else:
			square.delay-=10

		#background
		win.screen.fill(bg_colour,(0,0,win.w,win.h))

		#text vars
		text_gen = font.render(str(square.generation), True, text_colour)
		text_pause = font.render("PAUSED", True, text_colour)
		text_credit = font2.render("Game imagined by: John Conway", True, text_colour)
		text_credit2 = font2.render("Developed by: SammygoodTunes, Warzou", True, text_colour)

		#grid
		for i in range(int(win.w/square.size)):
			pygame.draw.rect(win.screen, grid_colour, (i*square.size,0,1,win.h))
		for i in range(int(win.h/square.size)):
			pygame.draw.rect(win.screen, grid_colour, (0,i*square.size,win.w,1))

		#squares
		for i in range(len(square.list)):
			pygame.draw.rect(win.screen, square.colour, square.list[i])

		#text
		win.screen.blit(text_gen, (5, 7))
		if win.pause:
			win.screen.blit(text_pause, (win.w-100, 20))
		if win.credit:
			win.screen.blit(text_credit, (win.w/2-100, win.h-30))
			win.screen.blit(text_credit2, (win.w/2-125, win.h-15))

		pygame.display.flip()
		win.clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()
