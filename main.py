# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'u5.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import design
import time

from data_manipulation import *
from working_of_emerg import *

wt = []
st = []
tt = []
count = [0, 0, 0, 0]
AllQueues = []
calling_floors = []
car_direc = [0,0,0,0]
newDF = [0,0,0,0]
y_cord = [650, 620]
moving_dir = [0,0,0,0]
prev_value = [650,650,650,650]
fc = [-1,-1,-1,-1]
timers = []
Cars = []
floors = []
Anim = []
Queues = []
q1 = []
q2 = []
q3 = []
q4 = []
q1_d = []
q2_d = []
q3_d = []
q4_d = []
upward_calls = []
downward_calls = []
assigned_car_dir = ['','','','']


class MyForm(QtWidgets.QWidget, design.Ui_Form):

    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.calculate()
        self.all_lists()

#------------------------------------------------- HANDLE EMERGENCY CASES -----------------------------------------------------------------------

    def TextBox(self,case):

        for i in range(8):                                                                          # clear all calls in queue
            AllQueues[i].clear()

        for i in range(40):                                                                         # clear all calling floor data
            calling_floors[i].setEnabled(False)
            calling_floors[i].setStyleSheet('border:1px solid grey; border-radius:3px')

        for i in range(4):                                                                          # stop all ongoing animation
            Anim[i].stop()

        if(case == 1 or case == 3):                                                                 # FIRE AND BOBM THREAT

            text,ok = QtWidgets.QInputDialog.getText(None,'Emergency Message','Enter the floor affected: ')

            while ok and text!='':
                try:
                    if(y_cord[int(text)]):
                        getParameters(self)
                        send_toFloor(int(text), y_cord, case)
                        break
                except IndexError:
                    text, ok = QtWidgets.QInputDialog.getText(None, 'Emergency Message', 'Enter valid floor affected (0 to 19): ')

        elif(case == 2):                                                                            # FLOOD

            getParameters(self)
            send_toFloor(1, y_cord, case)

# ------------------------------------------------ Y-CORDINATES OF EACH FLOOR ------------------------------------------------------------------

    def calculate(self):
        for i in range(2, 20):
            y_cord.append(round(y_cord[i - 1] - 34.35, 2))
        # print(y_cord)
        parameters.initialize(self)

# ----------------------------------------------------------------------------------------------------------------------------------------------

    def all_lists(self):

        global Cars
        global floors
        global Anim
        global Queues
        global timers
        global AllQueues
        global calling_floors

        floors = [[self.L1_G, self.L1_1, self.L1_2, self.L1_3, self.L1_4, self.L1_5, self.L1_6, self.L1_7, self.L1_8,
                   self.L1_9, self.L1_10, self.L1_11, self.L1_12, self.L1_13, self.L1_14, self.L1_15, self.L1_16,
                   self.L1_17, self.L1_18, self.L1_19],
                  [self.L2_G, self.L2_1, self.L2_2, self.L2_3, self.L2_4, self.L2_5, self.L2_6, self.L2_7, self.L2_8,
                   self.L2_9, self.L2_10, self.L2_11, self.L2_12, self.L2_13, self.L2_14, self.L2_15, self.L2_16,
                   self.L2_17, self.L2_18, self.L2_19],
                  [self.L3_G, self.L3_1, self.L3_2, self.L3_3, self.L3_4, self.L3_5, self.L3_6, self.L3_7, self.L3_8,
                   self.L3_9, self.L3_10, self.L3_11, self.L3_12, self.L3_13, self.L3_14, self.L3_15, self.L3_16,
                   self.L3_17, self.L3_18, self.L3_19],
                  [self.L4_G, self.L4_1, self.L4_2, self.L4_3, self.L4_4, self.L4_5, self.L4_6, self.L4_7, self.L4_8,
                   self.L4_9, self.L4_10, self.L4_11, self.L4_12, self.L4_13, self.L4_14, self.L4_15, self.L4_16,
                   self.L4_17, self.L4_18, self.L4_19]]

        calling_floors = [self.UG,self.U1,self.U2,self.U3,self.U4,self.U5,self.U6,self.U7,self.U8,self.U9,self.U10,
                          self.U11,self.U12,self.U13,self.U14,self.U15,self.U16,self.U17,self.U18,self.U19,
                          self.DG,self.D1,self.D2,self.D3,self.D4,self.D5,self.D6,self.D7,self.D8,self.D9,self.D10,
                          self.D11,self.D12,self.D13,self.D14,self.D15,self.D16,self.D17,self.D18,self.D19]

        Cars = [self.Car1, self.Car2, self.Car3, self.Car4]
        Anim = [self.anim1, self.anim2, self.anim3, self.anim4]
        Queues = [self.Queue1,self.Queue2,self.Queue3,self.Queue4]
        timers = [self.timer1,self.timer2,self.timer3,self.timer4,self.timer5,self.timer6,self.timer7,self.timer8,self.timer9
                  ,self.timer10,self.timer11,self.timer12,self.timer13,self.timer14,self.timer15,self.timer16]
        AllQueues = [q1, q2, q3, q4, q1_d, q2_d, q3_d, q4_d]

        for g in range(4):
            for h in range(20):
                floors[g][h].setEnabled(False)
                floors[g][h].setStyleSheet("color:black")

