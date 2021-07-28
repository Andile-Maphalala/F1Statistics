from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import csv
from os import path
from .models import *
import pdb;
import os
from .forms import *
import math
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from django.contrib import messages #import messages
# Create your views here.

#Qauly variables
d1 = ''
d2 = ''
Driver1Best = 0
Driver2Best = 0
Driver1Worst = 0
Driver2Worst = 0
Driver1Avg = 0
Driver2Avg = 0
Driver1Q3 = 0
Driver2Q3 = 0
Driver1Q2 = 0
Driver2Q2 = 0
Delta = 0
Driver1Poles = 0
Driver2Poles = 0


#Race variables

D1TotalPoints = 0
D1AveragePoints = 0
D1AverageWithNCPoints = 0
D1AverageFinishs = 0
D1BestFinish = 0
D1RaceWins = 0
D1RacePodiums = 0
D1TeamContribution = 0
D1RaceFastestLaps = 0
D1RaceDNF = 0
D1AveragePositionGain = 0
D1MostPositionsGained = 0

D2TotalPoints = 0
D2AveragePoints = 0
D2AverageWithNCPoints = 0
D2AverageFinishs = 0
D2BestFinish = 0
D2RaceWins = 0
D2RacePodiums = 0
D2TeamContribution = 0
D2RaceFastestLaps = 0
D2RaceDNF = 0
D2AveragePositionGain = 0
D2MostPositionsGained = 0



def index(request):
    # LoadDrivers()
    # LoadQauly()
    # GetStartingGrid()
    # GetFastLaps()
    # GetRaceResult()
    return render(request,'Head2Head/index.html')

def drivers(request):
    DriverObjetList = DriverClass.objects.all()
    context = {'myDrivers':DriverObjetList}

    return render(request,'Head2Head/drivers.html',context)


def comparedrivers(request):
    if request.method == 'GET':
        print('Printing Post: ',request.GET)
        form = Driverform(request.GET)
        if form.is_valid():
  
            
            driv1 = form.cleaned_data['driver1']
            driv2 = form.cleaned_data['driver2']
            
    

            GetQaulyDriverStats(driv1,driv2)
            GetRaceDriverStats(driv1,driv2)
            

            DriverObjetList = DriverClass.objects.all().order_by('Name')

            searchd1 = [x for x in DriverObjetList if x.No == driv1]
            searchd2 = [x for x in DriverObjetList if x.No == driv2]


            Qualyobject = {'d1best': Driver1Best, 'd2best': Driver2Best,
                            'd1worst': Driver1Worst, 'd2worst': Driver2Worst,
                            'd1avg': Driver1Avg, 'd2avg': Driver2Avg,
                            'd1q3': Driver1Q3, 'd2q3': Driver2Q3,
                            'd1q2': Driver1Q2, 'd2q2': Driver2Q2,
                            'd1': d1, 'd2': d2,
                            'd1img': searchd1[0].img, 'd2img': searchd2[0].img,
                            'd1pole': Driver1Poles, 'd2pole': Driver2Poles,
                            'd1no': driv1, 'd2no': driv2,
                             'delta': Delta,
            
            }

            Raceobject = {'d1total': D1TotalPoints, 'd2total': D2TotalPoints,
                            'd1avgpts': D1AveragePoints, 'd2avgpts': D2AveragePoints,
                            'd1avgptsnc': D1AverageWithNCPoints, 'd2avgptsnc': D2AverageWithNCPoints,
                            'd1avgfin': D1AverageFinishs, 'd2avgfin': D2AverageFinishs,
                            'd1best': D1BestFinish, 'd2best': D2BestFinish,
                            'd1wins': D1RaceWins, 'd2wins': D2RaceWins,
                            'd1pod': D1RacePodiums, 'd2pod': D2RacePodiums,
                            'd1team': D1TeamContribution, 'd2team': D2TeamContribution,
                            'd1fast': D1RaceFastestLaps, 'd2fast': D2RaceFastestLaps,
                            'd1dnf': D1RaceDNF, 'd2dnf': D2RaceDNF,
                            'd1avgposgain': D1AveragePositionGain, 'd2avgposgain': D2AveragePositionGain,
                            'd1mostposgain': D1MostPositionsGained, 'd2mostposgain': D2MostPositionsGained,

                            
            
            }


            context = {'Qaulystats':Qualyobject,'Racestats':Raceobject,'myDrivers':DriverObjetList}

            return render(request,'Head2Head/DriverCompare.html',context)


    DriverObjetList = DriverClass.objects.all().order_by('Name')
    context = {'myDrivers':DriverObjetList}

    return render(request,'Head2Head/DriverCompare.html',context)


