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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
from django.templatetags.static import static
from django.http import JsonResponse
import json
from django.conf import settings
from json import dumps
# Create your views here.

#Qauly variables
d1 = ''
d2 = ''
d1No = ''
d2No = ''
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
D1QaulyRecord = 0
D2QaulyRecord = 0

#Race variables

D1TotalPoints = 0
D1AveragePoints = 0
D1AverageWithNCPoints = 0
D1AverageFinishs = 0
D1AverageFinishsWithNC = 0
D1BestFinish = 0
D1RaceWins = 0
D1RacePodiums = 0
D1TeamContribution = 0
D1RaceFastestLaps = 0
D1RaceDNF = 0
D1AveragePositionGain = 0
D1MostPositionsGained = 0
D1RaceRecord = 0

D2TotalPoints = 0
D2AveragePoints = 0
D2AverageWithNCPoints = 0
D2AverageFinishs = 0
D2AverageFinishsWithNC = 0
D2BestFinish = 0
D2RaceWins = 0
D2RacePodiums = 0
D2TeamContribution = 0
D2RaceFastestLaps = 0
D2RaceDNF = 0
D2AveragePositionGain = 0
D2MostPositionsGained = 0
D2RaceRecord = 0


#/////////////////////////////////////////////  Admin Tasks  ///////////////////////////////////////////////////////////////////

#Admin Page
def Load(request):
  

    if request.user.is_authenticated:
        #Get List of objects in database
        ListOFprac = PracticeClass.objects.all()
        ListOFqualy = QaulyClass.objects.all()
        ListOFspr = SprintClass.objects.all()
        ListOFstart = StartingClass.objects.all()
        ListOFpit = PitstopClass.objects.all()
        ListOFfast = FastesLapClass.objects.all()
        ListOFres= ResultClass.objects.all()

    #Get list of table names
        ListOFSessions = []
        ListOFSessions.append(PracticeClass.objects.model._meta.db_table)
        ListOFSessions.append(QaulyClass.objects.model._meta.db_table)
        ListOFSessions.append(SprintClass.objects.model._meta.db_table)
        ListOFSessions.append(StartingClass.objects.model._meta.db_table)
        ListOFSessions.append(PitstopClass.objects.model._meta.db_table)
        ListOFSessions.append(FastesLapClass.objects.model._meta.db_table)
        ListOFSessions.append(ResultClass.objects.model._meta.db_table)
        ListOFSessions.append("ALL")

        ListofGrandPrix = GetListOfGrandPrix()
        ListofGrandPrix.append("ALL")

        #Get number of objects i tables
        countobject = {
            'qualycount' : len(ListOFqualy), 'praccount' : len(ListOFprac), 'sprcount' : len(ListOFspr),
            'startcount' : len(ListOFstart), 'pitcount' : len(ListOFpit),'fastcount' : len(ListOFfast),
            'rescount' : len(ListOFres)

        }

        value = request.GET.get('value','')
        context = {'data':value, "gplist" : ListofGrandPrix, "sesslist":ListOFSessions,'prac':ListOFprac, "qualy" : ListOFqualy, "sprint":ListOFspr,
        "start":ListOFstart,'pit':ListOFpit, "fast" : ListOFfast, "res":ListOFres, 'countobject' : countobject,
        
        }
        return render(request,'Head2Head/LoadData.html',context)
    else:
        return HttpResponseRedirect('drivers')

def LoadAllNewData(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            Password = form.cleaned_data['pw']
            if Password == os.environ.get('DjangoPw'):
                # LoadDrivers()
                LoadRaceWeekendData()
                return HttpResponseRedirect('load')
            else:
                dataJSON = False
                context = {'data':dataJSON}
                url = 'load?value=False'
                return HttpResponseRedirect(url)

def DeleteSpecifiedData(request):
    if request.method == 'POST':
        form = DeleteSpecificForm(request.POST)
        if form.is_valid():
            Password = form.cleaned_data['pw']
            Session = form.cleaned_data['sess']
            Grandprix = form.cleaned_data['gp']
            if Password == os.environ.get('DjangoPw') or os.environ.get('DjangoPw') == None:
                # LoadDrivers()
                DelSpeciFiedMethod(Grandprix,Session)
                return HttpResponseRedirect('load')
            else:
                dataJSON = False
                context = {'data':dataJSON}
                url = 'load?value=False'
                return HttpResponseRedirect(url)

def DelSpeciFiedMethod(GrandPrix,Session):
    if Session == 'ALL' and GrandPrix == 'ALL':
        PracticeClass.objects.all().delete()
        QaulyClass.objects.all().delete()
        SprintClass.objects.all().delete()
        StartingClass.objects.all().delete()
        PitstopClass.objects.all().delete()
        FastesLapClass.objects.all().delete()
        ResultClass.objects.all().delete()
    elif Session == 'ALL':
        PracticeClass.objects.filter(GP = GrandPrix).delete()
        QaulyClass.objects.filter(GP = GrandPrix).delete()
        SprintClass.objects.filter(GP = GrandPrix).delete()
        StartingClass.objects.filter(GP = GrandPrix).delete()
        PitstopClass.objects.filter(GP = GrandPrix).delete()
        FastesLapClass.objects.filter(GP = GrandPrix).delete()
        ResultClass.objects.filter(GP = GrandPrix).delete()
    elif GrandPrix == 'ALL':
        if Session == PracticeClass.objects.model._meta.db_table:
            PracticeClass.objects.all().delete()
        if Session == QaulyClass.objects.model._meta.db_table:
            QaulyClass.objects.all().delete()
        if Session == SprintClass.objects.model._meta.db_table:
            SprintClass.objects.all().delete()
        if Session == StartingClass.objects.model._meta.db_table:
            StartingClass.objects.all().delete()
        if Session == PitstopClass.objects.model._meta.db_table:
            PitstopClass.objects.all().delete()
        if Session == FastesLapClass.objects.model._meta.db_table:
            FastesLapClass.objects.all().delete()
        if Session == ResultClass.objects.model._meta.db_table:
            ResultClass.objects.all().delete()
    

#/////////////////////////////////////////////  Graphs  ///////////////////////////////////////////////////////////////////
class LineGraphClass: 
    def __init__(self, Label= '', Data = [],Color =''): 
        self.Label = Label 
        self.Data = Data
        self.Color = Color
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=3)
    
    def to_dict(self):
      return {"data": self.Data, "label": self.Label, "borderColor": self.Color, "fill": False}


