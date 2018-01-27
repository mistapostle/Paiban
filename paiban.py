
from functools import reduce 

#INIT ITEMS 
JOB_ITEMS = ['onCall', 'aShift', 'nightCall']
JOB_ITEMS_FOR_YONGONLY = ['nightCall']
JOB_ITEMS_CANNOT_REPEAT = ['nightCall','aShift']


#INIT MEMBERS 

class Person:
    def __init__(self, name, isOld ):
        self.name = name 
        self.isOld = isOld
        self.state={}

teamMembers =  [   Person('j',True),
  Person('a',True),
  Person('b',False),
  Person('c',False), 
  Person('e',False),
  Person('d',False)
  ]

youngTeamMembers  = [  m for m in teamMembers if not m.isOld ] 
def _mm(m,x):
    m[x.name] = x 
    x.state = dict.fromkeys(JOB_ITEMS,0)
    return m   
teamMembersMap = reduce(_mm,teamMembers,{})
print('teamMembersMap:  {0!s} '.format (teamMembersMap) ) 



#INIT PLANS 
def readPlans(fn):
    plans = []
    with open(fn) as f :
        for l in f.readlines():
            j = l.split(',')
            if len(j ) != len(JOB_ITEMS):
                raise Exception("invalid plan line : %s " % str(j) )   
            plans.append( {  JOB_ITEMS[i]: j[i].strip()  for i in range(len(JOB_ITEMS) )  } )
    return plans 
def writePlans(fn,plans):
    with open(fn,'w') as f :
        for p in plans:
            f.write(",".join(  (p[j] for j in JOB_ITEMS ) ) + "\n" ) 

plans = readPlans('plan.txt')
#plans  = [
 #   {'onCall': 'j' , 'aShift':'b', 'nightCall':'e'},
 #   {'onCall': 'a' , 'aShift':'c', 'nightCall':'d'}  
#]
def updateStateByPlan(oneWeekPlan):
    for k,v in oneWeekPlan.items() : 
        p = teamMembersMap[v]
        p.state[k] += 1 
for p in plans:
    updateStateByPlan(p)



#   PLANNING FUNCS 
def findLowestRateMember(mbs, j):
    l = 9999
    i = 0  
    for m in mbs : 
        r = m.state[j] 
        if r < l :
            l =r 
            li = m
        i += 1 
    return li


def planNext(lastWeekPlan):
    cannotRepeatMembers =  (lastWeekPlan[j] for j in JOB_ITEMS_CANNOT_REPEAT ) 
    pickedMemberInThisWeek = []
    thisWeekPlan = {}
    for j in JOB_ITEMS:
        mbs = teamMembers 
        if j in JOB_ITEMS_FOR_YONGONLY:
            mbs = youngTeamMembers 
        if j in JOB_ITEMS_CANNOT_REPEAT:
            mbs =  (m for  m in mbs if m.name not in  cannotRepeatMembers  )
        mbs = (m for  m in mbs if  m.name not in  pickedMemberInThisWeek  )
        m = findLowestRateMember(mbs,j)
        m.state[j] += 1 
        thisWeekPlan[j] =  m.name
        pickedMemberInThisWeek.append(m.name)
    return thisWeekPlan


#EXECUTE PLANNING 
for x in range(10):
    p = planNext(plans[-1])
    plans.append(p)
print("\n".join( str(p) for p in plans))
writePlans('plans2.txt',plans)