def compareteams(request):
    if request.method == 'GET':
        # print('Printing Post: ',request.POST)
        form = Teamform(request.GET)
        if form.is_valid():

            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']
            
            

            GetTeamQaulyStats(team1,team2)
            GetTeamRaceStats(team1,team2)
           

            DriverObjetList = DriverClass.objects.all().order_by('Car')

            # searchd1 = [x for x in DriverObjetList if x.No == tea]
            # searchd2 = [x for x in DriverObjetList if x.No == driv2]

            Driverobject = {'d1best': Driver1Best, 'd2best': Driver2Best,
                            'd1worst': Driver1Worst, 'd2worst': Driver2Worst,
                            'd1avg': Driver1Avg, 'd2avg': Driver2Avg,
                            'd1q3': Driver1Q3, 'd2q3': Driver2Q3,
                            'd1q2': Driver1Q2, 'd2q2': Driver2Q2,
                            't1': team1, 't2': team2,
                            # 'd1img': searchd1[0].img, 'd2img': searchd2[0].img,
                            'd1pole': Driver1Poles, 'd2pole': Driver2Poles,
                             'delta': Delta,
            
            }

            Raceobject = {'d1total': D1TotalPoints, 'd2total': D2TotalPoints,
                            'd1avgpts': D1AveragePoints, 'd2avgpts': D2AveragePoints,
                            'd1avgptsnc': D1AverageWithNCPoints, 'd2avgptsnc': D2AverageWithNCPoints,
                            'd1avgfin': D1AverageFinishs, 'd2avgfin': D2AverageFinishs,
                            'd1best': D1BestFinish, 'd2best': D2BestFinish,
                            'd1wins': D1RaceWins, 'd2wins': D2RaceWins,
                            'd1pod': D1RacePodiums, 'd2pod': D2RacePodiums,
                            'd1fast': D1RaceFastestLaps, 'd2fast': D2RaceFastestLaps,
                            'd1dnf': D1RaceDNF, 'd2dnf': D2RaceDNF,
                            'd1avgposgain': D1AveragePositionGain, 'd2avgposgain': D2AveragePositionGain,
                            'd1mostposgain': D1MostPositionsGained, 'd2mostposgain': D2MostPositionsGained,              
            
            }




            context = {'stats':Driverobject,'Racestats':Raceobject,'myTeams':GetTeams(DriverObjetList)}

            return render(request,'Head2Head/TeamCompare.html',context)



    #################################################
    DriverObjetList = DriverClass.objects.all().order_by('Car')
    context = {'myTeams':GetTeams(DriverObjetList)}

    return render(request,'Head2Head/TeamCompare.html',context)


def Load(request):
    return render(request,'Head2Head/loadData.html')

def LoadAllNewData(request):
    LoadDrivers()
    LoadQauly()
    GetStartingGrid()
    GetFastLaps()
    GetRaceResult()
    GetSprintRaces()
    messages.success(request, "Successfuly Loaded New Data" )
    return HttpResponseRedirect('Load')
#/////////////////////////////////////////////  Get statistsics  ///////////////////////////////////////////////////////////////////


def GetQaulyDriverStats(Driver1,Driver2):
    QaulyList = QaulyClass.objects.all()

    # Driver1 = 'Pierre Gasly'
    # Driver2 = 'Lando Norris'

    # Get all the qualy sessions the drivers have participated in
    Driver1Sessions = [x for x in QaulyList if x.No == Driver1]
    Driver2Sessions = [x for x in QaulyList if x.No == Driver2]


    #Used for tracking if driver has skipped a race
    #Get a list of all the GP's
    GPList = []
    for t in QaulyList:
        if t.GP in GPList:
            x= 2
        else:
            GPList.append(t.GP)

    #qualy appearnaces tracking
    D1Q1 = 0
    D1Q2 = 0
    D1Q3 = 0
    D2Q1 = 0
    D2Q2 = 0
    D2Q3 = 0

    #List of all qualyfying positions
    Driver1PosList = []
    Driver2PosList = []

    GapList = []

    D1Skipped = False
    D2Skipped = False

    GPCount = []
    countd1 =  0
    countd2 = 0
    for y in GPList:

        #Get current gp qualy for each driver
        x = next((z for z in Driver1Sessions if z.GP == y),'NotFound')
        p = next((z for z in Driver2Sessions if z.GP == y),'NotFound')
    
        if x == 'NotFound':
            D1Skipped = True
        if p == 'NotFound':
            D2Skipped = True


        Driver1Time = ''
        Driver2Time = ''

        d1qualsession = []
        d2qualsession = []

        if D1Skipped == False:
            if x.Pos == "RT" or x.Pos == "NC":
                d1qualsession = [z for z in QaulyList if z.GP == x.GP]
                countPos = 0
                for s in d1qualsession:
                    if s.No == x.No:
                        countPos +=1
                        Driver1PosList.append(countPos)
                        break
                    else:
                        countPos +=1
            else:
                Driver1PosList.append(int(x.Pos))
        
        if D2Skipped == False:
            if p.Pos == "RT" or p.Pos == "NC":
                d2qualsession = [z for z in QaulyList if z.GP == p.GP]
                countPos = 0
                for s in d2qualsession:
                    if s.No == p.No:
                        countPos +=1
                        Driver2PosList.append(countPos)
                        break
                    else:
                        countPos +=1
            else:
                Driver2PosList.append(int(p.Pos))

        if D1Skipped == False:
            if x.Q3 != '':
                if x.Q3 == 'DNF':
                    Driver1Time = x.Q2

                else:
                    Driver1Time = x.Q3

            elif x.Q2 != '':
                if x.Q3 == 'DNF':
                    Driver1Time = x.Q1

                else:
                    Driver1Time = x.Q2

            else:
                Driver1Time = x.Q1
        if D2Skipped == False:
            if p.Q3 != '':
                if p.Q3 == 'DNF':
                    Driver2Time = p.Q2

                else:
                    Driver2Time = p.Q3

            elif p.Q2 != '':
                if p.Q3 == 'DNF':
                    Driver2Time = p.Q1

                else:
                    Driver2Time = p.Q2

            else:
                Driver2Time = p.Q1

        if D1Skipped == False:
            if int(x.Pos) <= 10:
                D1Q3 += 1
                D1Q2 += 1
            if int(x.Pos) > 10 and int(x.Pos) <= 15:
                D1Q2 += 1
        if D2Skipped == False:
            if int(p.Pos) <= 10:
                D2Q3 += 1
                D2Q2 += 1
            if int(p.Pos) > 10 and int(p.Pos) <= 15:
                D2Q2 += 1
        

        if Driver1Time == 'DNF' or Driver1Time == 'RT' or Driver2Time == 'DNF' or Driver2Time == 'RT' or Driver1Time == '' or Driver2Time == '':
            D1Skipped = False
            D2Skipped = False
        else:
            Gap = GetTimeDiffernace(Driver1Time,Driver2Time)
            GapList.append(Gap)
            D1Skipped = False
            D2Skipped = False
        

    global Driver1Best
    Driver1Best = min(Driver1PosList) 
    global Driver2Best
    Driver2Best = min(Driver2PosList)


    global Driver1Worst
    Driver1Worst = max(Driver1PosList)
    global Driver2Worst
    Driver2Worst = max(Driver2PosList)


    global Driver1Avg
    Driver1Avg = round(sum(Driver1PosList)/len(Driver1PosList),2)
    global Driver2Avg
    Driver2Avg = round(sum(Driver2PosList)/len(Driver2PosList),2)

   

    global Driver1Q3
    Driver1Q3 = D1Q3
    global Driver2Q3
    Driver2Q3 = D2Q3

    
    global Driver1Q2
    Driver1Q2 = D1Q2
    global Driver2Q2
    Driver2Q2 = D2Q2

    global d1
    d1 = Driver1Sessions[0].Driver
    global d2
    d2 = Driver2Sessions[0].Driver

    global Driver1Poles
    Driver1Poles = len([z for z in Driver1PosList if z == 1])
    global Driver2Poles
    Driver2Poles = len([z for z in Driver2PosList if z == 1])


    global Delta
    Delta = round(sum(GapList)/ len(GapList),3)


