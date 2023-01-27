#BOT6.3
import numpy as np

EMPTY = 0


class player:
    def __init__(self):
        self.step = 0
        # Player Properties
        self.PlayerNumber = 0
        self.plans = ["BestPlace", "RectanglePlan", "RectanglePlanStep1","closestEmpty"]
        self.currentPlan = None
        self.targetPos = [0,0]

        # Rectangle Properties
        self.rectangleChosen = [0, 0]
        self.Rect = {"dim_x": 6,
                     "dim_y": 6,
                     "RectPos": [[0, 0], [0, 0], [0, 0], [0, 0]],
                     "RectLine": [-1, 0],
                     "case":[-2,-2]
                     }
        self.possibleRectangles = []

        # Opponent Properties
        self.oppNum = 2

    def move(self, B, N, cur_x, cur_y):
        if self.step == 400:
            return (0,0)
        Barr = np.array(B)

        #updating the rectangular conquered cells
        minx = min(self.Rect["RectPos"][1][0],
                   self.Rect["RectPos"][1][0] - self.Rect["case"][0] * (self.Rect["dim_x"] - 1))
        maxx = max(self.Rect["RectPos"][1][0],
                   self.Rect["RectPos"][1][0] - self.Rect["case"][0] * (self.Rect["dim_x"] - 1))
        miny = min(self.Rect["RectPos"][1][1],
                   self.Rect["RectPos"][1][1] - self.Rect["case"][1] * (self.Rect["dim_y"] - 1))
        maxy = max(self.Rect["RectPos"][1][1],
                   self.Rect["RectPos"][1][1] - self.Rect["case"][1] * (self.Rect["dim_y"] - 1))
        allTargetConquered = 1
        for i in range(minx, maxx + 1):
            if Barr[i, miny] != self.PlayerNumber:
                allTargetConquered = 0
            if Barr[i, maxy] != self.PlayerNumber:
                allTargetConquered = 0
        for j in range(miny, maxy + 1):
            if Barr[minx, j] != self.PlayerNumber:
                allTargetConquered = 0
            if Barr[maxx, j] != self.PlayerNumber:
                allTargetConquered = 0

        if allTargetConquered == 1:
            for i in range(minx,maxx+1):
                for j in range(miny,maxy + 1):
                    Barr[i,j] = self.PlayerNumber

        #updating the rectangular conquered cells end

        self.step += 1
        # print(self.step)
        # print("curx = " , cur_x , ",cury = " , cur_y)
        if self.step == 1:
            self.PlayerNumber = B[cur_x][cur_y]
            if self.PlayerNumber == 1:
                self.oppNum = 2
            else:
                self.oppNum = 1
            self.currentPlan = 1
            self.chooseRectangle(Barr,N,6,6,cur_x,cur_y)


        move = (0,0)
        if self.currentPlan == 1:
            if self.isRectanglePlanFine(Barr,N,cur_x,cur_y) == 1:
                move = self.RectMove(Barr,N,self.Rect["dim_x"],self.Rect["dim_y"],cur_x,cur_y)
            else:
                self.chooseRectangle(Barr,N,6,6,cur_x,cur_y)
                if self.currentPlan == 1:
                    move = self.RectMove(Barr,N,self.Rect["dim_x"],self.Rect["dim_y"],cur_x,cur_y)
                else:
                    move = self.BestPlace(Barr,N,cur_x,cur_y)
 
        return move

    # Rectangle Functions
    def chooseRectangle(self, Barr, N, dim_x, dim_y, cur_x, cur_y):
        # print("choose Rectangle Function called")
        cases = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
        bestPossibleRectangle = {"dim_x": 0,
                                 "dim_y": 0,
                                 "case": [-2, -2],
                                 "steps": 0,
                                 "cells_conquered": 0,
                                 "ratio": 0,
                                 "lineselected":"horizontal"}
        bestPossibleRectangleCase = [{"dim_x": 0,
                                      "dim_y": 0,
                                      "steps": 0,
                                      "cells_conquered": 0,
                                      "ratio": 0,
                                      "lineselected":"horizontal"},
                                     {"dim_x": 0,
                                      "dim_y": 0,
                                      "steps": 0,
                                      "cells_conquered": 0,
                                      "ratio": 0,
                                      "lineselected":"horizontal"},
                                     {"dim_x": 0,
                                      "dim_y": 0,
                                      "steps": 0,
                                      "cells_conquered": 0,
                                      "ratio": 0,
                                      "lineselected":"horizontal"},
                                     {"dim_x": 0,
                                      "dim_y": 0,
                                      "steps": 0,
                                      "cells_conquered": 0,
                                      "ratio": 0,
                                      "lineselected":"horizontal"}]

        bestPossibleRectangleCase[0] = self.findBestRectangle(Barr, N, cur_x, cur_y, 6, 6, cases[0]).copy()
        bestPossibleRectangleCase[1] = self.findBestRectangle(Barr, N, cur_x, cur_y, 6, 6, cases[1]).copy()
        bestPossibleRectangleCase[2] = self.findBestRectangle(Barr, N, cur_x, cur_y, 6, 6, cases[2]).copy()
        bestPossibleRectangleCase[3] = self.findBestRectangle(Barr, N, cur_x, cur_y, 6, 6, cases[3]).copy()

        ratios = [bestPossibleRectangleCase[0]["ratio"], bestPossibleRectangleCase[1]["ratio"],
                    bestPossibleRectangleCase[2]["ratio"], bestPossibleRectangleCase[3]["ratio"]]
        maxRatio = max(ratios)
        bprIndex = ratios.index((maxRatio))


        bestPossibleRectangle["dim_x"] = bestPossibleRectangleCase[bprIndex]["dim_x"]
        bestPossibleRectangle["dim_y"] = bestPossibleRectangleCase[bprIndex]["dim_y"]
        bestPossibleRectangle["case"] = cases[bprIndex].copy()
        bestPossibleRectangle["steps"] = bestPossibleRectangleCase[bprIndex]["steps"]
        bestPossibleRectangle["cells_conquered"] = bestPossibleRectangleCase[bprIndex]["cells_conquered"]
        bestPossibleRectangle["ratio"] = bestPossibleRectangleCase[bprIndex]["ratio"]
        bestPossibleRectangle["lineselected"] = bestPossibleRectangleCase[bprIndex]["lineselected"]

        if bestPossibleRectangle["ratio"] < 1:

            self.currentPlan = 3
        else:
            self.Rect["dim_x"] = bestPossibleRectangle["dim_x"]
            self.Rect["dim_y"] = bestPossibleRectangle["dim_y"]
            case = bestPossibleRectangle["case"].copy()
            dim_x = self.Rect["dim_x"]
            dim_y = self.Rect["dim_y"]
            if bestPossibleRectangle["lineselected"] == "vertical":
                if dim_x == 1:
                    thirdx = cur_x
                else:
                    thirdx = cur_x + case[0]
                self.Rect["RectPos"] = [[cur_x,cur_y + (dim_y-1)*case[1]], [cur_x + (dim_x-1)*case[0],cur_y + (dim_y-1)*case[1]],
                                        [cur_x + (dim_x-1)*case[0],cur_y], [thirdx, cur_y]]
            else:
                if dim_y == 1:
                    thirdy = cur_y
                else:
                    thirdy = cur_y + case[1]
                self.Rect["RectPos"] = [[cur_x + (dim_x-1)*case[0],cur_y],
                                        [cur_x + (dim_x-1) * case[0], cur_y + (dim_y-1) * case[1]],
                                        [cur_x,cur_y + (dim_y-1)*case[1]], [cur_x, thirdy]]
            self.Rect["RectLine"] = [-1,0]
            self.Rect["case"] = bestPossibleRectangle["case"]
            self.targetPos = self.Rect["RectPos"][0].copy()
            self.currentPlan = 1

    def findBestRectangle(self, Barr, N, cur_x, cur_y, dim_x, dim_y, case):
        #ex curx = 12 , cury = 2 case -1,-1
        DIMX = dim_x
        DIMY = dim_y
        if cur_x + case[0] * (dim_x - 1) < 0: #12 + -1*5 = 7
            dim_x = cur_x + 1
        if cur_x + case[0] * (dim_x - 1) > 29:
            dim_x = N - cur_x
        if cur_y + case[1] * (dim_y - 1) < 0: #2 + -1*5 = -3
            dim_y = cur_y + 1 #dimy = 3
        if cur_y + case[1] * (dim_y - 1) > 29:
            dim_y = N - cur_y
        #dimx = 6 dimy =3
        if dim_x <= 1 and dim_y <= 1:
            return {"dim_x": 0,
                    "dim_y": 0,
                    "steps": 0,
                    "cells_conquered": 0,
                    "ratio": 0,
                    "lineselected":"horizontal"}

        minx = min(cur_x, cur_x + case[0] * (dim_x - 1))
        miny = min(cur_y, cur_y + case[1] * (dim_y - 1))
        maxx = max(cur_x, cur_x + case[0] * (dim_x - 1))
        maxy = max(cur_y, cur_y + case[1] * (dim_y - 1))

        #minx = 7, maxx = 12, miny = 0, maxy = 2

        flag = 0
        dmin = 2*N + 1
        for i in range(minx, maxx + 1):
            for j in range(miny, maxy + 1):
                if Barr[i, j] == self.oppNum:
                    dx = abs(cur_x -i)
                    dy = abs(cur_y -j)
                    d = dx + dy
                    if d < dmin:
                        d = dmin
                    flag = 1
                    break
            if flag == 1:
                break

        if flag == 1:
            return self.findBestRectangle(Barr,N,cur_x,cur_y,DIMX-1,DIMY-1,case)
        if dim_x == 0:
            dim_x = 1
        if dim_y == 0:
            dim_y = 1
        
        if dim_x <= 1 and dim_y <= 1:
            return {"dim_x": 0,
                    "dim_y": 0,
                    "steps": 0,
                    "cells_conquered": 0,
                    "ratio": 0,
                    "lineselected":"horizontal"}

        # Calculating steps and conquered cells

        conqueredCells = 0
        for i in range(minx, maxx + 1):
            for j in range(miny,maxy+1):
                if Barr[i,j] == 0:
                    conqueredCells += 1

        lineselected = "vertical"

        count = 0
        steps = 0

        for i in range(cur_x+case[0], cur_x + case[0]*(dim_x),case[0]):
            count += 1
            if Barr[i,cur_y] == 0:
                steps = count
        for i in range(cur_y + case[1], cur_y + case[1]*dim_y,case[1]):
            count += 1
            if Barr[cur_x + case[0]*(dim_x - 1),i] == 0:
                steps = count
        for i in range(cur_x + case[0]*(dim_x-1) - case[0], cur_x - case[0], -case[0]):
            count += 1
            if Barr[i, cur_y + case[1]*(dim_y-1)] == 0:
                steps = count
        for i in range(cur_y + case[1]*(dim_y-1) - case[1],cur_y , - case[1]):
            count+=1
            if Barr[cur_x,i] == 0:
                steps = count
        stepsHorizontal = steps

        count = 0
        steps = 0


        for i in range(cur_y + case[1], cur_y + case[1]*(dim_y),case[1]):
            count += 1
            if Barr[cur_x,i] == 0:
                steps = count
        for i in range(cur_x + case[0], cur_x + case[0]*dim_x,case[0]):
            count += 1
            if Barr[i,cur_y + case[1]*(dim_y - 1)] == 0:
                steps = count
        for i in range(cur_y + case[1]*(dim_y-1) - case[1], cur_y - case[1], -case[1]):
            count += 1
            if Barr[cur_x + case[0]*(dim_x-1),i] == 0:
                steps = count
        for i in range(cur_x + case[0]*(dim_x-1) - case[0],cur_x , - case[0]):
            count+=1
            if Barr[i,cur_y] == 0:
                steps = count

        stepsVertical = steps

        if stepsHorizontal > stepsVertical:
            lineselected = "vertical"
            steps = stepsVertical
        else:
            lineselected = "horizontal"
            steps = stepsHorizontal



        if steps == 0:
            ratio = 0
        else:
            ratio = conqueredCells / steps

        return {"dim_x": dim_x,
                "dim_y": dim_y,
                "steps": steps,
                "cells_conquered": conqueredCells,
                "ratio": ratio,
                "lineselected":lineselected}

    def RectMove(self, Barr, N, dim_x, dim_y, cur_x, cur_y):
        self.Rect["dim_x"] = dim_x
        self.Rect["dim_y"] = dim_y

        if [cur_x, cur_y] in self.Rect["RectPos"]:
            self.Rect["RectLine"][0] = self.Rect["RectLine"][0] + 1
            self.Rect["RectLine"][1] = (self.Rect["RectLine"][1] + 1) % 4
            self.targetPos = self.Rect["RectPos"][self.Rect["RectLine"][1]]

        return self.moveTowardsRectangularTarget(cur_x, cur_y)

    def moveTowardsRectangularTarget(self, cur_x, cur_y):
        if cur_x == self.targetPos[0]:
            if abs(cur_y - self.targetPos[1]) <= 5:
                if self.targetPos[1] > cur_y:
                    return (0, 1)
                else:
                    return (0, -1)
            else:
                if self.targetPos[1] > cur_y:
                    return (0, -1)
                else:
                    return (0, 1)
        if cur_y == self.targetPos[1]:
            if abs(cur_x - self.targetPos[0]) <= 5:
                if self.targetPos[0] > cur_x:
                    return (1, 0)
                else:
                    return (-1, 0)
            else:
                if self.targetPos[1] > cur_x:
                    return (-1, 0)
                else:
                    return (1, 0)

        return (0, 0)

    def isRectanglePlanFine(self,Barr,N,cur_x,cur_y):
       
        minx = min(self.Rect["RectPos"][1][0], self.Rect["RectPos"][1][0] - self.Rect["case"][0] * (self.Rect["dim_x"]-1))
        maxx = max(self.Rect["RectPos"][1][0], self.Rect["RectPos"][1][0] - self.Rect["case"][0] * (self.Rect["dim_x"]-1))
        miny = min(self.Rect["RectPos"][1][1], self.Rect["RectPos"][1][1] - self.Rect["case"][1] * (self.Rect["dim_y"]-1))
        maxy = max(self.Rect["RectPos"][1][1], self.Rect["RectPos"][1][1] - self.Rect["case"][1] * (self.Rect["dim_y"]-1))
        unconqueredFlag = 0
        opponentConqueredFlag = 0
        for i in range(minx, maxx+1):
            for j in range(miny, maxy + 1):
                if Barr[i,j] == 0:
                    unconqueredFlag = 1

                if Barr[i,j] == self.oppNum:
                    opponentConqueredFlag = 1
                    break

        allTargetConquered = 1
        for i in range(minx, maxx + 1):
            if Barr[i, miny] != self.PlayerNumber:
                allTargetConquered = 0
            if Barr[i, maxy] != self.PlayerNumber:
                allTargetConquered = 0
        for j in range(miny, maxy + 1):
            if Barr[minx, j] != self.PlayerNumber:
                allTargetConquered = 0
            if Barr[maxx, j] != self.PlayerNumber:
                allTargetConquered = 0

        if allTargetConquered == 1:
            return 0
        if unconqueredFlag == 0 or opponentConqueredFlag == 1:
            return 0
        else:
            return 1


    # Best Place Plans
    def BestPlace(self,Barr,N,cur_x,cur_y):
        
        bestYuvrajCell = [410000,[0,0]]
        NearestFive = []

        NearestFive = self.closestCells(Barr,N,cur_x,cur_y,5)

        # Nearest Five is a list of tuples . Each tuple is distance , (x,y)
        # Now i have a list of 5 closest cells.

        NearestTwentyFive = []

        for i in range(len(NearestFive)):
            NearestTwentyFive.append(self.closestCells(Barr,N,NearestFive[i][1][0],NearestFive[i][1][1],25))
        lenNearestFive = len(NearestFive)

        # for 5 nearest cells we will calculate sum of nearestTwentyFive Cells
        for j in range(lenNearestFive):

            sumNearestTwentyFive = 0
            for i in range(len(NearestTwentyFive[j])):
                sumNearestTwentyFive += NearestTwentyFive[j][i][0]
            sumNearestTwentyFive += NearestFive[j][0]
            if sumNearestTwentyFive/(1+len(NearestTwentyFive[j])) < bestYuvrajCell[0]:
                bestYuvrajCell = [sumNearestTwentyFive/(1+len(NearestTwentyFive[j])),NearestFive[j][1]]

        bestCell = tuple(bestYuvrajCell[1])

        move = self.moveTowardsTarget(cur_x,cur_y,bestCell,N)

        self.currentPlan = 1

        return move

    def closestCells(self,Barr,N,cur_x,cur_y,n,): # n is number of closest cells you want to look for
        distanceCells = {}
        for i in range(N):
            for j in range(N):
                if i == cur_x and j == cur_y:
                    continue
                if Barr[i,j] != 0:
                    continue
                distance = self.distanceBetweenTwoCells(Barr, N, cur_x, cur_y, (i, j))
                distanceCells[distance] = (i, j)


        sortedDistanceCells = sorted(distanceCells.items())
        nBestSortedDistanceCells = []
        l = 0
        for k in range(len(sortedDistanceCells)):
            if l < n:
                nBestSortedDistanceCells.append(sortedDistanceCells[k])
                l += 1
            else:
                break
        return nBestSortedDistanceCells

    def moveTowardsTarget(self,cur_x,cur_y,target,N):
        if cur_x == target[0]:
            if abs(cur_y - target[1]) < N/2:
                if target[1] > cur_y:
                    return (0,1)
                if target[1] < cur_y:
                    return (0,-1)
            else:
                if target[1] > cur_y:
                    return (0,-1)
                if target[1] < cur_y:
                    return (0,1)
        else:
            if abs(cur_x - target[0]) < N/2:
                if target[0] > cur_x:
                    return (1,0)
                if target[0] < cur_x:
                    return (-1,0)
            else:
                if target[0] > cur_x:
                    return (-1,0)
                if target[0] < cur_x:
                    return (1,0)

        return (0,0)

    def distanceBetweenTwoCells(self,Barr,N,cur_x,cur_y,target):
        dx = min(abs(target[0] - cur_x), 30 - abs(target[0] - cur_x))
        dy = min(abs(target[1] - cur_y), 30 - abs(target[1] - cur_y))
        return dx + dy
