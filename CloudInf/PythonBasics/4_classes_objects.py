class Player:  # name is unique
    def __init__(self, length):  # constructor
        self.x = 0
        self.y = 0
        self.step_length = length

    def right(self):
        self.x += self.step_length

    def left(self):
        self.x -= self.step_length

    def up(self):
        self.y += self.step_length

    def down(self):
        self.y -= self.step_length

    def position(self):
        return self.x, self.y

    def name(self):
        return ('I am a player')


class Frog(Player):
    def __init__(self):
        Player.__init__(self, 3)

    def name(self):
        return('I am a frog')

class Bug(Player):
    def __init__(self):
        Player.__init__(self, 1)

    def name(self):
        return('I am a bug')

bug = Bug()
bug.down()
bug.right()
print(bug.position())
print(bug.name())

frog = Frog()
print(frog.name())