def GetRaceDriverStats(Driver1,Driver2):
    RaceList = ResultClass.objects.all()

    FastestLaps = FastesLapClass.objects.all()

    StartingGridList = StartingClass.objects.all()

    SprintQualyList =  SprintClass.objects.all()

    D1FastestLapsCounter = 0
    D2FastestLapsCounter = 0

    

    D1DNF = 0
    D2DNF = 0

    # Driver1 = '44'
    # Driver2 = '33'

    D1PositionGainList =[]
    D2PositionGainList =[]

    # Get all the qualy sessions the drivers have participated in
    Driver1Sessions = [x for x in RaceList if x.No == Driver1]
    Driver2Sessions = [x for x in RaceList if x.No == Driver2]

    Driver1Sprint = [x for x in SprintQualyList if x.No == Driver1]
    Driver2Sprint = [x for x in SprintQualyList if x.No == Driver2]

    Driver1 = Driver1Sessions[0].Driver
    Driver2 = Driver2Sessions[0].Driver

    #Used for tracking if driver has skipped a race
    #Get a list of all the GP's
    GPList = []
    for t in RaceList:
        if t.GP in GPList:
            x= 2
        else:
            GPList.append(t.GP)

    Driver1PosList = []
    Driver2PosList = []

    D1Skipped = False
    D2Skipped = False

    Driver1PointList = []
    Driver1PointListWithNC = []
    Driver2PointList = []
    Driver2PointListWithNC = []

    for y in GPList:

        #Get current sessions for both drivers
        x = next((z for z in Driver1Sessions if z.GP == y),'NotFound')
        p = next((z for z in Driver2Sessions if z.GP == y),'NotFound')

        #Add drivers position gain/loss to list dnf on included
        if x.Time == 'DNF' or x.Time == 'DNS':
            h = 'I have to use this cause python is drunk and cant pick up !='
        else:
            StartPos = next((z.Pos for z in StartingGridList if z.No == x.No and z.GP == y),'NotFound')
            PositionsMade = int(StartPos)  - int(x.Pos)
            D1PositionGainList.append(PositionsMade)
        if p.Time == 'DNF' or p.Time == 'DNS':
            h = 'I have to use this cause python i drunk and cant pick up !='
        else:
            StartPos = next((z.Pos for z in StartingGridList if z.No == p.No and z.GP == y),'NotFound')
            PositionsMade = int(StartPos) - int(p.Pos)
            D2PositionGainList.append(PositionsMade)

        #Total DNFS
        if x.Time == 'DNF':
            D1DNF +=1
        if p.Time == 'DNF':
            D2DNF +=1

        if x == []:
            T1Skipped = True
        if p == []:
            T2Skipped = True


        # Get drivers Postions thyve finiished in and the points they ended with
        # CHeck if driver has been classifed and depending on that add to one list or another
        if D1Skipped == False:
            if x.Pos == "RT" or x.Pos == "NC":
                d1qualsession = [z for z in RaceList if z.GP == x.GP]
                countPos = 0
                for s in d1qualsession:
                    if s.No == x.No:
                        countPos +=1
                        Driver1PosList.append(countPos)
                        Driver1PointListWithNC.append(int(x.Pts))
                        break
                    else:
                        countPos +=1

            else:
                Driver1PosList.append(int(x.Pos))
                Driver1PointList.append(int(x.Pts))
                Driver1PointListWithNC.append(int(x.Pts))

        if D2Skipped == False:
            if p.Pos == "RT" or p.Pos == "NC":
                d2qualsession = [z for z in RaceList if z.GP == p.GP]
                countPos = 0
                for s in d2qualsession:
                    if s.No == p.No:
                        countPos +=1
                        Driver2PosList.append(countPos)
                        Driver2PointListWithNC.append(int(p.Pts))
                        break
                    else:
                        countPos +=1
            
            else:
                Driver2PosList.append(int(p.Pos))
                Driver2PointList.append(int(p.Pts))
                Driver2PointListWithNC.append(int(p.Pts))



        # Get fastes laps of that race from drivers
        D1FastestLaps = next((z for z in FastestLaps if z.No == x.No and z.GP == y),'NotFound')
        D2FastestLaps = next((z for z in FastestLaps if z.No == p.No and z.GP == y),'NotFound')

         # Determine who was faster based on psotion
        if D1FastestLaps != 'NotFound' and D2FastestLaps != 'NotFound':
            if int(D1FastestLaps.Pos) < int(D2FastestLaps.Pos):
                D1FastestLapsCounter += 1
            elif int(D1FastestLaps.Pos) > int(D2FastestLaps.Pos):
               D2FastestLapsCounter += 1
            
    D1Wins = len([z for z in Driver1PosList if z == 1])
    D2Wins = len([z for z in Driver2PosList if z == 1])

    D1Podiums = len([z for z in Driver1PosList if z <= 3])
    D2Podiums = len([z for z in Driver2PosList if z <= 3])


    Driver1SprintPoints = 0
    Driver2SprintPoints = 0

    for w in Driver1Sprint:
        currentpts = int(w.Pts)
        if currentpts > 0:
            Driver1SprintPoints += currentpts

    for w in Driver2Sprint:
        currentpts = int(w.Pts)
        if currentpts > 0:
            Driver2SprintPoints += currentpts

    D1Total = sum(Driver1PointList) + Driver1SprintPoints
    D2Total = sum(Driver2PointList) + Driver2SprintPoints

       # Get last team driver raced for
    D1LastTeam = Driver1Sessions[len(Driver1Sessions)-1].Car
    D2LastTeam = Driver2Sessions[len(Driver2Sessions)-1].Car


    # Get list of points scored for that team  #contingency for if any team pulls a redbull
    D1PointsWithTeam =  [int(z.Pts) for z in Driver1Sessions if z.Car == D1LastTeam]
    D2PointsWithTeam =  [int(z.Pts) for z in Driver2Sessions if z.Car == D2LastTeam]

    D1PointsWithTeamSprint =  [int(z.Pts) for z in Driver1Sprint if z.Car == D1LastTeam]
    D2PointsWithTeamSprint  =  [int(z.Pts) for z in Driver2Sprint if z.Car == D2LastTeam]

    FinalDriver1ListPoint = D1PointsWithTeam + D1PointsWithTeamSprint
    FinalDriver2ListPoint = D2PointsWithTeam + D2PointsWithTeamSprint


    # Get total points for the 2 teams in the standings
    Pointob = GetTeamPoints(D1LastTeam,D2LastTeam)


    global D1TotalPoints
    D1TotalPoints = D1Total

    global D1AveragePoints
    D1AveragePoints = round(sum(Driver1PointList)/len(Driver1PointList),2)

    global D1AverageWithNCPoints
    D1AverageWithNCPoints = round(sum(Driver1PointListWithNC)/len(Driver1PointListWithNC),2)

    global D1AverageFinishs
    D1AverageFinishs = round(sum(Driver1PosList)/len(Driver1PosList),2)

    global D1BestFinish
    D1BestFinish = min(Driver1PosList)

    global D1RaceWins
    D1RaceWins = D1Wins

    global D1RacePodiums
    D1RacePodiums = D1Podiums

    global D1TeamContribution
    D1TeamContribution = round((sum(D1PointsWithTeam)/Pointob["T1Points"]) * 100,2)

    global D1RaceFastestLaps
    D1FastestLaps = D1FastestLapsCounter

    global D1RaceDNF
    D1RaceDNF = D1DNF

    global D1AveragePositionGain
    D1AveragePositionGain = round(sum(D1PositionGainList)/len(D1PositionGainList),2)

    global D1MostPositionsGained
    D1MostPositionsGained = max(D1PositionGainList)

    #//////////////////////////////////////////////////////// driver 2
    global D2TotalPoints
    D2TotalPoints = D2Total

    global D2AveragePoints
    D2AveragePoints = round(sum(Driver2PointList)/len(Driver2PointList),2)

    global D2AverageWithNCPoints
    D2AverageWithNCPoints = round(sum(Driver2PointListWithNC)/len(Driver2PointListWithNC),2)

    global D2AverageFinishs
    D2AverageFinishs = round(sum(Driver2PosList)/len(Driver2PosList),2)

    global D2BestFinish
    D2BestFinish = min(Driver2PosList)

    global D2RaceWins
    D2RaceWins = D2Wins

    global D2RacePodiums
    D2RacePodiums = D2Podiums

    global D2TeamContribution
    D2TeamContribution = round((sum(D2PointsWithTeam)/Pointob["T2Points"]) * 100,2)

    global D2RaceFastestLaps
    D2FastestLaps = D2FastestLapsCounter

    global D2RaceDNF
    D2RaceDNF = D2DNF

    global D2AveragePositionGain
    D2AveragePositionGain = round(sum(D2PositionGainList)/len(D2PositionGainList),2)

    global D2MostPositionsGained
    D2MostPositionsGained = max(D2PositionGainList)