def Graphs(request):
    return render(request,'Head2Head/Graph.html')

def GetGraphData(request, *args, **kwargs):
    listofLabels = GetListOfGrandPrix()
    ListofObjects = GetPointGraphObjects(listofLabels)
    
    # jsonLabels = json.dumps(listofLabels)
    results = [obj.to_dict() for obj in ListofObjects]

    jsdata = json.dumps({"results": results})


    data = { "title" : "Point Progression", 
             "labels": listofLabels,
             "items" : results }
    return JsonResponse(data, safe=False)

#////////////////////////////////////////////  Graph data  ///////////////////////////////////////////////////////////////////
def GetListOfGrandPrix():
    QaulyList = QaulyClass.objects.all()
    GPList = []
    for t in QaulyList:
        if t.GP in GPList:
            x= 2
        else:
            GPList.append(t.GP)
    return GPList
#get Data for total point graph
def GetPointGraphObjects(GPList):
    driverList = DriverClass.objects.all()
    RaceList = ResultClass.objects.all()
    SrpintList = SprintClass.objects.all()
    Objectlist = []

    #Get points
    for x in driverList:
        DriverTotalPoints = 0
        DriverTotalPointList = []
        for y in GPList:
            RaceSession = next((z for z in RaceList if z.No == x.No and z.GP == y),'NotFound')
            SprintSession = next((z for z in SrpintList if z.No == x.No and z.GP == y),'NotFound')

            if SprintSession != 'NotFound':
                DriverTotalPoints += SprintSession.Pts

            if RaceSession != 'NotFound':
                DriverTotalPoints += RaceSession.Pts
                DriverTotalPointList.append(DriverTotalPoints)
            else:
                DriverTotalPointList.append(DriverTotalPoints)

            
    
        if x.Car.upper() == "RED BULL RACING HONDA":
            LineColor = '#0600ef'
        elif x.Car.upper() == "MERCEDES":
            LineColor = '#00d2be'
        elif x.Car.upper() == "MCLAREN MERCEDES":
            LineColor = '#FF9800'
        elif x.Car.upper() == "FERRARI":
            LineColor = '#dc0000'
        elif x.Car.upper() == "ALPHATAURI HONDA":
            LineColor = '#2b4562'
        elif x.Car.upper() == "ASTON MARTIN MERCEDES":
            LineColor = '#006f62'
        elif x.Car.upper() == "ALPINE RENAULT":
            LineColor = '#0090ff'
        elif x.Car.upper() == "ALFA ROMEO RACING FERRARI":
            LineColor = '#900000'
        elif x.Car.upper() == "WILLIAMS MERCEDES":
            LineColor = '#005aff'
        elif x.Car.upper() == "HAAS FERRARI":
            LineColor = '#ffffff'

        NewObject = LineGraphClass()
        NewObject.Color = LineColor
        NewObject.Label = x.Abbr
        NewObject.Data = DriverTotalPointList

        Objectlist.append(NewObject)

    return Objectlist

def getQualyGaps():
    QaulyList = QaulyClass.objects.all()
    DriverList = DriverClass.objects.all()
    class QualyGraph(object):
        pass

    GPList = GetListOfGrandPrix()
    AllDriversWithTime = []
    for x in DriverList:
        print(x.Name)
        DriverTotalTime = []
        for y in GPList:
            QualySession = next((z for z in QaulyList if z.No == x.No and z.GP == y),'NotFound')

            if QualySession != 'NotFound':
                if QualySession.Q3 != '':
                    if QualySession.Q3 == 'DNF':
                        if QualySession.Pos != 'NC'and QualySession.Pos != 'RT':
                            DriverTime = QualySession.Q2

                    else:
                        if QualySession.Pos != 'NC'and QualySession.Pos != 'RT':
                            DriverTime = QualySession.Q3

                elif QualySession.Q2 != '':
                    if QualySession.Q3 == 'DNF':
                        if QualySession.Pos != 'NC'and QualySession.Pos != 'RT':
                            DriverTime = QualySession.Q1

                    else:
                        if QualySession.Pos != 'NC'and QualySession.Pos != 'RT':
                            if QualySession.Q2 == 'DNF':
                                DriverTime = QualySession.Q1
                            else:
                                DriverTime = QualySession.Q2

                else:
                    if QualySession.Pos != 'NC'and QualySession.Pos != 'RT':
                        if QualySession.Q1 != 'DNF':
                            DriverTime = QualySession.Q1
                
            DriverTotalTime.append(DriverTime)
        ConvertedDriverTime = []
        for time in DriverTotalTime:
            minute = time[:time.index(':')]
            second = time[time.index(':') + 1 :time.index('.') ]
            milliseconds = time[-3:]

            Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)

            ConvertedDriverTime.append(Compiled)

        NewDriver = QualyGraph()
        NewDriver.Driver = x.Name + ' ' + x.Surname
        NewDriver.AvgTime = sum(ConvertedDriverTime)/len(ConvertedDriverTime)/100
        AllDriversWithTime.append(NewDriver)
    FastestDriverTime = min(d.AvgTime for  d in AllDriversWithTime)
    AllDriversWithTime.sort(key=lambda item: item.AvgTime, reverse = True)
    print("works")



