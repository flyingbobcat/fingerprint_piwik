#!/usr/bin/env python

import sys

import probing
import vectors
import versions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time
import pickle
import argparse
import pprint


G="\033[32m"
GR="\033[2m"
B="\033[34m"
R="\033[31m"
W="\033[m"
BOG="\033[30m\033[42m"

plot_scale=100
plot_highlight_versions = versions.NOT_INSTALLABLE
plot_savedir = "/tmp/fpp_plots"
plot_matrix = {}

def plot_init():
	fig,ax = plt.subplots()
	currentAxis = plt.gca()
	boxes = ['0.1.0','0.4.2','1.0.0','2.0.0','2.11.2-rc1']
	lines = versions.minors()
	
	# label axes
	plt.xlabel('tested version')
	plt.ylabel('recognised versions')

	# draw boxes
	ps = [0] + [ versions.VERSIONS.index(v) * plot_scale for v in boxes ]
	for i in range(len(ps)-1):
		currentAxis.add_patch(
			Rectangle(
				[ ps[i], ps[i] ],
				ps[i+1] - ps[i],
				ps[i+1] - ps[i],
				facecolor='blue',
				alpha=.1,
				)
			)

	# draw annotations
	linepositions = [ versions.VERSIONS.index(v) * plot_scale for v in lines ]
	if False: # annotate on the x-axis
		plt.vlines(linepositions,0,linepositions,linestyle='dotted')
		for label, xpos, no in zip(lines,linepositions,range(len(lines))):
			labelpos = (20,-20 - (20*(no%3)))
			plt.annotate(
				label,
				xy = (xpos, -5), xytext = labelpos,
				textcoords = 'offset points', ha = 'right', va = 'bottom',
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'gray', alpha = 0.5),
				arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'), size=10)
	if True: # annotate on the diagonale
		for label, x, y,no in zip(lines,linepositions,linepositions,range(len(lines))):
			labelpos = ( ( -60  + 20 * (no%2) ) * (-1 if no%4>1 else 1) , ( 60 - 20 * (no%2)  ) * (-1 if no%4>1 else 1))
			plt.annotate(
				label, 
				xy = (x, y), xytext = labelpos,
				textcoords = 'offset points', ha = 'right', va = 'bottom',
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'gray', alpha = 0.5),
				arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0', alpha=0.75),size=8)
	
def plot_add(correct_version,version_range):
	plot_matrix[correct_version] = version_range
	current_h_pos = versions.VERSIONS.index(correct_version)
	v_pos = [ versions.VERSIONS.index(x) * plot_scale for x in version_range ]
	h_pos = [ current_h_pos * plot_scale ] * len(v_pos)
	color = 'red' if correct_version in plot_highlight_versions else 'black'
	plt.scatter(h_pos, v_pos, s=4, facecolors=color, edgecolors='none')
	
def plot_show():
	# add diagonale
	pos = [ x * plot_scale for x in range(len(versions.VERSIONS)) ]
	plt.scatter(pos, pos, s=8, facecolors='none', edgecolors='g')

	if raw_input("save the results to disk? [yN] ") in ['y','Y']:
		
		# format the timestamps
		timestr = time.strftime("%y-%m-%d %H:%M:%S")
		
		# matrix
		with open(plot_savedir + "/version plot %s matrix.txt"%timestr,"w") as f:
			pprint.pprint(plot_matrix,stream=f)
		
		# scale high
		fig = plt.gcf()
		fig.set_size_inches(25,25)
		fig.savefig(plot_savedir + "/version plot %s high.png"%timestr, dpi=600)
	
		# scale low
		fig.set_size_inches(7,7)
		fig.savefig(plot_savedir + "/version plot %s low.png"%timestr, dpi=600)
		print "3 files written to", plot_savedir

	#show
	plt.show()

