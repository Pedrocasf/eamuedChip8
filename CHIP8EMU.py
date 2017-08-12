import pygame
import sys
import random
import numpy as np
import time
pygame.init()

class cpu():
	def main():
		self.key = [0]*16
		self.screen = pygame.display.set_mode((640,320)) 
		self.surface_array = np.zeros(64*32)
		self.surface_array = np.asarray(surface_array,dtype=int).reshape(32,64)
		self.memory = [0]*4096
		self.i = 0
		self.V =[0]*16
		self.st = 0
		self.dt = 0
		self.VI = 0
		self.pc = 0x200
		self.stack = [0] *16
		self.sp = 0
		self.x = 0
		self.y = 0
		self.opcode = '0x009e'
		self.fontset =[0xF0, 0x90, 0x90, 0x90, 0xF0,
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
		
	def load(self):
		while self.i < len (self.fontset):
			self.memory[i] = self.fontset[i]
			i += 1
		
		with open('games/'+"MAZE","rb") as f:
			i = 0
			self.rom = f.read()
			
			while i < len (rom) : 
				self.memory[i+pc] = rom[i]
				i += 1
				
			i = 0
			while i < len (self.memory):
				self.memory[i] = hex(self.memory[i])
				self.memory[i] = int(self.memory[i], 16)
				i += 1					
	
	def sys_addr(self) :
		self.pc += 2
		
	def cls(self) :
		self.screen.fill((0,0,0))
		self.pc +=2
		
	def ret(self) :
		self.pc = stack[sp]
		self.sp -= 1 
		self.pc += 2
					
	def jp_addr(self) :
		self.pc = int(self.opcode [3:],16) 
			
	def call_addr(self) :
		self.sp +=1
		self.stack[sp] = self.pc
		self.pc = int(self.opcode[3:],16)
			
	def se_vx_byte(self) :
		self.x = int(self.opcode[3],16)
		if int(hex(self.V[self.x])[2:],16) == int(str(self.opcode [4:]),16):
			self.pc +=  2
		self.pc +=2	
		
	def sne_vx_byte(self) :
		self.x = int(self.opcode[3],16)
		if int(hex(self.V[self.x])[2:],16) != int(str(self.opcode [4:]),16):
			self.pc += 2
		self.pc +=2
			
	def se_vx_vy(self) :
		self.x = int(opcode[3],16)
		self.y = int(opcode[4],16)
		if self.V[self.x] == self.V[self.y]:
			self.pc += 2
		self.pc +=2
			
	def ld_vx_byte(self) :
		self.x = int(self.opcode[3],16)
		self.V[self.x] = int(self.opcode[4:],16)
		self.pc +=2
			
	def add_vx_byte(self) :
		self.x = int(opcode [3],16)
		self.V[self.x] = self.V[self.x] + int(self.opcode [4:],16)
		self.pc +=2
		
	def ld_vx_vy(self):
		self.x = int(self.opcode[3],16)
		self.y = int(self.opcode [4],16)
		self.V[self.x] = self.V[self.y]
		self.pc +=2
			
	def or_vx_vy(self):
		self.x = int(self.opcode[3],16)
		self.y = int (self.opcode[4],16)
		self.V[self.x] = self.V[self.x] | self.V[self.y]
		self.pc +=2
				
	def and_vx_vy(self):
		self.x = int(self.opcode[3],16)
		self.y = int(self.opcode[4],16)
		self.V[self.x] = self.V[self.x] & self.V[self.y]
		self.pc +=2
				
	def xor_vx_vy(self):
		self.x = int(self.opcode[3],16)
		self.y = int(self.opcode[4],16)
		self.V[x] = self.V[self.x] ^ self.V[self.y]
		self.pc +=2
				
	def add_vx_vy(self):
		self.x = int(opcode[3],16)
		self.y = int(opcode[4],16)
		self.V[self.x] = V[self.x] + V[self.y]
		if self.V[self.x] > 255:
			self.V[0xf] = 1
			self.V[self.x] = int(bin(self.V[self.x])[-4:])
		self.pc +=2
				
	def sub_vx_vy(self):
		self.x = int(opcode[3],16)
		self.y = int(opcode[4],16)
		if self.V[x] > self.V[y] :
			self.V[0xf] = 1
		else:
			V[0xf] = 0
		V[x] = V[x] - V[y]
		pc +=2
				
	def shr_vx_vy(self):
		x = int(opcode[3],16)
		y = int(opcode[4],16)
		if bin(V[x])[-0:] == 1:
			V[0xf] = 1
		else :
			V[0xf] = 0
		V[x] = V[x]//2
		pc +=2
				
	def subn_vx_vy(self):
		x = int(opcode[3],16)
		y = int(opcode[4],16)
		if V[y] > V[x] :
			V[0xf] = 1
		else:
			V[0xf] = 0
		V[x] = V[y] - V[x]
		pc +=2
				
	def shl_vx_vy(self):
		x = int(opcode[3],16)
		y = int(opcode[4],16)
		if bin(V[x])[0:] == 1:
			V[0xf] = 1
		else :
			V[0xf] = 0
		V[x] = V[x]*2
		pc +=2
			
	def sne_vx_vy(self):
		x = int(opcode[3],16)
		y = int(opcode[4],16)
		if V[x] != V[y]:
			pc += 2
		pc +=2
			
	def ld_i_addr():
		self.VI = int(opcode[3:],16)
		self.pc +=2
		
	def jp_v0_addr(self):
		pc = int(opcode[3:],16)+V[0]
		
	def rnd_vx_byte(self):
		x = int(opcode[3],16)
		V[x] =  random.randint(0,255) & int(opcode[4:],16)
		pc +=2
		
	def drw_vx_vy_nibble(self):
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
					
	def skp_vx(self):
		x = int(opcode[3],16) 
		if key[V[x]] == True:
			pc += 2
		pc +=2	
					
	def sknp_vx(self):
			x = int(opcode[3],16)
			if key[V[x]] == False:
				pc += 2
			pc +=2
				
	def ld_vx_dt(self):
		x = int(opcode[3],16)
		V[x] = dt
		pc +=2
				
	def ld_vx_k(self):
		x = int(opcode[3],16)
		while pygame.key.get_pressed() == False:
			pass
		V[x] = key[True]
		pc +=2
					
	def ld_dt_vx(self):
		x = int(opcode[3],16)
		dt = V[x]
		pc +=2
					
	def ld_st_vx(self):
		x = int(opcode[3],16)
		st = V[x]
		pc +=2
					
	def add_i_vx(self):
		x = int(opcode[3],16)
		VI = VI + V[x]
		pc +=2
					
	def ld_f_vx(self):
		x = int(opcode[3],16)
		VI = V[x] *5
		pc +=2
					
	def ld_b_vx(self):
		x = int(opcode[3],16)
		V[x] = str(V[x])
		memory[VI] = int(V[x][0])
		if len (V[x]) >= 2: 
			memory[VI+1] = int(V[x][1])
		if len (V[x]) >= 3:
			memory[VI+2] = int(V[x][2])
		V[x] = int(V[x]) 
		pc +=2
					
	def ld_i_vx(self):
		x = int(opcode[3],16)
		i = 0
		while i < x:
			memory[VI+i] = V[i]
			i += 1
			pc +=2
					
	def ld_vx_i(self):
		x = int(opcode[3],16)
		i = 0
		while i < x:
			V[i] = memory[VI+i]
			i += 1
		pc +=2

	while True:
				
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
								'65' : ld_vx_i(),
								'e0' : cls(),
								'ee' : ret()}
					
			opcodes = { 0x1: jp_addr(),
						0x2: call_addr(),
						0x3: se_vx_byte(),
						0x4: sne_vx_byte(),
						0x5: se_vx_vy(),
						0x6: ld_vx_byte(),
						0x7: add_vx_byte(),
						0x8: logical_dictionarie[opcode[5]],
						0x9: sne_vx_vy(),
						0xa: ld_i_addr(),
						0xb: jp_v0_addr(),
						0xc: rnd_vx_byte(),
						0xd: drw_vx_vy_nibble(),
						0xe: misc_dictionarie[opcode[-2:]],
						0xf: misc_dictionarie[opcode[-2:]]}

				
			self.opcode = int(hex(self.memory[self.pc]<<8),16)| int(hex(self.memory[self.pc + 1]),16)
			self.opcode = hex(self.opcode)
			self.opcode = str(self.opcode)
			extracted_op = int(self.opcode[:3],16)
			print (self.opcode)
			print(self.pc)
			opcodes[extracted_op]
			if self.dt > 0 :
				time.sleep(0.16)	
				self.dt -= 1
			if self.st > 0 :
				time.sleep(0.16)	
				self.st -= 1		