#/////////////////////////////////////////////  F1 statistsics  ///////////////////////////////////////////////////////////////////
# def index(request):
    
#     return render(request,'Head2Head/index.html')

#To hide the real admin site
def FakeAdmin(request):
    return render(request,'Head2Head/Fake.html')

#list of drivers
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
            
    
            #get stats
            GetQaulyDriverStats(driv1,driv2)
            GetRaceDriverStats(driv1,driv2)
            
            #list of drivers
            DriverObjetList = DriverClass.objects.all().order_by('Name')


            searchd1 = [x for x in DriverObjetList if x.No == driv1]
            searchd2 = [x for x in DriverObjetList if x.No == driv2]

            #assign values
            Qualyobject = {'d1qualy': D1QaulyRecord, 'd2qualy': D2QaulyRecord,
                            'd1best': Driver1Best, 'd2best': Driver2Best,
                            'd1worst': Driver1Worst, 'd2worst': Driver2Worst,
                            'd1avg': Driver1Avg, 'd2avg': Driver2Avg,
                            'd1q3': Driver1Q3, 'd2q3': Driver2Q3,
                            'd1q2': Driver1Q2, 'd2q2': Driver2Q2,
                            'd1': d1, 'd2': d2,
                            'd1No': d1No, 'd2No': d2No,
                            'd1img': searchd1[0].img, 'd2img': searchd2[0].img,
                            'd1pole': Driver1Poles, 'd2pole': Driver2Poles,
                            'd1no': driv1, 'd2no': driv2,
                             'delta': Delta,
            
            }

            Raceobject = {'d1race': D1RaceRecord, 'd2race': D2RaceRecord,
                            'd1total': D1TotalPoints, 'd2total': D2TotalPoints,
                            'd1avgpts': D1AveragePoints, 'd2avgpts': D2AveragePoints,
                            'd1avgptsnc': D1AverageWithNCPoints, 'd2avgptsnc': D2AverageWithNCPoints,
                            'd1avgfin': D1AverageFinishs, 'd2avgfin': D2AverageFinishs,
                            'd1avgfinWithNC': D1AverageFinishsWithNC, 'd2avgfinWithNC': D2AverageFinishsWithNC,
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
            
            
            #get stats
            GetTeamQaulyStats(team1,team2)
            GetTeamRaceStats(team1,team2)
           
            #list of teams
            DriverObjetList = DriverClass.objects.all().order_by('Car')

            # searchd1 = [x for x in DriverObjetList if x.No == tea]
            # searchd2 = [x for x in DriverObjetList if x.No == driv2]

            #assign values
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
                            'd1avgfinWithNC': D1AverageFinishsWithNC, 'd2avgfinWithNC': D2AverageFinishsWithNC,
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



#/////////////////////////////////////////////  Get statistsics  ///////////////////////////////////////////////////////////////////


def GetQaulyDriverStats(Driver1,Driver2):
    QaulyList = QaulyClass.objects.all()


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

    D1Record = 0
    D2Record = 0

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

        #check if driver finished the eace and add pos to list
        if D1Skipped == False:
            if x.Pos == "RT" or x.Pos == "NC":
                d1qualsession = [z for z in QaulyList if z.GP == x.GP]
                countPos = 0
                for s in d1qualsession:
                    if s.No == x.No:
                        countPos +=1
                        # Driver1PosList.append(countPos)
                        break
                    else:
                        countPos +=1
            else:
                Driver1PosList.append(int(x.Pos))
        
        #check if driver finished the eace and add pos to list
        if D2Skipped == False:
            if p.Pos == "RT" or p.Pos == "NC":
                d2qualsession = [z for z in QaulyList if z.GP == p.GP]
                countPos = 0
                for s in d2qualsession:
                    if s.No == p.No:
                        countPos +=1
                        # Driver2PosList.append(countPos)
                        break
                    else:
                        countPos +=1
            else:
                Driver2PosList.append(int(p.Pos))

            #Get driver best time from highest session
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
        
        #Get driver best time from highest session
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

        #count qualy appearnaces
        if D1Skipped == False:
            if x.Pos != 'NC' and x.Pos != 'RT':
                if int(x.Pos) <= 10:
                    D1Q3 += 1
                    D1Q2 += 1
                if int(x.Pos) > 10 and int(x.Pos) <= 15:
                    D1Q2 += 1
        if D2Skipped == False:
            if p.Pos != 'NC' and p.Pos != 'RT':
                if int(p.Pos) <= 10:
                    D2Q3 += 1
                    D2Q2 += 1
                if int(p.Pos) > 10 and int(p.Pos) <= 15:
                    D2Q2 += 1
        
    
        #count time driver finished ahead of other
        if D1Skipped == False and D2Skipped == False:
            if x.Pos == "RT" or x.Pos == "NC":
                if p.Pos == "RT" or p.Pos == "NC": 
                    D1Record += 0
                    D2Record += 0
                else:
                    D2Record += 1
            elif p.Pos == "RT" or p.Pos == "NC":
                if x.Pos == "RT" or x.Pos == "NC": 
                    D1Record += 0
                    D2Record += 0
                else:
                    D1Record += 1
            else:
                if int(x.Pos) < int(p.Pos):
                    D1Record += 1
                elif int(x.Pos) > int(p.Pos):
                    D2Record += 1

        #check if both drivers have set a proper time.
        if Driver1Time == 'DNF' or Driver1Time == 'RT' or Driver2Time == 'DNF' or Driver2Time == 'RT' or Driver1Time == '' or Driver2Time == '' or x.Pos == 'NC' or p.Pos == 'NC':
            D1Skipped = False
            D2Skipped = False
        else:
            Gap = GetTimeDiffernace(Driver1Time,Driver2Time)
            GapList.append(Gap)
            D1Skipped = False
            D2Skipped = False
        
       

    global D1QaulyRecord
    D1QaulyRecord = D1Record 
    global D2QaulyRecord
    D2QaulyRecord = D2Record

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

    global d1No
    d1No = Driver1Sessions[0].No
    global d2No
    d2No = Driver2Sessions[0].No

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

    D1Record = 0
    D2Record = 0

    #Used for tracking if driver has skipped a race
    #Get a list of all the GP's
    GPList = []
    for t in RaceList:
        if t.GP in GPList:
            x= 2
        else:
            GPList.append(t.GP)

    Driver1PosList = []
    Driver1PosListWithNC = []
    Driver2PosList = []
    Driver2PosListWithNC = []

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
        if x.Time == 'DNF' or x.Time == 'DNS' or x.Pos == "DQ":
            h = 'I have to use this cause python is drunk and cant pick up !='
        else:
            StartPos = next((z.Pos for z in StartingGridList if z.No == x.No and z.GP == y),'NotFound')
            if StartPos != 'NotFound':
                PositionsMade = int(StartPos)  - int(x.Pos)
                D1PositionGainList.append(PositionsMade)
        if p.Time == 'DNF' or p.Time == 'DNS' or p.Pos == "DQ":
            h = 'I have to use this cause python i drunk and cant pick up !='
        else:
            StartPos = next((z.Pos for z in StartingGridList if z.No == p.No and z.GP == y),'NotFound')
            if StartPos != 'NotFound':
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
            if x.Pos == "RT" or x.Pos == "NC" or x.Pos == "DQ":
                d1qualsession = [z for z in RaceList if z.GP == x.GP]
                countPos = 0
                for s in d1qualsession:
                    if s.No == x.No:
                        countPos +=1
                        Driver1PosListWithNC.append(countPos)
                        Driver1PointListWithNC.append(int(x.Pts))
                        break
                    else:
                        countPos +=1

            else:
                Driver1PosList.append(int(x.Pos))
                Driver1PosListWithNC.append(int(x.Pos))
                Driver1PointList.append(int(x.Pts))
                Driver1PointListWithNC.append(int(x.Pts))

        if D2Skipped == False:
            if p.Pos == "RT" or p.Pos == "NC" or p.Pos == "DQ":
                d2qualsession = [z for z in RaceList if z.GP == p.GP]
                countPos = 0
                for s in d2qualsession:
                    if s.No == p.No:
                        countPos +=1
                        Driver2PosListWithNC.append(countPos)
                        Driver2PointListWithNC.append(int(p.Pts))
                        break
                    else:
                        countPos +=1
            
            else:
                Driver2PosList.append(int(p.Pos))
                Driver2PosListWithNC.append(int(p.Pos))
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
        
        #who finiahed ahead
        if D1Skipped == False and D2Skipped == False:
            if x.Pos == "RT" or x.Pos == "NC" or x.Pos == "DQ":
                if p.Pos == "RT" or p.Pos == "NC" or p.Pos == "DQ": 
                    D1Record += 0
                    D2Record += 0
                else:
                    D2Record += 1
            elif p.Pos == "RT" or p.Pos == "NC" or p.Pos == "DQ":
                if x.Pos == "RT" or x.Pos == "NC" or x.Pos == "DQ": 
                    D1Record += 0
                    D2Record += 0
                else:
                    D1Record += 1
            else:
                if int(x.Pos) < int(p.Pos):
                    D1Record += 1
                else:
                    D2Record += 1
            
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


    global D1RaceRecord
    D1RaceRecord = D1Record


    global D1TotalPoints
    D1TotalPoints = D1Total

    global D1AveragePoints
    D1AveragePoints = round(sum(Driver1PointList)/len(Driver1PointList),2)

    global D1AverageWithNCPoints
    D1AverageWithNCPoints = round(sum(Driver1PointListWithNC)/len(Driver1PointListWithNC),2)

    global D1AverageFinishs
    D1AverageFinishs = round(sum(Driver1PosList)/len(Driver1PosList),2)

    global D1AverageFinishsWithNC
    D1AverageFinishsWithNC = round(sum(Driver1PosListWithNC)/len(Driver1PosListWithNC),2)

    global D1BestFinish
    D1BestFinish = min(Driver1PosList)

    global D1RaceWins
    D1RaceWins = D1Wins

    global D1RacePodiums
    D1RacePodiums = D1Podiums

    global D1TeamContribution
    if Pointob["T1Points"] > 0:
        D1TeamContribution = round((sum(D1PointsWithTeam)/Pointob["T1Points"]) * 100,2)
    else:
        D1TeamContribution = 0

    global D1RaceFastestLaps
    D1FastestLaps = D1FastestLapsCounter

    global D1RaceDNF
    D1RaceDNF = D1DNF

    global D1AveragePositionGain
    D1AveragePositionGain = round(sum(D1PositionGainList)/len(D1PositionGainList),2)

    global D1MostPositionsGained
    D1MostPositionsGained = max(D1PositionGainList)

    #//////////////////////////////////////////////////////// driver 2

    global D2RaceRecord
    D2RaceRecord = D2Record

    global D2TotalPoints
    D2TotalPoints = D2Total

    global D2AveragePoints
    D2AveragePoints = round(sum(Driver2PointList)/len(Driver2PointList),2)

    global D2AverageWithNCPoints
    D2AverageWithNCPoints = round(sum(Driver2PointListWithNC)/len(Driver2PointListWithNC),2)

    global D2AverageFinishs
    D2AverageFinishs = round(sum(Driver2PosList)/len(Driver2PosList),2)

    global D2AverageFinishsWithNC
    D2AverageFinishsWithNC = round(sum(Driver2PosListWithNC)/len(Driver2PosListWithNC),2)

    global D2BestFinish
    D2BestFinish = min(Driver2PosList)

    global D2RaceWins
    D2RaceWins = D2Wins

    global D2RacePodiums
    D2RacePodiums = D2Podiums

    global D2TeamContribution
    if Pointob["T2Points"] > 0:
        D2TeamContribution = round((sum(D2PointsWithTeam)/Pointob["T2Points"]) * 100,2)
    else:
        D2TeamContribution = 0

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
                            # x[countDriverPos].Pos = countPos
                            # Team1PosList.append(countPos)
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
                            # p[countDriverPos].Pos = countPos
                            # Team2PosList.append(countPos)
                            break
                        else:
                            countPos +=1
                else:
                    Team2PosList.append(int(d2.Pos))
                countDriverPos += 1


        #Get both driver best time from highest session
        if T1Skipped == False:
            for w in x :
                if w.Pos != 'NC' and w.Pos != 'RT':
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
    #Get both driver best time from highest session
        if T2Skipped == False:
            for w in p :
                if w.Pos != 'NC' and w.Pos != 'RT':
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
                if w.Pos != 'NC' and w.Pos != 'RT':
                    if int(w.Pos) <= 10:
                        T1Q3 += 1
                        T1Q2 += 1
                    elif int(w.Pos) > 10 and int(w.Pos) <= 15:
                        T1Q2 += 1

        if T2Skipped == False:
            for w in p :
                if w.Pos != 'NC' and w.Pos != 'RT':
                    if int(w.Pos) <= 10:
                        T2Q3 += 1
                        T2Q2 += 1
                    elif int(w.Pos) > 10 and int(w.Pos) <= 15:
                        T2Q2 += 1

        #check if atleast 1 driver from both teams has an applicable time set
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
    Team1PosListWithNC = []
    Team2PosList = []
    Team2PosListWithNC = []

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
            if d1.Time == 'DNF' or d1.Time == 'DNS' or d1.Pos == "DQ":
                h = 'I have to use this cause python is drunk and cant pick up !='
            else:
                StartPos = next((z.Pos for z in StartingGridList if z.No == d1.No and z.GP == y),'NotFound')
                if StartPos != 'NotFound':
                    PositionsMade = int(StartPos)  - int(d1.Pos)
                    T1PositionGainList.append(PositionsMade)
        for d2 in p:
            if d2.Time == 'DNF' or d2.Time == 'DNS' or d2.Pos == "DQ":
                h = 'I have to use this cause python i drunk and cant pick up !='
            else:
                StartPos = next((z.Pos for z in StartingGridList if z.No == d2.No and z.GP == y),'NotFound')
                if StartPos != 'NotFound':
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
                if d1.Pos == "RT" or d1.Pos == "NC" or d1.Pos == "DQ":
                    t1qualsession = [z for z in RaceList if z.GP == d1.GP]
                    countPos = 0
                    for s in t1qualsession:
                        if s.No == d1.No:
                            countPos +=1
                            Team1PosListWithNC.append(countPos)
                            Team1PointListWithNC.append(int(d1.Pts))
                            break
                        else:
                            countPos +=1

                else:
                    Team1PosList.append(int(d1.Pos))
                    Team1PosListWithNC.append(int(d1.Pos))
                    Team1PointList.append(int(d1.Pts))
                    Team1PointListWithNC.append(int(d1.Pts))

        if T2Skipped == False:
            for d2 in p:
                if d2.Pos == "RT" or d2.Pos == "NC" or d2.Pos == "DQ":
                    t2qualsession = [z for z in RaceList if z.GP == d2.GP]
                    countPos = 0
                    for s in t2qualsession:
                        if s.No == d2.No:
                            countPos +=1
                            Team2PosListWithNC.append(countPos)
                            Team2PointListWithNC.append(int(d2.Pts))
                            break
                        else:
                            countPos +=1
                
                else:
                    Team2PosList.append(int(d2.Pos))
                    Team2PosListWithNC.append(int(d2.Pos))
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

    global D1AverageFinishsWithNC
    D1AverageFinishsWithNC = round(sum(Team1PosListWithNC)/len(Team1PosListWithNC),2)

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

    global D2AverageFinishsWithNC
    D2AverageFinishsWithNC = round(sum(Team2PosListWithNC)/len(Team2PosListWithNC),2)

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



# get differance between 2 drivers time
def GetTimeDiffernace(T1,T2):

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

#list of teams 
def GetTeams(DriverList):
    TeamList = []
    for t in DriverList:
        if t.Car in TeamList:
            dd= 'test'
        else:
            TeamList.append(t.Car)
    return TeamList


#get differance between 2 teams time
def GetTeamTimeDiffernace(T1,T2):
    T1Combined = 0
    for x in T1:
        if x != 'DNF':
            minute = x[:x.index(':')]
            second = x[x.index(':') + 1 :x.index('.') ]
            milliseconds = x[x.index('.') +1:]

            Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)
            T1Combined = T1Combined + Compiled


    T2Combined = 0
    for x in T2:
        if x != 'DNF':
            minute = x[:x.index(':')]
            second = x[x.index(':') + 1 :x.index('.') ]
            milliseconds = x[x.index('.') +1:]

            Compiled = (int(minute)*60000) + (int(second)*1000) + int(milliseconds)
            T2Combined = T2Combined + Compiled

    Final = ((T1Combined/ len(T1)) - (T2Combined/len(T2))) / 1000

    return Final



