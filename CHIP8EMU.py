import pygame
import sys
import random
import numpy as np
pygame.init()
class cpu():
	key_inputs = [0]*16
	screen = pygame.display.set_mode((640,320)) 
	memory = [0]*4096
	i = 0
	V =[0]*16
	sound_timer = 0
	delay_timer = 0
	VI = 0
	pc = 0x200 
	stack = [0] 
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
	
	with open('games/'+"PONG","rb") as f:
		i = 0
		rom = f.read()
		
		while i < len (rom) -1: 
			memory[i+pc] = rom[i]
			i += 1
		
		i = 0
		while i < len (memory): 
			memory[i] = hex(memory[i])
			memory[i] = int(memory[i], 16) 
			i += 1
	while pc < len(rom)+ 0x200:
		opcode = int(hex(memory[pc]<<8),16)| int(hex(memory[pc + 1]),16)
		opcode = hex(opcode)
		opcode = str(opcode)
		print (V)
		print(opcode)
		if opcode [:3] == "0x0":
			if opcode == "e00":
				screen.fill((0,0,0))
				pc += 2
			elif opcode == "0ee":
				sp -= 1 
				pc = stack[0]
				pc += 2
			
		elif opcode[:3] == "0x1":
			pc = opcode [3:] 
			pc = int(pc,16)
			pc += 2
			
		elif opcode [:3] == "0x2":
			stack[sp] = pc
			sp += 1
			pc = int(opcode[3:],16)
			
		elif opcode[:3] == "0x3":
			x = int(opcode[3],16)
			if int(hex(V[x])[2:],16) == int(str(opcode [4:]),16):
				pc += 4
			else :
				pc += 2
			
		elif opcode[:3] == "0x4":
			x = int(opcode[3],16)
			if int(hex(V[x])[2:],16) != int(str(opcode [4:]),16):
				pc += 2
			pc += 2
			
		elif opcode[:3] == "0x5":
			x = int(opcode[3],16)
			y = int(opcode[4],16)
			if V[x] == V[y]:
				pc += 2
			pc +=2
			
		elif opcode [:3] == "0x6":
			x = int(opcode[3],16)
			V[x] = int(opcode[4:],16)
			pc += 2
			
		elif opcode[:3] == "0x7":
			x = int(opcode [3],16)
			V[x] = V[x] + int(opcode [4:],16)
			pc += 2
			
		elif opcode[:3] == "0x8":
			
			if opcode [5] == "0":
				x = int(opcode[3],16)
				y = int(opcode [4],16)
				V[x] = V[y]
				pc += 2
			
			elif opcode [5] == "1":
				x = int(opcode[3],16)
				y = int (opcode[4],16)
				V[x] = V[x] | V[y]
				pc +=2
				
			elif opcode [5] == "2":
				pc +=2
				
			elif opcode [5] == "3":
				pc +=2
				
			elif opcode [5] == "4":
				pc +=2
				
			elif opcode [5] == "5":
				pc +=2
				
			elif opcode [5] == "6":
				pc +=2
				
			elif opcode [5] == "7":
				pc +=2
				
			elif opcode [5] == "e":
				pc +=2
				
		elif opcode[:3] == "0x9":
			pc +=2
			
		elif opcode[:3] == "0xa":
			VI = int(opcode[3:],16)
			print(VI)
			pc += 2
		
		elif opcode[:3] == "0xb":
			pc += 2
			
		elif opcode[:3] == "0xc":
			
			x = int(opcode[3],16)
			V[x] =  random.randint(0,int(opcode[4:]))
			pc += 2
		
		elif opcode[:3] == "0xd":
			
			n = int(opcode[5],16)
			x = int (opcode[3],16)
			y = int(opcode[4],16)
			V[0xf] = 0
			WHITE=(255,255,255)
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
			surface = pygame.pixelcopy.make_surface(sprite_buffer)
			surface = pygame.transform.scale(surface,(n*10,80))
			screen.blit(surface,(V[x]*10,V[y]*10))
			pygame.display.update()
			VI = saved_VI 	
			pc = saved_pc + 2

		elif opcode[:3] == "0xe":
			
			if opcode [4:] == "9e":
				pc += 2
			elif opcode [4:] == "a1":
				pc += 2
			elif opcode [2:] == "e0":
				pc += 2
		elif opcode[:3] == "0xf":
			
			if opcode[4:] == "07":
				pc += 2
			elif opcode[4:] == "0a":
				pc += 2
			elif opcode[4:] == "15":
				pc += 2	
			elif opcode[4:] == "18":
				pc += 2	
			elif opcode[4:] == "1e":
				pc += 2	
			elif opcode[4:] == "29":
				pc += 2	
			elif opcode[4:] == "33":
				pc += 2	
			elif opcode[4:] == "55":
				pc += 2	
			elif opcode[4:] == "65":
				pc += 2	
