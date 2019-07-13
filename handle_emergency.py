floor_population = [200, 100, 100, 50, 100, 100, 100, 100, 100, 100, 300, 300, 120, 120, 120, 120, 120, 120, 120, 50]       # population on each floor

#----------------------------------------------------------- FIRE --------------------------------------------------------------------

def fire(aff_floor):

    if(aff_floor == 0):

        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [4, 4, 4, 4]
        after_evac_from = [aff_floor+1, aff_floor+1, aff_floor+2, aff_floor+3]
        after_evac_to = [5, 5, 6, 6]

    elif((aff_floor-4) <= 0):

        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [0, 0, 0, 0]
        if(aff_floor == 1):
            after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor + 2, aff_floor + 3]
        else:
            after_evac_from = [aff_floor+1, aff_floor+1, aff_floor-1, aff_floor+2]
        after_evac_to = [0, 0, 0, 0]

    elif((aff_floor-4) > 0):

        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [aff_floor - 4, aff_floor - 4, aff_floor - 4, aff_floor - 4]
        if(aff_floor == 18):
            after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor - 1, aff_floor - 2]
        elif(aff_floor == 19):
            after_evac_from = [aff_floor - 1, aff_floor - 1, aff_floor - 2, aff_floor - 3]
        else:
            after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor - 1, aff_floor + 2]
        after_evac_to = [after_evac_from[0]-4, after_evac_from[1]-4, after_evac_from[2]-4, after_evac_from[3]-4]

    return aff_floor_evac_from,aff_floor_evac_to,after_evac_from,after_evac_to

#----------------------------------------------------------------- BOMB THREAT -------------------------------------------------------------------

def threat(aff_floor):

    if(aff_floor == 18):
        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [aff_floor - 4, aff_floor - 4, aff_floor - 4, aff_floor - 4]
        after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor - 1, aff_floor - 1]
        after_evac_to = [after_evac_from[0] - 4, after_evac_from[1] - 4, after_evac_from[2] - 4, after_evac_from[3] - 4]

    elif(aff_floor == 19):
        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [aff_floor - 4, aff_floor - 4, aff_floor - 4, aff_floor - 4]
        after_evac_from = [aff_floor - 1, aff_floor - 1, aff_floor - 2, aff_floor - 2]
        after_evac_to = [after_evac_from[0] - 4, after_evac_from[1] - 4, after_evac_from[2] - 4, after_evac_from[3] - 4]

    elif (aff_floor == 0):
        aff_floor_evac_from = 0
        aff_floor_evac_to = [4, 4, 4, 4]
        after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor + 2, aff_floor + 3]
        after_evac_to = [5, 5, 6, 6]

    elif(aff_floor <= 4):
        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [0, 0, 0, 0]
        after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor + 2, aff_floor + 2]
        after_evac_to = [0, 0, 0, 0]

    elif(aff_floor > 4):
        aff_floor_evac_from = aff_floor
        aff_floor_evac_to = [aff_floor - 4, aff_floor - 4, aff_floor - 4, aff_floor - 4]
        after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor - 1, aff_floor - 1]
        after_evac_to = [after_evac_from[0] + 4, after_evac_from[1] + 4, after_evac_from[2] - 4, after_evac_from[3] - 4]


    return aff_floor_evac_from, aff_floor_evac_to, after_evac_from, after_evac_to

#------------------------------------------------------------------ FLOOD ---------------------------------------------------------------------

def flood():

    aff_floor = 1
    aff_floor_evac_from = aff_floor
    aff_floor_evac_to = [aff_floor + 3, aff_floor + 3, aff_floor + 3, aff_floor + 3]
    after_evac_from = [aff_floor + 1, aff_floor + 1, aff_floor + 2, aff_floor + 2]
    after_evac_to = [aff_floor + 4, aff_floor + 4, aff_floor + 4, aff_floor + 4]

    return aff_floor_evac_from,aff_floor_evac_to,after_evac_from,after_evac_to

#-------------------------------------------------------- TRIPS REQUIRED ---------------------------------------------------------------

def calculate_trips_required(floor):

    # Considering maximum capacity of each lift as 15, trips required to cover the floor with highest population is returned.
    no_trip = 0

    for i in range(len(floor)):
        popu = floor_population[floor[i]]
        if (no_trip < round(popu / 60)):
            no_trip = round(popu / 60)

    return (no_trip)