#////////////////////////////////////// Race Methods and data //////////////////////////////////////////////////////////  

#Get total points for teams
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



#/////////////////////////////////////////////////////////// Get Race Data  Methods  ////////////////////////////////////////////////
def LoadDrivers():

    driverList = DriverClass.objects.all()
    URL = 'https://www.formula1.com/en/results.html/2021/drivers.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows


    count = 0
    columns = []
    DriverObjectList = []

    for currentrow in rows:
        Standingcolumns =currentrow.find_all("td")

        FullName = Standingcolumns[2].text.replace('\n', ' ').strip()
        

        #Get the link to the driver result page
        LinkObject = Standingcolumns[2].find("a")
        LinkToDriver = LinkObject.get("href") 
        LinkToDriver = 'https://www.formula1.com' + LinkToDriver

        #Get the link to the driver first race they participated in
        page = requests.get(LinkToDriver)
        soup = BeautifulSoup(page.content, 'html.parser')

        racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
        rows = racesTable.tbody.find_all("tr")  # contains 2 rows

        columns =rows[0].find_all("td")
        LinkObject = columns[1].find("a")
        LinkToRace = LinkObject.get("href") 
        LinkToRace = 'https://www.formula1.com' + LinkToRace

        #Get the driver record and get thier number
        page = requests.get(LinkToRace)
        soup = BeautifulSoup(page.content, 'html.parser')

        racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
        rows = racesTable.tbody.find_all("tr")  # contains 2 rows

        for currentrow in rows:
            columns =currentrow.find_all("td")

            RaceFullName = columns[3].text.replace('\n', ' ').strip()
            if RaceFullName == FullName:
                DriverNo = columns[2].text.replace('\n', ' ').strip()
                break


        space = FullName.index(' ')
        Name = FullName[:space]
        FullName = FullName.replace(Name + ' ','')

        space = FullName.index(' ')
        Surname = FullName[:space]
        FullName = FullName.replace(Surname + ' ','')

        Abbr = FullName

        Driver = DriverClass()
        Driver.No = DriverNo
        Driver.Car = columns[4].text.replace('\n', ' ').strip()
        Driver.Name = Name
        Driver.Surname = Surname
        Driver.Abbr = Abbr
        DriverObjectList.append(Driver)
        foundobject = next((z for z in driverList if z.No == Driver.No and z.Surname ==  Driver.Surname and z.Name ==  Driver.Name),'NotFound')
        if foundobject == 'NotFound' :
            Driver.save()


