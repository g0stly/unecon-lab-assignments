#def tick(current_time='00:00', incr=1):
#    hours = current_time[:2]
#    minutes = (int(current_time[3:]) + 1) % 60
#    return hours + ':' + str(minutes)


#if __name__ == '__main__':
 #   print(tick('02:59'))
def inc(current_time='00:00', incr=1):
    
    hours = current_time[:2]
    minutes = current_time[3:]

    if incr == 1:
        minutes = str((int(current_time[3:]) + 1) % 60)
        if minutes == '0':
            hours = str(int(hours) + 1)
        if len(hours) == 1:
            hours = '0' + hours
        if len(minutes) == 1:
            minutes = '0' + minutes
    elif incr == 60:
        hours = str(int(hours) + 1)

    return hours + ':' + minutes

print(inc('21:43', 60))
