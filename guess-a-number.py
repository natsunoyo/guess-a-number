from tkinter import *
from random import randint
import pygame

pygame.mixer.init()

def quit():
    root.destroy()

def difficulty_window():
    difficulty = Toplevel(root)
    difficulty.title('Вибір складності')
    difficulty.geometry('300x200')
    difficulty.configure(bg='lightyellow')

    Label(difficulty, text="Оберіть складність:", font='Arial 14', bg='lightyellow').pack(pady=10)

    Button(difficulty, text="Легка (1-50)", font='Arial 12', command=lambda: set_difficulty('easy')).pack(pady=5)
    Button(difficulty, text="Середня (1-100)", font='Arial 12', command=lambda: set_difficulty('medium')).pack(pady=5)
    Button(difficulty, text="Складна (1-200)", font='Arial 12', command=lambda: set_difficulty('hard')).pack(pady=5)

def set_difficulty(level):
    global number, difficulty_level
    difficulty_level = level
    if level == 'easy':
        number = randint(1, 50)
        lab1.config(text='Я загадав число від 1 до 50')
    elif level == 'medium':
        number = randint(1, 100)
        lab1.config(text='Я загадав число від 1 до 100')
    elif level == 'hard':
        number = randint(1, 200)
        lab1.config(text='Я загадав число від 1 до 200')
    reset_game()

def reset_game():
    global attempt
    attempt = 0
    entry.config(state=NORMAL)
    button.config(state=NORMAL)
    entry.delete(0, END)
    text.delete(1.0, END)

def settings_window():
    settings = Toplevel(root)
    settings.title('Налаштування')
    settings.geometry('400x300')
    settings.configure(bg='lightyellow')

    sound_label = Label(settings, text="Звуки", font='Arial 14', bg='lightyellow')
    sound_label.pack(anchor='w', padx=10, pady=5)

    sound_var = BooleanVar(value=sound_enabled)
    sound_checkbox = Checkbutton(settings, text="Увімкнути звуки", var=sound_var, font='Arial 12', bg='lightyellow')
    sound_checkbox.pack(anchor='w', padx=20, pady=5)

    resolution_label = Label(settings, text="Роздільна здатність", font='Arial 14', bg='lightyellow')
    resolution_label.pack(anchor='w', padx=10, pady=5)

    resolution_var = StringVar(value='800x640')
    resolutions = ['800x640', '1024x768', '1280x720']

    for res in resolutions:
        radio_button = Radiobutton(settings, text=res, variable=resolution_var, value=res, font='Arial 12', bg='lightyellow')
        radio_button.pack(anchor='w', padx=20)

    save_button = Button(settings, text="Зберегти", font='Arial 14', command=lambda: apply_settings(sound_var.get(), resolution_var.get()))
    save_button.pack(pady=20)

def info_window():
    info = Toplevel(root)
    info.title('Про нас')
    info.geometry('400x300')
    info.configure(bg='lightyellow')
    info_label = Label(info, text="Проект №1.\n Гра \"Вгадай число\"\nАвтори: \nТопольський Олександр\nСкрипник Анастасія\nЯнківська Богдана", font='Arial 14', bg='lightyellow')
    info_label.pack(padx=10, pady=10)

sound_enabled = True

def apply_settings(sound, resolution):
    global sound_enabled
    sound_enabled = sound 
    if sound_enabled:
        print("Sounds enabled")
        pygame.mixer.init()
    else:
        print("Sounds disabled")
        pygame.mixer.quit()

    root.geometry(resolution)
    print(f"Resolution set to {resolution}")

    if resolution == '800x640':
        adjust_sizes(22, 16, 40, 5, 14)
    elif resolution == '1024x768':
        adjust_sizes(24, 18, 45, 6, 16)
    elif resolution == '1280x720':
        adjust_sizes(28, 20, 50, 7, 18)

def adjust_sizes(label_size, button_size, text_width, text_height, entry_size):
    lab1.config(font=f'Arial {label_size}')
    button.config(font=f'Arial {button_size}')
    text.config(width=text_width, height=text_height, font=f'Arial {button_size}')
    entry.config(font=f'Arial {entry_size}', width=10)

def play_huh():
    if sound_enabled:  
        pygame.mixer.music.load("audio/xp.mp3")
        pygame.mixer.music.play(loops=0)

def play_win():
    if sound_enabled:  
        pygame.mixer.music.load("audio/tada.mp3")
        pygame.mixer.music.play(loops=0)

def play_lose():
    if sound_enabled:  
        pygame.mixer.music.load("audio/error.mp3")
        pygame.mixer.music.play(loops=0)

def play_stop():
    pygame.mixer.music.stop()

root = Tk()
root.configure(bg='lightyellow')
my_menubar = Menu(root)
my_menubar.add_command(label='Складність', command=difficulty_window)
my_menubar.add_command(label='Налаштування', command=settings_window)
my_menubar.add_command(label='Про нас', command=info_window)
my_menubar.add_command(label='Вихід', command=quit)
root.config(menu=my_menubar)

root.geometry('800x640')

lab1 = Label(root, text='Я загадав число від 1 до 100', font='Arial 20', bg='lightyellow')
lab1.grid(row=0, column=0, columnspan=4, pady=10, sticky='w')

frame_entry = Frame(root, bg='lightyellow')
frame_entry.grid(row=1, column=0, columnspan=4, pady=10)

entry = Entry(frame_entry, width=10, font='Arial 14')
entry.pack(side=LEFT, padx=5)

button = Button(frame_entry, text='Спробуй', font='Arial 14', bg='lightpink', command=lambda: check())
button.pack(side=LEFT, padx=5)

text = Text(root, width=50, height=10, bg='lightblue', font='Arial 14')
text.grid(row=2, column=0, columnspan=4, pady=10)

number = randint(1, 100)
difficulty_level = 'medium'
attempt = 0

def check():
    global attempt
    try:
        guess = int(entry.get())
        text.delete(1.0, END)
        if (difficulty_level == 'easy' and (guess < 1 or guess > 50)) or \
           (difficulty_level == 'medium' and (guess < 1 or guess > 100)) or \
           (difficulty_level == 'hard' and (guess < 1 or guess > 200)):
            play_huh()
            text.insert(1.0, 'Введи число в правильному діапазоні')
        elif guess > number:
            attempt += 1
            text.insert(1.0, f'Спроба № {attempt}. Число менше.')
            play_lose()
        elif guess < number:
            attempt += 1
            text.insert(1.0, f'Спроба № {attempt}. Число більше.')
            play_lose()
        else:
            attempt += 1
            text.insert(1.0, f'ТИ ВГАДАВ з {attempt} спроби!\nЦе число {number}.')
            entry.config(state=DISABLED)
            button.config(state=DISABLED)
            play_win()
    except ValueError:
        text.delete(1.0, END)
        text.insert(1.0, 'Введіть допустиме число.')
        play_huh()
    entry.delete(0, END)

root.mainloop()

