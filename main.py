#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>
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
#
RALC_VERSION = 'Beta v0.63'
try:
	import Tkinter as tk
	import tkSimpleDialog
	import tkMessageBox
	import ttk
	import mapGen
	import charGen
	import collections as col
	from PIL import Image, ImageTk
	import cPickle as pickle
	import itemGen
	import os
	import shutil
except ImportError:
	tkMessageBox.showerror(
		"Error","You are missing essential Libraries. See README.md")
	print "You are missing essential Libraries. See README.md"
	exit()


class UI(tk.Frame):

	'''
	Class that describes the UI and how the information is formatted.
	'''
	
	def __init__(self):
		
		self.init_dir()
		tk.Frame.__init__(self)
		self.image_frame = tk.Frame(self)
		self.master.title('RALC %s'%RALC_VERSION)
		self.new_data()

		self.create_widgets()
		self.grid()
		self.image_frame.grid(row=0, column=2)
		self.get_photo()
		print "UI.__init__.Done"

####
# Data Gathering
####

	def init_dir(self):
		
		dir_list = os.listdir('.')
		if 'save' not in dir_list:
			os.makedirs('save')
		if 'data' not in dir_list:
			tkMessageBox.showerror(
				"Error","You are missing your data folder.")
			exit()
		
	def new_data(self):
		
		(self.im, self.cityName,
			self.towns) = mapGen.main('tk')
		print "UI.new_data.Retrieved Data"

	def new_items(self, item_type):

		if item_type == 'wep':
			return itemGen.main('wep','rnd')

	def save_all(self, save_name):

		def make_dir():

			if not os.path.exists('save/%s'%save_name):
				os.makedirs('save/%s'%save_name)

		def save_image():

			self.im.save('save/%s/img'%save_name,'PNG')

		def save_names():

			savef = open('save/%s/name'%save_name, 'w')
			pickle.dump((self.cityName,
				self.towns),savef)
			savef.close

		make_dir()
		save_image()
		print 'UI.save_all.Image Saved'
		save_names()
		print 'UI.save_all.Names Saved'


	def load_all(self, load_name):
		
		'''
		Ensures that the save name to load is valid, then loads the
		associated content and refreshes widgets.
		'''
		
		def check_dir():

			if os.path.exists('save/%s'%load_name):
				return 1

		def load_image():

			self.im = Image.open('save/%s/img'%load_name)


		def load_names():

			savef = open('save/%s/name'%load_name, 'r')
			(self.cityName,
				self.towns) = pickle.load(savef)
			savef.close

		if check_dir():
			load_image()
			print 'UI.load_all.Loaded Image From Disk'
			load_names()
			print 'UI.load_all.Loaded Names From Disk'
			#self.loading_compensation = True
			self.create_widgets()
			self.get_photo()
			#self.loading_compensation = False
			print 'UI.load_all.Refreshed Widgets'
		else:
			print 'UI.load_all.Failed[NO FOLDER PRESENT]'

