reverse={East:West, West:East, North:South, South:North}
global snaky2_size
global snaky2_hoping
snaky2_size=32
snaky2_hoping=33480000

def LtoH(x,y):
	n=get_world_size()
	if x==0:
		return n-y
	elif y%2==0:
		return n+(n-1)*y+x
	else:
		return n+(n-1)*y+n-x
		
def is_in_area(location, area, upper=False, can_equal=True):
	size=get_world_size()
	main_area=((1,size-1),size-1, West, North)
	(x_n,y_n), width, dir, up = area
	x,y = location
	a, b= get_pos_x(), get_pos_y()
	if area==main_area:
		if upper==False:
			return x!=0
		else:
			return size< LtoH(a,b) <= LtoH(x,y)
	if upper==True:
		flg=False
		if is_in_area((a,b), area)==False:
			return False
		if up==East:
			if a>x:
				return False
			elif a==x:
				if can_equal==False:
					return False
				else:
					flg=True
		elif up==West:
			if a<x:
				return False
			elif a==x:
				if can_equal==False:
					return False
				else:
					flg=True
		elif up==North:
			if b>y:
				return False
			elif b==y:
				if can_equal==False:
					return False
				else:
					flg=True
		else:
			if b<y:
				return False
			elif b==y:
				if can_equal==False:
					return False
				else:
					flg=True
		
		if flg!=False:
			d=snaky_move(area, (a,b))
			if a>x:
				if d!=West:
					return False
			elif a<x:
				if d!=East:
					return False
			elif b>y:
				if d!=South:
					return False
			elif b<y:
				if d!=North:
					return False
		
	if dir==East:
		if x <= x_n-width or x > x_n:
			return False
	elif dir==West:
		if x<x_n or x>=x_n+width:
			return False
	elif dir==North:
		if y>y_n or y<=y_n-width:
			return False
	else:
		if y<y_n or y>=y_n+width:
			return False
	
	if up==North:
		if y>y_n:
			return False
	elif up==West:
		if x<x_n:
			return False
	elif up==South:
		if y<y_n:
			return False
	else:
		if x>x_n:
			return False	
	return True
			
def snaky_move(area, simulating=None):
	(x_n,y_n), width, dir, up = area
	if simulating==None:
		x, y = get_pos_x(), get_pos_y()
		if is_in_area((x,y),area)==False:
			return None
	else:
		x,y = simulating
	
	if dir==East or dir==West:
		up_dist=abs(y-y_n)
		hor_dist=abs(x-x_n)
	else:
		up_dist=abs(x-x_n)
		hor_dist=abs(y-y_n)

	new_dir=dir
	if up_dist%2==0:
		if hor_dist==0 and up_dist!=0:
			new_dir=up
		else:
			pass
	else:
		if hor_dist==width-1:
			new_dir=up
		else:
			new_dir=reverse[dir]
	if simulating==None:
		move(new_dir)
	return new_dir
		
def snaky_quick_move(target, area):
	a, b = target
	(x_n,y_n), width, dir, up = area
	break_point=None
	x, y = get_pos_x(), get_pos_y()
	if is_in_area((x,y), area)==False:
		return None
	if is_in_area(target, area, True, True)==False:
		snaky_quick_move((x_n,y_n), area)
		snaky_move(area)
		return None
	while True:
		x, y = get_pos_x(), get_pos_y()
		if x==a and y==b:
			if break_point==None:
				break_point=(a,b)
			return break_point
		if dir==East or dir==West:
			if x==a:
				break_point = (x,y)
				for _ in range(abs(y-b)):
					move(up)
				continue
			temp=snaky_move(area,(x,y))
			if temp==East:
				if x>a:
					move(up)
				else:
					for _ in range(a-x):
						move(East)
			elif temp==West:
				if x<a:
					move(up)
				else:
					for _ in range(x-a):
						move(West)
			else:
				move(temp)
		else:
			if y==b:
				break_point = (x,y)
				for _ in range(abs(x-a)):
					move(up)
				continue
			temp=snaky_move(area,(x,y))
			if temp==North:
				if y>b:
					move(up)
				else:
					for _ in range(b-y):
						move(North)
			elif temp==South:
				if y<b:
					move(up)
				else:
					for _ in range(y-b):
						move(South)
			else:
				move(temp)

def quick_getout(area):
	(x_n,y_n), width, dir, up = area
	x, y = get_pos_x(), get_pos_y()
	if is_in_area((x,y),area)==False:
		return True
	if up==North or up==South:
		if y!=y_n:
			move(up)
		for _ in range(abs(x-x_n)+1):
			move(dir)
	else:
		if x!=x_n:
			move(up)
		for _ in range(abs(y-y_n)+1):
			move(dir)

	