def GetTeamQaulyStats(Team1,Team2):
    QaulyList = QaulyClass.objects.all()



    # Get all the qualy sessions the drivers have participated in
    Team1Sessions = [x for x in QaulyList if x.Car == Team1]
    Team2Sessions = [x for x in QaulyList if x.Car == Team2]


    #Used for tracking if driver has skipped a race
    #Get a list of all the GP's
    GPList = []
    for t in QaulyList:
        if t.GP in GPList:
            dd= 'test'
        else:
            GPList.append(t.GP)

    #qualy appearnaces tracking
    T1Q1 = 0
    T1Q2 = 0
    T1Q3 = 0
    T2Q1 = 0
    T2Q2 = 0
    T2Q3 = 0

    #List of all qualyfying positions
    Team1PosList = []
    Team2PosList = []

    GapList = []

    T1Skipped = False
    T2Skipped = False

    GPCount = []
    countd1 =  0
    countd2 = 0
    for y in GPList:

        #Get current gp qualy for each driver
        x = [z for z in Team1Sessions if z.GP == y]
        p = [z for z in Team2Sessions if z.GP == y]
    
        if x == []:
            T1Skipped = True
        if p == []:
            T2Skipped = True


        Team1Driver1Time = ''
        Team1Driver2Time = ''
        Team2Driver1Time = ''
        Team2Driver2Time = ''

        Team1TimeList = []
        Team2TimeList = []
        
        d1qualsession = []
        d2qualsession = []


        #List of postions teams have finished in
        countDriverPos = 0
        if T1Skipped == False:
            for d1 in x:
                if d1.Pos == "RT" or d1.Pos == "NC":
                    d1qualsession = [z for z in QaulyList if z.GP == d1.GP]
                    countPos = 0
                    for s in d1qualsession:
                        if s.No == d1.No:
                            countPos +=1
                            x[countDriverPos].Pos = countPos
                            Team1PosList.append(countPos)
                            break
                        else:
                            countPos +=1
                else:
                    Team1PosList.append(int(d1.Pos))
                countDriverPos += 1
        
        countDriverPos = 0
        if T2Skipped == False:
            for d2 in p:
                if d2.Pos == "RT" or d2.Pos == "NC":
                    d2qualsession = [z for z in QaulyList if z.GP == d2.GP]
                    countPos = 0
                    for s in d2qualsession:
                        if s.No == d2.No:
                            countPos +=1
                            p[countDriverPos].Pos = countPos
                            Team2PosList.append(countPos)
                            break
                        else:
                            countPos +=1
                else:
                    Team2PosList.append(int(d2.Pos))
                countDriverPos += 1


        #Get session qually time
        if T1Skipped == False:
            for w in x :
                if w.Q3 != '':
                    if w.Q3 == 'DNF':
                        DriverTime = w.Q2
                        Team1TimeList.append(DriverTime)
                    else:
                        DriverTime = w.Q3
                        Team1TimeList.append(DriverTime)
                elif w.Q2 != '':
                    if w.Q3 == 'DNF':
                        DriverTime = w.Q1
                        Team1TimeList.append(DriverTime)
                    else:
                        DriverTime = w.Q2
                        Team1TimeList.append(DriverTime)
                else:
                    DriverTime = w.Q1
                    Team1TimeList.append(DriverTime)

        if T2Skipped == False:
            for w in p :
                if w.Q3 != '':
                    if w.Q3 == 'DNF':
                        DriverTime = w.Q2
                        Team2TimeList.append(DriverTime)
                    else:
                        DriverTime = w.Q3
                        Team2TimeList.append(DriverTime)
                elif w.Q2 != '':
                    if w.Q3 == 'DNF':
                        DriverTime = w.Q1
                        Team2TimeList.append(DriverTime)
                    else:
                        DriverTime = w.Q2
                        Team2TimeList.append(DriverTime)
                else:
                    DriverTime = w.Q1
                    Team2TimeList.append(DriverTime)

        #get no. of q2 and q2 appreances

        if T1Skipped == False:
            for w in x :
                if int(w.Pos) <= 10:
                    T1Q3 += 1
                    T1Q2 += 1
                elif int(w.Pos) > 10 and int(w.Pos) <= 15:
                    T1Q2 += 1

        if T2Skipped == False:
            for w in p :
                if int(w.Pos) <= 10:
                    T2Q3 += 1
                    T2Q2 += 1
                elif int(w.Pos) > 10 and int(w.Pos) <= 15:
                    T2Q2 += 1


        T1Applicable = True
        T2Applicable = True
        for z in Team1TimeList:
            if z == 'DNF' or z == 'RT' or z == '':
                T1Applicable = False
            else:
                T1Applicable = True

        for z in Team2TimeList:
            if z == 'DNF' or z == 'RT' or z == '':
                T2Applicable = False
            else:
                T2Applicable = True

        if T1Applicable == False or T2Applicable == False:
            T1Skipped = False
            T2Skipped = False
        else:
            Gap = GetTeamTimeDiffernace(Team1TimeList,Team2TimeList)
            GapList.append(Gap)
            T1Skipped = False
            T2Skipped = False

    global Driver1Best
    Driver1Best = min(Team1PosList) 
    global Driver2Best
    Driver2Best = min(Team2PosList)


    global Driver1Worst
    Driver1Worst = max(Team1PosList)
    global Driver2Worst
    Driver2Worst = max(Team2PosList)


    global Driver1Avg
    Driver1Avg = round(sum(Team1PosList)/len(Team1PosList),2)
    global Driver2Avg
    Driver2Avg = round(sum(Team2PosList)/len(Team2PosList),2)

   

    global Driver1Q3
    Driver1Q3 = T1Q3
    global Driver2Q3
    Driver2Q3 = T2Q3

    
    global Driver1Q2
    Driver1Q2 = T1Q2
    global Driver2Q2
    Driver2Q2 = T2Q2

    # global d1
    # d1 = Driver1Sessions[0].Driver
    # global d2
    # d2 = Driver2Sessions[0].Driver

    global Driver1Poles
    Driver1Poles = len([z for z in Team1PosList if z == 1])
    global Driver2Poles
    Driver2Poles = len([z for z in Team2PosList if z == 1])


    global Delta
    Delta = round(sum(GapList)/ len(GapList),3)

