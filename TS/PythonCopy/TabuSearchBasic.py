import copy
import random
class TabuSearchBasic:
    # 最大迭代次数
    def __init__(self):
        self.MAX_TIME = 100
        pass

    def getNewPlan(self,route):
        newRoute = copy.copy(route)
        r_num = len(route)
        
        op1 = random.randint(0,r_num-1)
        op2 = random.randint(0,r_num-1)
        while op1 == op2:
            op2 = random.randint(0,r_num-1)

        newRoute[op1],newRoute[op2] = newRoute[op1],newRoute[op2]
        return newRoute

    def initData(self):

        pass

    def getNeighbourhoodList(self):
        return None

    def flushTabuTable(self):
        pass

    def run(self):
        self.initData()

        i_time = 0
        while i_time < self.MAX_TIME:
            newPlanList = self.getNeighbourhood()

            for newPlan in newPlanList:
                # record current Best
                pass
            # compare the best
            self.flushTabuTable()

            i_time += 1
            pass