##########
# UI Init
##########
	def create_widgets(self):

		'''
		Creates menu bar, tree view and details pane.
		'''
		
		def make_menu_bar():
			
			'''
			Used for callbacks, instumental for loading/saving and
			accessing the tools/about menus. Will feature many other
			tools later.
			'''
			self.option_add('*tearOff', False)
			self.menubar = tk.Menu(self.master)
			self.filemenu = tk.Menu(self.menubar)
			self.infomenu = tk.Menu(self.menubar)
			self.toolmenu = tk.Menu(self.menubar)

			self.menubar.add_cascade(label="File", menu=self.filemenu)
			self.filemenu.add_command(label="New", command=self.new_state)
			self.filemenu.add_command(label="Save", command=self.create_save_dialog)
			self.filemenu.add_command(label="Load", command=self.create_load_dialog)
			self.filemenu.add_command(label="Exit", command=self.quit)

			self.menubar.add_cascade(label="Info", menu=self.infomenu)
			self.infomenu.add_command(label="About", command=self.create_about_dialog)

			self.menubar.add_cascade(label="Tools", menu=self.toolmenu)
			self.toolmenu.add_command(label="Char Sheet", command=self.create_char_sheet_dialog)

			self.tk.call(self.master, "config", "-menu", self.menubar)

			print 'UI.make_menu_bar.Done'

		def make_tree_view():

			'''
			Defines tree instance for use later in fill_tree
			'''
			
			self.tree = ttk.Treeview(self, height=25,
				selectmode='browse')
			ysb = ttk.Scrollbar(self, orient='vertical',
				command=self.tree.yview)
			ysb.grid(row=0, column=1, sticky='ns')
			self.tree.heading('#0', text='Name', anchor='w')
			self.tree.column('#0', width=300, anchor='w')
			self.tree.grid(row=0, column=0, sticky='NSEW')

			self.tree.bind("<<TreeviewSelect>>", self.update_details)
			print "UI.make_tree_view.Done"

		def make_details_pane():
			
			'''
			Defines first instance of the details pane.
			'''
			
			self.details_frame = ttk.Frame(self, borderwidth=2,
				relief="sunken", width=200, height=600)
			self.details = tk.Text(self.details_frame, width=50,
				height=40, state='disabled')

			self.details_frame.grid(row=0, column=4, sticky='N', pady=5)
			self.details.grid(row=0, column=0)

			print "UI.make_details_pane.Done"


		make_tree_view()
		print 'UI.create_widgets.make_tree_view.Done'
		make_menu_bar()
		make_details_pane()
		self.fill_tree()
		print 'UI.create_widgets.make_menu_bar.Done'

	def create_about_dialog(self):
		info_text = '''
RALC %s

Authored by:
Tyler Dinsmoor - (pappad@airmail.cc)
Madii Salazar - (madison.m.salazar@gmail.com)

Source:
https://github.com/Dinsmoor/ralc

Licenced under GNU GPLv2+
https://www.gnu.org/licenses/gpl-2.0.html
		'''%RALC_VERSION

		tkMessageBox.showinfo(
		"About",info_text)

	def create_load_dialog(self):
		
		'''
		Interior handler for an external class
		'''
		
		LoadDialog(self)


	def create_save_dialog(self):
		
		'''
		Interior handler for an external class
		'''
		
		SaveDialog(self)

	def create_char_sheet_dialog(self):
		
		'''
		Interior handler for an external class
		'''
		
		CharSheetGen(self)

	def load_state(self):
		
		'''
		Loads saved data and redraws widgets.
		'''
		
		self.load_all()
		self.create_widgets()
		self.get_photo()
		print 'UI.load_state.Done'

	def new_state(self):
		
		'''
		Just calles for new data and redraws widgets.
		'''
		
		self.new_data()
		self.create_widgets()
		self.get_photo()
		print 'UI.new_state.Done'

	def get_photo(self):
		
		'''
		Converts PIL/PNG image into a Tk-compatible image type, creates
		a canvas that has a clickable surface that is able to select
		settlements using a callback to city_map_select.
		'''
		
		self.img = ImageTk.PhotoImage(self.im)

		self.canvas = tk.Canvas(self.image_frame, background='grey',
			width=600, height=600)
		self.canvas.grid(row=0, column=0)
		self.canvas.create_image(301,301,state='normal',image=self.img)
		self.canvas.bind('<Button>', self.city_map_select)
		print 'UI.get_photo.Done'

	def fill_tree(self):
		
		'''
		Abandon all hope, ye who enter here.
		
		Very sensitive to upstream datatypes and needs to get better
		ways of handling invalid datatypes. Eventually will migrate
		everything to dictionaries so they can be unpacked easier later. 
		'''

		self.actor_coor = dict()
		self.town_coor = dict()
		self.city_coor = dict()
		self.item_coor = dict()
		self.click_coor = dict()
		city_population = 0

		for city_dic in self.towns:
			if city_dic['Name'] == self.cityName:
				city_parent = self.tree.insert('', 0, text=city_dic['Name'])
				self.tree.insert('', 1)
				self.click_coor[city_parent] = city_dic['click_area']
			else:
				city_parent = self.tree.insert('', 'end', text=city_dic['Name'])#,
				
				self.click_coor[city_parent] = city_dic['click_area']

			for city, city_info in city_dic.iteritems():

				if city == 'Distance':
					pass
					#self.town_coor[city_parent]
				if city == 'Data':
					for street, bldg_li in city_info.iteritems():
						# add streets
						street_parent = self.tree.insert(city_parent,
								'end', text=street, tags=street)
						for bldg in bldg_li:
							# add buildings
							bldg_parent = self.tree.insert(street_parent,
								'end', text=bldg['Purpose'])
							for rooms, roomsdata in bldg.iteritems():
								# add list of rooms
								if rooms != 'Purpose':
									rooms_parent = self.tree.insert(bldg_parent,
										'end', text=rooms)
									#bldg_item_parent = self.tree.insert(bldg_parent,
									#	'end', text='Quests')
								if type(roomsdata) == list:
									for room in roomsdata: # list
										# ensure that the room type gets parsed first
										room = col.OrderedDict(room)
										tempvalue = room.pop('Actors')
										room['Actors'] = tempvalue
										tempvalue = room.pop('Weapons')
										room['Weapons'] = tempvalue
										tempvalue = room.pop('Armor')
										room['Armor'] = tempvalue


										for key, value in room.iteritems(): # dict
											if key == 'Type':
												# add the rooms themselves
												room_parent = self.tree.insert(rooms_parent,
													'end', text=value)

											if key == 'Actors':
												if room['Actors']:
													# add the name of the actors
													actor_parent = self.tree.insert(room_parent,
														'end', text=key)
													for actor_name, actor_info in value.iteritems():
														if city_dic['Name'] == self.cityName:
															city_dic['Population'] += 1
														else:
															city_dic['Population'] += 1
														#The data of the actor
														actor = self.tree.insert(actor_parent,
															'end', text=actor_name, value=actor_info,
															tags=actor_name)

														self.actor_coor[actor] = actor_info

											if key == 'Weapons':
												if True:# bldg['Purpose'] == 'Weapon Smith':
													wep_items_parent = self.tree.insert(room_parent,
														'end', text='Weapons')
													for item_dict in value:
														item = self.tree.insert(wep_items_parent,
															'end', text=item_dict['Name'])

														self.item_coor[item] = item_dict['Name']

											if key == 'Armor':
												if True:#bldg['Purpose'] == 'Armorer':
													armor_items_parent = self.tree.insert(room_parent,
														'end', text='Armor')
													for item_dict in value:
														item = self.tree.insert(armor_items_parent,
															'end', text=item_dict['Name'])

														self.item_coor[item] = item_dict['Name']
											
											self.town_coor[city_parent] = self.make_town_metadata(city_dic)



	def make_town_metadata(self, town):
		
		desc = '''
Name:	%s
Population:	%d
Distance:	%skm to %s.
		'''%(town['Name'], town['Population'],
			town['Distance'], self.cityName)
		return desc