def GetTeamRaceStats(Team1,Team2):

    RaceList = ResultClass.objects.all()

    FastestLaps = FastesLapClass.objects.all()

    StartingGridList = StartingClass.objects.all()

    SprintQualyList =  SprintClass.objects.all()

    T1FastestLapsCounter = 0
    T2FastestLapsCounter = 0

    T1DNF = 0
    T2DNF = 0


    T1PositionGainList =[]
    T2PositionGainList =[]

    # Get all the race sessions the drivers have participated in
    Team1Sprint = [x for x in SprintQualyList if x.Car == Team1]
    Team2Sprint = [x for x in SprintQualyList if x.Car == Team2]

    Team1Sessions = [x for x in RaceList if x.Car == Team1]
    Team2Sessions = [x for x in RaceList if x.Car == Team2]    

   

    

    #Used for tracking if driver has skipped a race
    #Get a list of all the GP's
    GPList = []
    for t in RaceList:
        if t.GP in GPList:
            x= 2
        else:
            GPList.append(t.GP)

    Team1PosList = []
    Team2PosList = []

    T1Skipped = False
    T2Skipped = False

    Team1PointList = []
    Team1PointListWithNC = []
    Team2PointList = []
    Team2PointListWithNC = []

    for y in GPList:

        #Get current sessions for both drivers
        x = [z for z in Team1Sessions if z.GP == y]
        p = [z for z in Team2Sessions if z.GP == y]

        #Add drivers position gain/loss to list dnf on included
        for d1 in x:
            if d1.Time == 'DNF' or d1.Time == 'DNS':
                h = 'I have to use this cause python is drunk and cant pick up !='
            else:
                StartPos = next((z.Pos for z in StartingGridList if z.No == d1.No and z.GP == y),'NotFound')
                PositionsMade = int(StartPos)  - int(d1.Pos)
                T1PositionGainList.append(PositionsMade)
        for d2 in p:
            if d2.Time == 'DNF' or d2.Time == 'DNS':
                h = 'I have to use this cause python i drunk and cant pick up !='
            else:
                StartPos = next((z.Pos for z in StartingGridList if z.No == d2.No and z.GP == y),'NotFound')
                PositionsMade = int(StartPos) - int(d2.Pos)
                T2PositionGainList.append(PositionsMade)

        #Total DNFS
        for d1 in x:
            if d1.Time == 'DNF':
                T1DNF +=1
        for d2 in x:
            if d2.Time == 'DNF':
                T2DNF +=1

        if x == []:
            T1Skipped = True
        if p == []:
            T2Skipped = True


        # Get drivers Postions thyve finiished in and the points they ended with
        # CHeck if driver has been classifed and depending on that add to one list or another
        if T1Skipped == False:
            for d1 in x:
                if d1.Pos == "RT" or d1.Pos == "NC":
                    t1qualsession = [z for z in RaceList if z.GP == d1.GP]
                    countPos = 0
                    for s in t1qualsession:
                        if s.No == d1.No:
                            countPos +=1
                            Team1PosList.append(countPos)
                            Team1PointListWithNC.append(int(d1.Pts))
                            break
                        else:
                            countPos +=1

                else:
                    Team1PosList.append(int(d1.Pos))
                    Team1PointList.append(int(d1.Pts))
                    Team1PointListWithNC.append(int(d1.Pts))

        if T2Skipped == False:
            for d2 in p:
                if d2.Pos == "RT" or d2.Pos == "NC":
                    t2qualsession = [z for z in RaceList if z.GP == d2.GP]
                    countPos = 0
                    for s in t2qualsession:
                        if s.No == d2.No:
                            countPos +=1
                            Team2PosList.append(countPos)
                            Team2PointListWithNC.append(int(d2.Pts))
                            break
                        else:
                            countPos +=1
                
                else:
                    Team2PosList.append(int(d2.Pos))
                    Team2PointList.append(int(d2.Pts))
                    Team2PointListWithNC.append(int(d2.Pts))



        # Get fastes laps of that race from drivers
        T1FastestLaps = [z for z in FastestLaps if z.Car == Team1 and z.GP == y]
        T2FastestLaps = [z for z in FastestLaps if z.Car == Team2 and z.GP == y]

        CombinedFastestlap = T1FastestLaps + T2FastestLaps
         # Determine who was faster based on psotion

        if CombinedFastestlap != []:
            bestlapPos = [s.Pos for s in CombinedFastestlap]
            bestlapPosConvert = []

            for z in bestlapPos:
               bestlapPosConvert.append(int(z))
            
            bestpos = min(bestlapPosConvert)

            bestlapobject = next(z for z in CombinedFastestlap if z.Pos == str(bestpos))
            
            if bestlapobject.Car == Team1:
                T1FastestLapsCounter += 1
            if bestlapobject.Car == Team2:
                T2FastestLapsCounter += 1
            
    T1Wins = len([z for z in Team1PosList if z == 1])
    T2Wins = len([z for z in Team2PosList if z == 1])

    T1Podiums = len([z for z in Team1PosList if z <= 3])
    T2Podiums = len([z for z in Team2PosList if z <= 3])


    Team1SprintPoints = 0
    Team2SprintPoints = 0

    for w in Team1Sprint:
        currentpts = int(w.Pts)
        if currentpts > 0:
            Team1SprintPoints += currentpts

    for w in Team2Sprint:
        currentpts = int(w.Pts)
        if currentpts > 0:
            Team2SprintPoints += currentpts

    T1Total = sum(Team1PointList) + Team1SprintPoints
    T2Total = sum(Team2PointList) + Team2SprintPoints

    global D1TotalPoints
    D1TotalPoints = T1Total
    global D1AveragePoints
    D1AveragePoints = round(sum(Team1PointList)/len(Team1PointList),2)

    global D1AverageWithNCPoints
    D1AverageWithNCPoints = round(sum(Team1PointListWithNC)/len(Team1PointListWithNC),2)

    global D1AverageFinishs
    D1AverageFinishs = round(sum(Team1PosList)/len(Team1PosList),2)

    global D1BestFinish
    D1BestFinish = min(Team1PosList)

    global D1RaceWins
    D1RaceWins = T1Wins

    global D1RacePodiums
    D1RacePodiums = T1Podiums

 
    global D1RaceFastestLaps
    D1FastestLaps = T1FastestLapsCounter

    global D1RaceDNF
    D1RaceDNF = T1DNF

    global D1AveragePositionGain
    D1AveragePositionGain = round(sum(T1PositionGainList)/len(T1PositionGainList),2)

    global D1MostPositionsGained
    D1MostPositionsGained = max(T1PositionGainList)

    #//////////////////////////////////////////////////////// driver 2
    global D2TotalPoints
    D2TotalPoints = T2Total

    global D2AveragePoints
    D2AveragePoints = round(sum(Team2PointList)/len(Team2PointList),2)

    global D2AverageWithNCPoints
    D2AverageWithNCPoints = round(sum(Team2PointListWithNC)/len(Team2PointListWithNC),2)

    global D2AverageFinishs
    D2AverageFinishs = round(sum(Team2PosList)/len(Team2PosList),2)

    global D2BestFinish
    D2BestFinish = min(Team2PosList)

    global D2RaceWins
    D2RaceWins = T2Wins

    global D2RacePodiums
    D2RacePodiums = T2Podiums


    global D2RaceFastestLaps
    D2FastestLaps = T2FastestLapsCounter

    global D2RaceDNF
    D2RaceDNF = T2DNF

    global D2AveragePositionGain
    D2AveragePositionGain = round(sum(T2PositionGainList)/len(T2PositionGainList),2)

    global D2MostPositionsGained
    D2MostPositionsGained = max(T2PositionGainList)


