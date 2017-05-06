from transitions import Machine


class MatchSearcher(object):

    states = ['Searching', 'YellowDetected', 'BlueDetected', 'RedDetected',
              'BlueRedDetected', 'RedYellowDetected', 'YellowRedDetected', 'BlueYellowDetected', 'YellowBlueDetected',
              'PylonFound']

    matches = []

    currentPos = None
    dx = None
    dy = None

    def __init__(self, filename):

        self.filename = filename

        self.matchStart = None
        self.matchEnd = None
        self.matches = []

        self.machine = Machine(model=self, states=self.states, initial='Searching')

        # add parameter to <trigger> , "conditions='xyz'", xyz gets the parameter
        self.machine.add_transition(source='Searching', trigger='foundRed',      dest='RedDetected',     before='rememberStart')
        self.machine.add_transition(source='Searching', trigger='foundYellow',   dest='YellowDetected',  before='rememberStart')
        self.machine.add_transition(source='Searching', trigger='foundBlue',     dest='BlueDetected',    before='rememberStart')
        self.machine.add_transition(source='Searching', trigger='foundWhite',    dest='Searching')
        self.machine.add_transition(source='Searching', trigger='foundOther',    dest='Searching')
        self.machine.add_transition(source='Searching', trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='RedDetected',        trigger='foundRed',    dest='RedDetected')
        self.machine.add_transition(source='RedDetected',        trigger='foundYellow', dest='RedYellowDetected')
        self.machine.add_transition(source='RedDetected',        trigger='foundBlue',   dest='Searching')
        self.machine.add_transition(source='RedDetected',        trigger='foundWhite',  dest='Searching')
        self.machine.add_transition(source='RedDetected',        trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='RedDetected',        trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='YellowDetected',     trigger='foundRed',    dest='YellowRedDetected')
        self.machine.add_transition(source='YellowDetected',     trigger='foundYellow', dest='YellowDetected')
        self.machine.add_transition(source='YellowDetected',     trigger='foundBlue',   dest='YellowBlueDetected')
        self.machine.add_transition(source='YellowDetected',     trigger='foundWhite',  dest='Searching')
        self.machine.add_transition(source='YellowDetected',     trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='YellowDetected',     trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='BlueDetected',       trigger='foundRed',    dest='BlueRedDetected')
        self.machine.add_transition(source='BlueDetected',       trigger='foundYellow', dest='BlueYellowDetected')
        self.machine.add_transition(source='BlueDetected',       trigger='foundBlue',   dest='BlueDetected')
        self.machine.add_transition(source='BlueDetected',       trigger='foundWhite',  dest='Searching')
        self.machine.add_transition(source='BlueDetected',       trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='BlueDetected',       trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='RedYellowDetected',  trigger='foundRed',    dest='Searching')
        self.machine.add_transition(source='RedYellowDetected',  trigger='foundYellow', dest='RedYellowDetected')
        self.machine.add_transition(source='RedYellowDetected',  trigger='foundBlue',   dest='Searching')
        self.machine.add_transition(source='RedYellowDetected',  trigger='foundWhite',  dest='PylonFound')
        self.machine.add_transition(source='RedYellowDetected',  trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='RedYellowDetected',  trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='YellowRedDetected',  trigger='foundRed',    dest='YellowRedDetected')
        self.machine.add_transition(source='YellowRedDetected',  trigger='foundYellow', dest='Searching')
        self.machine.add_transition(source='YellowRedDetected',  trigger='foundBlue',   dest='Searching')
        self.machine.add_transition(source='YellowRedDetected',  trigger='foundWhite',  dest='PylonFound')
        self.machine.add_transition(source='YellowRedDetected',  trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='YellowRedDetected',  trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='YellowBlueDetected', trigger='foundRed',    dest='Searching')
        self.machine.add_transition(source='YellowBlueDetected', trigger='foundYellow', dest='Searching')
        self.machine.add_transition(source='YellowBlueDetected', trigger='foundBlue',   dest='YellowBlueDetected')
        self.machine.add_transition(source='YellowBlueDetected', trigger='foundWhite',  dest='PylonFound')
        self.machine.add_transition(source='YellowBlueDetected', trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='YellowBlueDetected', trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='BlueYellowDetected', trigger='foundRed',    dest='Searching')
        self.machine.add_transition(source='BlueYellowDetected', trigger='foundYellow', dest='BlueYellowDetected')
        self.machine.add_transition(source='BlueYellowDetected', trigger='foundBlue',   dest='Searching')
        self.machine.add_transition(source='BlueYellowDetected', trigger='foundWhite',  dest='PylonFound')
        self.machine.add_transition(source='BlueYellowDetected', trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='BlueYellowDetected', trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='BlueRedDetected',    trigger='foundRed',    dest='BlueRedDetected')
        self.machine.add_transition(source='BlueRedDetected',    trigger='foundYellow', dest='Searching')
        self.machine.add_transition(source='BlueRedDetected',    trigger='foundBlue',   dest='Searching')
        self.machine.add_transition(source='BlueRedDetected',    trigger='foundWhite',  dest='PylonFound')
        self.machine.add_transition(source='BlueRedDetected',    trigger='foundOther',  dest='Searching')
        self.machine.add_transition(source='BlueRedDetected',    trigger='foundColumnEnd', dest='Searching')

        self.machine.add_transition(source='PylonFound', trigger='foundRed',     dest='Searching',  before='addMatch')
        self.machine.add_transition(source='PylonFound', trigger='foundYellow',  dest='Searching',  before='addMatch')
        self.machine.add_transition(source='PylonFound', trigger='foundBlue',    dest='Searching',  before='addMatch')
        self.machine.add_transition(source='PylonFound', trigger='foundWhite',   dest='PylonFound', before='rememberEnd')
        self.machine.add_transition(source='PylonFound', trigger='foundOther',   dest='Searching',  before='addMatch')
        self.machine.add_transition(source='PylonFound', trigger='foundColumnEnd', dest='Searching', before='addMatch')

    def addMatch(self):
        #self.rememberEnd()
        # if we are at the end of the column, us the last pixel
        if self.matchEnd is None:
            self.matchEnd = self.currentPos

        #print("Start:", self.matchStart)
        #print("End:", self.matchEnd)
        self.matches.append([self.matchStart, self.matchEnd])
        self.currentPos = None
        self.matchStart = None
        self.matchEnd = None

    def rememberEnd(self):
        #print("Possible end")
        self.matchEnd = (self.currentPos[0]+self.dx, self.currentPos[1]+self.dy)

    def rememberStart(self):
        #print("Possible start")
        self.matchStart = self.currentPos