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
	opcode = '0x00e0'
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
		
	def load(self):
		for i in range (len(self.fontset)):
			self.memory[i] = self.fontset[i]
		
		with open('games/'+"BRIX","rb") as f:
			i = 0
			rom = f.read()
			
			while i < len (rom) : 
				self.memory[i+self.pc] = rom[i]
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
		self.pc = self.stack[self.sp]
		self.sp -= 1 
		self.pc += 2
					
	def jp_addr(self) :
		self.pc = int(self.opcode [3:],16) 
			
	def call_addr(self) :
		self.sp +=1
		self.stack[self.sp] = self.pc
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
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if self.V[x] == self.V[y]:
			self.pc += 2
		self.pc +=2
			
	def ld_vx_byte(self) :
		x = int(self.opcode[3],16)
		self.V[x] = int(self.opcode[4:],16)
		self.pc +=2
			
	def add_vx_byte(self) :
		x = int(self.opcode [3],16)
		self.V[self.x] = self.V[self.x] + int(self.opcode [4:],16)
		self.pc +=2
		
	def ld_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode [4],16)
		self.V[self.x] = self.V[self.y]
		self.pc +=2
			
	def or_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int (self.opcode[4],16)
		self.V[x] = self.V[x] | self.V[y]
		self.pc +=2
				
	def and_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		self.V[x] = self.V[x] & self.V[y]
		self.pc +=2
				
	def xor_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		self.V[x] = self.V[x] ^ self.V[y]
		self.pc +=2
				
	def add_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		self.V[x] = self.V[x] + self.V[y]
		if self.V[x] > 255:
			self.V[0xf] = 1
			self.V[x] = int(bin(self.V[x])[-4:])
		self.pc +=2
				
	def sub_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if self.V[x] > self.V[y] :
			self.V[0xf] = 1
		else:
			self.V[0xf] = 0
			self.V[x] = self.V[x] - self.V[y]
		self.pc +=2
				
	def shr_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if bin(self.V[x])[-0:] == 1:
			self.V[0xf] = 1
		else :
			self.V[0xf] = 0
			self.V[x] = self.V[x]//2
		self.pc +=2
				
	def subn_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if self.V[y] >self. V[x] :
			self.V[0xf] = 1
		else:
			self.V[0xf] = 0
			self.V[x] = self.V[y] - self.V[x]
		self.pc +=2
				
	def shl_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if bin(self.V[x])[0:] == 1:
			self.V[0xf] = 1
		else :
			self.V[0xf] = 0
			self.V[x] = self.V[x]*2
		self.pc +=2
			
	def sne_vx_vy(self):
		x = int(self.opcode[3],16)
		y = int(self.opcode[4],16)
		if self.V[x] != self.V[y]:
			self.pc += 2
			self.pc +=2
			
	def ld_i_addr(self):
		self.VI = int(self.opcode[3:],16)
		self.pc +=2
		
	def jp_v0_addr(self):
		self.pc = int(self.opcode[3:],16)+self.V[0]
		
	def rnd_vx_byte(self):
		x = int(self.opcode[3],16)
		self.V[x] =  random.randint(0,255) & int(self.opcode[4:],16)
		self.pc +=2
		
	def drw_vx_vy_nibble(self):
		n = int(self.opcode[5], 16)
		x = int(self.opcode[3], 16)
		y = int(self.opcode[4], 16)
		saved_x = self.V[x]
		saved_y = self.V[y]
		self.V[0xf] = 0
		saved_pc = self.pc
		self.pc = self.VI
		saved_VI = self.VI
		sprite_buffer = []
		es = []
		if self.V[x] > 63:
			self.V[x] = self.V[x] % 63
		if self.V[y] > 31:
			self.V[y] = self.V[y] % 31
		while self.pc < saved_VI + n:
			self.VI = self.memory[self.pc]
			es = list(bin(self.VI)[2:].zfill(8))
			self.pc += 1
			sprite_buffer.extend(es)
		sprite_buffer = np.asarray(sprite_buffer, dtype=int).reshape(n, 8)
		sprite_buffer = sprite_buffer * 255
		width = 0

		while width != 7:
			height = 0
			if self.V[x] + width > 63:
				self.V[x] = (self.V[x] + width) % 63
			if self.V[y] + height > 31:
				self.V[y] = (self.V[y] + height) % 31
			while height != n:
				self.surface_array[self.V[y] + height, self.V[x] + width] = self.surface_array[self.V[y] + height, self.V[x] + width] ^ sprite_buffer[height, width]
				if self.surface_array[self.V[y] + height, self.V[x] + width] != 0 & sprite_buffer[height, width] != 0:
					V[0xf] = 1
					print(V[0xf])
				height += 1
			width += 1

		surface = pygame.pixelcopy.make_surface(self.surface_array)
		surface = pygame.transform.scale(surface, (320, 640))
		surface = pygame.transform.rotate(surface, 90)
		surface = pygame.transform.flip(surface, False, True)
		self.screen.blit(surface, (0, 0))
		pygame.display.update()
		self.VI = saved_VI
		self.pc = saved_pc + 2
		self.V[x] = saved_x
		self.V[y] = saved_y
					
	def skp_vx(self):
		x = int(self.opcode[3],16)
		if self.key[self.V[x]] == True:
			self.pc += 2
		self.pc +=2
					
	def sknp_vx(self):
		x = int(self.opcode[3],16)
		if self.key[self.V[x]] == False:
			self.pc += 2
		self.pc +=2
				
	def ld_vx_dt(self):
		x = int(self.opcode[3],16)
		self.V[x] = self.dt
		self.pc +=2
				
	def ld_vx_k(self):
		x = int(self.opcode[3],16)
		while pygame.key.get_pressed() == False:
			pass
			self.V[x] = self.key[True]
		self.pc +=2
					
	def ld_dt_vx(self):
		x = int(self.opcode[3],16)
		self.dt = self.V[x]
		self.pc +=2
					
	def ld_st_vx(self):
		x = int(self.opcode[3],16)
		self.st = self.V[x]
		self.pc +=2
					
	def add_i_vx(self):
		x = int(self.opcode[3],16)
		self.VI = self.VI + self.V[x]
		self.pc +=2
					
	def ld_f_vx(self):
		x = int(self.opcode[3],16)
		self.VI = self.V[x] *5
		self.pc +=2
					
	def ld_b_vx(self):
		x = int(self.opcode[3],16)
		self.V[x] = str(self.V[x])
		self.memory[self.VI] = int(self.V[x][0])
		if len (self.V[x]) >= 2:
			self.memory[self.VI+1] = int(self.V[x][1])
		if len (self.V[x]) >= 3:
			self.memory[self.VI+2] = int(self.V[x][2])
		self.V[x] = int(self.V[x])
		self.pc +=2
					
	def ld_i_vx(self):
		x = int(self.opcode[3],16)
		i = 0
		while i < x:
			self.memory[self.VI+i] = self.V[i]
			i += 1
			self.pc +=2
					
	def ld_vx_i(self):
		x = int(self.opcode[3],16)
		i = 0
		while i < x:
			self.V[i] = memory[self.VI+i]
			i += 1
			self.pc +=2

	def __init__(self):
				
			logical_dictionarie = { '0': self.ld_vx_vy,
									'1': self.or_vx_vy,
									'2': self.and_vx_vy,
									'3': self.xor_vx_vy,
									'4': self.add_vx_vy,
									'5': self.sub_vx_vy,
									'6': self.shr_vx_vy,
									'7': self.subn_vx_vy,
									'e': self.shl_vx_vy}

			misc_dictionarie = {'9e' : self.skp_vx,
								'a1' : self.sknp_vx,
								'07' : self.ld_vx_dt,
								'0a' : self.ld_vx_k,
								'15' : self.ld_dt_vx,
								'18' : self.ld_st_vx,
								'1e' : self.add_i_vx,
								'29' : self.ld_f_vx,
								'33' : self.ld_b_vx,
								'55' : self.ld_i_vx,
								'65' : self.ld_vx_i,
								'e0' : self.cls,
								'ee' : self.ret}

			self.opcodes = { 0x0: misc_dictionarie[self.opcode[-2:]],
						0x1: self.jp_addr,
						0x2: self.call_addr,
						0x3: self.se_vx_byte,
						0x4: self.sne_vx_byte,
						0x5: self.se_vx_vy,
						0x6: self.ld_vx_byte,
						0x7: self.add_vx_byte,
						0x8: logical_dictionarie[self.opcode[5]],
						0x9: self.sne_vx_vy,
						0xa: self.ld_i_addr,
						0xb: self.jp_v0_addr,
						0xc: self.rnd_vx_byte,
						0xd: self.drw_vx_vy_nibble,
						0xe: misc_dictionarie[self.opcode[-2:]],
						0xf: misc_dictionarie[self.opcode[-2:]]}
	def cycle(self):
			while True:
				self.opcode = int(hex(self.memory[self.pc]<<8),16)| int(hex(self.memory[self.pc + 1]),16)
				self.opcode = hex(self.opcode)
				self.opcode = str(self.opcode)
				extracted_op = int(self.opcode[:3],16)
				print (self.opcode)
				print(self.pc)
				self.opcodes[extracted_op]()
				if self.dt > 0 :
					time.sleep(0.16)
					self.dt -= 1
				if self.st > 0 :
					time.sleep(0.16)
					self.st -= 1

emu = cpu()
load = emu.load()
cycle= emu.cycle()
cycle()