# ///////////////////////////////////////////////// Qauly Methods and data  //////////////////////////////////////////////////////////////////
def LoadQauly():
    directory = "C:\_Andile\Road To Software Development\Projects\F1 statistics\Data"

    list_subfolders_with_names = sorted([x for x in os.scandir(directory) if x.is_dir()], key=os.path.getmtime)

    QaulyList = QaulyClass.objects.all()

    LastPos =  0

    for x in list_subfolders_with_names:
        index = x.name.index("_")
        Foldername = x.name[index+1:]
        with open(directory +'/' + x.name + '/'+ Foldername + '_Qaulifying_2021.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] != 'Pos':
                    LastPos = int(LastPos) + 1
                    QualySession = QaulyClass()
                    if row[0] == 'NC' or  row[0] == 'RT':
                        QualySession.Pos = LastPos
                    else:
                        QualySession.Pos = row[0]

                    QualySession.No = row[1]
                    QualySession.Driver = row[2][:-4]
                    QualySession.Car = row[3]
                    QualySession.Q1 = row[4]
                    QualySession.Q2 = row[5]
                    QualySession.Q3 = row[6]
                    QualySession.Laps = row[7]
                    QualySession.GP = row[8]
                    LastPos = QualySession.Pos

                    foundobject = next((z for z in QaulyList if z.No == QualySession.No and z.GP == QualySession.GP),'NotFound')
                    if foundobject == 'NotFound' :
                        QualySession.save()


def LoadDrivers():

    driverList = DriverClass.objects.all()
    path = 'C:\_Andile\Road To Software Development\Projects\F1 statistics\Data\DriverList2021.csv'
    with open(path) as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            if row[0] != 'Name':
                myDrivers = DriverClass()
                myDrivers.Name = row[0]
                myDrivers.Surname = row[1] 
                myDrivers.Abbr = row[2] 
                myDrivers.No = row[3] 
                myDrivers.Car = row[4]
                myDrivers.img = 'Head2Head/Drivers/' + row[3] + '.png'
                foundobject = next((z for z in driverList if z.No == myDrivers.No),'NotFound')
                if foundobject == 'NotFound' :
                    myDrivers.save()



def GetTimeDiffernace(T1,T2):

    print(T1 + '////' + T2)
    minute = T1[:T1.index(':')]
    second = T1[T1.index(':') + 1 :T1.index('.') ]
    milliseconds = T1[-3:]

    T1Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)

    minute = T2[:T2.index(':')]
    second = T2[T2.index(':') + 1 :T2.index('.') ]
    milliseconds = T2[-3:]

    T2Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)

    Final = (T1Compiled - T2Compiled) / 1000

    return Final