# ----------------------------------------------------- ALGORITHM ------------------------------------------------------------------

    def move_whichCar(self,btn):

        global d1
        global count
        # global newDF
        floor_calling = btn.objectName()
        # DF = 1
        selected_car = 0

        for i in range(4):
            for j in range(20):                                                             # current position of all elevators
                if(Cars[i].y() >= int(y_cord[j])):
                    d1 = j
                    break

            d = abs(d1 - int(floor_calling[1:3]))                                            # distance between calling floor and current position


            if(moving_dir[i] == 0):                                                          #idle condition
                newDF[i] = 20 + 1 - d

            elif(moving_dir[i] == -1):                                                       #car moving down
                if(floor_calling[0] == 'U'):
                    newDF[i] = 1

                elif(floor_calling[0] == 'D'):
                    if (Cars[i].y() > y_cord[int(floor_calling[1:3])]):                     # car has left the calling floor
                        newDF[i] = 1
                    elif (Cars[i].y() < y_cord[int(floor_calling[1:3])] and assigned_car_dir[i] == floor_calling[0]):
                        
                        newDF[i] = 20 + 2 - d
                    else:
                        
                        newDF[i] = 2

            elif(moving_dir[i] == 1):                                                       #car moving up
                
                if(floor_calling[0] == 'D'):
                    if (Cars[i].y() < y_cord[int(floor_calling[1:3])]):
                        newDF[i] = 1
                    elif(Cars[i].y() > y_cord[int(floor_calling[1:3])] and assigned_car_dir[i] == floor_calling[0]):
                        
                        newDF[i] = 20 + 2 - d
                    else:
                        newDF[i] = 2

                elif(floor_calling[0] == 'U'):
                    
                    if(Cars[i].y() < y_cord[int(floor_calling[1:3])]):                  #car has left the calling floor
                        newDF[i] = 1
                    elif(Cars[i].y() > y_cord[int(floor_calling[1:3])] and assigned_car_dir[i] == floor_calling[0]):
                        newDF[i] = 20 + 2 - d
                    else:
                        newDF[i] = 2

            
            selected_car = newDF.index(max(newDF))
           

        return selected_car,floor_calling

