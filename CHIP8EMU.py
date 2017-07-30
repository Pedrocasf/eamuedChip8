import pygame
import sys
import random
import numpy as np
import time
pygame.init()
class cpu():
	key={0  :pygame.K_1,
		 1  :pygame.K_2,
		 2	:pygame.K_3,
		 3  :pygame.K_4,
		 4	:pygame.K_q,
		 5	:pygame.K_w,
		 6	:pygame.K_e,
		 7	:pygame.K_r,
		 8	:pygame.K_a,
		 9	:pygame.K_s,
		 10	:pygame.K_d,
		 11	:pygame.K_f,
		 12	:pygame.K_z,
		 13	:pygame.K_x,
		 14	:pygame.K_c,
		 15	:pygame.K_v,}
	screen = pygame.display.set_mode((640,320)) 
	memory = [0]*4096
	surface_array = [0]*32*64
	surface_array = np.asarray(surface_array,dtype=int).reshape(32,64)
	i = 0
	V =[0]*16
	st = 0
	dt = 0
	VI = 0
	pc = 0x200
	stack = [0] *16
	sp = 0
	x = 0
	y = 0
	opcode = 0
	fontset =[
		0xF0, 0x90, 0x90, 0x90, 0xF0,
		0x20, 0x60, 0x20, 0x20, 0x70,
		0xF0, 0x10, 0xF0, 0x80, 0xF0,
		0xF0, 0x10, 0xF0, 0x10, 0xF0,
		0x90, 0x90, 0xF0, 0x10, 0x10,	
		0xF0, 0x80, 0xF0, 0x10, 0xF0,
		0xF0, 0x80, 0xF0, 0x90, 0xF0,
		0xF0, 0x10, 0x20, 0x40, 0x40,
		0xF0, 0x90, 0xF0, 0x90, 0xF0,
		0xF0, 0x90, 0xF0, 0x10, 0xF0,
		0xF0, 0x90, 0xF0, 0x90, 0x90,
		0xE0, 0x90, 0xE0, 0x90, 0xE0,
		0xF0, 0x80, 0x80, 0x80, 0xF0,
		0xE0, 0x90, 0x90, 0x90, 0xE0,
		0xF0, 0x80, 0xF0, 0x80, 0xF0,
		0xF0, 0x80, 0xF0, 0x80, 0x80]
	while i < len (fontset):
		memory[i] = fontset[i]
		i += 1
	
	with open('games/'+"BRIX","rb") as f:
		i = 0
		rom = f.read()
		
		while i < len (rom) : 
			memory[i+pc] = rom[i]
			i += 1
		
		i = 0
		while i < len (memory): 
			memory[i] = hex(memory[i])
			memory[i] = int(memory[i], 16) 
			i += 1
			
	while True:
		opcode = int(hex(memory[pc]<<8),16)| int(hex(memory[pc + 1]),16)
		opcode = hex(opcode)
		opcode = str(opcode)
		print(pc)
		print(opcode)
		
		if opcode[:3] == "0x0":
			pc +=2
			
		elif opcode[:3] == "0x1":
			pc = int(opcode [3:],16) 
			
		elif opcode [:3] == "0x2":
			sp +=1
			stack [sp] = pc
			pc = int(opcode[3:],16)
			
		elif opcode[:3] == "0x3":
			
			x = int(opcode[3],16)
			if int(hex(V[x])[2:],16) == int(str(opcode [4:]),16):
				pc +=  2
			pc +=2	
		
		elif opcode[:3] == "0x4":
			x = int(opcode[3],16)
			if int(hex(V[x])[2:],16) != int(str(opcode [4:]),16):
				pc += 2
			pc +=2
			
		elif opcode[:3] == "0x5":
			x = int(opcode[3],16)
			y = int(opcode[4],16)
			if V[x] == V[y]:
				pc += 2
			pc +=2
			
		elif opcode [:3] == "0x6":
			x = int(opcode[3],16)
			V[x] = int(opcode[4:],16)
			pc +=2
			
		elif opcode[:3] == "0x7":
			x = int(opcode [3],16)
			V[x] = V[x] + int(opcode [4:],16)
			pc +=2
			
		elif opcode[:3] == "0x8":
			
			if opcode [5] == "0":
				x = int(opcode[3],16)
				y = int(opcode [4],16)
				V[x] = V[y]
				pc +=2
			
			elif opcode [5] == "1":
				x = int(opcode[3],16)
				y = int (opcode[4],16)
				V[x] = V[x] | V[y]
				pc +=2
				
			elif opcode [5] == "2":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				V[x] = V[x] & V[y]
				pc +=2
				
			elif opcode [5] == "3":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				V[x] = V[x] ^ V[y]
				pc +=2
				
			elif opcode [5] == "4":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				V[x] = V[x] + V[y]
				if V[x] > 255:
					V[0xf] = 1
					V[x] = int(bin(V[x])[-4:])
				pc +=2
				
			elif opcode [5] == "5":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				if V[x] > V[y] :
					V[0xf] = 1
				else:
					V[0xf] = 0
				V[x] = V[x] - V[y]
				pc +=2
				
			elif opcode [5] == "6":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				if bin(V[x])[-0:] == 1:
					V[0xf] = 1
				else :
					V[0xf] = 0
				V[x] = V[x]//2
				pc +=2
				
			elif opcode [5] == "7":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				if V[y] > V[x] :
					V[0xf] = 1
				else:
					V[0xf] = 0
				V[x] = V[y] - V[x]
				pc +=2
				
			elif opcode [5] == "e":
				x = int(opcode[3],16)
				y = int(opcode[4],16)
				if bin(V[x])[0:] == 1:
					V[0xf] = 1
				else :
					V[0xf] = 0
				V[x] = V[x]*2
				pc +=2
				
		elif opcode[:3] == "0x9":
			x = int(opcode[3],16)
			y = int(opcode[4],16)
			if V[x] != V[y]:
				pc += 2
			pc +=2
		
		elif opcode[:3] == "0xa":
			VI = int(opcode[3:],16)
			pc +=2
	
		elif opcode[:3] == "0xb":
			pc = int(opcode[3:],16)+V[0]
	
		elif opcode[:3] == "0xc":
			x = int(opcode[3],16)
			V[x] =  random.randint(0,255) & int(opcode[4:],16)
			pc +=2
		
		elif opcode[:3] == "0xd":
			n = int(opcode[5],16)
			x = int (opcode[3],16)
			y = int(opcode[4],16)
			saved_x = V[x]
			saved_y = V[y]
			V[0xf] = 0
			saved_pc = pc
			pc = VI
			saved_VI = VI
			sprite_buffer = []
			es = []
			if V[x] > 63:
				V[x] = V[x] % 63 
			if V[y] > 31:
				V[y] = V[y] % 31
			while pc < saved_VI + n :
				VI = memory[pc]
				es = list(bin(VI)[2:].zfill(8))	
				pc +=1
				sprite_buffer.extend(es)
			sprite_buffer = np.asarray(sprite_buffer,dtype=int).reshape(n,8)
			sprite_buffer = sprite_buffer * 255
			width = 0
			
			while width !=7:
				height = 0
				if V[x] + width > 63:
					V[x] = (V[x]+width) % 63
				if V[y] + height >  31:
					V[y] = (V[y]+height) % 31
				while height != n:
					surface_array[V[y]+height,V[x]+width] = surface_array[V[y]+height,V[x]+width] ^ sprite_buffer[height,width] 
					if surface_array[V[y]+height,V[x]+width] != 0 & sprite_buffer[height,width] != 0:
						V[0xf]= 1
						print (V[0xf])
					height += 1
				width += 1
				
			surface = pygame.pixelcopy.make_surface(surface_array)
			surface = pygame.transform.scale(surface,(320,640))
			surface = pygame.transform.rotate(surface,90)
			surface = pygame.transform.flip(surface,False,True)
			screen.blit(surface,(0,0))
			pygame.display.update()
			VI = saved_VI 	
			pc = saved_pc +2
			V[x] = saved_x
			V[y] = saved_y

		elif opcode[:3] == "0xe":
			
			if opcode == "0xee":
				pc = stack[sp]
				sp -= 1 
				
			
			elif opcode == "0xe0":
				surface_array = [0]*32*64
				surface_array = np.asarray(surface_array,dtype=int).reshape(32,64)
				pc +=2
			
			elif opcode [4:] == "9e":
				x = int(opcode[3],16) 
				if key[V[x]] == True:
					pc += 2
				pc +=2	
				
			elif opcode [4:] == "a1":
				x = int(opcode[3],16)
				if key[V[x]] == False:
					pc += 2
				pc +=2
				
		elif opcode[:3] == "0xf":
			
			if opcode[4:] == "07":
				x = int(opcode[3],16)
				V[x] = dt
				pc +=2
				
			elif opcode[4:] == "0a":
				x = int(opcode[3],16)
				while pygame.key.get_pressed(keys) == False:
					pass
				pc +=2
				
			elif opcode[4:] == "15":
				x = int(opcode[3],16)
				dt = V[x]
				pc +=2
				
			elif opcode[4:] == "18":
				x = int(opcode[3],16)
				st = V[x]
				pc +=2
				
			elif opcode[4:] == "1e":
				x = int(opcode[3],16)
				VI = VI + V[x]
				pc +=2
				
			elif opcode[4:] == "29":
				x = int(opcode[3],16)
				VI = V[x] *5
				pc +=2
				
			elif opcode[4:] == "33":
				x = int(opcode[3],16)
				V[x] = str(V[x])
				memory[VI] = int(V[x][0])
				if len (V[x]) >= 2: 
					memory[VI+1] = int(V[x][1])
				if len (V[x]) >= 3:
					memory[VI+2] = int(V[x][2])
				V[x] = int(V[x]) 
				pc +=2
				
			elif opcode[4:] == "55":
				x = int(opcode[3],16)
				i = 0
				while i < x:
					memory[VI+i] = V[i]
					i += 1
				pc +=2
				
			elif opcode[4:] == "65":
				x = int(opcode[3],16)
				i = 0
				while i < x:
					V[i] = memory[VI+i]
					i += 1
				pc +=2
		
		if dt > 0 :
			time.sleep(0.16)	
			dt -= 1
		if st > 0 :
			time.sleep(0.16)	
			st -= 1		
