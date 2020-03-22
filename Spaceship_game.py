from tkinter import *
from tkinter import messagebox
import time, random, sys

class Game:
	def __init__(self):
		self.tk = Tk()
		self.tk.title(__file__)
		self.canvas = Canvas(self.tk, width=500, height=500, bg="yellow")
		self.canvas.pack()
		for x in range(2):
			self.canvas.create_line([0,0,500,500] if x == 0 else [500,0,0,500])
		csx, csy, csx1, csy1 = 250-(100/2), 250-(100/2), 250+(100/2), 250+(100/2)
		self.canvas.create_rectangle(csx, csy, csx1, csy1, fill="lightblue")
		self.canvas.bind("<Motion>", self.motion)
		self.score = 0
		self.scoretext = self.canvas.create_text(10, 10, text="Score: {}".format(self.score), anchor="nw", font="Purisa 15 bold", fill="red")
		self.p_x, self.p_y = 0, 0
	def motion(self, e):
		self.p_x, self.p_y = e.x, e.y
	def mainloop(self):
		while True:
			w.draw()
			s.draw()
			self.canvas.tag_raise(self.scoretext)
			self.tk.update()
			time.sleep(0.01)
	def get_pointer_coord(self):
		return self.p_x, self.p_y
	def get_coord_area(self, cor, area):
		if area < 0 or area > 3:
			raise ValueError('Area value must be between 0 and 3  inclusive')
		sx, sy, sx1, sy1 = cor[0], cor[1], cor[2], cor[3]
		center = sx+((sx1-sx)/2), sy+((sy1-sy)/2)
		#print("Center:", center)

		pcoord = [[(sx+((sx1-sx)/2), sy),(sx1, sy),(sx1, sy1),(sx, sy1),(sx,sy+((sy1-sy)/2)),center],           #area1
							[(sx,sy),(sx+((sx1-sx)/2),sy),center,(sx1,sy+((sy1-sy)/2)),(sx1,sy1),(sx,sy1)],     #area2
							[(sx,sy),(sx1,sy),(sx1,sy+((sy1-sy)/2)),center,(sx+((sx1-sx)/2),sy1),(sx,sy1)],     #area3
							[(sx,sy),(sx1,sy),(sx1, sy1),(sx+((sx1-sx)/2), sy1),center,(sx,sy+((sy1-sy)/2))]    #area4
						]

		return pcoord[area]

class Wall:
	def __init__(self, game, x, y, runtime=2):
		self.runtime = runtime
		self.game = game
		w = 4
		self.x, self.y, self.x1, self.y1 = x-w, y-w, x+w, y+w
		self.correct = random.randint(0,3) #Options are from 0 to 3 inclusive
		self.id = self.game.canvas.create_polygon(self.game.get_coord_area([self.x, self.y, self.x1, self.y1], self.correct), fill="blue")
	def draw(self):
		if not self.x <= 8:
			self.x -= self.runtime
			self.y -= self.runtime
			self.x1 += self.runtime
			self.y1 += self.runtime
		else:
			area_s = self.s.check_area()
			if area_s != self.correct:
				messagebox.showerror("Game Over", "You touched the wall")
				sys.exit()
			self.x, self.y, self.x1, self.y1 = 245, 245, 255, 255
			self.game.score += 1
			self.game.canvas.itemconfig(self.game.scoretext, text="Score: {}".format(self.game.score))
			self.correct = random.randint(0,3)
		self.game.canvas.delete(self.id)
		self.id = self.game.canvas.create_polygon(self.game.get_coord_area([self.x, self.y, self.x1, self.y1], self.correct), fill="blue")
	def add_sp(self, s):
		self.s = s

class Spaceship:
	def __init__(self, game, x, y, x1, y1):
		self.game = game
		self.id = self.game.canvas.create_rectangle(x, y, x1, y1, fill="red")
	def check_area(self):
		p = self.game.canvas.coords(self.id)
		areas = [p[2] < 250 and p[3] < 250,
						p[0] > 250 and p[3] < 250,
						p[0] > 250 and p[1] > 250,
						p[0] < 250 and p[3] > 250
						]
		try:
			return areas.index(True)
		except:
			return areas.index(False)
	def goto(self, x, y):
		self.game.canvas.delete(self.id)
		self.id = self.game.canvas.create_rectangle(x-30, y-30, x+30, y+30, fill="red")
	def draw(self):
		px, py = self.game.get_pointer_coord()
		self.goto(px, py)

if __name__ == '__main__':
	g = Game()
	runtime = 5 #Yo can modify this line for a game more difficult
	w = Wall(g, 250, 250, runtime=runtime) #width = 5
	s = Spaceship(g, 10, 10, 60, 60) #width = 50
	w.add_sp(s)
	g.mainloop()
