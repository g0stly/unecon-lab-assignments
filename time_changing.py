# функция, которая прибавляет минуту вручную и что-то дальше делает со строкой времени.
# посмотри, Саня, мб у тебя получится сделать что-то менее громоздкое и тупое? 


def tick(current_time='00:00'):

    hours = current_time[:2]
    minutes = current_time[3:]

    if minutes == '59':
        if hours == '23':
            hours = '00'
        else:
            hours = str(int(hours) + 1)
            if len(hours) == 1:
                hours = '0' + hours
        minutes = '00'
    else:
        minutes = str(int(minutes) + 1)
        if len(minutes) == 1:
            minutes = '0' + minutes

    return hours + ':' + minutes


if __name__ == '__main__':
    print(tick('02:59'))
