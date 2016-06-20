#################################################################
#    File Name: music.py
#       Author: JiangTao
#       E-mail: jt_2010@hust.edu.cn
#  Description: music.py
# Created Time: 2013/2/22 13:25:42
#################################################################
#/usr/bin/env python
import Tkinter as tk
import audiotools

sound = audio.Sound.open('Life is Cool.wav')
def play():
    sound.play()
    print 'Play music returns...'

top = tk.Tk()
label = top.Label(top, activebackground = 'blue', compound = 'DianLogo.png')
label.pack()

button = top.Button(top, text='play', command = play)
button.pack()
quit = top.Button(top, text='Exit', command = top.quit)
quit.pack()

mainloop()

