def addHerb(state, col, row, agility):
    entType = 'herb'
    others = state['others']
    others.update({(col, row): {'type': entType, 'agility': agility}})
    state['others'] = others


def addBread(state, col, row, strength):
    entType = 'bread'
    others = state['others']
    others.update({(col, row): {'type': entType, 'strength': strength}})
    state['others'] = others


def addBlock(state, col, row, height):
    entType = 'block'
    others = state['others']
    others.update({(col, row): {'type': entType, 'height': height}})
    state['others'] = others


def initialiseState(col, row, orientation, agility, strength):
    entType = 'player'
    initState = {'playerSquare': (col, row),
                 'player': {'type': entType, 'orientation': orientation, 'agility': agility, 'strength': strength},
                 'others': {}}
    return initState


def getEntityAt(state, col, row):
    playerCoord = state['playerSquare']
    otherDictionary = state['others']
    otherCoord = list(otherDictionary.keys())

    if playerCoord[0] == col and playerCoord[1] == row:
        return state['player']
    else:
        for i in range(len(otherCoord)):
            if otherCoord[i][0] == col and otherCoord[i][1] == row:
                return otherDictionary[(col, row)]
        return {}


def showBoard(state, cols, rows):
    colsNew = 2 * cols + 1
    rowsNew = 2 * rows + 1

    for i in range(rowsNew):
        for k in range(colsNew):
            ent = getEntityAt(state, k - cols + state['playerSquare'][0], i - rows + state['playerSquare'][1])
            if ent == {}:
                print(' . ', end='')
            elif ent['type'] == 'bread':
                print(' @ ', end='')
            elif ent['type'] == 'herb':
                print(' # ', end='')
            elif ent['type'] == 'block':
                print(' ', ent['height'], end='')
            elif ent['type'] == 'player':
                printPlayerOrientation(ent)
        print()


def printPlayerOrientation(ent):
    if ent['orientation'] == 'right':
        print(' \u2192 ', end='')
    elif ent['orientation'] == 'left':
        print(' \u2190 ', end='')
    elif ent['orientation'] == 'up':
        print(' \u2191 ', end='')
    elif ent['orientation'] == 'down':
        print(' \u2193 ', end='')


def getPlayer(state):
    return state['player']


def getPlayerSquare(state):
    return state['playerSquare']


def turn(state, orientation):
    if orientation == 'left' or orientation == 'right' or orientation == 'up' or orientation == 'down':
        state['player']['orientation'] = orientation
        return 1
    else:
        return -1


def step(state):
    if checkOrientation(state) != -1:
        vertical = checkOrientation(state)[0]
        horizontal = checkOrientation(state)[1]
        makeStep(state, vertical, horizontal)
    else:
        return -1


def checkOrientation(state):
    if state['player']['orientation'] == 'left':
        return -1, 0
    elif state['player']['orientation'] == 'right':
        return 1, 0
    elif state['player']['orientation'] == 'up':
        return 0, -1
    elif state['player']['orientation'] == 'down':
        return 0, 1
    else:
        return -1


def makeStep(state, vertical, horizontal):
    place = getEntityAt(state, state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
    if place == {}:
        state['playerSquare'] = (state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
        return 1
    return -1


def showPlayer(state):
    print('column: ', state['playerSquare'][0])
    print('row: ', state['playerSquare'][1])
    print('orientation: ', state['player']['orientation'])
    print('agility: ', state['player']['agility'])
    print('strength: ', state['player']['strength'])


def showFacing(state):
    vertical = checkOrientation(state)[0]
    horizontal = checkOrientation(state)[1]
    place = getEntityAt(state, state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
    if place == {}:
        print('No entity in facing square')
    else:
        print('column: ', state['playerSquare'][0] + vertical)
        print('row: ', state['playerSquare'][1] + horizontal)
        print('type: ', place['type'])
        if place['type'] == 'block':
            print('height: ', place['height'])
        elif place['type'] == 'herb':
            print('agility: ', place['agility'])
        elif place['type'] == 'bread':
            print('strength: ', place['strength'])
    return place


def eat(state):
    vertical = checkOrientation(state)[0]
    horizontal = checkOrientation(state)[1]
    place = getEntityAt(state, state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
    if place != {}:
        if place['type'] == 'herb':
            state['player']['agility'] = state['player']['agility'] + place['agility']
            state['others'][(state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)] = {}
            return 1
        elif place['type'] == 'bread':
            state['player']['strength'] = state['player']['strength'] + place['strength']
            state['others'][(state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)] = {}
            return 1
        else:
            return -1
    else:
        return -1


def batter(state):
    vertical = checkOrientation(state)[0]
    horizontal = checkOrientation(state)[1]
    place = getEntityAt(state, state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
    if place != {} and place['type'] == 'block':
        state['others'][(state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)]['height'] -= 2
        state['player']['strength'] -= 1
        if state['others'][(state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)]['height'] <= 0:
            state['others'][(state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)] = {}
        return 1
    else:
        return -1


def jump(state):
    vertical = checkOrientation(state)[0]
    horizontal = checkOrientation(state)[1]
    place = getEntityAt(state, state['playerSquare'][0] + vertical, state['playerSquare'][1] + horizontal)
    placeBehind = getEntityAt(state, state['playerSquare'][0] + vertical * 2, state['playerSquare'][1] + horizontal * 2)
    if place != {} and placeBehind == {}:
        state['playerSquare'] = (state['playerSquare'][0] + vertical * 2, state['playerSquare'][1] + horizontal * 2)
        if place['type'] == 'block' and state['player']['agility'] > place['height']:
            state['player']['agility'] -= 1
        elif place['type'] == 'block' and state['player']['agility'] < place['height']:
            return -1
        return 1
    elif place == {}:
        return -2
    elif placeBehind != {}:
        return -3


def readState(file):
    global state
    document = open(file)
    for eachLine in document:
        lineSplited = eachLine.split(" ")
        if lineSplited[0] == 'player':
            state = initialiseState(int(lineSplited[1]), int(lineSplited[2]), lineSplited[5].strip(),
                                    int(lineSplited[3]), int(lineSplited[4]))
        elif lineSplited[0] == 'bread':
            addBread(state, int(lineSplited[1]), int(lineSplited[2]), int(lineSplited[3]))
        elif lineSplited[0] == 'herb':
            addHerb(state, int(lineSplited[1]), int(lineSplited[2]), int(lineSplited[3]))
        elif lineSplited[0] == 'block':
            addBlock(state, int(lineSplited[1]), int(lineSplited[2]), int(lineSplited[3]))
        else:
            return -1
    document.close()


def help():
    print('commands: \n turn left \n turn right \n turn up \n turn down \n jump \n batter \n eat \n step \n show '
          'player \n show facing \n quit')


def playConsole(file):
    readState(file)
    height = 6
    length = 6
    quit = 0
    showBoard(state, height, length)

    while quit == 0:
        userInput = input('Enter a command or ask for a "help": ')
        match userInput:
            case 'help':
                help()
            case 'turn left':
                turn(state, 'left')
            case 'turn right':
                turn(state, 'right')
            case 'turn up':
                turn(state, 'up')
            case 'turn down':
                turn(state, 'down')
            case 'jump':
                jump(state)
            case 'batter':
                batter(state)
            case 'eat':
                eat(state)
            case 'step':
                step(state)
            case 'show player':
                showPlayer(state)
            case 'show facing':
                showFacing(state)
            case 'quit':
                print('Thank you for playing')
                break
        showBoard(state, height, length)


if __name__ == "__main__":
    playConsole('file.txt')