def GetTeams(DriverList):
    TeamList = []
    for t in DriverList:
        if t.Car in TeamList:
            dd= 'test'
        else:
            TeamList.append(t.Car)
    return TeamList



def GetTeamTimeDiffernace(T1,T2):
    T1Combined = 0
    for x in T1:
        minute = x[:x.index(':')]
        second = x[x.index(':') + 1 :x.index('.') ]
        milliseconds = x[x.index('.') +1:]

        Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)
        T1Combined = T1Combined + Compiled


    T2Combined = 0
    for x in T2:
        minute = x[:x.index(':')]
        second = x[x.index(':') + 1 :x.index('.') ]
        milliseconds = x[x.index('.') +1:]

        Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)
        T2Combined = T2Combined + Compiled

    Final = (T1Combined - T2Combined) / 1000

    return Final



#////////////////////////////////////// Race Methods and data //////////////////////////////////////////////////////////  

def GetTeamPoints(Team1,Team2):
    URL = 'https://www.formula1.com/en/results.html/2021/team.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    T1Points = 0
    T2Points = 0
    for currentrow in rows:
        columns =currentrow.find_all("td")
        CurrentTeam = columns[2].text.replace('\n', ' ').strip()
        if CurrentTeam == Team1:
                T1Points = int(columns[3].text.replace('\n', ' ').strip())

        if CurrentTeam == Team2:
                T2Points = int(columns[3].text.replace('\n', ' ').strip())

    PointsObjects = {} # empty dict instance

    PointsObjects["T1Points"] = T1Points
    PointsObjects["T2Points"] = T2Points

    return PointsObjects

