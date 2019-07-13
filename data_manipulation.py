tables = []
table = []
table1 = []
table2 = []
table3 = []

class parameters:

    def __init__(self,floor_call,destination,elev,direction,start,t1,WT,JT,status):
        self.floor_call = floor_call
        self.destination = destination
        self.elev = elev
        self.direction = direction
        self.start = start
        self.t1 = t1
        self.WT = WT
        self.JT = JT
        self.status = status

#---------------------------------------------------------- INITIALIZATION ---------------------------------------------------------------

    def initialize(self):

        for i in range(40):
            obj = parameters("", "", "", "", 0.0, 0.0, 0.0, 0.0, "no")
            table.append(obj)
            obj1 = parameters("", "", "", "", 0.0, 0.0, 0.0, 0.0, "no")
            table1.append(obj1)
            obj2 = parameters("", "", "", "", 0.0, 0.0, 0.0, 0.0, "no")
            table2.append(obj2)
            obj3 = parameters("", "", "", "", 0.0, 0.0, 0.0, 0.0, "no")
            table3.append(obj3)

        tables.append(table)
        tables.append(table1)
        tables.append(table2)
        tables.append(table3)

# --------------------------------------- CALL IS GIVEN AT THE DESTINATION PANEL ---------------------------------------------------------------

    def search_dest_without_floor_call(self, car, fc, dir):

            if(dir == 1):
                if(tables[car][fc].floor_call == "" and tables[car][fc].destination != ""):
                    return fc
            elif(dir == -1):
                if (tables[car][20 + fc].floor_call == "" and tables[car][20 + fc].destination != ""):
                    return 20 + fc
            return -1

# ------------------------------------------------ IF MULTIPLE FLOOR CALLS HAVE SAME DESTINATION ----------------------------------------

    def check_for_same_dest(self,floor,dir,car):

            sub_list = []
            for i in range(40):
                if(tables[car][i].destination != "" and str(floor) in tables[car][i].destination and dir == tables[car][i].direction):
                    sub_list.append(tables[car][i])
            return sub_list

#----------------------------------------------------- DELETE DESTINATION WHEN REACHED ---------------------------------------

    def remove(self,str,floor,st):
        calls = str.split(",")
        if(floor in calls):
            calls.remove(floor)
        st.destination = ",".join(calls)

#--------------------------------------------- CLEAR DATA AFTER COMPLETION STATUS ---------------------------------------------

    def clear(self,car):

            for i in range(40):
                if(tables[car][i].status == "yes"):
                    tables[car][i].floor_call = ""
                    tables[car][i].destination = ""
                    tables[car][i].elev = ""
                    tables[car][i].direction = ""
                    tables[car][i].start = 0.0
                    tables[car][i].t1 = 0.0
                    tables[car][i].WT = 0.0
                    tables[car][i].JT = 0.0
                    tables[car][i].status = "no"

#------------------------------------------------------------- CLEAR ----------------------------------------------------------

    def allClear(self, dir, car):

        if(dir == 1):
            for i in range(20):
                if(tables[car][i].floor_call != ""):
                    return  -1
            return 0
        elif(dir == -1):
            for i in range(20):
                if(tables[car][20 + i].floor_call != ""):
                    return  -1
            return 0