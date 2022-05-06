import numpy as np
import pyautogui
import cv2
import keyboard
import time

class learning:

    def __init__(self,acrn = 1,ac_num = 10) -> None:
        self.state_list = []
        self.acnum = ac_num
        self.tablesdate = []
        self.table = {}
        self.acrn = acrn # 0 ~ 10
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

        pick = np.array(pick,np.float32)
        #print(pick.shape)
        #print(pick)
        self.stsize = pick.shape
        self.state = pick
        self.Raw_state = pik
        return pick,pik #2차원 배열 || 1차원 배열

    def actions(self):
        op = []
        i = self.acrn
        for l in range(10):
            if i > 0:
                i -= 1
                op.append(1)
            else:
                op.append(0)
        rn = np.random.randint(0,10)
        acrn = op[rn]
        ac_num = self.acnum
        ac_list = []
        sc = self.state
        sc_list = self.state_list
        key = True
        if 0 != len(sc_list):
            for i in sc_list:
                if np.array_equal(sc, i[0]) and i[1] == 2:
                    ac_list.append(i[2])
                    key = False

        if key or acrn == 't':
            ac = np.random.randint(0,ac_num) #호기심? 넣기

        else:
            ip = {}
            for i in ac_list:
                try: ip[str(i)] += 1
                except: ip[str(i)] = 1
            ac = ac_list[0  ]

        self.action = ac
        return ac

    def reward_save(self,reward):
        self.reward = reward
        sclist = self.state_list
        st = self.state
        ac = self.action
        sclist.append([st,reward,ac])
        self.state_list = sclist
        return sclist

    def tables(self):
        tinQ = {}
        tinqs = self.tablesdate
        tinQ['state'] = self.state
        tinQ['reward'] = self.reward
        tinQ['actions'] = self.action
        tinqs.append([self.state,self.reward,self.action])
        self.table = tinQ
        return tinQ

    def tables_date(self):
        return self.tablesdate



import test_game

games = test_game.game()
ki = learning(0,4)
games.games()
ki.point_up()
games.chek(0)
for i in range(100):
    games.games()
    time.sleep(0.1)
    ki.load_state()
    ac = ki.actions()
    #print(ac)
    re = games.chek(ac)
    ki.reward_save(re)
    print(ki.tables())
    time.sleep(0.2)
for i in ki.tables_date():
    print(i)
