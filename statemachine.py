from transitions import Machine


class MatchSearcher(object):

    matches = []

    currentPos = None
    dx = None
    dy = None

    def __init__(self, filename, topdown = True):

        self.topdown = topdown

        self.filename = filename

        self.matchStart = None
        self.matchEnd = None
        self.matches = []

        if self.topdown:

            states = ['Searching', 'YellowDetected', 'BlueDetected', 'RedDetected',
                      'BlueRedDetected', 'RedYellowDetected', 'YellowRedDetected', 'BlueYellowDetected', 'YellowBlueDetected',
                      'WhiteDetected']

            self.machine = Machine(model=self, states=states, initial='Searching')

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
            self.machine.add_transition(source='RedYellowDetected',  trigger='foundWhite',  dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='RedYellowDetected',  trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='RedYellowDetected',  trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='YellowRedDetected',  trigger='foundRed',    dest='YellowRedDetected')
            self.machine.add_transition(source='YellowRedDetected',  trigger='foundYellow', dest='Searching')
            self.machine.add_transition(source='YellowRedDetected',  trigger='foundBlue',   dest='Searching')
            self.machine.add_transition(source='YellowRedDetected',  trigger='foundWhite',  dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='YellowRedDetected',  trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='YellowRedDetected',  trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='YellowBlueDetected', trigger='foundRed',    dest='Searching')
            self.machine.add_transition(source='YellowBlueDetected', trigger='foundYellow', dest='Searching')
            self.machine.add_transition(source='YellowBlueDetected', trigger='foundBlue',   dest='YellowBlueDetected')
            self.machine.add_transition(source='YellowBlueDetected', trigger='foundWhite',  dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='YellowBlueDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='YellowBlueDetected', trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='BlueYellowDetected', trigger='foundRed',    dest='Searching')
            self.machine.add_transition(source='BlueYellowDetected', trigger='foundYellow', dest='BlueYellowDetected')
            self.machine.add_transition(source='BlueYellowDetected', trigger='foundBlue',   dest='Searching')
            self.machine.add_transition(source='BlueYellowDetected', trigger='foundWhite',  dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='BlueYellowDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='BlueYellowDetected', trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='BlueRedDetected',    trigger='foundRed',    dest='BlueRedDetected')
            self.machine.add_transition(source='BlueRedDetected',    trigger='foundYellow', dest='Searching')
            self.machine.add_transition(source='BlueRedDetected',    trigger='foundBlue',   dest='Searching')
            self.machine.add_transition(source='BlueRedDetected',    trigger='foundWhite',  dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='BlueRedDetected',    trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='BlueRedDetected',    trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='WhiteDetected', trigger='foundRed',     dest='Searching',  before='addMatch')
            self.machine.add_transition(source='WhiteDetected', trigger='foundYellow',  dest='Searching',  before='addMatch')
            self.machine.add_transition(source='WhiteDetected', trigger='foundBlue',    dest='Searching',  before='addMatch')
            self.machine.add_transition(source='WhiteDetected', trigger='foundWhite',   dest='WhiteDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteDetected', trigger='foundOther',   dest='Searching',  before='addMatch')
            self.machine.add_transition(source='WhiteDetected', trigger='foundColumnEnd', dest='Searching', before='addMatch')
        else:

            states = ['Searching',
                      'WhiteDetected',
                      'WhiteRedDetected', 'WhiteYellowDetected', 'WhiteBlueDetected',
                      'WhiteRedBlueDetected', 'WhiteRedYellowDetected', 'WhiteYellowRedDetected', 'WhiteYellowBlueDetected', 'WhiteBlueYellowDetected']

            self.machine = Machine(model=self, states=states, initial='Searching')

            self.machine.add_transition(source='Searching', trigger='foundRed',      dest='Searching')
            self.machine.add_transition(source='Searching', trigger='foundYellow',   dest='Searching')
            self.machine.add_transition(source='Searching', trigger='foundBlue',     dest='Searching')
            self.machine.add_transition(source='Searching', trigger='foundWhite',    dest='WhiteDetected', before='rememberStart')
            self.machine.add_transition(source='Searching', trigger='foundOther',    dest='Searching')
            self.machine.add_transition(source='Searching', trigger='foundColumnEnd', dest='Searching')

            #
            self.machine.add_transition(source='WhiteDetected', trigger='foundRed',    dest='WhiteRedDetected')
            self.machine.add_transition(source='WhiteDetected', trigger='foundYellow', dest='WhiteYellowDetected')
            self.machine.add_transition(source='WhiteDetected', trigger='foundBlue',   dest='WhiteBlueDetected')
            self.machine.add_transition(source='WhiteDetected', trigger='foundWhite',  dest='WhiteDetected')
            self.machine.add_transition(source='WhiteDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='WhiteDetected', trigger='foundColumnEnd', dest='Searching')

            #
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundRed',    dest='WhiteRedDetected')
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundYellow', dest='WhiteRedYellowDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundBlue',   dest='WhiteRedBlueDetected',  before='rememberEnd')
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundWhite',  dest='WhiteDetected',         before='rememberStart')
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='WhiteRedDetected', trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundRed',    dest='WhiteYellowRedDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundYellow', dest='WhiteYellowDetected')
            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundBlue',   dest='WhiteYellowBlueDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundWhite',  dest='WhiteDetected',      before='rememberStart')
            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='WhiteYellowDetected', trigger='foundColumnEnd', dest='Searching')

            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundRed',    dest='Searching')
            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundYellow', dest='WhiteBlueYellowDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundBlue',   dest='WhiteBlueDetected')
            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundWhite',  dest='WhiteDetected',        before='rememberStart')
            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundOther',  dest='Searching')
            self.machine.add_transition(source='WhiteBlueDetected', trigger='foundColumnEnd', dest='Searching')

            #
            self.machine.add_transition(source='WhiteRedBlueDetected', trigger='foundRed',    dest='Searching',         before='addMatch')
            self.machine.add_transition(source='WhiteRedBlueDetected', trigger='foundYellow', dest='Searching',         before='addMatch')
            self.machine.add_transition(source='WhiteRedBlueDetected', trigger='foundBlue',   dest='WhiteRedBlueDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteRedBlueDetected',  trigger='foundWhite',  dest='WhiteDetected',    before='addMatch')
            self.machine.add_transition(source='WhiteRedBlueDetected',  trigger='foundOther',  dest='Searching',        before='addMatch')
            self.machine.add_transition(source='WhiteRedBlueDetected',  trigger='foundColumnEnd', dest='Searching',     before='addMatch')

            self.machine.add_transition(source='WhiteRedYellowDetected', trigger='foundRed',    dest='Searching',       before='addMatch')
            self.machine.add_transition(source='WhiteRedYellowDetected', trigger='foundYellow', dest='WhiteRedYellowDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteRedYellowDetected', trigger='foundBlue',   dest='Searching',       before='addMatch')
            self.machine.add_transition(source='WhiteRedYellowDetected',  trigger='foundWhite',  dest='WhiteDetected',  before='addMatch')
            self.machine.add_transition(source='WhiteRedYellowDetected',  trigger='foundOther',  dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteRedYellowDetected',  trigger='foundColumnEnd', dest='Searching',   before='addMatch')

            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundRed',    dest='WhiteYellowRedDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundYellow', dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundBlue',   dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundWhite',  dest='WhiteDetected',  before='addMatch')
            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundOther',  dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowRedDetected',  trigger='foundColumnEnd', dest='Searching',   before='addMatch')

            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundRed',    dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundYellow', dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundBlue',   dest='WhiteYellowBlueDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundWhite',  dest='WhiteDetected',  before='addMatch')
            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundOther',  dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteYellowBlueDetected', trigger='foundColumnEnd', dest='Searching',   before='addMatch')

            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundRed',    dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundYellow', dest='WhiteBlueYellowDetected', before='rememberEnd')
            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundBlue',   dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundWhite',  dest='WhiteDetected',  before='addMatch')
            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundOther',  dest='Searching',      before='addMatch')
            self.machine.add_transition(source='WhiteBlueYellowDetected', trigger='foundColumnEnd', dest='Searching',   before='addMatch')

    #TODO the matches at the coulumn end are a problem
    def addMatch(self):
        #self.rememberEnd()
        # if we are at the end of the column, us the last pixel
        if self.topdown:
            if self.matchEnd is None:
                self.matchEnd = self.currentPos
        else:
            if self.topdown:#TODO does work without this???
                self.matchEnd = (self.currentPos[0]+self.dx, self.currentPos[1]+self.dy)
            else:
                self.matchEnd = (self.currentPos[0]+self.dx, self.currentPos[1]-self.dy)

        #print("Start:", self.matchStart)
        #print("End:", self.matchEnd)
        self.matches.append([self.matchStart, self.matchEnd])
        self.currentPos = None
        self.matchStart = None
        self.matchEnd = None

    def rememberEnd(self):
        #print("Possible end")
        if self.topdown:#TODO does work without this???
            self.matchEnd = (self.currentPos[0]+self.dx, self.currentPos[1]+self.dy)
        else:
            self.matchEnd = (self.currentPos[0]+self.dx, self.currentPos[1]-self.dy)


    def rememberStart(self):
        #print("Possible start")
        self.matchStart = self.currentPos