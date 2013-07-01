import subprocess
from datetime import datetime

def checkTime():
    currentTime=str(datetime.now())
    currentTime=translateTime(currentTime)
    return currentTime

def translateTime(time):    
    time_info=[]
    if int(time[11:13])<12 and int(time[11:13])>0:
        time_info.append(time[11:13])
        time_info.append('a m')
    if int(time[11:13])==12:
        time_info.append(time[11:13])
        time_info.append('p m')
    if int(time[11:13])>12:
        atime=int(time[11:13])-12
        time_info.append(str(atime))
        time_info.append('p m')
    if int(time[11:13])==00:
        atime=int(time[11:13])+12
        time_info.append(str(atime))
        time_info.append('a m')
    if time[14:15]=='0':
        time_info.append('o '+time[15:16])
    else:
        time_info.append(time[14:16])
    return time_info[0]+time_info[2]+time_info[1]
    time_info.append(time[14:16])

def shutdown(time):
    subprocess.call(["shutdown.exe", "-f", "-s", "-t", str(time)])

def returnFalse():
    return False
    
