import base64
import codecs

who = 'developer'
what = (10 * 130) + 30 + 27 % 20

dare = base64.b64decode('aHR0cHM6Ly8=').decode('utf-8')
dare += "%s" % (who) + chr(46) + "cisco"
dare = ''.join([dare, codecs.decode(".pbz", "rot-13")])
dare += "/be-%s" %str(what)

print(dare)