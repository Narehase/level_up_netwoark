import time
import os
import keyboard
import numpy as np
def down():
	print("####  ####\n####  ####\n##      ##\n###    ###\n####  ####")
def l():
    print("####### ##\n#######  #\n\n#######  #\n####### ##")
def r():
    print("## #######\n#  #######\n\n#  #######\n## #######")
def up():
    print("####  ####\n###    ###\n##      ##\n####  ####\n####  ####")
class game:
    def __init__(self) -> None:
        pass

    def games(self):
        i = 0
        while i == 0:
            i += 1
            os.system('cls')
            a = np.random.randint(0,4)
            print(a)
            if a == 0:
                up()
            if a == 1:
                down()
            if a == 2:
                l()
            if a == 3:
                r()
            print("\n\n\n\n\n\n\n\n")

            self.game = a

    def chek(self, ok):
        f = self.game
        print(ok,'  ||  ',f)
        if f == ok:
            print("정답이야!")
            return 2

        else:
            print("틀렸어!")
            return 0

