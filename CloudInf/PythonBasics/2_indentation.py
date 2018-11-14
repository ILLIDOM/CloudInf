import datetime

now = datetime.datetime.now()
print ('Today is the ' + str(now.day) + '.' + str(now.month) + '.' + str(now.year))

if now.hour < 5 or now.hour > 22:
    print('Good night')
elif now.hour < 12:
    print('God morning')
elif now.hour == 12:
    print('It\'s lunch time')
    print('I am hungry')
elif now.hour < 18:
    print('Good afternoon')
else:
    print('Good evening')

print('See you!')