# --------------------------------------------------------- DIRECTION OF THE ELEVATOR ------------------------------------------------------------

    def check_direction(self,car,floor):

        if(car == 0 and floor[1] == 1 or floor[1] == 10):
            # count[0] = parameters.no_of_dest(self, 1, 0)
            if(len(q1) > 1):
                if(q1[1][0] - q1[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif(q1[1][0] - q1[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif(len(q1) == 1):
                assigned_car_dir[car] = ''

        elif(car == 1 and floor[1] == 1 or floor[1] == 10):
            # count[1] = parameters.no_of_dest(self, 1, 1)
            if (len(q2) > 1):
                if (q2[1][0] - q2[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q2[1][0] - q2[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q2) == 1):
                assigned_car_dir[car] = ''

        elif (car == 2 and floor[1] == 1 or floor[1] == 10):
            if (len(q3) > 1):
                if (q3[1][0] - q3[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q3[1][0] - q3[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q3) == 1):
                assigned_car_dir[car] = ''

        elif (car == 3 and floor[1] == 1 or floor[1] == 10):
            if (len(q4) > 1):
                if (q4[1][0] - q4[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q4[1][0] - q4[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q4) == 1):
                assigned_car_dir[car] = ''

        elif (car == 0 and floor[1] == -1 or floor[1] == -10):
            if (len(q1_d) > 1):
                if (q1_d[1][0] - q1_d[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q1_d[1][0] - q1_d[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q1_d) == 1):
                assigned_car_dir[car] = ''

        elif (car == 1 and floor[1] == -1 or floor[1] == -10):
            if (len(q2_d) > 1):
                if (q2_d[1][0] - q2_d[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q2_d[1][0] - q2_d[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q2_d) == 1):
                assigned_car_dir[car] = ''

        elif (car == 2 and floor[1] == -1 or floor[1] == -10):
            if (len(q3_d) > 1):
                if (q3_d[1][0] - q3_d[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q3_d[1][0] - q3_d[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q3_d) == 1):
                assigned_car_dir[car] = ''

        elif (car == 3 and floor[1] == -1 or floor[1] == -10):
            if (len(q4_d) > 1):
                if (q4_d[1][0] - q4_d[0][0] >= 1):
                    assigned_car_dir[car] = 'U'
                elif (q4_d[1][0] - q4_d[0][0] <= 1):
                    assigned_car_dir[car] = 'D'
            elif (len(q4_d) == 1):
                assigned_car_dir[car] = ''

# ---------------------------------------------------------- ANIMATION -------------------------------------------------------------------

    def move_Car(self,car,floor_calling):

        for k in range(4):
            Cars[k].setPixmap(QtGui.QPixmap("Images/close.jpg"))

        dist = floor_calling[0] - y_cord.index(prev_value[car])

        timers[car+12].timeout.connect(lambda: self.check_direction(car,floor_calling))
        timers[car+12].start(1000)

        if(dist < 0):
            moving_dir[car] = -1
        elif(dist == 0):
            moving_dir[car] = 0
        elif(dist > 0):
            moving_dir[car] = 1

        if(dist == 0):
            quantum = 0.1
        else:
            quantum = abs(dist)

        Anim[car].setDuration(quantum * 1000)
        Anim[car].setStartValue(QRect(30, prev_value[car], 30, 28))
        Anim[car].setEndValue(QRect(30, y_cord[floor_calling[0]], 30, 28))

        Anim[car].start()

        Anim[car].finished.connect(lambda: self.destination_panel(floor_calling,car))
        Anim[car].finished.connect(lambda :self.replace_open(car))

        QtTest.QTest.qWait(quantum * 1000)

# --------------------------------------- ELEVATOR REACHED AT THE DESIRED LOCATION FOR UPWARD CALL ----------------------------------------------------

    def proceed_up(self,floor,car,list_in_use):

        global wt
        global st

        if (list_in_use and floor == list_in_use[0]):

            if (floor[0] not in upward_calls):
                upward_calls.append(floor[0])

                prev_value[car] = y_cord[floor[0]]
                car_direc[car] = floor[1]

                for i in range(20):
                    if (i != floor[0]):
                        floors[car][i].setEnabled(True)
                        floors[car][i].setStyleSheet('color:red')
                    else:
                        floors[car][i].setEnabled(False)
                        floors[car][i].setStyleSheet('color:black')

                if (floor[1] == 10):

                    dest = parameters.check_for_same_dest(self, floor[0], 'U', car)

                    while len(dest):
                            dest[0].JT = time.time() - dest[0].t1
                            # if(car == 0 and dest[0].WT != 0):
                            st.append(round(dest[0].JT, 2))
                            wt.append(round(dest[0].WT, 2))

                            self.Output.append("Time taken to travel from " + dest[0].floor_call[1:3] + " to " + str(floor[0]) + " is : " +
                                               str(round(dest[0].JT + dest[0].WT,2)) + " [ WT : " + str(dest[0].WT) + ", JT : " + str(round(dest[0].JT,2)) + " ]\n")

                            parameters.remove(self,dest[0].destination,str(floor[0]),dest[0])
                            if(dest[0].destination == ""):
                                dest[0].status = "yes"
                            del dest[0]

                    parameters.clear(self, car)
                    ret = parameters.allClear(self, 1, car)
                    if (ret == 0):
                        moving_dir[car] = 0

                elif (floor[1] == 1):

                    floor[2].setStyleSheet('border:1px solid grey; border-radius:3px')
                    tables[car][floor[0]].t1 = time.time()
                    tables[car][floor[0]].WT = round(tables[car][floor[0]].t1- tables[car][floor[0]].start,2)

                    timers[car+4].timeout.connect(lambda: self.destination(car,floor[0]))
                    timers[car+4].setSingleShot(True)
                    timers[car+4].start(4000)

                if (upward_calls):
                    del upward_calls[0]

                if (car == 0):
                    del q1[0]
                    timers[car + 4].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 4].setSingleShot(True)
                    timers[car + 4].start(8000)
                elif (car == 1):
                    del q2[0]
                    timers[car + 4].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 4].setSingleShot(True)
                    timers[car + 4].start(8000)
                elif (car == 2):
                    del q3[0]
                    timers[car + 4].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 4].setSingleShot(True)
                    timers[car + 4].start(8000)
                elif (car == 3):
                    del q4[0]
                    timers[car + 4].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 4].setSingleShot(True)
                    timers[car + 4].start(8000)

# ----------------------------------------------- NEXT CALL TO ATTEND --------------------------------------------------------------------

    def next_call_to_attend(self, car):

        if(car == 0 and q1 and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(0, q1[0])
        elif(car == 1 and q2 and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(1, q2[0])
        elif(car == 2 and q3 and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(2, q3[0])
        elif(car == 3 and q4 and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(3, q4[0])

        elif (car == 0 and q1_d and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(0, q1_d[0])
        elif (car == 1 and q2_d and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(1, q2_d[0])
        elif (car == 2 and q3_d and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(2, q3_d[0])
        elif (car == 3 and q4_d and Anim[car].state() == QAbstractAnimation.Stopped):
            self.move_Car(3, q4_d[0])

# ----------------------------------------- ELEVATOR REACHED AT THE DESIRED LOCATION FOR DOWNWARD CALL ------------------------------------------------------

    def proceed_down(self,floor,car,list_in_use):

        global st
        global wt

        if (list_in_use and floor == list_in_use[0]):

            if (floor[0] not in downward_calls):
                downward_calls.append(floor[0])
                prev_value[car] = y_cord[floor[0]]
                car_direc[car] = floor[1]

                for i in range(20):
                    if (i != floor[0]):
                        floors[car][i].setEnabled(True)
                        floors[car][i].setStyleSheet("color:red")
                    else:
                        floors[car][i].setEnabled(False)
                        floors[car][i].setStyleSheet("color:black")

                if (floor[1] == -10):

                    dest = parameters.check_for_same_dest(self, floor[0], 'D', car)

                    while len(dest):

                        dest[0].JT = time.time() - dest[0].t1
                        # if(car == 0 and dest[0].WT != 0):
                        st.append(round(dest[0].JT, 2))
                        wt.append(round(dest[0].WT, 2))

                        self.Output.append("Time taken to travel from " + dest[0].floor_call[1:3] + " to " + str(floor[0]) + " is : " +
                                           str(round(dest[0].JT + dest[0].WT,2)) + " [ WT : " + str(dest[0].WT) + ", JT : " + str(round(dest[0].JT,2)) + " ]\n")

                        parameters.remove(self,dest[0].destination,str(floor[0]),dest[0])

                        if(dest[0].destination == ""):
                            dest[0].status = "yes"
                        del dest[0]

                    parameters.clear(self, car)
                    ret = parameters.allClear(self, -1, car)
                    if(ret == 0):
                        moving_dir[car] = 0

                elif (floor[1] == -1):

                    floor[2].setStyleSheet('border:1px solid grey; border-radius:3px')

                    tables[car][20 + floor[0]].t1 = time.time()
                    tables[car][20 + floor[0]].WT = round(tables[car][20 + floor[0]].t1 - tables[car][20 + floor[0]].start, 2)

                    timers[car+8].timeout.connect(lambda: self.destination(car,20 + floor[0]))
                    timers[car+8].setSingleShot(True)
                    timers[car+8].start(4000)

                if (downward_calls):
                    del downward_calls[0]

                if (car == 0):
                    del q1_d[0]
                    timers[car + 8].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 8].setSingleShot(True)
                    timers[car + 8].start(8000)
                elif (car == 1):
                    del q2_d[0]
                    timers[car + 8].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 8].setSingleShot(True)
                    timers[car + 8].start(8000)
                elif (car == 2):
                    del q3_d[0]
                    timers[car + 8].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 8].setSingleShot(True)
                    timers[car + 8].start(8000)
                elif (car == 3):
                    del q4_d[0]
                    timers[car + 8].timeout.connect(lambda: self.next_call_to_attend(car))
                    timers[car + 8].setSingleShot(True)
                    timers[car + 8].start(8000)

#------------------------------------------- REACHED AT CALLING FLOOR BUT DESTINATION NOT GIVEN ------------------------------------------------------------------

    def destination(self,car,floor):

        for i in range(20):
            floors[car][i].setEnabled(False)
            floors[car][i].setStyleSheet('color:black')

        if(car == 0 and not q1):
            self.make_changes(floor,car)
        elif (car == 1 and not q2):
            self.make_changes(floor, car)
        elif (car == 2 and not q3):
            self.make_changes(floor, car)
        elif (car == 3 and not q4):
            self.make_changes(floor, car)

        elif (car == 0 and not q1_d):
            self.make_changes(floor, car)
        elif (car == 1 and not q2_d):
            self.make_changes(floor, car)
        elif (car == 2 and not q3_d):
            self.make_changes(floor, car)
        elif (car == 3 and not q4_d):
            self.make_changes(floor, car)

#------------------------------------------------------------- MANIPULATE DATA ---------------------------------------------------------------

    def make_changes(self,floor,car):

        if(tables[car][floor].floor_call != "" and tables[car][floor].destination == ""):
            moving_dir[car] = 0
            tables[car][floor].status = "yes"
            parameters.clear(self, car)

# ------------------------------------------------- AFTER COMPLETION OF ANIMATION --------------------------------------------------------------------------

    def destination_panel(self,floor,car):

        if (Cars[car].y() == int(y_cord[floor[0]]) or Cars[car].y() == int(y_cord[floor[0]]) - 1):

            if(floor[1] ==  1 or floor[1] == 10):

                if(car == 0):
                    self.proceed_up(floor,car,q1)
                elif(car == 1):
                    self.proceed_up(floor,car,q2)
                elif(car == 2):
                    self.proceed_up(floor,car,q3)
                else:
                    self.proceed_up(floor,car,q4)


            elif(floor[1] == -1 or floor[1] == -10):

                if(car == 0):
                    self.proceed_down(floor,car,q1_d)
                elif(car == 1):
                    self.proceed_down(floor,car,q2_d)
                elif(car == 2):
                    self.proceed_down(floor,car,q3_d)
                else:
                    self.proceed_down(floor,car,q4_d)

# -------------------------------------------------------------- SORT THE CALLS ------------------------------------------------------------------------

    def sort_tuples(self,listTuple,asc_desc):

        if(asc_desc == 0):
            listTuple.sort(key=lambda x: x[0])
        else:
            listTuple.sort(reverse=True,key=lambda x: x[0])

# ------------------------------------------------------ IF SAME CALL GIVEN MULTIPLE TIMES --------------------------------------------------------------

    def check(self,listTuple,floor,dir):

        for item in listTuple:
            if(floor == item[0] and dir == item[1]):
                return -1
            if(floor == item[0] and item[1] == 1 or item[1] == -1):
                return -1
        return 0

# ------------------------------------------------ ADD DESTINATION DETAILS IN DATA MANIPULATION -----------------------------------------------------------

    def dest_add(self,car,fc,call_or_dest,dir):

        if(dir == 1):

            if (tables[car][fc].destination == ""):
                tables[car][fc].destination = call_or_dest[3:5]
                tables[car][fc].direction = 'U'     ###################################
                Queues[car].append(call_or_dest[3:5])
            else:
                var = tables[car][fc].destination
                if (call_or_dest[3:5] not in var):
                    tables[car][fc].destination = var + "," + call_or_dest[3:5]
                    Queues[car].append(call_or_dest[3:5])

        elif(dir == -1) :

            if (tables[car][20 + fc].destination == ""):
                tables[car][20 + fc].destination = call_or_dest[3:5]
                tables[car][20 + fc].direction = 'D'  ###################################
                Queues[car].append(call_or_dest[3:5])
            else:
                var = tables[car][20 + fc].destination
                if (call_or_dest[3:5] not in var):
                    tables[car][20 + fc].destination = var + "," + call_or_dest[3:5]
                    Queues[car].append(call_or_dest[3:5])

#------------------------------------------------ IF NEXT CALL IS GIVEN THROUGH DESTINATION PANEL --------------------------------------------

    def only_dest(self, car, fc, call_or_dest, dir):

        if(dir  == 1):
            var = tables[car][fc].destination
            if(call_or_dest[3:5] not in var):
                tables[car][fc].destination = var + "," + call_or_dest[3:5]
            tables[car][fc].floor_call = 'U' + str(fc)
            tables[car][fc].WT = 0.0
            tables[car][fc].t1 = time.time()

        elif(dir == -1):
            var = tables[car][20 + fc].destination
            if (call_or_dest[3:5] not in var):
                tables[car][20 + fc].destination = var + "," + call_or_dest[3:5]
            tables[car][20 + fc].floor_call = 'D' + str(fc)
            tables[car][20 + fc].WT = 0.0
            tables[car][20 + fc].t1 = time.time()


# ------------------------------------------------------- WHEN BUTTON IS CLICKED -------------------------------------------------------------

    def startAnimation(self, btn):

        call_or_dest = btn.objectName()

        if(call_or_dest.startswith('U')):                                                                   # if upward call i.e (U2)

            chk = 1                                                                                         # to check whether already entered in table
            btn.setStyleSheet('border:1px solid grey; border-radius:3px; background-color: yellow')
            car , floor_call = self.move_whichCar(btn)

            if (tables[car][int(floor_call[1:3])].floor_call == ""):
                chk = 0

            tables[car][int(floor_call[1:3])].floor_call = call_or_dest
            tables[car][int(floor_call[1:3])].elev = car
            tables[car][int(floor_call[1:3])].start = time.time()

            if(chk == 0):

                if(car == 0 ):
                    q1.append((int(floor_call[1:3]), 1, btn))
                    self.sort_tuples(q1, 0)
                    self.move_Car(car, q1[0])

                elif(car == 1):
                    q2.append((int(floor_call[1:3]), 1, btn))
                    self.sort_tuples(q2, 0)
                    self.move_Car(car,q2[0])

                elif(car == 2):
                    q3.append((int(floor_call[1:3]), 1, btn))
                    self.sort_tuples(q3, 0)
                    self.move_Car(car, q3[0])

                else:
                    q4.append((int(floor_call[1:3]), 1, btn))
                    self.sort_tuples(q4, 0)
                    self.move_Car(car, q4[0])

        elif(call_or_dest.startswith('D')):                                                                    # if downward call i.e (D2)

            btn.setStyleSheet('border:1px solid grey; border-radius:3px; background-color: yellow')
            car, floor_call = self.move_whichCar(btn)
            chk = 1

            if (tables[car][20 + int(floor_call[1:3])].floor_call == ""):
                chk = 0

            tables[car][20 + int(floor_call[1:3])].floor_call = call_or_dest
            tables[car][20 + int(floor_call[1:3])].elev = car
            tables[car][20 + int(floor_call[1:3])].start = time.time()

            if (chk == 0):

                if (car == 0):
                    q1_d.append((int(floor_call[1:3]), -1, btn))
                    self.sort_tuples(q1_d, 1)
                    self.move_Car(car, q1_d[0])

                elif (car == 1):
                    q2_d.append((int(floor_call[1:3]), -1, btn))
                    self.sort_tuples(q2_d, 1)
                    self.move_Car(car, q2_d[0])

                elif (car == 2):
                    q3_d.append((int(floor_call[1:3]), -1, btn))
                    self.sort_tuples(q3_d, 1)
                    self.move_Car(car, q3_d[0])

                else:
                    q4_d.append((int(floor_call[1:3]), -1, btn))
                    self.sort_tuples(q4_d, 1)
                    self.move_Car(car, q4_d[0])

        else:                                                                                                  # if call from destination panel i.e (L1_2)
            global fc
            car = int(call_or_dest[1]) - 1
            fc[car] = y_cord.index(prev_value[car])

            if(car_direc[car] > 0):

                if (car == 0):
                    self.dest_add(0, fc[car], call_or_dest, 1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], 1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, 1)
                    chk = self.check(q1, int(call_or_dest[3:5]), 10)
                    if (chk == 0):
                        q1.append((int(call_or_dest[3:5]), 10))
                    self.dest_sort(q1, 0, y_cord.index(prev_value[car]))

                elif (car == 1):
                    self.dest_add(1, fc[car], call_or_dest, 1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], 1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, 1)
                    chk = self.check(q2, int(call_or_dest[3:5]), 10)
                    if (chk == 0):
                        q2.append((int(call_or_dest[3:5]), 10))
                    self.dest_sort(q2, 0, y_cord.index(prev_value[car]))

                elif (car == 2):
                    self.dest_add(2, fc[car], call_or_dest, 1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], 1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, 1)
                    chk = self.check(q3, int(call_or_dest[3:5]), 10)
                    if (chk == 0):
                        q3.append((int(call_or_dest[3:5]), 10))
                    self.dest_sort(q3, 0, y_cord.index(prev_value[car]))

                else:
                    self.dest_add(3, fc[car], call_or_dest, 1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], 1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, 1)
                    chk = self.check(q4, int(call_or_dest[3:5]), 10)
                    if (chk == 0):
                        q4.append((int(call_or_dest[3:5]), 10))
                    self.dest_sort(q4, 0, y_cord.index(prev_value[car]))


            elif(car_direc[car] < 0):

                if (car == 0):
                    self.dest_add(0, fc[car], call_or_dest, -1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], -1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, -1)
                    chk = self.check(q1_d, int(call_or_dest[3:5]), -10)
                    if (chk == 0):
                        q1_d.append((int(call_or_dest[3:5]), -10))
                    self.dest_sort(q1_d, 1, y_cord.index(prev_value[car]))

                elif (car == 1):
                    self.dest_add(1, fc[car], call_or_dest, -1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], -1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, -1)
                    chk = self.check(q2_d, int(call_or_dest[3:5]), -10)
                    if (chk == 0):
                        q2_d.append((int(call_or_dest[3:5]), -10))
                    self.dest_sort(q2_d, 1, y_cord.index(prev_value[car]))

                elif (car == 2):
                    self.dest_add(2, fc[car], call_or_dest, -1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], -1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, -1)
                    chk = self.check(q3_d, int(call_or_dest[3:5]), -10)
                    if (chk == 0):
                        q3_d.append((int(call_or_dest[3:5]), -10))
                    self.dest_sort(q3_d, 1, y_cord.index(prev_value[car]))

                else:
                    self.dest_add(3, fc[car], call_or_dest, -1)
                    x = parameters.search_dest_without_floor_call(self, car, fc[car], -1)
                    if (x != -1):
                        self.only_dest(car, fc[car], call_or_dest, -1)
                    chk = self.check(q4_d, int(call_or_dest[3:5]), -10)
                    if (chk == 0):
                        q4_d.append((int(call_or_dest[3:5]), -10))
                    self.dest_sort(q4_d, 1, y_cord.index(prev_value[car]))

# ------------------------------------------------------ SORT DESTINATION ----------------------------------------------------------------------

    def dest_sort(self,li,dir,threshold):

        if(dir == 0):
            sub = []
            for sub_list in li:
                if(sub_list[0] < threshold):
                    sub.append(sub_list)

            if(sub):
                for i in range(len(sub)):
                    del li[li.index(sub[i])]
                self.sort_tuples(sub,1)
            else:
                self.sort_tuples(li,0)

            while sub:
                li.append(sub[0])
                del sub[0]

        elif(dir == 1):
            sub = []
            for sub_list in li:
                if (sub_list[0] > threshold):
                    sub.append(sub_list)

            if (sub):
                for i in range(len(sub)):
                    del li[li.index(sub[i])]
                self.sort_tuples(sub, 0)
            else:
                self.sort_tuples(li, 1)

            while sub:
                li.append(sub[0])
                del sub[0]

# ------------------------------------------------------- OPEN ELEVATOR DOOR --------------------------------------------------------------------

    def replace_open(self,num):

        if(assigned_car_dir[num] == 'U'):
            Cars[num].setPixmap(QtGui.QPixmap("Images/open_up.png"))
        elif(assigned_car_dir[num] == 'D'):
            Cars[num].setPixmap(QtGui.QPixmap("Images/open_down.png"))
        elif(assigned_car_dir[num] == ''):
            Cars[num].setPixmap(QtGui.QPixmap("Images/open.jpg"))

        timers[num].timeout.connect(lambda :self.replace_close(num))
        timers[num].setSingleShot(True)
        timers[num].start(3000)

# ----------------------------------------------------- CLOSE ELEVATOR DOOR -----------------------------------------------------------------------

    def replace_close(self,num):

        Cars[num].setPixmap(QtGui.QPixmap("Images/close.jpg"))

# ------------------------------------------------ AFTER EMERGENCY SITUATION -----------------------------------------------------------------------

    def back_to_normal(self):
        import subprocess
        # self.close()
        p = subprocess.Popen("python main.py", shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

# ----------------------------------------------------------------------------------------------------------------------------------------------------

    def analysis(self):

        tm = 0
        for i in range(len(wt)):
            tm += wt[i]

        self.AWT.setText(str(round(tm/len(wt), 2)) + " sec")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.showMaximized()
    sys.exit(app.exec_())