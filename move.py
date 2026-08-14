leftdown_position=[0,21]
rightup_position=[31,31]

def mmove(dir):
	if move(dir)==False:
		return False
	else:
		return True
		
		
def move_in_order(breaking=False):
	x_0,y_0=leftdown_position[0],leftdown_position[1]
	x_1,y_1=rightup_position[0],rightup_position[1]
	x, y=get_pos_x(), get_pos_y()
	if x<x_0 or x>x_1 or y<y_0 or y>y_1:
		change_hat(Hats.Green_Hat)
		quick_goto(x_0,y_0)
	if x==x_0:
		if y==y_0:
			if not mmove(East): 
				if breaking:
					return False
		else:
			if not mmove(South):
				if breaking:
					return False 
	elif (y-y_0)%2==0:
		if x==x_1:
			if y==y_1:
				quick_goto(x_0,y_1)
			else:
				if not mmove(North):
					if breaking:
						return False
		else:
			if not mmove(East):
				if breaking:
					return False
	elif x==x_0+1 and y!=y_1:
		if not mmove(North):
			if breaking:
				return False
	else:
		if not mmove(West):
			if breaking:
				return False
	return True

def move_in_order2():
	r=get_world_size()
	x, y=get_pos_x(), get_pos_y()
	if y%2==0:
		if x==0:
			move(South)
		else:
			move(West)
	elif x==r-1:
		move(South)
	else:
		move(East)

def quick_goto(x,y):
	a, b =get_pos_x(), get_pos_y()
	n_0=get_world_size()
	n=n_0//2
	if not 0<=x<n_0 or not 0<=y<n_0:
		print("ERROR")
		return False
	while True:
		dir=None
		a, b =get_pos_x(), get_pos_y()
		if a==x and b==y:
			return True
		if 0<x-a<=n or -n_0<x-a<-n:
			dir=East
		elif -n<=x-a<0 or n<x-a<n_0:
			dir=West
		elif 0<y-b<=n or -n_0<y-b<-n:
			dir=North
		elif -n<=y-b<0 or n<y-b<n_0:
			dir=South
		move(dir)
	return False

def straightmove_upright(x,y):
	a, b =get_pos_x(), get_pos_y()
	