def GetPractice(soup,Name,CurrentSession):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    PracticeList = PracticeClass.objects.all()
    

    for currentrow in rows:
        columns =currentrow.find_all("td")
        PracticeObject = PracticeClass()
        PracticeObject.Pos = columns[1].text.replace('\n', ' ').strip()
        PracticeObject.No = columns[2].text.replace('\n', ' ').strip()
        PracticeObject.Driver = columns[3].text.replace('\n', ' ').strip()
        PracticeObject.Car = columns[4].text.replace('\n', ' ').strip()
        PracticeObject.Time = columns[5].text.replace('\n', ' ').strip()
        PracticeObject.Gap = columns[6].text.replace('\n', ' ').strip()
        PracticeObject.Laps = columns[7].text.replace('\n', ' ').strip()
        PracticeObject.Session = CurrentSession
        PracticeObject.GP = Name

        foundobject = next((z for z in PracticeList if z.No == PracticeObject.No and z.GP == PracticeObject.GP and z.Session == PracticeObject.Session ),'NotFound')
        if foundobject == 'NotFound' :
            PracticeObject.save()
    #     PracticeList.append(PracticeObject)

    # return PracticeList

def GetQualy(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    QaulyList = []
    QaulyList = QaulyClass.objects.all()

    for currentrow in rows:
        columns =currentrow.find_all("td")
        QaulyObject = QaulyClass()
        QaulyObject.Pos = columns[1].text.replace('\n', ' ').strip()
        QaulyObject.No = columns[2].text.replace('\n', ' ').strip()
        QaulyObject.Driver = columns[3].text.replace('\n', ' ').strip()
        QaulyObject.Car = columns[4].text.replace('\n', ' ').strip()
        QaulyObject.Q1 = columns[5].text.replace('\n', ' ').strip()
        QaulyObject.Q2 = columns[6].text.replace('\n', ' ').strip()
        QaulyObject.Q3 = columns[7].text.replace('\n', ' ').strip()
        QaulyObject.Laps = columns[8].text.replace('\n', ' ').strip()
        QaulyObject.GP = Name

        foundobject = next((z for z in QaulyList if z.No == QaulyObject.No and z.GP == QaulyObject.GP),'NotFound')
        if foundobject == 'NotFound' :
            QaulyObject.save()

        # QaulyList.append(QaulyObject)

    # return QaulyList

def GetStart(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    StartObjectList = []
    StartingList = StartingClass.objects.all()

    # NoteObject  = soup.find("p", attrs={"class": "note"})
    # if NoteObject != None:
    #     MyRetrunClass.Note = NoteObject.text

    for currentrow in rows:
        columns =currentrow.find_all("td")
        startObject = StartingClass()
        startObject.Pos = columns[1].text.replace('\n', ' ').strip()
        startObject.No = columns[2].text.replace('\n', ' ').strip()
        startObject.Driver = columns[3].text.replace('\n', ' ').strip()
        startObject.Car = columns[4].text.replace('\n', ' ').strip()
        startObject.Time = columns[5].text.replace('\n', ' ').strip()
        startObject.GP = Name

        foundobject = next((z for z in StartingList if z.No == startObject.No and z.GP == startObject.GP),'NotFound')
        if foundobject == 'NotFound' :
            startObject.save()


    #     StartObjectList.append(startObject)

    # MyRetrunClass.List = StartObjectList
    # return MyRetrunClass

def GetPit(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    PitObjectList = []
    PitList = PitstopClass.objects.all()

    for currentrow in rows:
        columns =currentrow.find_all("td")
        Pitstop = PitstopClass()
        Pitstop.Stops = columns[1].text.replace('\n', ' ').strip()
        Pitstop.No = columns[2].text.replace('\n', ' ').strip()
        Pitstop.Driver = columns[3].text.replace('\n', ' ').strip()
        Pitstop.Car = columns[4].text.replace('\n', ' ').strip()
        Pitstop.Lap = columns[5].text.replace('\n', ' ').strip()
        Pitstop.TOD = columns[6].text.replace('\n', ' ').strip()
        Pitstop.Time = columns[7].text.replace('\n', ' ').strip()
        Pitstop.Total = columns[8].text.replace('\n', ' ').strip()
        Pitstop.GP = Name
        foundobject = next((z for z in PitList if z.No == Pitstop.No and z.GP == Pitstop.GP),'NotFound')
        if foundobject == 'NotFound' :
            Pitstop.save()

    #     PitObjectList.append(Pitstop)

    # return PitObjectList

def GetFast(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    FastLapObjectList = []
    fastestList = FastesLapClass.objects.all()

    for currentrow in rows:
        columns =currentrow.find_all("td")
        Fastlap = FastesLapClass()
        Fastlap.Pos = columns[1].text.replace('\n', ' ').strip()
        Fastlap.No = columns[2].text.replace('\n', ' ').strip()
        Fastlap.Driver = columns[3].text.replace('\n', ' ').strip()
        Fastlap.Car = columns[4].text.replace('\n', ' ').strip()
        Fastlap.Lap = columns[5].text.replace('\n', ' ').strip()
        Fastlap.TOD = columns[6].text.replace('\n', ' ').strip()
        Fastlap.Time = columns[7].text.replace('\n', ' ').strip()
        Fastlap.AVGSpeed = columns[8].text.replace('\n', ' ').strip()
        Fastlap.GP = Name
        foundobject = next((z for z in fastestList if z.No == Fastlap.No and z.GP == Fastlap.GP),'NotFound')
        if foundobject == 'NotFound' :
            Fastlap.save()

        # FastLapObjectList.append(Fastlap)

    # return FastLapObjectList

def GetResult(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    RaceObjectList = []
    RacetList = ResultClass.objects.all()

    for currentrow in rows:
        columns =currentrow.find_all("td")
        RaceResult = ResultClass()
        RaceResult.Pos = columns[1].text.replace('\n', ' ').strip()
        RaceResult.No = columns[2].text.replace('\n', ' ').strip()
        RaceResult.Driver = columns[3].text.replace('\n', ' ').strip()
        RaceResult.Car = columns[4].text.replace('\n', ' ').strip()
        RaceResult.Laps = columns[5].text.replace('\n', ' ').strip()
        RaceResult.Time = columns[6].text.replace('\n', ' ').strip()
        RaceResult.Pts = columns[7].text.replace('\n', ' ').strip()
        RaceResult.GP = Name
        foundobject = next((z for z in RacetList if z.No == RaceResult.No and z.GP == RaceResult.GP),'NotFound')
        if foundobject == 'NotFound' :
            RaceResult.save()
        # RaceObjectList.append(RaceResult)

    # return RaceObjectList

def GetSprint(soup,Name):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    RaceObjectList = []
    SprintList = SprintClass.objects.all()

    for currentrow in rows:
        columns =currentrow.find_all("td")
        SprintResult = SprintClass()
        SprintResult.Pos = columns[1].text.replace('\n', ' ').strip()
        SprintResult.No = columns[2].text.replace('\n', ' ').strip()
        SprintResult.Driver = columns[3].text.replace('\n', ' ').strip()
        SprintResult.Car = columns[4].text.replace('\n', ' ').strip()
        SprintResult.Laps = columns[5].text.replace('\n', ' ').strip()
        SprintResult.Time = columns[6].text.replace('\n', ' ').strip()
        SprintResult.Pts = columns[7].text.replace('\n', ' ').strip()
        SprintResult.GP = Name
        foundobject = next((z for z in SprintList if z.No == SprintResult.No and z.GP == SprintResult.GP),'NotFound')
        if foundobject == 'NotFound' :
            SprintResult.save()
        # RaceObjectList.append(RaceResult)

    # return RaceObjectList


class RaceResultClass:
    def __init__(self,GP = '',Date = '',Winner = '',Car = '',Laps = 0,Time= ''):
        self.GP = GP
        self.Date = Date
        self.Winner = Winner
        self.Car = Car
        self.Laps = Laps
        self.Time = Time
#Get the most recent grand prix raced at
def GetLastRace(soup):
    racesTable = soup.find("table", attrs={"class": "resultsarchive-table"})
    rows = racesTable.tbody.find_all("tr")  # contains 2 rows

    count = 0
    columns = []
    RaceObjectList = []

    for currentrow in rows:
        columns =currentrow.find_all("td")
        RaceResult = RaceResultClass()
        RaceResult.GP = columns[1].text.replace('\n', ' ').strip()
        RaceResult.Date = columns[2].text.replace('\n', ' ').strip()
        RaceResult.Winner = columns[3].text.replace('\n', ' ').strip()
        RaceResult.Car = columns[4].text.replace('\n', ' ').strip()
        RaceResult.Laps = columns[5].text.replace('\n', ' ').strip()
        RaceResult.Time = columns[6].text.replace('\n', ' ').strip()
        RaceObjectList.append(RaceResult)

    Lastelement = RaceObjectList[-1]

    return Lastelement.GP

class LinkClass: 
    def __init__(self, Url= '',Name =''): 
        self.Url = Url 
        self.Name = Name

#Get All the links to the different grand prix
def GetLinks():
    URL = 'https://www.formula1.com/en/results.html/2021/races.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    AllRacesLinks = soup.find_all("a", attrs={"data-name": "meetingKey"})

    FinalRaceLinkList = []
    LastRace = GetLastRace(soup)

    for x in AllRacesLinks:
        Name = x.find("span", attrs={"class": "clip"})
        GPName = Name.text
        if GPName != 'All':
            #Used to only get the lonks of grandprix we have raced at 
            FinalRaceLink = LinkClass()
            if GPName == LastRace:
                FinalRaceLink.Url = 'https://www.formula1.com/' + x.get('href')
                FinalRaceLink.Name = GPName
                FinalRaceLinkList.append(FinalRaceLink)

                break
            else:
                FinalRaceLink.Url = 'https://www.formula1.com/' + x.get('href')
                FinalRaceLink.Name = GPName
                FinalRaceLinkList.append(FinalRaceLink)

    return FinalRaceLinkList

#checl whether it is a sprint weekend or not 
def testIFsprintweekend(Link):
    page = requests.get(Link)
    soup = BeautifulSoup(page.content, 'html.parser')


    nav = soup.find("ul", attrs={"class": "resultsarchive-side-nav"})
    listofsessions = nav.find_all("li")
    for session in listofsessions:
        text = session.text.replace('\n', ' ').strip()
        if text == "Sprint qualifying":
            return True

    return False
#gets all new race data 
def LoadRaceWeekendData():
    LinkList = GetLinks()
    for x in LinkList:
        RaceName = x.Name
        isSprintWeekend = testIFsprintweekend(x.Url)

        print("---------------------------Staring with " + RaceName +" -------------------------------------------------")
        newLink = x.Url
        page = requests.get(x.Url)
        soup = BeautifulSoup(page.content, 'html.parser')
        GetResult(soup,RaceName)
        


        print("---------------------------Done with Race-------------------------------------------------")


        FastestLapLink = newLink.replace('race-result.html','fastest-laps.html')
        page = requests.get(FastestLapLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        GetFast(soup,RaceName)


        print("---------------------------Done with Fastest-------------------------------------------------")



        PitstopLink = FastestLapLink.replace('fastest-laps.html','pit-stop-summary.html')
        page = requests.get(PitstopLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        GetPit(soup,RaceName)




        print("---------------------------Done with Pitstop-------------------------------------------------")


        Note = ''
        StartingLink = PitstopLink.replace('pit-stop-summary.html','starting-grid.html')
        page = requests.get(StartingLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        GetStart(soup,RaceName)


        print("---------------------------Done with Starting grid-------------------------------------------------")

        
        if isSprintWeekend == False:
            QaulyLink = StartingLink.replace('starting-grid.html','qualifying.html')
            page = requests.get(QaulyLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetQualy(soup,RaceName)
            
            



            print("---------------------------Done with Qauly-------------------------------------------------")


            PracticeLink = QaulyLink.replace('qualifying.html','practice-3.html')
            page = requests.get(PracticeLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetPractice(soup,RaceName,'P3')



            print("---------------------------Done with P3-------------------------------------------------")


            PracticeLink = PracticeLink.replace('practice-3.html','practice-2.html')
            page = requests.get(PracticeLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetPractice(soup,RaceName,'P2')

            

            print("---------------------------Done with P2 -------------------------------------------------")

            soup = ''
            PracticeLink = PracticeLink.replace('practice-2.html','practice-1.html')
            page = requests.get(PracticeLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetPractice(soup,RaceName,'P1')
            



            print("---------------------------Done with P1-------------------------------------------------")
        elif isSprintWeekend == True:
            SprintQaulyLink = StartingLink.replace('starting-grid.html','sprint-qualifying-results.html')
            page = requests.get(SprintQaulyLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetSprint(soup,RaceName)
     

            print("---------------------------Done with Sprint Qaulifying-------------------------------------------------")

            
            SprintQaulyLinkGrid = SprintQaulyLink.replace('sprint-qualifying-results.html','sprint-qualifying-grid.html')
            page = requests.get(SprintQaulyLinkGrid)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetStart(soup,RaceName)

      

            print("---------------------------Done with Sprint Qaulifying Grid-------------------------------------------------")


            PracticeLink = SprintQaulyLinkGrid.replace('sprint-qualifying-grid.html','practice-2.html')
            page = requests.get(PracticeLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            Practice2List = GetPractice(soup,RaceName,'P2')

         

            print("---------------------------Done with P2 -------------------------------------------------")


            QaulyLink = PracticeLink.replace('practice-2.html','qualifying.html')
            page = requests.get(QaulyLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetQualy(soup,RaceName)
            
          



            print("---------------------------Done with Qauly-------------------------------------------------")

            soup = ''
            PracticeLink = QaulyLink.replace('qualifying.html','practice-1.html')
            page = requests.get(PracticeLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            GetPractice(soup,RaceName,'P1')
            

            


            print("---------------------------Done with P1-------------------------------------------------")




    print("---------------------------Done with everything-------------------------------------------------")



