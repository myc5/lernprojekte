from math import floor
def convert(time):
    hours = floor(time/3600)
    minutes = floor((time-hours*3600)/60)
    seconds = floor(time-hours*3600-minutes*60)
    return print(str(hours)+"h " + str(minutes) + "min " + str(seconds) +"s")
    
time = int(input("Time in seconds: "))
convert(time)
