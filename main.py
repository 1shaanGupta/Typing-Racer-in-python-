import copy
import os

import pygame
import random

pygame.init()
wordlist = ["Patriotism", "Independence", "Peace", "Mahatma", "Gandhi",
            "Tricolor", "Freedom", "Unity", "Diversity", "Green", "Ashoka", "Chakra",
            "Nationalism", "Non-violence", "Respect", "Constitution", "Sacrifice",
            "INA", "Martyr", "Revolution", "Liberation", "Swaraj",
            "Courage", "Tolerance", "Tiranga", "Motherland", "Inspirational",
            "Equality", "Himalayas", "boycott", "swadeshi", "swaraj",
            "constitution", "Congress",
            "Harmony", "Love", "Kindness", "Forgiveness", "Tolerance", "Compassion", "Tranquility",
            "Unity", "Mediation", "Gentleness", "Understanding", "Coexistence", "Nonviolence",
            "Harmonious", "Calm", "Peaceful", "Serenity", "Conciliation", "Peacemaker", "Empathy",
            "Resolution", "Nonviolent", "Pacifism", "Amicability", "Truce", "Reconciliation",
            "Solidarity", "Friendship", "Humanitarian", "Diplomacy", "Equality", "Harvesting",
            "Nonaggression", "Stability", "Agreement",
            "Harbor", "Ceasefire", "Harmony", "Serene", "Pacify", "Tranquil", "Accord",
            "Concord", "Hug", "Community", "Sanctuary", "Egalitarian", "Peacetalks", "Empathetic",
            "Harmonize", "Tranquillity", "Harmonious", "Dove", "Cohesion", "Rebuild", "Recovery",
            "Understanding", "Solemn", "Peacetime", "Empathize", "Accommodation", "Restoration",
            "Unite", "Healing", "Hope", "Empowerment", "Hug", "Meditation", "Vow", "Patience"]


opposite_wordlist = ["Conflict", "War", "Violence", "Aggression", "Hate", "Anger", "Hostility", "Chaos",
                    "Destruction", "Terrorism", "Discord", "Strife", "Hatred", "Battle", "Rage", "Warfare",
                    "Fury", "Confrontation", "Turmoil", "Revolt", "Militancy", "Anarchy", "Oppression",
                    "Injustice", "Inequality", "Intolerance", "Retaliation", "Brutality", "Revolutionary",
                    "Opposition", "Combat", "Bloodshed", "Riot", "Revenge", "Insurgency", "Tyranny", "Suppression",
                    "Tension", "Conflict", "Disagreement", "Harm", "Disharmony", "Unrest", "Dissension", "Rebellion",
                    "Dissent", "Struggle", "Violent", "Divisiveness", "Vengeance", "Clash", "Vendetta", "Uprising",
                    "Fighting", "Havoc", "Crisis", "Turmoil", "Disorder", "Mistrust", "Distrust", "Separation",
                    "Division", "Disunity", "Cruelty", "Mayhem", "Chaos", "Annihilation", "Invasion", "Conquest",
                    "Oppress", "Belligerent", "Aggressor", "Dispute", "Enemy", "Assault", "Defeat", "Conflict",
                    "Injure", "Hostile", "Oppose", "Harmful", "Vandalism", "Provocation", "Disarmament", "Supremacy",
                    "Friction", "Insurrection", "Exacerbate", "Revolt", "Reprisal", "Stratagem", "Malevolence", "Retribution",
                    "Conquer", "Subdue", "Intimidate", "Retaliate", "Injure", "Disrupt", "Provocation", "Tension"]

# from nltk.corpus import words
#
# wordlist = words.words()

len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

# print(len_indexes)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Typing Racer!')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

score = 0

header_font = pygame.font.Font('assets/fonts/RobotoSlab-Regular.ttf', 40)
pause_font = pygame.font.Font('assets/fonts/PixelifySans-Regular.ttf', 38)
banner_font = pygame.font.Font('assets/fonts/PixelifySans-Regular.ttf', 30)
font = pygame.font.Font('assets/fonts/AldotheApache.ttf', 48)
# music and sounds
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('assets/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('assets/sounds/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 5
word_objects = []
file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()
pz = True
new_level = True
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# 2 letter, 3 letter, 4 letter, 5 letter, 6 letter, etc
choices = [False, True, False, False, False, False, False]

#background image-
image = pygame.image.load('background.png')
def Background(image):
    size = pygame.transform.scale(image, (WIDTH, HEIGHT))

class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    def draw(self):
        color = 'white'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed


class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


def draw_screen():
    # screen outlines for main game window and 'header' section
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    # text for showing current level, player's current string, high score and pause options
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 75))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 75))
    pause_btn = Button(748, HEIGHT - 52, '| |', False, screen)
    pause_btn.draw()
    # draw lives, score, and high score on top of screen
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (250, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'white'), (550, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'white'), (10, 10))
    return pause_btn.clicked


def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()
    surface.blit(header_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(header_font.render('PLAY!', True, 'white'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'white'), (450, 175))
    surface.blit(header_font.render('Active Letter Lengths:', True, 'white'), (110, 250))

    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked


def generate_level():
    word_objs = []
    word_opp = []

    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))
    for i in range(level):
        speed = random.randint(2, 5)
        y_pos = random.randint(10 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word)
    return word_objs


def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            scor += int(points)
            word_objects.remove(wrd)
            woosh.play()
    return scor


def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()


run = True
while run:

    screen.fill((211, 223, 223))
    Background(image)
    timer.tick(fps)
    # draw static background
    pause_butt = draw_screen()
    if pz:
        resume_butt, changes, quit_butt = draw_pause()
        if resume_butt:
            pz = False
        if quit_butt:
            check_high_score()
            run = False
    if new_level and not pz:
        word_objects = generate_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1
    if len(word_objects) <= 0 and not pz:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    active_string += event.unicode
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if pz:
                    pz = False
                else:
                    pz = True
        if event.type == pygame.MOUSEBUTTONUP and pz:
            if event.button == 1:
                choices = changes

    if pause_butt:
        pz = True

    if lives <= 0:
        pz = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()
pygame.quit()