def GetRaceResult():
    directory = "C:\_Andile\Road To Software Development\Projects\F1 statistics\Data"

    # list_subfolders_with_names = [f.name for f in os.scandir(directory) if f.is_dir()]
    
    list_subfolders_with_names = sorted([x for x in os.scandir(directory) if x.is_dir()], key=os.path.getmtime)

    RacetList = ResultClass.objects.all()

    RaceList = []
    for x in list_subfolders_with_names:
        index = x.name.index("_")
        Foldername = str(x.name[index+1:])
        with open(directory +'/' + x.name + '/'+ Foldername + '_RaceResults_2021.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] != 'Pos':
                    RaceSession = ResultClass()
                    RaceSession.Pos = row[0]
                    RaceSession.No = row[1]
                    RaceSession.Driver = row[2][:-4]
                    RaceSession.Car = row[3]
                    RaceSession.Laps = row[4]
                    RaceSession.Time = row[5]
                    RaceSession.Pts = row[6]
                    RaceSession.GP = row[7]
                    foundobject = next((z for z in RacetList if z.No == RaceSession.No and z.GP == RaceSession.GP),'NotFound')
                    if foundobject == 'NotFound' :
                        RaceSession.save()
                    # RaceList.append(RaceSession)
    return RaceList


def GetFastLaps():
    directory = "C:\_Andile\Road To Software Development\Projects\F1 statistics\Data"

    list_subfolders_with_names = sorted([x for x in os.scandir(directory) if x.is_dir()], key=os.path.getmtime)

    fastestList = FastesLapClass.objects.all()

    RaceList = []
    for x in list_subfolders_with_names:
        index = x.name.index("_")
        Foldername = x.name[index+1:]
        with open(directory +'/' + x.name + '/'+ Foldername + '_FastestLap_2021.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0].isnumeric() == True:
                    FastestLapObject = FastesLapClass()
                    FastestLapObject.Pos = row[0]
                    FastestLapObject.No = row[1]
                    FastestLapObject.Driver = row[2][:-4]
                    FastestLapObject.Car = row[3]
                    FastestLapObject.Lap = row[4]
                    FastestLapObject.TOD = row[5]
                    FastestLapObject.Time = row[6]
                    FastestLapObject.AVGSpeed = row[7]
                    FastestLapObject.GP = row[8]
                    foundobject = next((z for z in fastestList if z.No == FastestLapObject.No and z.GP == FastestLapObject.GP),'NotFound')
                    if foundobject == 'NotFound' :
                        FastestLapObject.save()
    return RaceList


def GetStartingGrid():
    directory = "C:\_Andile\Road To Software Development\Projects\F1 statistics\Data"

    list_subfolders_with_names = sorted([x for x in os.scandir(directory) if x.is_dir()], key=os.path.getmtime)

    StartingList = StartingClass.objects.all()

    RaceList = []
    for x in list_subfolders_with_names:
        index = x.name.index("_")
        Foldername = x.name[index+1:]
        with open(directory +'/' + x.name + '/'+ Foldername + '_StartingGrid_2021.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0].isnumeric() == True:
                    StartingGridObject = StartingClass()
                    StartingGridObject.Pos = row[0]
                    StartingGridObject.No = row[1]
                    StartingGridObject.Driver = row[2][:-4]
                    StartingGridObject.Car = row[3]
                    StartingGridObject.Time = row[4]
                    StartingGridObject.GP = row[5]
                    foundobject = next((z for z in StartingList if z.No == StartingGridObject.No and z.GP == StartingGridObject.GP),'NotFound')
                    if foundobject == 'NotFound' :
                        StartingGridObject.save()
                    #RaceList.append(StartingGridObject)
    return RaceList


#check if sprint weekend or not
def Issprintweekend(name):
    directory = 'C:\_Andile\Road To Software Development\Projects\F1 statistics\Data/' + name

    ListofFiles = os.listdir(directory)

    index = name.index("_")
    newname = name[index+1:]
    count = len(newname)
    test = ListofFiles[0][count:]
    found = [x for x in ListofFiles if '_SprintQaulifying_2021.csv' == x[count:]]

    if len(found) == 0:
        return False
    else:
        return True


def GetSprintRaces():

    sprintList = SprintClass.objects.all()

    
    directory = "C:\_Andile\Road To Software Development\Projects\F1 statistics\Data"

    list_subfolders_with_names = sorted([x for x in os.scandir(directory) if x.is_dir()], key=os.path.getmtime)

    RaceList = []
    for x in list_subfolders_with_names:
        if Issprintweekend(x.name) == True:
            index = x.name.index("_")
            Foldername = x.name[index+1:]
            with open(directory +'/' + x.name + '/'+ Foldername + '_SprintQaulifying_2021.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[0] != 'Pos':
                        RaceSession = SprintClass()
                        RaceSession.Pos = row[0]
                        RaceSession.No = row[1]
                        RaceSession.Driver = row[2][:-4]
                        RaceSession.Car = row[3]
                        RaceSession.Laps = row[4]
                        RaceSession.Time = row[5]
                        RaceSession.Pts = row[6]
                        RaceSession.GP = row[7]

                        foundobject = next((z for z in sprintList if z.No == RaceSession.No and z.GP == RaceSession.GP),'NotFound')
                        if foundobject == 'NotFound' :
                            RaceSession.save()

                       
    return RaceList

def Test(request):
    return render(request,'Head2Head/loadData.html')
