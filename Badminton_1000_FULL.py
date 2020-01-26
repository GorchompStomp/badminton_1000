# Byron Jones   bjone079@uottawa.ca
# This program is for organising badminton rounds.
# The badminton club I will use it for is doubles play, with 4 available courts.

import random
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled
from tkinter import messagebox
import csv
from operator import itemgetter
import datetime
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog


class Badminton:

    def __init__(self, master):

        # *** Accessible variable(s), see load() for others ***

        self.total = [0]

        # self.mainframe has all wigets except top menu, and listboxes
        # Create & Configure root
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        # Create & Configure frame
        self.mainframe = Frame(master)
        self.mainframe.grid(row=0, column=0, sticky='nsew')

        # Create a 5x3 (rows x columns) grid of buttons inside the frame

        Grid.rowconfigure(self.mainframe, 1, weight=1)
        for col_index in range(3):
            Grid.columnconfigure(self.mainframe, col_index, weight=1)

        # *** Top Menu ***

        self.menubar = Menu(master, tearoff=0)

        filemenu = Menu(self.menubar, tearoff=0)

        filemenu.add_command(label="Load", command=self.load)

        filemenu.add_command(label="Save", command=self.save)

        filemenu.add_command(label="Save as", command=self.save_as)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.destroy)

        self.menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=self.menubar)

        # *** self.mainframe wigets ***

        # *** toolbar ***

        self.toolbar_frame = Frame(self.mainframe, bg='grey')
        self.toolbar_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

        self.add_button = Button(
            self.toolbar_frame, text="Edit Player", command=self.edit_player)
        self.add_button.pack(side="left", pady=2, padx=2)

        self.remove_button = Button(
            self.toolbar_frame, text="New Player", command=self.new_player)
        self.remove_button.pack(side="left", pady=2, padx=2)

        self.new_player_button = Button(
            self.toolbar_frame, text="Delete Player", command=self.delete_player)
        self.new_player_button.pack(side="left", pady=2, padx=2)

        self.partner_button = Button(
            self.toolbar_frame, text="Change Partnership", command=self.partner)
        self.partner_button.pack(side="left", pady=2, padx=2)

        # *** Round Display ***

        self.round_display_frame = Frame(self.mainframe)

        self.new_round_button = Button(
            self.round_display_frame, text="New Round", font=0, command=self.new_game)

        self.new_round_button.focus()
        self.new_round_button.bind("<Return>", self.new_game)

        self.round_display = tkscrolled.ScrolledText(
            self.round_display_frame, undo=True, width=30, height=27, font=0)

        self.round_label_text = StringVar()
        self.round_label_text.set('Round ' + str(self.total[0]) + ' Display')

        self.round_label = Label(self.round_display_frame,
                                 textvariable=self.round_label_text, font=10)

        self.round_display.grid(row=1, column=0, padx=2, pady=2, sticky='nsew')

        self.new_round_button.grid(row=1, column=2, pady=2, padx=2, sticky='w')

        self.round_label.grid(row=0, columnspan=3)

        self.round_display_frame.rowconfigure(1, weight=1)

        self.round_display_frame.grid_columnconfigure(0, weight=1)

        self.round_display_frame.grid(row=1, column=1, sticky='nsew')

        # ***Remove Player Frame ***

        remove_frame = Frame(self.mainframe, bd=2, relief=SUNKEN, bg='light gray')

        self.remove_listbox = Listbox(remove_frame, font=0, width=30)
        self.remove_scrollbar = Scrollbar(remove_frame, orient=VERTICAL)
        self.remove_listbox.config(yscrollcommand=self.remove_scrollbar.set)
        self.remove_scrollbar.config(command=self.remove_listbox.yview)

        self.remove_button = Button(
            remove_frame, text="Remove Player", font=0, command=self.remove_player)

        self.remove_label = Label(
            remove_frame, text='Currently Playing', bg='light gray', font=10)

        self.remove_listbox.bind("<Double-Button-1>", self.remove_player)
        self.remove_listbox.bind("<ButtonRelease-1>", self.label_update)

        self.remove_listbox.grid(row=1, sticky='nsew')

        self.remove_scrollbar.grid(row=1, column=1, sticky='ns')

        self.remove_button.grid(row=1, column=2, padx=2)

        self.remove_label.grid(row=0, columnspan=3)

        remove_frame.rowconfigure(1, weight=1)

        remove_frame.grid_columnconfigure(0, weight=1)

        remove_frame.grid(row=1, column=0, sticky='nsew')

        # *** Add Player Frame ***

        add_frame = Frame(self.mainframe, bd=2, relief=SUNKEN, bg='light gray')

        self.add_listbox = Listbox(add_frame, font=0, width=30)
        self.add_scrollbar = Scrollbar(add_frame, orient=VERTICAL)
        self.add_listbox.config(yscrollcommand=self.add_scrollbar.set)

        self.add_scrollbar.config(command=self.add_listbox.yview)

        self.add_button = Button(add_frame, text="Add Player",
                                 font=0, command=self.add_player)

        self.add_label = Label(add_frame, text='Not Playing',
                               bg='light gray', font=10)

        self.add_listbox.bind("<Double-Button-1>", self.add_player)
        self.add_listbox.bind("<ButtonRelease-1>", self.label_update)

        self.add_listbox.grid(row=1, sticky='nsew')

        self.add_scrollbar.grid(row=1, column=1, sticky='ns')

        self.add_button.grid(row=1, column=2, padx=2, sticky='e')

        self.add_label.grid(row=0, columnspan=3)

        add_frame.rowconfigure(1, weight=1)

        add_frame.grid_columnconfigure(0, weight=1)

        add_frame.grid(row=1, column=2, sticky='nsew')

        # ***Status bar ***

        self.status_bar_frame = Frame(self.mainframe)

        self.text_display = StringVar()
        self.text_display.set(
            'Displays name, skill group, and number of games played ^^')

        self.info = Label(self.mainframe, textvariable=self.text_display,
                          fg="blue", bd=1, font=0, relief=SUNKEN, anchor=W)
        self.info.grid(row=2, column=0, columnspan=3, sticky='ew', padx=2)

        self.load()

        

    def partner(self, *args):

        self.partner_top = Toplevel(self.mainframe)
        self.partner_top.title("Partner Menu")

        self.full_list = sorted(self.playing_list_str + self.not_playing_list_str)

    # *** Selector 1 Frame ***

        self.partner_1_select = Frame(
            self.partner_top, bd=2, relief=SUNKEN, bg='light gray')

        self.partner_1_listbox = Listbox(
            self.partner_1_select, font=0, width=30, height=20)
        self.partner_1_scrollbar = Scrollbar(self.partner_1_select, orient=VERTICAL)
        self.partner_1_listbox.config(yscrollcommand=self.partner_1_scrollbar.set)

        self.partner_1_scrollbar.config(command=self.partner_1_listbox.yview)

        self.partner_1_label = Label(
            self.partner_1_select, text='Select First Partner',  bg='light gray', font=10)

        self.partner_1_label.grid(row=0, column=0, columnspan=3)

        self.partner_1_listbox.grid(row=1, sticky='nsew')

        self.partner_1_scrollbar.grid(row=1, column=1, sticky='ns')

        self.partner_1_select.rowconfigure(1, weight=1)

        self.partner_1_select.grid_columnconfigure(0, weight=1)

        self.partner_1_select.grid(row=0, column=0, sticky='nsew')

        for player in self.full_list:
            self.partner_1_listbox.insert(END, player)

        self.partner_1_listbox.bind("<ButtonRelease-1>", self.partner_box_update)

    # *** Partner Buttons ***

        self.partner_buttons = Frame(self.partner_top, width=30)

        self.partner_text_var = StringVar(value='partner info displayed here')

        self.partner_label = Label(
            self.partner_buttons, textvariable=self.partner_text_var, font=0, width=30, height=3)
        self.partner_label.pack(side='top', pady=20, padx=5)

        self.create_partner_button = Button(
            self.partner_buttons, text="Create Partnership", command=self.create_partner)
        self.create_partner_button.pack(side='top', pady=20, padx=5)

        self.break_partner_button = Button(
            self.partner_buttons, text="Break Partnership", command=self.break_partner)
        self.break_partner_button.pack(side="top", pady=20, padx=5)

        self.break_partner_button = Button(
            self.partner_buttons, text="Change Partner Skill", command=self.change_partner_skill)
        self.break_partner_button.pack(side="top", pady=20, padx=5)

        self.partner_buttons.grid(row=0, column=1)

        self.partner_1 = []

        self.partner_2 = []

    def change_partner_skill(self, *args):

        self.change_1 = self.partner_1_listbox.curselection()  

        if self.change_1 == ():
            messagebox.showerror('None Selected', 'Please select someone with a partner to change their skill.')
            self.partner_top.destroy()
            self.partner()
            return

        for i in range(0, len(self.master_list)):
            if self.master_list[int(i)]['name'] == str(self.full_list[self.change_1[0]]):
                self.change_1 = self.master_list[i]['name']
                self.change_1_skill = self.master_list[i]['skill']
                self.change_2 = self.master_list[i]['partner name']
                self.change_2_skill = self.master_list[i]['skill']
                break
                
        self.partner_skill_change_top = Toplevel(self.partner_top)
        self.partner_skill_change_top.title("Select New Skill")

        self.change_partner_skill_entry_frame = Frame(self.partner_skill_change_top)

        self.change_partner_skill_label = Label(self.change_partner_skill_entry_frame, text=('Please select the Skill level of\n'
                              + self.change_1 + ' and ' + self.change_2 + ' together.'), font=0, width=40, height=5)
        self.change_partner_skill_label.grid(row=0, column=0, columnspan=2)

        self.change_partner_skill = IntVar()
        self.change_partner_skill.set(2)
        self.change_partner_skill_label = Label(
            self.change_partner_skill_entry_frame, text='Skill level: ', font=0)
        self.change_partner_skill_menu = OptionMenu(
            self.change_partner_skill_entry_frame, self.change_partner_skill, 1, 2, 3, 4)

        self.change_partner_skill_label.grid(row=1, column=0, pady=20, padx=2)
        self.change_partner_skill_menu.grid(row=1, column=1, pady=20, padx=2)

        self.change_partner_skill_entry_button = Button(
            self.change_partner_skill_entry_frame, text='Confirm', command=self.partner_skill_change_confirm, font=0)
        self.change_partner_skill_entry_button.grid(row=2, columnspan=2, pady=10)

        self.change_partner_skill_entry_frame.grid_columnconfigure(0, weight=1)
        self.change_partner_skill_entry_frame.grid(row=0, column=0)
        pass

    def partner_skill_change_confirm(self, *args):
        
        MsgBox = messagebox.askyesno('Are you sure?', 'You want to change the partner skill of:\n' + self.change_1 + '\nand '
                                     + self.change_2 + '\'s skill level to: ' + str(self.change_partner_skill.get()) + '?')

        if MsgBox == True:
                    for i in range(0, len(self.master_list)):
                        if self.master_list[i]['name'] == self.change_1:
                            for x in range(0, len(self.master_list)):
                                if self.master_list[x]['name'] == self.change_2:
                                    self.master_list[i]['skill'] = self.change_partner_skill.get()
                                    self.master_list[x]['skill'] = self.change_partner_skill.get()

                                    SaveBox = messagebox.askyesno('Change Complete!', 'You have just Changed the skill of ' + self.change_1
                                            + ' and ' + self.change_2
                                            + '! Would you like to save?', icon='question')

                                    if SaveBox == True:
                                        self.partner_top.destroy()
                                        self.partner_skill_change_top.destroy()
                                        self.save()
                                        return

                                    else:

                                        self.partner_top.destroy()
                                        self.partner_skill_change_top.destroy()
                                        return
        

    def break_partner(self, *args):
        
        self.break_1 = self.partner_1_listbox.curselection()

        if self.partner_1_listbox.curselection() == ():
            messagebox.showerror('None Selected', 'Please select someone with a partner to breakup.')
            self.partner_top.destroy()
            self.partner()
            return

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[self.break_1[0]]):
                if self.master_list[i]['partner name'] == '':
                    MsgBox = messagebox.showerror('No one to breakup with!',self.master_list[i]['name'] + 'does\'t have a partner!'\
                                 + '\nPlease select someone who has a partner to break.', icon='error')

                    self.partner_top.destroy()
                    self.partner()
                    return

        for i in range(0, len(self.master_list)):
            if self.master_list[int(i)]['name'] == str(self.full_list[self.break_1[0]]):
                self.break_1 = self.master_list[i]['name']
                self.break_1_skill = self.master_list[i]['skill']
                self.break_2 = self.master_list[i]['partner name']
                self.break_2_skill = self.master_list[i]['skill']
                self.create_break_skill()
                return

    def create_break_skill(self, *args):

        self.break_skill_top = Toplevel(self.partner_top)
        self.break_skill_top.title("Select Skill")

        self.edit_break_skill_entry_frame = Frame(self.break_skill_top)

        self.edit_break_skill_1_label = Label(self.edit_break_skill_entry_frame, text='Please select the Skill level of\n'
                              + self.break_1
                              , font=0, width=30, height=5)

        self.edit_break_skill_1_label.grid(row=0, column=0, columnspan=2)

        self.edit_break_skill_1 = IntVar()
        self.edit_break_skill_1.set(self.break_1_skill)
        self.edit_break_skill_1_label = Label(
            self.edit_break_skill_entry_frame, text='Skill level: ', font=0)
        self.edit_break_skill_1_menu = OptionMenu(
            self.edit_break_skill_entry_frame, self.edit_break_skill_1, 1, 2, 3, 4)

        self.edit_break_skill_1_label.grid(row=1, column=0, pady=20, padx=2, columnspan = 2)
        self.edit_break_skill_1_menu.grid(row=1, column=1, pady=20, padx=2)
        

        self.edit_break_skill_2_label = Label(self.edit_break_skill_entry_frame, text='Please select the Skill level of\n'
                              + self.break_2
                              , font=0, width=30, height=5)

        self.edit_break_skill_2_label.grid(row=2, column=0, columnspan=2)

        self.edit_break_skill_2 = IntVar()
        self.edit_break_skill_2.set(self.break_2_skill)
        self.edit_break_skill_2_label = Label(
            self.edit_break_skill_entry_frame, text='Skill level: ', font=0)
        self.edit_break_skill_2_menu = OptionMenu(
            self.edit_break_skill_entry_frame, self.edit_break_skill_2, 1, 2, 3, 4)

        self.edit_break_skill_2_label.grid(row = 3, column=0, pady=20, padx=2)
        self.edit_break_skill_2_menu.grid(row = 3, column=1, pady=20, padx=2)

        self.edit_break_skill_entry_button = Button(
            self.edit_break_skill_entry_frame, text='Confirm', command=self.break_confirm, font=0)
        self.edit_break_skill_entry_button.grid(row=4, columnspan=2, pady=10)

        self.edit_break_skill_entry_frame.grid_columnconfigure(0, weight=1)
        self.edit_break_skill_entry_frame.grid(row=0, column=0)

    def break_confirm(self, *args):
        MsgBox = messagebox.askyesno('Are you sure?', 'You want to breakup:\n' + self.break_1
                        + '\nand\n' + self.break_2 + '\nand set ' + self.break_1 + '\'s skill level to: ' + str(self.edit_break_skill_1.get()) +
                                     '\nand set ' + self.break_2 + '\'s skill level to: ' + str(self.edit_break_skill_2.get()) + '?')

        if MsgBox == True:
                    for i in range(0, len(self.master_list)):
                        if self.master_list[i]['name'] == self.break_1:
                            for x in range(0, len(self.master_list)):
                                if self.master_list[x]['name'] == self.break_2:
                                    self.master_list[i]['partner name'] = ''
                                    self.master_list[x]['partner name'] = ''
                                    self.master_list[i]['skill'] = self.edit_break_skill_1.get()
                                    self.master_list[x]['skill'] = self.edit_break_skill_2.get()

                                    SaveBox = messagebox.askyesno('break Complete!', 'You have just brokenup ' + self.break_1
                                            + ' and ' + self.break_2
                                            + '! Would you like to save?', icon='question')

                                    if SaveBox == True:
                                        self.partner_top.destroy()
                                        self.break_skill_top.destroy()
                                        self.save()
                                        return

                                    else:

                                        self.partner_top.destroy()
                                        self.break_skill_top.destroy()
                                        return

    def partner_box_update(self, *args):

        self.partner_1 = self.partner_1_listbox.curselection()

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[self.partner_1[0]]):
                if self.master_list[i]['partner name'] == '':
                    self.partner_text_var.set(self.master_list[i]['name'] + '\nhas no partner.')

                else:
                    self.partner_text_var.set(self.master_list[i]['name'] + '\nis partnered with:\n' + self.master_list[i]['partner name'])

    def create_partner(self, *args):

        if self.partner_1_listbox.curselection() == ():
            messagebox.showerror('None Selected', 'Please select someone without a partner to make a partnership with.')
            self.partner_top.destroy()
            self.partner()
            return

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[self.partner_1[0]]):
                if self.master_list[i]['partner name'] != '':
                    MsgBox = messagebox.showerror('Player Already has partner', self.master_list[i]['name'] + '\nis already partnered with:\n' + self.master_list[i]['partner name']
                                 + '\nPlease end their partnership before starting a new one.', icon='error')

                    self.partner_top.destroy()
                    self.partner()
                    return

        self.partner_create_top = Toplevel(self.mainframe)
        self.partner_create_top.title("Select Partner")

        self.full_list = sorted(self.playing_list_str + self.not_playing_list_str)

    # *** Selector 2 Frame ***

        self.partner_create_select = Frame(
            self.partner_create_top, bd=2, relief=SUNKEN, bg='light gray')

        self.partner_create_listbox = Listbox(
            self.partner_create_select, font=0, width=30, height=20)
        self.partner_create_scrollbar = Scrollbar(
            self.partner_create_select, orient=VERTICAL)
        self.partner_create_listbox.config(
            yscrollcommand=self.partner_create_scrollbar.set)

        self.partner_create_scrollbar.config(
            command=self.partner_create_listbox.yview)

        self.partner_create_label = Label(
            self.partner_create_select, text='Select Second Partner',  bg='light gray', font=10)

        self.partner_create_label.grid(row=0, column=0, columnspan=3)

        self.partner_create_listbox.grid(row=1, sticky='nsew')

        self.partner_create_scrollbar.grid(row=1, column=1, sticky='ns')

        self.partner_create_select.rowconfigure(1, weight=1)

        self.partner_create_select.grid_columnconfigure(0, weight=1)

        self.partner_create_select.grid(row=0, column=0, sticky='nsew')

        for player in self.full_list:
            self.partner_create_listbox.insert(END, player)


    # *** partner_create Buttons ***

        self.partner_create_buttons = Frame(self.partner_create_top, width=30)

        self.partner_create_text_var = StringVar(
            value='Who would you like to partner with:\n' + str(self.full_list[self.partner_1[0]]) + '?')

        self.partner_create_label = Label(
            self.partner_create_buttons, textvariable=self.partner_create_text_var, font=0, width=30, height=4)
        self.partner_create_label.pack(side='top', pady=20, padx=5)

        self.create_partner_create_button = Button(
            self.partner_create_buttons, text="Select partner", command=self.confirm_create_partner)
        self.create_partner_create_button.pack(side='top', pady=20, padx=5)

        self.partner_create_buttons.grid(row=0, column=1)

        self.partner_create_listbox.bind(
            "<ButtonRelease-1>", self.partner_create_box_update)

    def partner_create_box_update(self, *args):

        self.partner_2 = self.partner_create_listbox.curselection()

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[self.partner_1[0]]):

                for e in range(0, len(self.master_list)):
                    if self.master_list[e]['name'] == str(self.full_list[self.partner_2[0]]):
                        self.partner_create_text_var.set('Would you like to partner:\n' + self.master_list[i]['name']
                                          + '\nwith\n' + self.master_list[e]['name'] + '?')
                        return

    def confirm_create_partner(self, *args):

        self.partner_2 = self.partner_create_listbox.curselection()

        if self.partner_2 == ():
            messagebox.showerror(  
                'Please select partner', 'Please select a partner.', icon='error')
            self.partner_create_top.destroy()
            self.partner_top.destroy()
            self.partner()
            return

        if str(self.full_list[self.partner_1[0]]) == str(self.full_list[self.partner_2[0]]):
            messagebox.showerror(
                'Can\'t self partner', 'Sorry you cannot partner a player with themselves', icon='error')
            self.partner_create_top.destroy()
            self.partner_top.destroy()
            self.partner()
        
        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[self.partner_2[0]]):
                if self.master_list[i]['partner name'] != '' and self.partner_2 != ():
                    messagebox.showwarning('Already has a partner!', self.master_list[i]['name'] + '\nis already partnered with\n' + self.master_list[i]['partner name']
                                + '\nplease end their partnership before making a new one.', icon='warning')
                    self.partner_create_top.destroy()
                    self.partner_top.destroy()
                    self.partner()
                    return

                elif self.partner_2 == ():
                    messagebox.showerror(
                        'Please select partner', 'Please select a partner.', icon='error')
                    self.partner_create_top.destroy()
                    self.partner_top.destroy()
                    self.partner()
                    return

                else:
                    self.create_partner_skill()
                    return
        
    def create_partner_skill(self, *args):

        self.partner_skill_top = Toplevel(self.partner_create_top)
        self.partner_skill_top.title("Select Skill")

        self.edit_partner_skill_entry_frame = Frame(self.partner_skill_top)

        self.edit_partner_skill_label = Label(self.edit_partner_skill_entry_frame, text='Please select the Skill level of\n'
                              + str(self.full_list[self.partner_2[0]])
                              + ' and ' + str(self.full_list[self.partner_1[0]]) + ' together', font=0, width=30, height=5)
        self.edit_partner_skill_label.grid(row=0, column=0, columnspan=2)

        self.edit_partner_skill = IntVar()
        self.edit_partner_skill.set(2)
        self.edit_partner_skill_label = Label(
            self.edit_partner_skill_entry_frame, text='Skill level: ', font=0)
        self.edit_partner_skill_menu = OptionMenu(
            self.edit_partner_skill_entry_frame, self.edit_partner_skill, 1, 2, 3, 4)

        self.edit_partner_skill_label.grid(row=1, column=0, pady=20, padx=2)
        self.edit_partner_skill_menu.grid(row=1, column=1, pady=20, padx=2)

        self.edit_partner_skill_entry_button = Button(
            self.edit_partner_skill_entry_frame, text='Confirm', command=self.partner_confirm, font=0)
        self.edit_partner_skill_entry_button.grid(row=2, columnspan=2, pady=10)

        self.edit_partner_skill_entry_frame.grid_columnconfigure(0, weight=1)
        self.edit_partner_skill_entry_frame.grid(row=0, column=0)

    def partner_confirm(self, *args):
        MsgBox = messagebox.askyesno('Are you sure?', 'You want to partner:\n' + str(self.full_list[self.partner_2[0]])
                        + '\nand\n' + str(self.full_list[self.partner_1[0]]) + '\nAt skill level ' + str(self.edit_partner_skill.get()) + '?')

        if MsgBox == True:
            for i in range(0, len(self.master_list)):
                if self.master_list[i]['name'] == str(self.full_list[self.partner_2[0]]):
                    for x in range(0, len(self.master_list)):
                        if self.master_list[x]['name'] == str(self.full_list[self.partner_1[0]]):
                            self.master_list[i]['partner name'] = self.master_list[x]['name']
                            self.master_list[x]['partner name'] = self.master_list[i]['name']
                            self.master_list[i]['skill'] = self.edit_partner_skill.get()
                            self.master_list[x]['skill'] = self.edit_partner_skill.get()

                            SaveBox = messagebox.askyesno('Partner Complete!', 'You have just made ' + str(self.full_list[self.partner_2[0]])
                                  + ' and ' + str(self.full_list[self.partner_1[0]])
                                  + ' partners! Would you like to save?', icon='question')

                            if SaveBox == True:
                                self.partner_create_top.destroy()
                                self.partner_top.destroy()
                                self.partner_skill_top.destroy()
                                self.save()
                                return

                            else:

                                self.partner_create_top.destroy()
                                self.partner_top.destroy()
                                self.partner_skill_top.destroy()
                                return

    def edit_player(self, *args):

        self.edit_top = Toplevel(self.mainframe)
        self.edit_top.title("Edit Player")

    # *** Selector Frame ***

        edit_select = Frame(self.edit_top, bd = 2, relief = SUNKEN, bg = 'light gray')

        self.edit_listbox = Listbox(edit_select, font = 0, width = 30, height = 20)
        self.edit_scrollbar = Scrollbar(edit_select, orient = VERTICAL)
        self.edit_listbox.config(yscrollcommand = self.edit_scrollbar.set)

        self.edit_scrollbar.config(command = self.edit_listbox.yview)

        self.edit_label = Label(edit_select, text = 'Select Member to Edit',  bg = 'light gray', font = 10)

        self.edit_label.grid(row = 0, column = 0, columnspan = 3)



        self.edit_listbox.grid(row = 1, sticky = 'nsew')

        self.edit_scrollbar.grid(row = 1, column = 1, sticky = 'ns')



        edit_select.rowconfigure(1, weight = 1)

        edit_select.grid_columnconfigure(0, weight=1)


        edit_select.grid(row = 0, column = 0, sticky = 'nsew')




    # *** Populate Edit listbox ***


        self.full_list = self.playing_list_str + self.not_playing_list_str

        for player in self.full_list:
            self.edit_listbox.insert(END, player)


    # *** Info Frame ***

        self.edit_entry_frame = Frame(self.edit_top)

        self.edit_current_name = StringVar()
        self.edit_current_name_label = Label(self.edit_entry_frame, textvariable = self.edit_current_name, font = 0)
        self.edit_current_name_label.grid(row = 0, column = 1, columnspan = 2)

        self.edit_name = StringVar()
        self.edit_name_label = Label(self.edit_entry_frame, text = 'New Name: ', font = 0)
        self.edit_name_entry = Entry(self.edit_entry_frame, textvariable = self.edit_name, font = 0, width = 30)

        self.edit_name_label.grid(row = 1, column = 0, sticky = 'e')
        self.edit_name_entry.grid(row = 1, column = 1, columnspan = 2, padx = 2)

        self.edit_current_email = StringVar()
        self.edit_current_email_label = Label(self.edit_entry_frame, textvariable = self.edit_current_email, font = 0)
        self.edit_current_email_label.grid(row = 2, column = 1, columnspan = 2)

        self.edit_email = StringVar()
        self.edit_email_label = Label(self.edit_entry_frame, text = 'New Email: ', font = 0)
        self.edit_email_entry = Entry(self.edit_entry_frame, textvariable = self.edit_email, font = 0, width = 30)

        self.edit_email_label.grid(row = 3, column = 0, sticky = 'e')
        self.edit_email_entry.grid(row = 3, column = 1, columnspan = 2, padx = 2)


        self.edit_current_method = StringVar()
        self.edit_current_method_label = Label(self.edit_entry_frame, textvariable = self.edit_current_method, font = 0)
        self.edit_current_method_label.grid(row = 4, column = 1, columnspan = 2)

        self.edit_method = StringVar()
        self.edit_method_label = Label(self.edit_entry_frame, text = 'New method + (dd/mm/yy): ', font = 0)
        self.edit_method_entry = Entry(self.edit_entry_frame, textvariable = self.edit_method, font = 0, width = 30)

        self.edit_method_label.grid(row = 5, column = 0, sticky = 'e')
        self.edit_method_entry.grid(row = 5, column = 1, columnspan = 2, padx = 2)


        self.edit_current_pay = StringVar()
        self.edit_current_pay_label = Label(self.edit_entry_frame, textvariable = self.edit_current_pay, font = 0)
        self.edit_current_pay_label.grid(row = 6, column = 1, columnspan = 2)

        self.edit_pay = StringVar()
        self.edit_pay_label = Label(self.edit_entry_frame, text = 'Pay Received?: ', font = 0)
        self.edit_pay_label.grid(row = 7, column = 0, sticky = 'e')
        Radiobutton(self.edit_entry_frame, text="Yes", variable = self.edit_pay, value = 'Yes', font = 0).grid(row = 7, column = 1, sticky = 'w')
        Radiobutton(self.edit_entry_frame, text="No", variable = self.edit_pay, value = 'No', font = 0).grid(row = 7, column = 2, sticky = 'w')

        self.edit_current_skill = StringVar()
        self.edit_current_skill_label = Label(self.edit_entry_frame, textvariable = self.edit_current_skill, font = 0)
        self.edit_current_skill_label.grid(row = 8, column = 1, columnspan = 2)

        self.edit_skill = IntVar()
        self.edit_skill_label = Label(self.edit_entry_frame, text = 'Skill level: ', font = 0)
        self.edit_skill_menu = OptionMenu(self.edit_entry_frame, self.edit_skill, 1, 2, 3, 4)

        self.edit_skill_label.grid(row = 9, column = 0, sticky = 'e')
        self.edit_skill_menu.grid(row = 9, column = 1, columnspan = 2)

        self.edit_entry_frame.grid_columnconfigure(0, weight=1)
        self.edit_entry_frame.grid(row = 0, column = 1)

        self.edit_listbox.bind("<ButtonRelease-1>", self.edit_box_update)

        self.edit_confirm_button = Button(self.edit_entry_frame, text = 'Confirm', command = self.edit_player_confirm, font = 0)
        self.edit_confirm_button.grid(row = 10, column = 0, columnspan = 3)


    def edit_box_update(self, *args):

        player = self.edit_listbox.curselection()

        self.edit_skill_menu.configure(state="active")

        self.edit_skill_label = Label(self.edit_entry_frame, text = 'Skill level: ', font = 0)


        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.full_list[player[0]]):

                self.edit_name.set(self.master_list[i]['name'])
                self.edit_current_name.set(self.master_list[i]['name'])

                self.edit_email.set(self.master_list[i]['uOttawa Email'])
                self.edit_current_email.set(self.master_list[i]['uOttawa Email'])

                self.edit_method.set(self.master_list[i]['Method of payment'])
                self.edit_current_method.set(self.master_list[i]['Method of payment'])

                self.edit_pay.set(self.master_list[i]['Paid Yet?'])
                self.edit_current_pay.set(self.master_list[i]['Paid Yet?'])

                self.edit_skill.set(self.master_list[i]['skill'])
                self.edit_current_skill.set(self.master_list[i]['skill'])

                if self.master_list[i]['partner name'] != '':
                    
                    self.edit_skill_menu.configure(state="disabled")
                    self.edit_current_skill.set('Can\'t change skill because\n they have a partner.\nBreakup, or change partner skill.\nCurrent partner skill: ' + str(self.master_list[i]['skill']))
                    self.edit_skill_label = Label(self.edit_entry_frame, text = 'Skill level: ', font = 0, height = 4)
                    self.edit_skill.set(self.master_list[i]['skill'])
                            
                    return
        
    def edit_player_confirm(self, *args):

        if self.edit_current_name.get() == '':
            messagebox.showerror('None selected error', 'Please select a player from the list to edit.')
            self.edit_top.destroy()
            self.edit_player()

            return

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.edit_current_name.get()):

                MsgBox = messagebox.askyesno('Are you sure?',\
                                'Is this correct? \nName: ' + str(self.edit_name.get()) \
                                    + '\nemail: ' + str(self.edit_email.get())\
                                    + '\npayment method: ' + str(self.edit_method.get()) \
                                    + '\npayment received?: ' + str(self.edit_pay.get())\
                                    + '\nSkill level: ' + str(self.edit_skill.get())\
                                    ,icon = 'warning')

                if MsgBox == True:

                    self.master_list[i]['name'] = self.edit_name.get()

                    self.master_list[i]['uOttawa Email'] = self.edit_email.get()

                    self.master_list[i]['Method of payment'] = self.edit_method.get()

                    self.master_list[i]['Paid Yet?'] = self.edit_pay.get()

                    self.master_list[i]['skill'] =  self.edit_skill.get()

                    self.populate_listboxes()

                    SaveBox = messagebox.askyesno('Save?', 'Player edited! Would you like to save changes?', icon = 'question')

                    if SaveBox == True:

                        self.save()

                    self.edit_entry_frame.destroy()

                else:

                    self.edit_entry_frame.destroy()

                    self.edit_player()

                return

    def new_player(self, *args):

        self.new_top = Toplevel(self.mainframe)
        self.new_top.title("New Player")

        self.new_entry_frame = Frame(self.new_top, padx = 2, pady = 2)



        self.new_name = StringVar()
        self.new_name_label = Label(self.new_entry_frame, text = 'Full Name: ', font = 0)
        self.new_name_entry = Entry(self.new_entry_frame, textvariable = self.new_name, font = 0, width = 30)

        self.new_name_label.grid(row = 1, column = 0, sticky = 'e')
        self.new_name_entry.grid(row = 1, column = 1, columnspan = 2, padx = 2)


        self.new_email = StringVar()
        self.new_email_label = Label(self.new_entry_frame, text = 'Email: ', font = 0)
        self.new_email_entry = Entry(self.new_entry_frame, textvariable = self.new_email, font = 0, width = 30)

        self.new_email_label.grid(row = 3, column = 0, sticky = 'e')
        self.new_email_entry.grid(row = 3, column = 1, columnspan = 2, padx = 2)



        self.new_method = StringVar()
        self.new_method_label = Label(self.new_entry_frame, text = 'Payment method + (dd/mm/yy): ', font = 0)
        self.new_method_entry = Entry(self.new_entry_frame, textvariable = self.new_method, font = 0, width = 30)

        self.new_method_label.grid(row = 5, column = 0, sticky = 'e')
        self.new_method_entry.grid(row = 5, column = 1, columnspan = 2, padx = 2)


        self.new_pay = StringVar()
        self.new_pay_label = Label(self.new_entry_frame, text = 'Pay Received?: ', font = 0)
        self.new_pay_label.grid(row = 7, column = 0, sticky = 'e')
        Radiobutton(self.new_entry_frame, text="Yes", variable = self.new_pay, value = 'Yes', font = 0).grid(row = 7, column = 1, sticky = 'w')
        Radiobutton(self.new_entry_frame, text="No", variable = self.new_pay, value = 'No', font = 0).grid(row = 7, column = 2, sticky = 'w')



        self.new_skill = IntVar()
        self.new_skill_label = Label(self.new_entry_frame, text = 'Skill level: ', font = 0)
        self.new_skill_menu = OptionMenu(self.new_entry_frame, self.new_skill, 1, 2, 3, 4)

        self.new_skill_label.grid(row = 9, column = 0, sticky = 'e')
        self.new_skill_menu.grid(row = 9, column = 1, columnspan = 2)

        self.new_entry_frame.grid_columnconfigure(0, weight=1)
        self.new_entry_frame.grid(row = 0, column = 1)



        self.new_confirm_button = Button(self.new_entry_frame, text = 'Confirm', command = self.new_player_confirm, font = 0)
        self.new_confirm_button.grid(row = 10, column = 0, columnspan = 3)

    def new_player_confirm(self, *args):

        if self.new_name.get() == '':
            messagebox.showerror('Name error', 'Player must have a name.')
            self.new_top.destroy()
            self.new_player()

            return

        MsgBox = messagebox.askyesno('Are you sure?',\
                        'Is this correct? \nName: ' + str(self.new_name.get()) \
                            + '\nemail: ' + str(self.new_email.get())\
                            + '\npayment method: ' + str(self.new_method.get()) \
                            + '\npayment received?: ' + str(self.new_pay.get())\
                            + '\nSkill level: ' + str(self.new_skill.get())\
                            ,icon = 'warning')

        if MsgBox == True:

            new_player = {'C' : '','name' : self.new_name.get(), 'uOttawa Email' : self.new_email.get(), 'Method of payment' : self.new_method.get()\
                  , 'Paid Yet?' : self.new_pay.get(), 'skill' : self.new_skill.get(), 'games' : 0, 'playing' : 1}

            self.master_list.append(new_player)

            self.populate_listboxes()

            newbox = messagebox.showinfo('New Player Confirm', 'Player added!')

            SaveBox = messagebox.askyesno('Save?', 'Would you like to save changes?', icon = 'question')

            if SaveBox == True:

                self.save()

            self.new_entry_frame.destroy()

        else:

            self.new_entry_frame.destroy()

            self.new_player()

    def delete_player(self, *args):

        self.delete_top = Toplevel(self.mainframe)
        self.delete_top.title("Delete Player")


        self.delete_select = Frame(self.delete_top, bd = 2, relief = SUNKEN, bg = 'light gray')

        self.delete_listbox = Listbox(self.delete_select, font = 0, width = 30, height = 20)
        self.delete_scrollbar = Scrollbar(self.delete_select, orient = VERTICAL)
        self.delete_listbox.config(yscrollcommand = self.delete_scrollbar.set)

        self.delete_scrollbar.config(command = self.delete_listbox.yview)

        self.delete_label = Label(self.delete_select, text = 'Select Member to delete',  bg = 'light gray', font = 10)

        self.delete_label.grid(row = 0, column = 0, columnspan = 3)

        self.delete_listbox.bind("<Double-Button-1>", self.confirm_delete)

        self.delete_listbox.grid(row = 1, sticky = 'nsew')

        self.delete_scrollbar.grid(row = 1, column = 1, sticky = 'ns')

        self.delete_button = Button(self.delete_select, text = "Delete", font = 0, command = self.confirm_delete)

        self.delete_button.grid(row = 1, column = 2, padx = 2, sticky = 'e')

        self.add_label.grid(row = 0, columnspan = 3)

        self.delete_select.rowconfigure(1, weight = 1)

        self.delete_select.grid_columnconfigure(0, weight=1)


        self.delete_select.grid(row = 0, column = 0, sticky = 'nsew')


    # *** Populate delete listbox ***


        self.delete_list = self.playing_list_str + self.not_playing_list_str

        for player in self.delete_list:
            self.delete_listbox.insert(END, player)

    def confirm_delete(self, *args):

        player = self.delete_listbox.curselection()

        if player == ():
            self.text_display.set("CANNOT ADD, NO PLAYER from *NOT PLAYING* SELECTED")
            messagebox.showerror('None selected error', 'Please select a player from the list to delete.')
            self.delete_top.destroy()
            self.delete_player()

            return



        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.delete_list[player[0]]):

                MsgBox = messagebox.askyesno('Are you sure?',\
                                'Delete this person? \nName: ' + str(self.master_list[i]['name']) \
                                    + '\nemail: ' + str(self.master_list[i]['uOttawa Email'])\
                                    + '\npayment method: ' + str(self.master_list[i]['Method of payment']) \
                                    + '\npayment received?: ' + str(self.master_list[i]['Paid Yet?'])\
                                    + '\nSkill level: ' + str(self.master_list[i]['skill'])\
                                    ,icon = 'warning')

                if MsgBox == True:

                    del self.master_list[i]

                    self.populate_listboxes()

                    deletebox = messagebox.showinfo('Delete Confirm', 'Player deleted.')

                    SaveBox = messagebox.askyesno('Save?', 'Would you like to save changes?', icon = 'question')

                    if SaveBox == True:

                        self.save()

                    self.delete_top.destroy()

                else:

                    self.delete_top.destroy()

                    self.delete_player()

                return



    def populate_listboxes(self, *args):

        self.playing_list_str = []
        self.not_playing_list_str = []


        for i in range(0, len(self.master_list)):
            if self.master_list[i]['playing'] == 1:
                self.playing_list_str.append(self.master_list[i]['name'])
            else:
                self.not_playing_list_str.append(self.master_list[i]['name'])


        self.playing_list_str = sorted(self.playing_list_str)
        self.remove_listbox.delete('0', 'end')


        for player in self.playing_list_str:
            self.remove_listbox.insert(END, player)


        self.not_playing_list_str = sorted(self.not_playing_list_str)
        self.add_listbox.delete('0', 'end')

        for member in self.not_playing_list_str:
            self.add_listbox.insert(END, member)

    def load(self, *args):

        self.file_path = filedialog.askopenfilename(filetypes = [('Comma Seperated List','.csv')], title = 'Load file')


        self.master_list = []

        self.playing_list_str = []

        self.not_playing_list_str = []

        self.full_list = []

        self.total = [0]


        with open(self.file_path, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.master_list.append(row)

        for i in range(0, len(self.master_list)):
            if self.master_list[i]['skill'] == '':
                self.master_list[i]['skill'] = 2
            self.master_list[i]['skill'] = int(self.master_list[i]['skill'])
            if self.master_list[i]['games'] == '':
                self.master_list[i]['games'] = 0
            self.master_list[i]['games'] = int(self.master_list[i]['games'])
            if self.master_list[i]['playing'] == '':
                self.master_list[i]['playing'] = 0
            self.master_list[i]['playing'] = int(self.master_list[i]['playing'])

        for i in range(0, len(self.master_list)):

            if self.master_list[i]['playing'] == 1:
                self.playing_list_str.append(self.master_list[i]['name'])

            else:
                self.not_playing_list_str.append(self.master_list[i]['name'])

        self.playing_list_str = sorted(self.playing_list_str)

        self.not_playing_list_str = sorted(self.not_playing_list_str)

        self.full_list = sorted(self.playing_list_str + self.not_playing_list_str)

        # *** populate listboxes ***

        self.populate_listboxes()

    def save(self, *args):

        self.master_list = sorted(self.master_list, key=itemgetter('name'))

        while True:
            try:

                with open(self.file_path, 'w', newline = '') as new_file:
                    fieldnames = ['name', 'uOttawa Email', 'Method of payment', 'Paid Yet?', 'skill', 'games', 'playing', 'partner name']

                    csv_writer = csv.DictWriter(new_file, dialect = 'excel', fieldnames = fieldnames)

                    csv_writer.writeheader()

                    for member in self.master_list:
                        csv_writer.writerow(member)

                self.text_display.set(str(self.file_path) + ' has been saved!')

                messagebox.showinfo("Saved", "File saved!")

                break

            except PermissionError:
                messagebox.showinfo("Save Failed", "Save failed, Try closing the excel sheet if open.")

    def save_as(self, *args):

        self.master_list = sorted(self.master_list, key = itemgetter('name'))

        self.file_path = asksaveasfilename(filetypes = [('Comma Seperated List','.csv')], title = 'Save File As', defaultextension = ".csv")

        while True:
            try:
                with open(self.file_path, 'w', newline = '') as new_file:
                    fieldnames = ['name', 'uOttawa Email', 'Method of payment', 'Paid Yet?', 'skill', 'games', 'playing', 'partner name']

                    csv_writer = csv.DictWriter(new_file, dialect = 'excel', fieldnames = fieldnames)

                    csv_writer.writeheader()

                    for member in self.master_list:
                        csv_writer.writerow(member)

                self.text_display.set('File has been saved as: ' + str(self.file_path))

                messagebox.showinfo("Saved", "File saved!")
                break

            except PermissionError:
                messagebox.showinfo("Save Failed", "Save failed, Try closing the excel sheet.")


    def label_update(self, *args):
        '''This displays the selected players stats'''

        r_player = self.remove_listbox.curselection()

        if r_player == '':                                  #prevents error message on doubleclick
            return

        if self.remove_listbox.curselection() != ():        #if something is selected find player

            for i in range(len(self.master_list)):
                if self.master_list[i]['name'] == str(self.playing_list_str[r_player[0]]):
                    self.text_display.set(self.master_list[i]['name'] + ' | Skill Group = ' + str(self.master_list[i]['skill']))
                    if self.master_list[i]['partner name'] != '':
                        self.text_display.set(self.master_list[i]['name'] + ' | Skill Group = ' + str(self.master_list[i]['skill']) + ' | Partner = ' + self.master_list[i]['partner name'])
                    break

        a_player = self.add_listbox.curselection()

        if a_player == '':
            return

        if self.add_listbox.curselection() != ():

            for i in range(len(self.master_list)):
                if self.master_list[i]['name'] == str(self.not_playing_list_str[a_player[0]]):
                    self.text_display.set(self.master_list[i]['name'] +  ' | Skill Group = ' + str(self.master_list[i]['skill']))
                    break

    def new_game(self, *args):
        '''This prints the game list, with courts to the text box'''

        random.shuffle(self.master_list)                         #shuffle list to randomise play

        self.master_list = sorted(self.master_list, key=itemgetter('games'))

        orgfield = []                                       #temp list for new round
        self.total[0] += 1

        for i in range(0, len(self.master_list)):

            if self.master_list[i]['partner name'] != '' and self.master_list[i]['playing'] == 1 and len(orgfield) < 15 and (self.master_list[i] not in orgfield):
                orgfield.append(self.master_list[i])
                self.master_list[i]['games'] = self.master_list[i]['games'] + 1

                for e in range(0, len(self.master_list)):
                    if self.master_list[i]['partner name'] == self.master_list[e]['name'] and self.master_list[e]['playing'] == 1 and (self.master_list[e] not in orgfield):

                        self.master_list[e]['games'] = self.master_list[i]['games']

                        orgfield.append(self.master_list[e])
                        break

            elif self.master_list[i]['playing'] == 1 and self.master_list[i]['partner name'] == '':
                orgfield.append(self.master_list[i])                #Add first 16 players to temp list for new game
                self.master_list[i]['games'] = self.master_list[i]['games'] + 1     #Increase the games played by those playing in round by 1

            if len(orgfield) == 16:
                break

        self.round_label_text.set('Round ' + str(self.total[0]) + ' Display')

        game_text = ''

        orgfield = sorted(orgfield, key=itemgetter('skill'))



        for i in range(0, len(orgfield)):

            if orgfield[i]['partner name'] != '' and i % 2 != 0:

                orgfield[i - 1], orgfield[i] = orgfield[i], orgfield[i - 1]

                for b in range(i, len(orgfield)):
                    if orgfield[b]['name'] == orgfield[i-1]['partner name']:
                        partner = orgfield[b]
                        orgfield.remove(orgfield[b])
                        orgfield.insert(i, partner)
                        break

            elif orgfield[i]['partner name'] != '':
                for e in range(0, len(orgfield)):
                    if orgfield[e]['name'] == orgfield[i]['partner name']:
                        partner = orgfield[e]
                        orgfield.remove(orgfield[e])
                        orgfield.insert(i, partner)
                        break

        b=0                                                 #index for courts

        for i in range(len(orgfield)):                      #go through temp list of players and print names and court placement

            game_text = game_text + orgfield[i]['name'] + '\n'
            b=b+1

            if (b % 4) == 0:                                #Court number

                game_text = game_text + '\nCOURT: ' + str(b // 4) + '\n\n'

        now = datetime.datetime.now()                       #timestamp for future reference

        game_text = game_text + '\nRound = ' + str(self.total[0]) + ' | Started at: ' + str(now.hour) + ':'
        if now.minute < 10:
            game_text = game_text + '0' + str(now.minute) + '\n\n'
        else:
            game_text = game_text + str(now.minute) + '\n\n'

        game_text = game_text + '------------------------------------------\n'

        self.round_display.insert(1.0, str(game_text))       #prints games to listbox

        orgfield = []                                       #clear temp list

        self.new_round_button.focus()

        self.text_display.set('Round ' + str(self.total[0]) + ' has begun')

    def remove_player(self, *args):
        '''This removes the selected player from the player list'''

        player = self.remove_listbox.curselection()

        if self.add_listbox.curselection() != ():
            self.text_display.set("CHOOSE PLAYER FROM *CURRENTLY PLAYING*")
            messagebox.showerror("Remove Error", "You can only remove players from the *CURRENTLY PLAYING* list")
            return

        if player == ():                                    #if nothing selected move on
            self.text_display.set("CANNOT REMOVE, NO PLAYER from *CURRENTLY PLAYING* SELECTED")
            messagebox.showerror('None selected error', 'Please select a player from the currently playing list to remove.')
            return
    # messagebox.askyesno("Remove Error", "You can only remove players from the *CURRENTLY PLAYING* list")
    # return

        # for person in playing_list:                          #removes selected player from player list
        for i in range(0, len(self.master_list)):
            if self.master_list[i]['name'] == str(self.playing_list_str[player[0]]):
                self.text_display.set(self.master_list[i]['name'] + ' has been removed.')
                self.master_list[i]['playing'] = 0
                break

        # Updates both listboxes

        self.populate_listboxes()

    def add_player(self, *args):
        '''This adds the selected to person to the player list'''

        player = self.add_listbox.curselection()

        if self.remove_listbox.curselection() != ():
            self.text_display.set("CHOOSE PLAYER FROM *NOT PLAYING*")
            messagebox.showerror("Add Error", "You can only add players from the *NOT PLAYING* list")
            return

        if player == ():
            self.text_display.set("CANNOT ADD, NO PLAYER from *NOT PLAYING* SELECTED")
            messagebox.showerror('None selected error', 'Please select a player from the not playing list to add.')
            return
        for i in range(0 , len(self.master_list)):
            if self.master_list[i]['playing'] == 1:
                games_played = self.master_list[i]['games']
                break
            if i == len(self.master_list) - 1 and self.master_list[i]['playing'] != 1:
                games_played = 0
                break

        for i in range(0 , len(self.master_list)):          #Adds selected player to the player list and makes the added players games equal to other players
            if self.master_list[i]['name'] == str(self.not_playing_list_str[player[0]]):
                self.master_list[i]['playing'] = 1
                self.master_list[i]['games'] = games_played
                self.text_display.set(self.master_list[i]['name'] + ' has been added.')
                break

        # This updates both listboxes

        self.populate_listboxes()

"-------------------------------------------------------------------------------------------------------------------------"


root = Tk()
root.title("Badminton 1000")
b = Badminton(root)
root.mainloop
