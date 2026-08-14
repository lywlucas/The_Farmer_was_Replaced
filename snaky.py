import move
import Maze
global snaky_size
global snaky_hoping
snaky_size=32
snaky_hoping=1

def LtoH(x,y):
	n=get_world_size()
	if x==0:
		return n-y
	elif y%2==0:
		return n+(n-1)*y+x
	else:
		return n+(n-1)*y+n-x

def snaky(size=16,hoping=2*10**7):
	clear()
	set_world_size(size)
	move.leftdown_position=[0,0]
	move.rightup_position=[size-1,size-1]
	now_bones=num_items(Items.Bone)
	while True:
		change_hat(Hats.Dinosaur_Hat)
		cnt=0
		while True:
			next_x,next_y=measure()
			cnt+=1
			next_id=LtoH(next_x,next_y)
			if cnt>=size**2:
				break
			while True:
				x,y=get_pos_x(),get_pos_y()
				id=LtoH(x,y)
				if id==next_id:
					break
				if cnt>=(size**2)//2:
					if cnt>=size**2-1:
						break
				elif cnt<id<next_id:
					if x==next_x and x!=0:
						for _ in range(next_y-y):
							move.mmove(North)
						continue 
					elif id<size and y<=next_y and y%2==0:
						for _ in range(next_x):
							move.mmove(East)
						continue
					elif x>next_x and y!=next_y and y%2==0:
						move.mmove(North)
					elif x<next_x and y!=next_y and y%2==1:
						move.mmove(North)
				elif id<=cnt:
					if not move.move_in_order(True):
						break
					else:
						continue
				elif id>next_id and y!=size-1:
					move.mmove(North)
					continue
				if not move.move_in_order(True):
					break
		change_hat(Hats.Straw_Hat)
		if num_items(Items.Bone)>now_bones+hoping:
			return True

def main():
	global snaky_size
	global snaky_hoping
	if snaky_size!=0 and snaky_hoping!=0:
		snaky(snaky_size,snaky_hoping)
	else:
		snaky()

if __name__=="__main__":
	main()
	