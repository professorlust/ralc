#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  questGen.py
#
#  Copyright 2014 Tyler Dinsmoor <d@d-netbook>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Responsible for coming up with quests the DM can give the players
#  via in-game NPCs generated by townGen. civGen assigns quests to
#  populated NPCs, listed out for the DM.
#  Loot for quests is handled by lootGen, and special items are earned
#  for harder quests. There are few special quests, and many generic
#  quests, designed to encourage players to value gold.

import random

def wChoice(wCh):
	import random
	'''must be in format: wChoice(('a',1.0),('b',2.0),('c',3.0))'''
	totalChoice = sum(w for c, w in wCh)
	random_uniform = random.uniform(0, totalChoice)
	upto = 0
	for c, w in wCh:
		if upto + w > random_uniform:
			return c
		upto += w
	assert False, "Shouldn't get here"

'''
Quest Requirements:
	Theme
	Difficulty
	Rewards
	Location
	NPCs

'''
class Quest(object):
	def __init__(self, actors):
		pass

	def get_reward(self, reward):
		pass

	def get_completion_requirements(self, reqire_list):
		pass

	def quest_description(self):
		print "Generic Quest"

class LootQuest(Quest):
	"Go hunt down this lost treasure"
	def __init__(self):
		Quest.quest_description(self)
	pass

class TheftQuest(LootQuest):
	"Silently Steal an item"
	pass

class MugQuest(LootQuest):
	"Mug person for item"
	pass


class LocateObjectQuest(Quest):
	"Locate an object"
	pass


class LocatePersonQuest(Quest):
	"Locate an person"
	pass

class RescueQuest(LocatePersonQuest):
	"Locate and rescure NPC"
	pass


class KillQuest(Quest):
	"Kill Someone/something"
	pass

class MurderQuest(KillQuest):
	"Kill person violently"
	pass

class AssasinateQuest(KillQuest):
	"Kill person Silently"
	pass


class UprisingQuest(Quest):
	"Cause a village to revolt"
	pass

class DefendQuest(Quest):
	"Fight back invading force"
	pass


LootQuest()

def main():
	return

if __name__ == '__main__':
	import def_settings
	default_settings = def_settings.get_def_settings()
	main()

