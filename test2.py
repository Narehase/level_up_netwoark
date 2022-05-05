import numpy as np
import pyautogui
import cv2
import keyboard
import time

import test_game

import tensorflow as tf
import tensorflow.keras as tink

state_list = []
Raw_list = []

def reward_save(state,coin,ac,state_list,state_RAW,R_list): #reward를 받고 memore save 저장
    state_list.append([state,coin,ac])
    R_list.append([state_RAW,coin,ac  ])
    #print(state_list)
    return state_list, R_list
class learning:
    def __init__(self,hint= 80,acnum = 4):
        self.onsx = [  0]
        self.onsy = []
        self.state_list = []
        self.hint = hint
        self.acnum = acnum
        pass

    def point_up(self):
        points = []
        key = 0
        i = 0
        print("point_UP! || 포인트순서 : 좌측상단 -> 우측하단")
        while True:
            if keyboard.is_pressed('space') and key == 0:
                x,y = pyautogui.position()
                print(i," : ",x)
                points.append([x,y])
                i += 1
                key = 1

            if key == 1:
                key = 0
                time.sleep(0.2)

            if i == 2:
                break
        print(points)
        self.points = points
        pass

    def load_state(self):

            #현재 상태 불러오기
        pount = self.points
        #print(pount[0][0],pount[0][1],pount[1][0],pount[1][1]  )
        ack = pyautogui.screenshot(region=  (pount[0][0],pount[0][1],int(pount[1][0] - pount[0][0]),int(pount[1][1]-pount[0][1])))
        #ack = cv2.imread("test.png")
        piks = np.array(ack)
        piks = cv2.cvtColor(piks,cv2.COLOR_RGB2BGR)
        pik = cv2.cvtColor(piks,cv2.COLOR_RGB2GRAY)
        pik = np.array(pik)
        #cv2.imshow("kiki",pik)
        #cv2.waitKey(16)
        #print(pik)

        self.state = pik

        pick = []
        for y in pik:
            for x in y:
                pick.append(x)

        pick = np.array(pick)
        #print(pick.shape)
        #print(pick)
        self.stsize = pick.shape
        self.state = pick
        return pick,pik
        pass

def actions(state,state_list): #행동 정하기
    ui = []
    ac = 0
    kui = 0
    key = True
    if 0 != len(state_list):
        for i in state_list:
        #print(i[1])
        #print(i[0])
            if np.array_equal(state, i[0]) and i[1] == 2:
                ui.append(i[2])
                key = False
    if key:
        ac = np.random.randint(0,4)
    else:
        ip = {}
        for j in ui:
            try: ip[str(j)] += 1
            except: ip[str(j  )] = 1
        print(ip)
        ac = ui[0  ]
    return ac

def test():
    game_num = np.random.randint(0,4)
    print("test_num : ",game_num, end='')
    return game_num

def tik(g,k):
    if g == k:
        print('  ',a,"  정답")
        return 2
    else:
        print('  ',a,"  오답")
        return 0

def learning_fraem(raw_list, target):
    k_list = []
    y_list = []
    for i in raw_list:
        if i[1] == target:
            k_list.append(i[0].tolist())
            y_list.append(i[2])
    return k_list,y_list


def models(ins):
    model = tink.Sequential()
    model.add(tink.layers.Conv2D(32, (3, 3), activation='relu', input_shape=ins  ))
    model.add(tink.layers.MaxPooling2D((2, 2)))
    model.add(tink.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tink.layers.MaxPooling2D((2, 2)))
    model.add(tink.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tink.layers.Flatten())
    model.add(tink.layers.Dense(64, activation='relu'))
    model.add(tink.layers.Dense(1, activation='softmax'))

    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['acc'])
    return model

ki = learning()

games = test_game.game()

games.games()
ki.point_up()
games.chek(0)
t,r = ki.load_state()
ap = t.shape
x,y = r.shape
print(  x,y)
model = models((x,y,1))
time.sleep(3)
for ik in range(100):
    games.games()
    time.sleep(0.1)
    t,r = ki.load_state()
    a = actions(t ,state_list)
    print(a)
    re = games.chek(a)
    print(re,end='  ||  ')
    print(a)
    state_list,Raw_list = reward_save(t,re,a,state_list,r,Raw_list)
    print('=====================')
    print(x,y)
    print(ik)
    time.sleep(0.1)
x,y = learning_fraem(Raw_list,2)
#print(x)
#print(y)
#print(len(x))
#print(len(y))
#model.fit(np.array(x),np.array(y),epochs=100)