####
# Callbacks
####

	def find_selection_type(self, event):
		items = list()
		items.append(itemGen.main('wep','all'))
		items.append(itemGen.main('arm','all'))

	def update_details(self, event):
		
		'''
		Since multiple types fo data will be updated, it inspects various
		data sources and just plugs in whatever is applicible. Kind of dumb,
		but works. Otherwise will just empty the text box.
		'''
		
		def actor_update():
			try:
				self.details.insert('end',self.actor_coor[self.tree.focus()]['Info'])
				print "UI.update_details.Actor.Done"
			except KeyError: pass
		
		def town_update():
			try:
				self.details.insert('end',str(self.town_coor[self.tree.focus()]))
				print "UI.update_details.Town.Done"
			except KeyError: pass
		
		self.details.config(state='normal')
		self.details.delete(1.0, 'end')
		
		actor_update()
		town_update()
		self.details.config(state='disabled')

	def city_map_select(self, event):
		
		'''
		Checks click coordinates against a bounding box equivalent to
		the graphic size of the settlement sprite in a coorelation
		dictionary filled with each sprite's location.
		
		Sets selection and focus to corresponding town, then change is
		reflected in self.details automatically.
		'''
		
		for city_id, click_corner in self.click_coor.items():
			x_true = event.x >= click_corner[0] >= event.x - 20 # png is 20x20px
			y_true = event.y >= click_corner[1] >= event.y - 20
			if x_true and y_true:
				self.tree.selection_set(city_id)
				self.tree.focus(city_id)

#####
# Dialogs
#####

class CharSheetGen(tkSimpleDialog.Dialog):

	def body(self, master):
		
		'''
		Just a text box for displaying generated sheet.
		Should use pages later to specify options for a custom sheet.
		'''
		
		self.title('Character Sheet Generator')
		inst = tk.Label(master, text="Generate a random character sheet.")
		inst.grid(row=0, columnspan=2)

		self.char_text = tk.Text(master, width=50,
			height=30, state='disabled')

		self.char_text.grid(row=1, column=0)
		self.apply()


	def ok(self, event=None):
		'''
		Need to replace stock ok() because I don't want it to exit
		immediately after creating a new sheet.
		'''

		self.apply()

	def apply(self):
		char_sheet = charGen.custom_param()
		self.char_text.config(state='normal')
		self.char_text.delete(1.0, 'end')
		self.char_text.insert('end',char_sheet['Info'])
		self.char_text.config(state='disabled')



class SaveDialog(tkSimpleDialog.Dialog):

	def body(self, master):

		self.title('Save')
		tk.Label(master, text="Choose a name to save your area.").grid(row=0, columnspan=2)
		tk.Label(master, text="Save Name:").grid(row=1)
		self.e1 = tk.Entry(master)
		self.e1.grid(row=1, column=1)
		return self.e1

	def apply(self):

		save_name = str(self.e1.get())
		ui.save_all(save_name)

class LoadDialog(tkSimpleDialog.Dialog):

	def body(self, master):

		self.title('Load')
		self.file_listbox = tk.Listbox(master, selectmode='single')
		self.get_save_dir()
		tk.Label(master,
			text="Choose a name to load your area.").grid(row=0,
				columnspan=2)
		self.file_listbox.grid(row=1, columnspan=2)
		self.del_opt = bool()
		self.del_cb = tk.Button(master, text="Delete",
			command=self.delete_save).grid(row=2, columnspan=2)

	def get_save_dir(self):

		self.file_listbox.delete(0, 'end')
		dir_list = os.listdir('save')
		if '.saveloc' in dir_list:
			dir_list.remove('.saveloc')
		for subfolder in dir_list:
			self.file_listbox.insert('end', subfolder)
		print "LoadDialog.get_save_dir.Done"

	def delete_save(self):

		selected = self.file_listbox.curselection()
		del_name = str(self.file_listbox.get(selected))
		try:
			shutil.rmtree('save/%s'%del_name)
			print "LoadDialog.delete_save.Done"
		except OSError:
			print "LoadDialog.delete_save.OSError['Item not a Dir?']"
		self.get_save_dir()


	def apply(self):

		selected = self.file_listbox.curselection()
		load_name = str(self.file_listbox.get(selected))
		ui.load_all(load_name)

ui = UI()
ui.mainloop()