def testcases(use_vectors=None):
	cases = [['192.168.56.102/piwik/piwik-0.1', '0.1'],
 ['192.168.56.102/piwik/piwik-0.1.1', '0.1.1'],
 ['192.168.56.102/piwik/piwik-0.1.2', '0.1.2'],
 ['192.168.56.102/piwik/piwik-0.1.3', '0.1.3'],
 ['192.168.56.102/piwik/piwik-0.1.4', '0.1.4'],
 ['192.168.56.102/piwik/piwik-0.1.5', '0.1.5'],
 ['192.168.56.102/piwik/piwik-0.1.6', '0.1.6'],
 ['192.168.56.102/piwik/piwik-0.1.7', '0.1.7'],
 ['192.168.56.102/piwik/piwik-0.1.8', '0.1.8'],
 ['192.168.56.102/piwik/piwik-0.1.9', '0.1.9'],
 ['192.168.56.102/piwik/piwik-0.1.10', '0.1.10'],
 ['192.168.56.102/piwik/piwik-0.2.1', '0.2.1'],
 ['192.168.56.102/piwik/piwik-0.2.2', '0.2.2'],
 ['192.168.56.102/piwik/piwik-0.2.3', '0.2.3'],
 ['192.168.56.102/piwik/piwik-0.2.4', '0.2.4'],
 ['192.168.56.102/piwik/piwik-0.2.5', '0.2.5'],
 ['192.168.56.102/piwik/piwik-0.2.6', '0.2.6'],
 ['192.168.56.102/piwik/piwik-0.2.7', '0.2.7'],
 ['192.168.56.102/piwik/piwik-0.2.8', '0.2.8'],
 ['192.168.56.102/piwik/piwik-0.2.9', '0.2.9'],
 ['192.168.56.102/piwik/piwik-0.2.10', '0.2.10'],
 ['192.168.56.102/piwik/piwik-0.2.11', '0.2.11'],
 ['192.168.56.102/piwik/piwik-0.2.12', '0.2.12'],
 ['192.168.56.102/piwik/piwik-0.2.13', '0.2.13'],
 ['192.168.56.102/piwik/piwik-0.2.14', '0.2.14'],
 ['192.168.56.102/piwik/piwik-0.2.16', '0.2.16'],
 ['192.168.56.102/piwik/piwik-0.2.17', '0.2.17'],
 ['192.168.56.102/piwik/piwik-0.2.18', '0.2.18'],
 ['192.168.56.102/piwik/piwik-0.2.19', '0.2.19'],
 ['192.168.56.102/piwik/piwik-0.2.20', '0.2.20'],
 ['192.168.56.102/piwik/piwik-0.2.22', '0.2.22'],
 ['192.168.56.102/piwik/piwik-0.2.23', '0.2.23'],
 ['192.168.56.102/piwik/piwik-0.2.24', '0.2.24'],
 ['192.168.56.102/piwik/piwik-0.2.25', '0.2.25'],
 ['192.168.56.102/piwik/piwik-0.2.26', '0.2.26'],
 ['192.168.56.102/piwik/piwik-0.2.27', '0.2.27'],
 ['192.168.56.102/piwik/piwik-0.2.28', '0.2.28'],
 ['192.168.56.102/piwik/piwik-0.2.29', '0.2.29'],
 ['192.168.56.102/piwik/piwik-0.2.30', '0.2.30'],
 ['192.168.56.102/piwik/piwik-0.2.31', '0.2.31'],
 ['192.168.56.102/piwik/piwik-0.2.32', '0.2.32'],
 ['192.168.56.102/piwik/piwik-0.2.33', '0.2.33'],
 ['192.168.56.102/piwik/piwik-0.2.34', '0.2.34'],
 ['192.168.56.102/piwik/piwik-0.2.35', '0.2.35'],
 ['192.168.56.102/piwik/piwik-0.2.36', '0.2.36'],
 ['192.168.56.102/piwik/piwik-0.2.37', '0.2.37'],
 ['192.168.56.102/piwik/piwik-0.4', '0.4'],
 ['192.168.56.102/piwik/piwik-0.4.1', '0.4.1'],
 ['192.168.56.102/piwik/piwik-0.4.2', '0.4.2'],
 ['192.168.56.102/piwik/piwik-0.4.3', '0.4.3'],
 ['192.168.56.102/piwik/piwik-0.4.4', '0.4.4'],
 ['192.168.56.102/piwik/piwik-0.4.5', '0.4.5'],
 ['192.168.56.102/piwik/piwik-0.5', '0.5'],
 ['192.168.56.102/piwik/piwik-0.5.1', '0.5.1'],
 ['192.168.56.102/piwik/piwik-0.5.2', '0.5.2'],
 ['192.168.56.102/piwik/piwik-0.5.3', '0.5.3'],
 ['192.168.56.102/piwik/piwik-0.5.4', '0.5.4'],
 ['192.168.56.102/piwik/piwik-0.5.5', '0.5.5'],
 ['192.168.56.102/piwik/piwik-0.6', '0.6'],
 ['192.168.56.102/piwik/piwik-0.6.1', '0.6.1'],
 ['192.168.56.102/piwik/piwik-0.6.2', '0.6.2'],
 ['192.168.56.102/piwik/piwik-0.6.3', '0.6.3'],
 ['192.168.56.102/piwik/piwik-0.6.4', '0.6.4'],
 ['192.168.56.102/piwik/piwik-0.7', '0.7'],
 ['192.168.56.102/piwik/piwik-0.8', '0.8'],
 ['192.168.56.102/piwik/piwik-0.9', '0.9'],
 ['192.168.56.102/piwik/piwik-0.9.9', '0.9.9'],
 ['192.168.56.102/piwik/piwik-1.0', '1.0'],
 ['192.168.56.102/piwik/piwik-1.1', '1.1'],
 ['192.168.56.102/piwik/piwik-1.1.1', '1.1.1'],
 ['192.168.56.102/piwik/piwik-1.2', '1.2'],
 ['192.168.56.102/piwik/piwik-1.2.1', '1.2.1'],
 ['192.168.56.102/piwik/piwik-1.3', '1.3'],
 ['192.168.56.102/piwik/piwik-1.4', '1.4'],
 ['192.168.56.102/piwik/piwik-1.5', '1.5'],
 ['192.168.56.102/piwik/piwik-1.5.1', '1.5.1'],
 ['192.168.56.102/piwik/piwik-1.6', '1.6'],
 ['192.168.56.102/piwik/piwik-1.7', '1.7'],
 ['192.168.56.102/piwik/piwik-1.7.1', '1.7.1'],
 ['192.168.56.102/piwik/piwik-1.8', '1.8'],
 ['192.168.56.102/piwik/piwik-1.8.1', '1.8.1'],
 ['192.168.56.102/piwik/piwik-1.8.2', '1.8.2'],
 ['192.168.56.102/piwik/piwik-1.8.3', '1.8.3'],
 ['192.168.56.102/piwik/piwik-1.8.4', '1.8.4'],
 ['192.168.56.102/piwik/piwik-1.9', '1.9'],
 ['192.168.56.102/piwik/piwik-1.9.1', '1.9.1'],
 ['192.168.56.102/piwik/piwik-1.9.2', '1.9.2'],
 ['192.168.56.102/piwik/piwik-1.10', '1.10'],
 ['192.168.56.102/piwik/piwik-1.10.1', '1.10.1'],
 ['192.168.56.102/piwik/piwik-1.11', '1.11'],
 ['192.168.56.102/piwik/piwik-1.11.1', '1.11.1'],
 ['192.168.56.102/piwik/piwik-1.12', '1.12'],
 ['192.168.56.102/piwik/piwik-2.0', '2.0'],
 ['192.168.56.102/piwik/piwik-2.0.1', '2.0.1'],
 ['192.168.56.102/piwik/piwik-2.0.2', '2.0.2'],
 ['192.168.56.102/piwik/piwik-2.0.3', '2.0.3'],
 ['192.168.56.102/piwik/piwik-2.1.0', '2.1.0'],
 ['192.168.56.102/piwik/piwik-2.1.1-b10', '2.1.1-b10'],
 ['192.168.56.102/piwik/piwik-2.1.1-b12', '2.1.1-b12'],
 ['192.168.56.102/piwik/piwik-2.1.1-b8', '2.1.1-b8'],
 ['192.168.56.102/piwik/piwik-2.1.1-b9', '2.1.1-b9'],
 ['192.168.56.102/piwik/piwik-2.2.0', '2.2.0'],
 ['192.168.56.102/piwik/piwik-2.2.0-b13', '2.2.0-b13'],
 ['192.168.56.102/piwik/piwik-2.2.0-b14', '2.2.0-b14'],
 ['192.168.56.102/piwik/piwik-2.2.0-b15', '2.2.0-b15'],
 ['192.168.56.102/piwik/piwik-2.2.0-b16', '2.2.0-b16'],
 ['192.168.56.102/piwik/piwik-2.2.0-b18', '2.2.0-b18'],
 ['192.168.56.102/piwik/piwik-2.2.0-rc1', '2.2.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.2.0-rc2', '2.2.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.2.0-rc3', '2.2.0-rc3'],
 ['192.168.56.102/piwik/piwik-2.2.0-rc4', '2.2.0-rc4'],
 ['192.168.56.102/piwik/piwik-2.2.1', '2.2.1'],
 ['192.168.56.102/piwik/piwik-2.2.1-b1', '2.2.1-b1'],
 ['192.168.56.102/piwik/piwik-2.2.1-b2', '2.2.1-b2'],
 ['192.168.56.102/piwik/piwik-2.2.1-b3', '2.2.1-b3'],
 ['192.168.56.102/piwik/piwik-2.2.1-b4', '2.2.1-b4'],
 ['192.168.56.102/piwik/piwik-2.2.1-rc1', '2.2.1-rc1'],
 ['192.168.56.102/piwik/piwik-2.2.1-rc3', '2.2.1-rc3'],
 ['192.168.56.102/piwik/piwik-2.2.2', '2.2.2'],
 ['192.168.56.102/piwik/piwik-2.2.2-b1', '2.2.2-b1'],
 ['192.168.56.102/piwik/piwik-2.2.3-b1', '2.2.3-b1'],
 ['192.168.56.102/piwik/piwik-2.2.3-b4', '2.2.3-b4'],
 ['192.168.56.102/piwik/piwik-2.2.3-b6', '2.2.3-b6'],
 ['192.168.56.102/piwik/piwik-2.2.3-b7', '2.2.3-b7'],
 ['192.168.56.102/piwik/piwik-2.3.0', '2.3.0'],
 ['192.168.56.102/piwik/piwik-2.3.0-rc1', '2.3.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.3.0-rc2', '2.3.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.3.0-rc3', '2.3.0-rc3'],
 ['192.168.56.102/piwik/piwik-2.3.0-rc4', '2.3.0-rc4'],
 ['192.168.56.102/piwik/piwik-2.4.0', '2.4.0'],
 ['192.168.56.102/piwik/piwik-2.4.0-b2', '2.4.0-b2'],
 ['192.168.56.102/piwik/piwik-2.4.0-b3', '2.4.0-b3'],
 ['192.168.56.102/piwik/piwik-2.4.0-b5', '2.4.0-b5'],
 ['192.168.56.102/piwik/piwik-2.4.0-b6', '2.4.0-b6'],
 ['192.168.56.102/piwik/piwik-2.4.0-b7', '2.4.0-b7'],
 ['192.168.56.102/piwik/piwik-2.4.0-b8', '2.4.0-b8'],
 ['192.168.56.102/piwik/piwik-2.4.0-rc1', '2.4.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.4.1', '2.4.1'],
 ['192.168.56.102/piwik/piwik-2.4.1-rc1', '2.4.1-rc1'],
 ['192.168.56.102/piwik/piwik-2.5.0', '2.5.0'],
 ['192.168.56.102/piwik/piwik-2.5.0-b1', '2.5.0-b1'],
 ['192.168.56.102/piwik/piwik-2.5.0-b2', '2.5.0-b2'],
 ['192.168.56.102/piwik/piwik-2.5.0-b3', '2.5.0-b3'],
 ['192.168.56.102/piwik/piwik-2.5.0-rc1', '2.5.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.5.0-rc3', '2.5.0-rc3'],
 ['192.168.56.102/piwik/piwik-2.5.0-rc4', '2.5.0-rc4'],
 ['192.168.56.102/piwik/piwik-2.6.0', '2.6.0'],
 ['192.168.56.102/piwik/piwik-2.6.0-b1', '2.6.0-b1'],
 ['192.168.56.102/piwik/piwik-2.6.0-rc1', '2.6.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.6.0-rc2', '2.6.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.6.0-rc3', '2.6.0-rc3'],
 ['192.168.56.102/piwik/piwik-2.6.0-rc4', '2.6.0-rc4'],
 ['192.168.56.102/piwik/piwik-2.6.1', '2.6.1'],
 ['192.168.56.102/piwik/piwik-2.6.1-b1', '2.6.1-b1'],
 ['192.168.56.102/piwik/piwik-2.7.0', '2.7.0'],
 ['192.168.56.102/piwik/piwik-2.7.0-b1', '2.7.0-b1'],
 ['192.168.56.102/piwik/piwik-2.7.0-b3', '2.7.0-b3'],
 ['192.168.56.102/piwik/piwik-2.7.0-b4', '2.7.0-b4'],
 ['192.168.56.102/piwik/piwik-2.7.0-rc1', '2.7.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.7.0-rc2', '2.7.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.8.0', '2.8.0'],
 ['192.168.56.102/piwik/piwik-2.8.0-b2', '2.8.0-b2'],
 ['192.168.56.102/piwik/piwik-2.8.0-b3', '2.8.0-b3'],
 ['192.168.56.102/piwik/piwik-2.8.0-rc1', '2.8.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.8.0-rc2', '2.8.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.8.1', '2.8.1'],
 ['192.168.56.102/piwik/piwik-2.8.1-b1', '2.8.1-b1'],
 ['192.168.56.102/piwik/piwik-2.8.1-b2', '2.8.1-b2'],
 ['192.168.56.102/piwik/piwik-2.8.1-rc1', '2.8.1-rc1'],
 ['192.168.56.102/piwik/piwik-2.8.2', '2.8.2'],
 ['192.168.56.102/piwik/piwik-2.8.3', '2.8.3'],
 ['192.168.56.102/piwik/piwik-2.9.0', '2.9.0'],
 ['192.168.56.102/piwik/piwik-2.9.0-b1', '2.9.0-b1'],
 ['192.168.56.102/piwik/piwik-2.9.0-b2', '2.9.0-b2'],
 ['192.168.56.102/piwik/piwik-2.9.0-b3', '2.9.0-b3'],
 ['192.168.56.102/piwik/piwik-2.9.0-b4', '2.9.0-b4'],
 ['192.168.56.102/piwik/piwik-2.9.0-b5', '2.9.0-b5'],
 ['192.168.56.102/piwik/piwik-2.9.0-b6', '2.9.0-b6'],
 ['192.168.56.102/piwik/piwik-2.9.0-b7', '2.9.0-b7'],
 ['192.168.56.102/piwik/piwik-2.9.0-b8', '2.9.0-b8'],
 ['192.168.56.102/piwik/piwik-2.9.0-b9', '2.9.0-b9'],
 ['192.168.56.102/piwik/piwik-2.9.0-rc1', '2.9.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.9.0-rc2', '2.9.0-rc2'],
 ['192.168.56.102/piwik/piwik-2.9.1', '2.9.1'],
 ['192.168.56.102/piwik/piwik-2.9.1-b1', '2.9.1-b1'],
 ['192.168.56.102/piwik/piwik-2.9.1-b2', '2.9.1-b2'],
 ['192.168.56.102/piwik/piwik-2.10.0', '2.10.0'],
 ['192.168.56.102/piwik/piwik-2.10.0-b1', '2.10.0-b1'],
 ['192.168.56.102/piwik/piwik-2.10.0-b10', '2.10.0-b10'],
 ['192.168.56.102/piwik/piwik-2.10.0-b11', '2.10.0-b11'],
 ['192.168.56.102/piwik/piwik-2.10.0-b2', '2.10.0-b2'],
 ['192.168.56.102/piwik/piwik-2.10.0-b3', '2.10.0-b3'],
 ['192.168.56.102/piwik/piwik-2.10.0-b4', '2.10.0-b4'],
 ['192.168.56.102/piwik/piwik-2.10.0-b5', '2.10.0-b5'],
 ['192.168.56.102/piwik/piwik-2.10.0-b6', '2.10.0-b6'],
 ['192.168.56.102/piwik/piwik-2.10.0-b7', '2.10.0-b7'],
 ['192.168.56.102/piwik/piwik-2.10.0-b8', '2.10.0-b8'],
 ['192.168.56.102/piwik/piwik-2.10.0-b9', '2.10.0-b9'],
 ['192.168.56.102/piwik/piwik-2.10.0-rc1', '2.10.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.10.0-rc3', '2.10.0-rc3'],
 ['192.168.56.102/piwik/piwik-2.10.0-rc4', '2.10.0-rc4'],
 ['192.168.56.102/piwik/piwik-2.11.0', '2.11.0'],
 ['192.168.56.102/piwik/piwik-2.11.0-b2', '2.11.0-b2'],
 ['192.168.56.102/piwik/piwik-2.11.0-b3', '2.11.0-b3'],
 ['192.168.56.102/piwik/piwik-2.11.0-b4', '2.11.0-b4'],
 ['192.168.56.102/piwik/piwik-2.11.0-b5', '2.11.0-b5'],
 ['192.168.56.102/piwik/piwik-2.11.0-b6', '2.11.0-b6'],
 ['192.168.56.102/piwik/piwik-2.11.0-b7', '2.11.0-b7'],
 ['192.168.56.102/piwik/piwik-2.11.0-rc1', '2.11.0-rc1'],
 ['192.168.56.102/piwik/piwik-2.11.1', '2.11.1'],
 ['192.168.56.102/piwik/piwik-2.11.1-b1', '2.11.1-b1'],
 ['192.168.56.102/piwik/piwik-2.11.1-b3', '2.11.1-b3'],
 ['192.168.56.102/piwik/piwik-2.11.1-rc1', '2.11.1-rc1'],
 ['192.168.56.102/piwik/piwik-2.11.2', '2.11.2'],
 ['192.168.56.102/piwik/piwik-2.11.2-b1', '2.11.2-b1'],
 ['192.168.56.102/piwik/piwik-2.11.2-b2', '2.11.2-b2'],
 ['192.168.56.102/piwik/piwik-2.11.2-b3', '2.11.2-b3'],
 ['192.168.56.102/piwik/piwik-2.11.2-rc1', '2.11.2-rc1']]
	
	# initialize monitoring vaiables
	plot_init()
	right = wrong = empty = exactly =  0
	
	print "Beginning with tests:"
	for url, version in cases:
		version = versions.check(version)
		probing.requests_made = 0
		print "Testing version", BOG + version + W, "at", url
		if version in versions.NOT_INSTALLABLE:
			if probing.VERBOSITY > probing.QUIET:
				print B+"Notice: This version was not installable"+W

		probing.DEBUG_VERSION_TO_PROBE = versions.check(version)
		result = probing.fingerprint(url, use_vectors)
		print "result :(%3d/%3d)"%(len(result),len(versions.VERSIONS)), versions.pprint(result), "\n"
			
		# monitor our success
		plot_add(version,result)
		if not result:
			empty += 1
		else:
			if version in result:
				right += 1
				if len(result) == 1:
					exactly += 1
			else:
				wrong += 1
	print "right:", right
	print "wrong:", wrong
	print "empty:", empty
	print "exactly:", exactly
	plot_show()


if __name__ == "__main__":
	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity. Can be stacked, e.g. -vvv")
	parser.add_argument("-tv", "--testvectors", help="comma separated list of vectors that shall be used for test cases. Use all if not provided.")

	g = parser.add_mutually_exclusive_group(required=True)
	g.add_argument("-t", "--test", action="store_true", help="initiate test cases. Parameter 'url' will be ignored")
	g.add_argument("-u", "--url", help="location of piwik")
	g.add_argument("-uf", "--urlfile", help="file with one piwik location per line. Each will be fingerprinted")
	
	args = parser.parse_args()
	
	# process arguments
	probing.VERBOSITY = args.verbosity
	
	if args.test:
		if 'testvectors' in args and args.testvectors:
			vectors = args.testvectors.split(",")
			testcases(vectors)
		else:
			testcases()
	else:
		if args.urlfile:
			with open(args.urlfile,"r") as f:
				urls = f.read().splitlines()
				for u in urls:
					if u:
						print u + ":",
						try:
							print probing.fingerprint(u)
						except:
							print "error"
							pass
		elif args.url:
			print probing.fingerprint(args.url)

