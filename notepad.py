from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import os
from datetime import datetime
from tkinter.messagebox import askquestion, showinfo

class Notepad(Tk):
    def __init__(self):
        super().__init__()
   
    #setting text area and scrollbar
    def creating_scrollbar(self):       
        self.title('Untitled -Notepad')
        scroller = Scrollbar(self)
        scroller.pack(side=RIGHT, fill=Y)
        self.font1=['times',11,'normal']
        self.text_area = Text(self, yscrollcommand=scroller.set,font=self.font1, undo=True)
        self.text_area.pack(expand=True, fill=BOTH)
        self.text_area.bind('<KeyRelease>', lambda e: self.status_bar(self.text_area.index('current')))
        self.status=Label(self)
        self.lines = Label(self, text='Lines: ', relief='sunken', border=1, padx=10)
        self.lines.pack(side='left')
        self.chars = Label(self, text='Chars: ', relief='sunken', border=1, padx=10)
        self.chars.pack(side='left')
        self.status.pack(fill=X,side=BOTTOM)
        scroller.config(command=self.text_area.yview)
        
    def status_bar(self,mouse_pos):
        self.lines['text'] = 'Line: ' + mouse_pos.split('.')[0]
        self.chars['text'] = 'Charater: ' + mouse_pos.split('.')[1]
        
    def New_File(self):
        self.title('Untitled -Notepad')
        self.file = None
        self.text_area.delete(1.0, END)
    def Open_File(self):
        self.open_File = askopenfilename(defaultextension='.txt', filetypes=[
                                    ('All documents', '*.*'), ('Text documents', '*.txt')])
        if self.open_File == "":
            self.open_File = None
        else:
            self.text_area.delete(1.0,END)
            self.file = open(self.open_File, 'r')
            self.text_area.insert(1.0, self.file.read())
            self.file.close()
            self.title(os.path.basename(self.open_File)+'-Notepad')
            
    def Save(self):
        self.file = 'Untitled '
        save_file = open(self.file, 'w')
        save_file.write(self.text_area.get(1.0, END))
        save_file.close()
        self.text_area.delete(1.0, END)
        self.title('Untitled -Notepad')

    def Save_As(self):
        self.save_as = asksaveasfilename(defaultextension='.txt', filetypes=[
                                    ('All documents', '*.*'), ('Text documents', '*.txt')])
        if self.save_as=="":
            self.save_as=None
        else:
            self.file=open(self.save_as,'w')
            self.file.write(self.text_area.get(1.0,END))
            self.file.close()
            self.text_area.delete(1.0,END)
            self.title('Untitled -Notepad')

    def Find(self):
        self.text_area.tag_config(SEL,  background='sky blue')
        self.word = askstring('Find', 'Word to find')
        self.offset = '+%dc' % len(self.word) 
        self.position_start = self.text_area.search(self.word, '1.0', END)
        while self.position_start:
            self.position_end = self.position_start + self.offset
            self.text_area.tag_add(SEL, self.position_start, self.position_end)
            self.position_start = self.text_area.search(self.word, self.position_end, END)

    def Replace(self):
        def replacing():
            lab=Label(self)
            lab.pack()
            whole=self.text_area.get('1.0','end')
            word1=self.word.get()
            replaced_word=self.word_now.get()
            whole=str.replace(whole, word1, replaced_word)
            lab['text']=whole
            self.text_area.delete(1.0,END)
            content=lab.cget('text')
            self.text_area.insert(INSERT, content )
            lab.destroy()
        def fun():
            self.l1.destroy()
            self.l2.destroy()
            self.entry1.destroy()
            self.entry2.destroy()
            self.but1.place_forget()
            self.but2.place_forget()
        self.l1=Label(self, text='Replace Word')
        self.l2=Label(self, text='Replace with ')
        self.l1.place(x=10,y=50)
        self.l2.place(x=10,y=80)
        self.word=StringVar()
        self.word_now=StringVar()
        self.entry1=Entry(self,textvariable=self.word)
        self.entry2=Entry(self,textvariable=self.word_now)
        self.entry1.place(x=100,y=50)
        self.entry2.place(x=100,y=80)
        self.but1=Button(self, text='Replace ALL',command=replacing)
        self.but1.place(x=50, y=115)
        self.but2=Button(self, text='Cancel', command=fun)
        self.but2.place(x=170,y=115)
        
    def Select_All(self):  
        self.text_area.tag_add(SEL, 1.0, END)
        
    def date_time(self):
        self.time=datetime.now()
        self.text_area.insert(INSERT, self.time)
        
    def zoom(self, str):
        if str=='in':
            self.font1[1]=self.font1[1]+2
        elif str=='out':
            self.font1[1]=self.font1[1]-2
        else:
            self.font1[1]=11
        self.text_area.config(font=self.font1)
        
    def rate_us(self):
        self.rate=askquestion('Rate_us','Was you experience good?')
        if YES:
            msg='Give us 5 stars'
        else:
            msg='We wil try to improve'
        showinfo('Rate us', msg)
        
    def about(self):
        self.about_me=showinfo('About', 'Welcome to the notepad by ashir')
        
    def Main_menu(self):
        self.main_menu = Menu(self)
        self.file = Menu(self.main_menu, tearoff=0)
        self.file.add_command(label='New',command=self.New_File)
        self.file.add_command(label='Open', command=self.Open_File)
        self.file.add_command(label='Save', command=self.Save)
        self.file.add_command(label='Save As', command=self.Save_As)
        self.file.add_separator()
        self.file.add_command(label='Exit', command=exit)
        self.config(menu=self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.file)
        
        self.edit=Menu(self.main_menu, tearoff=0)
        self.edit.add_command(label='Undo', command=lambda: self.text_area.edit_undo() )
        self.edit.add_command(label='Redo', command=lambda: self.text_area.edit_redo() )
        self.edit.add_separator()
        self.edit.add_command(label='Cut', command=lambda: self.text_area.event_generate(('<<Cut>>')))
        self.edit.add_command(label='Copy', command=lambda: self.text_area.event_generate(('<<Copy>>')))
        self.edit.add_command(label='Paste', command=lambda: self.text_area.event_generate(('<<Paste>>')))
        self.edit.add_separator()
        self.edit.add_command(label='Find', command=self.Find)
        self.edit.add_command(label='Replace All', command=self.Replace)
        self.edit.add_command(label='Select All', command=self.Select_All)
        self.edit.add_command(label='Date/Time', command=self.date_time)
        self.config(menu=self.main_menu)
        self.main_menu.add_cascade(label='Edit', menu=self.edit)
        
        self.view=Menu(self.main_menu, tearoff=0) 
        self.submenu=Menu(self.main_menu,tearoff=0)
        self.submenu.add_command(label='Zoom In',command=lambda: self.zoom('in'))
        self.submenu.add_command(label='Zoom Out',command=lambda: self.zoom('out'))
        self.submenu.add_command(label='Default Zoom',command=lambda: self.zoom('default'))
        self.view.add_cascade(label='Zoom', menu=self.submenu)
        self.config(menu=self.main_menu)
        self.main_menu.add_cascade(label='View', menu=self.view)
        
        self.help=Menu(self.main_menu, tearoff=0) 
        self.help.add_command(label='About Notepad', command=self.about) 
        self.help.add_command(label='Rate us', command=self.rate_us) 
        self.config(menu=self.main_menu)
        self.main_menu.add_cascade(label='Help', menu=self.help)
        
if __name__ == '__main__':
    ashir = Notepad()
    ashir.creating_scrollbar()
    ashir.Main_menu()
    ashir.mainloop()
