import pygame
import sys
import random
import numpy as np
import time
pygame.init()

class cpu():
	key = [0]*16
	screen = pygame.display.set_mode((640,320)) 
	surface_array = np.zeros(64*32)
	surface_array = np.asarray(surface_array,dtype=int).reshape(32,64)
	memory = [0]*4096
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
	opcode = ''
	fontset =[0xF0, 0x90, 0x90, 0x90, 0xF0,
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
	
	with open('games/'+"MAZE","rb") as f:
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
		
	opcode = int(hex(memory[pc]<<8),16)| int(hex(memory[pc + 1]),16)		
	opcode = hex(opcode)
	opcode = str(opcode)	
	
	def sys_addr() :
		pc += 2
		
	def cls() :
		screen.fill((0,0,0))
		pc +=2
		
	def ret() :
		pc = stack[sp]
		sp -= 1 
		pc += 2
					
	def jp_addr() :
		pc = int(opcode [3:],16) 
			
	def call_addr() :
		sp +=1
		stack[sp] = pc
		pc = int(opcode[3:],16)
			
	def se_vx_byte() :
	x = int(opcode[3],16)
	if int(hex(V[x])[2:],16) == int(str(opcode [4:]),16):
		pc +=  2
	pc +=2	
		
def sne_vx_byte() :
	x = int(opcode[3],16)
	if int(hex(V[x])[2:],16) != int(str(opcode [4:]),16):
		pc += 2
	pc +=2
			
def se_vx_vy() :
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if V[x] == V[y]:
		pc += 2
	pc +=2
			
def ld_vx_byte() :
	x = int(opcode[3],16)
	V[x] = int(opcode[4:],16)
	pc +=2
			
def add_vx_byte() :
	x = int(opcode [3],16)
	V[x] = V[x] + int(opcode [4:],16)
	pc +=2
		
def ld_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode [4],16)
	V[x] = V[y]
	pc +=2
			
def or_vx_vy():
	x = int(opcode[3],16)
	y = int (opcode[4],16)
	V[x] = V[x] | V[y]
	pc +=2
				
def and_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	V[x] = V[x] & V[y]
	pc +=2
				
def xor_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	V[x] = V[x] ^ V[y]
	pc +=2
				
def add_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	V[x] = V[x] + V[y]
	if V[x] > 255:
		V[0xf] = 1
		V[x] = int(bin(V[x])[-4:])
	pc +=2
				
def sub_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if V[x] > V[y] :
		V[0xf] = 1
	else:
		V[0xf] = 0
	V[x] = V[x] - V[y]
	pc +=2
				
def shr_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if bin(V[x])[-0:] == 1:
		V[0xf] = 1
	else :
		V[0xf] = 0
	V[x] = V[x]//2
	pc +=2
				
def subn_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if V[y] > V[x] :
		V[0xf] = 1
	else:
		V[0xf] = 0
	V[x] = V[y] - V[x]
	pc +=2
				
def shl_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if bin(V[x])[0:] == 1:
		V[0xf] = 1
	else :
		V[0xf] = 0
	V[x] = V[x]*2
	pc +=2
			
def sne_vx_vy():
	x = int(opcode[3],16)
	y = int(opcode[4],16)
	if V[x] != V[y]:
		pc += 2
	pc +=2
		
def ld_i_addr():
	VI = int(opcode[3:],16)
	pc +=2
	
def jp_v0_addr():
	pc = int(opcode[3:],16)+V[0]
	
def rnd_vx_byte():
	x = int(opcode[3],16)
	V[x] =  random.randint(0,255) & int(opcode[4:],16)
	pc +=2
	
def drw_vx_vy_nibble():
	n = int(opcode[5],16)
	x = int (opcode[3],16)
	y = int(opcode[4],16)
	V[0xf] = 1
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
	surface = pygame.surfarray.make_surface(sprite_buffer)
	surface.set_colorkey(0)
	surface = pygame.transform.scale(surface,(n*10,80))
	surface = pygame.transform.rotate(surface,90)
	surface = pygame.transform.flip(surface,False,True)
	screen.blit(surface,(V[x]*10,V[y]*10))
	pygame.display.update()
	VI = saved_VI 	
	pc = saved_pc +2
				
