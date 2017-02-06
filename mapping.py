#!/usr/bin/env python
# encoding: utf-8

__title__ = "Mapping"
__author__ = "Walid Yasir (w1995@windowslive.com)"

"""
    mapping
    ~~~~~~~~~~~~~
    A program that read data from mines.txt and print a grid
    map from A B or N depending on the readings.
    :copyright: (c) 2015 by Walid Yasir <w1995@windowlive.com>
"""

from random import randint
from time import sleep

def mines_maker():
	""" 
		simulate arduino and make file contain encoder reading 
		and random metal detector reading 
	"""
	print "creating new file ..."
	f = open("mines.txt", "w")
	print "file created successfully ..."
	# 20 * 20 devided square each 1 m
	total_distance = 20 * 20 * 100
	distance = 0

	print "writing data to the file ..."
	while (distance <= total_distance):
		# 1 if mine above, 2 if below
	    metal_det = randint(0, 2)
	    distance += randint(25, 50)

	    print distance , ":" , metal_det
	    f.write(str(distance) + ":" + str(metal_det) + "\n")

	print "closing file ..."
	f.close()
	print "done ::)"

def get_encoder(msg):
	""" return encoder reading """
	i = msg.split(":")
	encoder = int(i[0])
	return encoder

def get_metal(msg):
	""" return metal detector reading """
	i = msg.split(":")
	metal = int(i[1])
	return metal


def get_position(msg):
	""" take the line , get encoder reading and return x, y """
	distance = get_encoder(msg)

	x = distance / 2000

	if x % 2 == 0:
		y = (distance / 100) % 20
	else:
		y = 19 - ((distance / 100) % 20)
	return x, y
	
def get_mines(msg):
	""" 
		take the line, get the metal reading from it and 
		return if their is metal above or below or not
	"""
	state = get_metal(msg)
	#mine bellow the ground
	if state == 2:
		text = "B"
	#mine above the ground
	elif state == 1:
		text = "A"
    #not mines
	elif state == 0:
		text = "N"
	return text

def generate_map(width, lenght):
	""" generating new map - list - and return it """
	playground = []
	for i in range(lenght):
		playground.append(['X'] * width)
	return playground

def print_map(playground):
	""" printing the map to screen """
	for row in playground:
		print ' '.join(row)

def detect_mines(playground, x, y, state):
	""" take map ,x , y and the metal det and update map """
	playground[y][x] = state
	return playground



# open the mines.txt file
f = open("mines.txt", "r")

# generate a 20 x 20 map and print the row map
m = generate_map(20, 20)
print_map(m)

# iterate through the file .. updating the map info
for line in f:
	x, y = get_position(line)
	s = get_mines(line)
	m = detect_mines(m, x, y, s)

# close the file .. printing the final map
f.close()
print "-" * 40
print_map(m)
print "-" * 40