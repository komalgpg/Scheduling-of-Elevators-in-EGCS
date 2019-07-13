from PyQt5 import QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QRect, QAbstractAnimation
from handle_emergency import *

y_cord1 = []
groups = []
dl = [0,0,0,0]
on_from = -1
on_to = []
after_from = []
after_to = []
mk = []
rt = []
quant = []
step = 0
trips = 0


def getParameters(obj):

    global anims
    global cars
    global Timer
    global groups

    anims = [obj.anim5,obj.anim6,obj.anim7,obj.anim8]
    cars = [obj.Car1,obj.Car2,obj.Car3,obj.Car4]
    Timer = [obj.timer1, obj.timer2, obj.timer3, obj.timer4, obj.timer5, obj.timer6, obj.timer7, obj.timer8, obj.timer9,
             obj.timer10]
    groups = [obj.group, obj.msgBox1, obj.msgBox2, obj.msgBox3]

#------------------------------------------------------ PARALLEL GROUP ANIMATION -----------------------------------------------------------

def anim1(quant,end):

    anims[0].setDuration(quant * 1000)
    anims[0].setStartValue(QRect(30, cars[0].y(), 30, 28))
    anims[0].setEndValue(QRect(30, end, 30, 28))
    anims[0].finished.connect(lambda: open(0))

def anim2(quant,end):

    anims[1].setDuration(quant * 1000)
    anims[1].setStartValue(QRect(30, cars[1].y(), 30, 28))
    anims[1].setEndValue(QRect(30, end, 30, 28))
    anims[1].finished.connect(lambda: open(1))

def anim3(quant,end):

    anims[2].setDuration(quant * 1000)
    anims[2].setStartValue(QRect(30, cars[2].y(), 30, 28))
    anims[2].setEndValue(QRect(30, end, 30, 28))
    anims[2].finished.connect(lambda: open(2))

def anim4(quant,end):

    anims[3].setDuration(quant * 1000)
    anims[3].setStartValue(QRect(30, cars[3].y(), 30, 28))
    anims[3].setEndValue(QRect(30, end, 30, 28))
    anims[3].finished.connect(lambda: open(3))

#----------------------------------------------------------- OPEN ELEVATOR DOOR --------------------------------------------------------------

def open(num):

        cars[num].setPixmap(QtGui.QPixmap("Images/open.jpg"))
        Timer[num].timeout.connect(lambda :replace_close(num))
        Timer[num].setSingleShot(True)
        Timer[num].start(3000)

# --------------------------------------------------------- CLOSE ELEVATOR DOOR ---------------------------------------------------------------

def replace_close(num):

        cars[num].setPixmap(QtGui.QPixmap("Images/close.jpg"))

#------------------------------------------------------- STATION LIFTS TO DESIRED LOCATION ----------------------------------------------------

def send_toFloor(floor_aff,y_cord,case):

    global y_cord1
    global dl
    global mk
    global rt
    global quant
    global on_to
    global on_from
    global after_from
    global after_to
    y_cord1 = y_cord.copy()

    for i in range(4):
        for j in range(20):
            if (cars[i].y() >= int(y_cord[j])):
                dl[i] = j
                break

        if(i == 0):
            anim1(abs(dl[0] - floor_aff), y_cord1[floor_aff])
        elif(i == 1):
            anim2(abs(dl[1] - floor_aff), y_cord1[floor_aff])
        elif(i == 2):
            anim3(abs(dl[2] - floor_aff), y_cord1[floor_aff])
        elif(i == 3):
            anim4(abs(dl[3] - floor_aff), y_cord1[floor_aff])

    if(case == 1):
        display_messages(0)                                                                   # alert message for fire
        on_from, on_to, after_from, after_to = fire(floor_aff)
    elif(case == 2):                                                                          # alert message for flood
        display_messages(1)
        on_from, on_to, after_from, after_to = flood()
    elif(case == 3):                                                                          # alert message for bomb threat
        display_messages(2)
        on_from, on_to, after_from, after_to = threat(floor_aff)
    # print(on_from,on_to,after_from,after_to)

    moveCar(0, [floor_aff], dl)
    mk = on_to
    rt = [on_from, on_from, on_from, on_from]
    quant = [abs(on_to[0]-floor_aff), abs(on_to[1]-floor_aff), abs(on_to[2]-floor_aff), abs(on_to[3]-floor_aff)]

#------------------------------------------------------------ START ANIMATION ---------------------------------------------------------

def moveCar(state,floor,dl):

    for k in range(4):
        cars[k].setPixmap(QtGui.QPixmap("Images/close.jpg"))

    groups[0].addAnimation(anims[0])
    groups[0].addAnimation(anims[1])
    groups[0].addAnimation(anims[2])
    groups[0].addAnimation(anims[3])

    if (state == 0):
        Timer[4].timeout.connect(lambda: calculate_trips(floor))
        Timer[4].setSingleShot(True)
        Timer[4].start(abs((max(dl)-max(floor))) * 1000)

    elif (state == 1):
        Timer[6].timeout.connect(lambda: returnTrip())
        Timer[6].setSingleShot(True)
        Timer[6].start(7000)

    groups[0].start()