def skp_vx():
	x = int(opcode[3],16) 
	if key[V[x]] == True:
		pc += 2
	pc +=2	
				
def sknp_vx():
		x = int(opcode[3],16)
		if key[V[x]] == False:
			pc += 2
		pc +=2
			
def ld_vx_dt():
	x = int(opcode[3],16)
	V[x] = dt
	pc +=2
			
def ld_vx_k():
	x = int(opcode[3],16)
	while pygame.key.get_pressed() == False:
		pass
	V[x] = key[True]
	pc +=2
				
def ld_dt_vx():
	x = int(opcode[3],16)
	dt = V[x]
	pc +=2
				
def ld_st_vx():
	x = int(opcode[3],16)
	st = V[x]
	pc +=2
				
def add_i_vx():
	x = int(opcode[3],16)
	VI = VI + V[x]
	pc +=2
				
def ld_f_vx():
	x = int(opcode[3],16)
	VI = V[x] *5
	pc +=2
				
def ld_b_vx():
	x = int(opcode[3],16)
	V[x] = str(V[x])
	memory[VI] = int(V[x][0])
	if len (V[x]) >= 2: 
		memory[VI+1] = int(V[x][1])
	if len (V[x]) >= 3:
		memory[VI+2] = int(V[x][2])
	V[x] = int(V[x]) 
	pc +=2
				
def ld_i_vx():
	x = int(opcode[3],16)
	i = 0
	while i < x:
		memory[VI+i] = V[i]
		i += 1
		pc +=2
				
def ld_vx_i():
	x = int(opcode[3],16)
	i = 0
	while i < x:
		V[i] = memory[VI+i]
		i += 1
	pc +=2
	
logical_dictionarie = { '0': ld_vx_vy(),
							'1': or_vx_vy(),
							'2': and_vx_vy(),
							'3': xor_vx_vy(),
							'4': add_vx_vy(),
							'5': sub_vx_vy(),
							'6': shr_vx_vy(),
							'7': subn_vx_vy(),
							'e': shl_vx_vy()}
								
misc_dictionarie = {'9e' : skp_vx(),
						'a1' : sknp_vx(),
						'07' : ld_vx_dt(),
						'0a' : ld_vx_k(),
						'15' : ld_dt_vx(),
						'18' : ld_st_vx(),
						'1e' : add_i_vx(),
						'29' : ld_f_vx(),
						'33' : ld_b_vx(),
						'55' : ld_i_vx(),
						'65' : ld_vx_i()}
	
special_dictionarie = { '0x0000' : sys_addr(),
							'0x00e0' : cls(),	
							'0x00ee' : ret()}
		
opcodes = { '0': special_dictionarie[opcode],
				'1': jp_addr(),
				'2': call_addr(),
				'3': se_vx_byte(),
				'4': sne_vx_byte(),
				'5': se_vx_vy(),
				'6': ld_vx_byte(),
				'7': add_vx_byte(),
				'8': logical_dictionarie[opcode[5]],
				'9': sne_vx_vy(),
				'a': ld_i_addr(),
				'b': jp_v0_addr(),
				'c': rnd_vx_byte(),
				'd': drw_vx_vy_nibble(),
				'e': misc_dictionarie[opcode[4:]],
				'f': misc_dictionarie[opcode[4:]]}
			
while True:
		
	opcode = int(hex(memory[pc]<<8),16)| int(hex(memory[pc + 1]),16)
	opcode = hex(opcode)
	opcode = str(opcode)
	print (opcode[2])				
	print(VI)
	try:
		opcodes[opcode[2]]
	except:
		print('unknown function')
	
	if dt > 0 :
		time.sleep(0.16)	
		dt -= 1
	if st > 0 :
		time.sleep(0.16)	
		st -= 1		
