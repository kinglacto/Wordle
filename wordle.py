import pygame
import json
import random
import sys

pygame.font.init()

with open('words.json', 'r') as words_file:
    WORDS_LIST = list(json.load(words_file))
    WORDS_SET = set(WORDS_LIST)

class Wordle:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Wordle")

        self.i = 0
        self.j = -1

        self.grids_list = [[pygame.Rect(65 + j * 75, 70 + i * 75, 70, 70) for j in range(5)] for i in range(5)]
        self.grid = [[[] for _ in range(5)] for __ in range(5)]

        self.myfont = pygame.font.SysFont('helvetica', 70)

        self.grey = (77, 83, 84)
        self.dark_grey = (55, 55, 55)
        self.green = (109, 207, 65)
        self.yellow = (217, 226, 45)
        self.white = (200, 200, 200)

    def draw_grid(self) -> None:
        self.screen.fill((0, 0, 0))
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(self.screen, self.grey , self.grids_list[i][j])

    def insert(self, char) -> None:
        if self.j != 4:
            self.j += 1
            self.grid[self.i][self.j] = char.upper()
            self.screen.blit(self.myfont.render(char.upper(), False, self.white), (self.grids_list[self.i][self.j][0] + 5, self.grids_list[self.i][self.j][1]))

    def check_word(self, line) -> bool:
        guessed = ''
        for j in range(5):
            guessed += self.grid[line][j]
        if guessed in WORDS_SET:
            green = []
            non_green = []
            green_indices = []
            for j in range(5):
                char = self.grid[line][j]
                letter_surface = self.myfont.render(char.upper(), False, self.white)
                if char == self.word[j]:
                    pygame.draw.rect(self.screen, self.green, self.grids_list[line][j])
                    self.screen.blit(letter_surface, (self.grids_list[line][j][0] + 5, self.grids_list[line][j][1]))
                    green_indices.append(j)
                    green.append(char)
                elif char not in green:
                    non_green.append(char)

            for j in range(5):
                if j not in green_indices:
                    char = self.grid[line][j]
                    letter_surface = self.myfont.render(char.upper(), False, self.white)
                    if char in non_green and char in self.word:
                        non_green = [x for x in non_green if x != char]
                        pygame.draw.rect(self.screen, self.yellow, self.grids_list[line][j])
                    else:
                        pygame.draw.rect(self.screen, self.dark_grey, self.grids_list[line][j])
                    self.screen.blit(letter_surface, (self.grids_list[line][j][0] + 5, self.grids_list[line][j][1]))
            self.i += 1
            self.j = -1
            if len(green_indices) == 5:
                return True
        return False

    def remove(self) -> None:
        self.grid[self.i][self.j] = []
        pygame.draw.rect(self.screen, self.grey , self.grids_list[self.i][self.j])

        if self.j > 0:
            self.j -= 1
        else:
            self.j = -1
        
    def reset(self, show_word=False) -> None:
        if show_word:
            for i in range(5):
                self.screen.blit(self.myfont.render(self.word[i], False, self.green), (70 + i * 75, 3))

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    self.word = list(random.choice(WORDS_LIST))
                    self.draw_grid()
                    return None
                pygame.time.wait(30)
        

    def run_game(self) -> None:
        self.word = list(random.choice(WORDS_LIST))
        self.draw_grid()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYUP:
                    char = pygame.key.name(event.key)
                    if event.key == pygame.K_BACKSPACE:
                        self.remove()

                    elif event.key == pygame.K_RETURN and self.grid[self.i][4] != []:
                        if self.check_word(self.i):
                            self.reset()

                        if self.i == 4 and self.j == 4:
                            self.reset(True)

                    elif not self.grid[self.i][4] != []:
                        try:
                            if ord(char) in range(97, 123) or ord(char) in range(65, 91):
                                self.insert(char)
                            else:
                                continue
                        except:
                            continue
                        
                    pygame.display.update()
                pygame.time.wait(30)

if __name__ == "__main__":
    wordle = Wordle()
    wordle.run_game()