#-------------------------------------------------------- TRIPS REQUIRED -------------------------------------------------------

def calculate_trips(floor):

    global trips

    trips = calculate_trips_required(floor)

    Timer[5].timeout.connect(lambda :check_if_finished(1,5))
    Timer[5].start(2000)

#----------------------------------------------- CHECK IF ANIMATION IS FINISHED--------------------------------------------------

def check_if_finished(no,which):

    if(anims[0].state() == QAbstractAnimation.Stopped and anims[1].state() == QAbstractAnimation.Stopped
        and anims[2].state() == QAbstractAnimation.Stopped and anims[3].state() == QAbstractAnimation.Stopped):

        if(no == 1):
            Timer[which].stop()
            makeTrip()

        elif(no == 2):
            Timer[which].stop()
            # QtTest.QTest.qWait(2000)
            check_for_more_trips()

#--------------------------------------------------------- CHECK FOR MORE TRIPS-- ------------------------------------------------

def check_for_more_trips():

    global trips
    global step
    trips -= 1

    if(trips == 0):
        if(step == 0):
            step += 1
            QtTest.QTest.qWait(2000)
            display_messages(3)
            after_evacuation()
        elif(step == 1):
            display_messages(4)

    if(trips >= 1):
        makeTrip()

#--------------------------------------------------------------------------------------------------------------------------------

def after_evacuation():

    global mk
    global rt
    global after_from
    global on_to
    global after_to
    global quant
    global on_from
    global y_cord1
    global dl

    for i in range(4):
        for j in range(20):
            if (cars[i].y() >= int(y_cord1[j])):
                dl[i] = j
                break

    for i in range(4):
        if (i == 0):
            anim1(abs(on_from - after_from[i]), y_cord1[after_from[i]])
        elif (i == 1):
            anim2(abs(on_from - after_from[i]), y_cord1[after_from[i]])
        elif (i == 2):
            anim3(abs(on_from - after_from[i]), y_cord1[after_from[i]])
        elif (i == 3):
            anim4(abs(on_from - after_from[i]), y_cord1[after_from[i]])

    moveCar(0, after_from, dl)
    mk = after_to
    rt = after_from
    quant = [abs(after_to[0]-after_from[0]), abs(after_to[1]-after_from[1]), abs(after_to[2]-after_from[2]), abs(after_to[3]-after_from[3])]

#---------------------------------------------------------------------------------------------------------------------------------------

def makeTrip():

    QtTest.QTest.qWait(2000)
    for i in range(4):
        if (i == 0):
            anim1(quant[0], y_cord1[mk[i]])
        elif (i == 1):
            anim2(quant[1], y_cord1[mk[i]])
        elif (i == 2):
            anim3(quant[2], y_cord1[mk[i]])
        elif (i == 3):
            anim4(quant[3], y_cord1[mk[i]])
    moveCar(1, -1, -1)

#-----------------------------------------------------------------------------------------------------------------------------------------

def returnTrip():

    for i in range(4):
        if (i == 0):
            anim1(quant[0], y_cord1[rt[i]])
        elif (i == 1):
            anim2(quant[1], y_cord1[rt[i]])
        elif (i == 2):
            anim3(quant[2], y_cord1[rt[i]])
        elif (i == 3):
            anim4(quant[3], y_cord1[rt[i]])

    moveCar(-1, -1, -1)
    Timer[7].timeout.connect(lambda: check_if_finished(2,7))
    Timer[7].start(4000)

#-------------------------------------------------------------- ALERT MESSAGES ---------------------------------------------------------

def display_messages(which):

    if(which == 0):
        groups[1].move(570, 250)
        groups[1].setText("Attention, Please! Fire alarm has been activated in the building. Please evacuate by the nearest staircase or wait for the elevators!")
        groups[1].show()
    elif(which == 1):
        groups[1].move(570, 250)
        groups[1].setText("Attention, Please! Flood warning is issued. Climb to safety immediately or wait for the elevators!")
        groups[1].show()
    elif(which == 2):
        groups[1].move(570, 250)
        groups[1].setText("Attention, Please! Bomb threat warning is issued. Climb to safety or wait for the elevators!")
        groups[1].show()
    elif(which == 3):
        groups[2].move(570, 250)
        groups[1].close()
        groups[2].setText("The floor at risk is evacuated. For further safety lifts are approaching to floor " + str(after_from))
        groups[2].show()
    elif(which == 4):
        groups[3].move(570, 250)
        groups[2].close()
        groups[3].setText("Emergency situation is now under control.")
        groups[3].show()