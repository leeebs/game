from pico2d import *
import time
import pickle
import fonts

class Highscore:
    class Entry:
        def __init__(self, score):
            self.score = score
            self.time = time.time()
    MAX_SCORE_COUNT = 5
    def __init__(self):
        self.fonts = fonts.get(fonts.FONT_1, 30)
        self.scores = []
    def add(self, score):
        inserted = False
        entry = Highscore.Entry(score)
        for i in range(len(self.scores)):
            e = self.scores[i]
            if e.score < entry.score:
                self.scores.insert(i, entry)
                inserted = True
                self.lastRank = i + 1
                break
        if not inserted:
            self.scores.append(entry)
            self.lastRank = len(self.scores)
        if (len(self.scores) > Highscore.MAX_SCORE_COUNT):
            self. scores.pop(-1)
    def draw(self):
        y = 160
        for e in self.scores:
            str = "{:5.1f}".format(e.score)
            self.fonts.draw(30, y, str, (255, 255, 128))
            self.fonts.draw(220, y, time.asctime(time.localtime(e.time)), (223, 255, 223))
            y -= 30