def eat_apple(target, area, cnt):
	(x_n,y_n), width, dir, up = area
	a, b = target
	x, y = get_pos_x(), get_pos_y()
	if is_in_area((x,y),area)==False:
		return (target, cnt)
	if a==0:
		snaky_quick_move((x_n, y_n), area)
		snaky_move(area)
		return (target, cnt)
	last_break=snaky_quick_move(target, area)
	if last_break==None:
		return (target, cnt)
	cnt+=1
	x, y = get_pos_x(), get_pos_y()
	x_b, y_b= last_break
	x_g, y_g= x, y
	x_f, y_f= x, y
	if up==North or up==South:
		warn=abs(y - y_n)
		n_width=abs(y - y_b)
		if dir==East:
			x_f = x_n - width + 1
			x_g = x_n
		else:
			x_f = x_n + width - 1
			x_g = x_n
	else:
		warn=abs(x-x_n)
		n_width=abs(x - x_b)
		if dir==North:
			y_f = y_n - width + 1
			y_g = y_n
		else:
			y_f = y_n + width - 1
			y_g = y_n
	
	w_g, w_f= n_width-1, n_width-1
	dir_b=snaky_move(area, (x_b,y_b))
	if dir_b==dir:
		w_g+=1
	elif dir_b==reverse[dir]:
		w_f+=1
	if cnt<=n_width*2:
		w_g, w_f= snaky2_size-2, snaky2_size-2
	
	area_ins=((x_g, y_g), n_width -1, up, dir)
	area_out=((x_f,y_f), n_width -1, up, reverse[dir])
	if x==a and y==b:
		newt = measure()
	else:
		return(target,cnt)
		
	if is_in_area(newt, area, True)==True:
		newt, cnt=eat_apple(newt, area, cnt)
	elif is_in_area(newt, area_ins, True, False)==True:
		move(dir)
		newt, cnt=eat_apple(newt, area_ins, cnt)
		newt, cnt=eat_apple(newt, area, cnt)
	elif warn!=0 and is_in_area(newt, area_out, True, False)==True:
		move(reverse[dir])
		newt, cnt=eat_apple(newt, area_out, cnt)
		newt, cnt=eat_apple(newt, area, cnt)

	if width<snaky2_size-1:
		quick_getout(area)
	elif cnt<=y*2+1:
		quick_getout(area)
	else:
		snaky_quick_move((x_n, y_n), area)
		snaky_move(area)
	
	return (newt, cnt)

def snaky2(size=32, hoping= 2*10**7):
	clear()
	set_world_size(size)
	A=size**2
	turn_point=A//2
	main_area=((1,size-1),size-1, West, North)
	#main_move=[[East]]
	#for _ in range(size-1):
	#	main_move[0].append(South)
	#for xi in range(1,size):
	#	main_move.append([])
	#	for yi in range(size):
	#		main_move[xi].append(snaky_move(main_area,(xi,yi)))
	main_move={}
	for xi in range(size):
		for yi in range(size):
			i=LtoH(xi,yi)
			if i<size:
				main_move[i]=South
			elif i==size:
				main_move[i]=East
			else:
				i=i%A
				main_move[i]=snaky_move(main_area,(xi,yi))
	while True:
		change_hat(Hats.Dinosaur_Hat)
		cnt=1
		next_x, next_y = measure()
		next_id=LtoH(next_x,next_y)
		while True:
			x, y= get_pos_x(), get_pos_y()
			id=LtoH(x,y)
			if id==next_id:
				cnt+=1
				next_x, next_y = measure()
				next_id=LtoH(next_x,next_y)
			if cnt>=turn_point:
				while True:
					id=id%A
					if move(main_move[id])==False:
						break
					id+=1
				break
			if id<cnt:
				if id<next_id<=cnt:
					l=next_id-id
					for _ in range(l):
						move(main_move[id])
						id+=1
					continue
				else:
					l=cnt-id
					for _ in range(l):
						move(main_move[id])
						id+=1
					continue
			elif x==0:
				move(main_move[id])
				continue
			else:
				next_target, new_cnt= eat_apple((next_x, next_y), main_area, cnt)
				next_x, next_y = next_target
				next_id=LtoH(next_x,next_y)
				cnt=new_cnt
		change_hat(Hats.Straw_Hat)
		return True
def main():
	if snaky2_size!=0 and snaky2_hoping!=0:
		snaky2(snaky2_size,snaky2_hoping)
	else:
		snaky2()

if __name__=="__main__":
	main()
	