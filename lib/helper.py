class Helper:

  @classmethod
  def fenToBoard(cls, fen):
    board = []
    for row in fen.split('/'):
      brow = []
      for c in row:
        if c == ' ':
          break
        elif c in '12345678':
          brow.extend( ['.'] * int(c) )
        elif c == 'p':
          brow.append( 'p' )
        elif c == 'P':
          brow.append( 'P' )
        elif c > 'Z':
          brow.append(c)
        else:
          brow.append(c.upper())

      board.append( brow )
    return board

  @classmethod
  def printableBoard(cls, fen):
    board = cls.fenToBoard(fen)
    result = ""

    for row in board:
      result += " ".join(row)
      result += "\n"

    return result.rstrip('\n')
  
  def userInput(layouts):
    for i,puzzle in enumerate(layouts):
      print('%d: '%(i)+puzzle)
    print('%d: custom input'%len(layouts))
    res = -1
    while res not in list(range(len(layouts)+1)):
        try:
            res = int(input('pick a puzzle: [%d-%d]\n'%(0,len(layouts))))
        except:
            continue
    if res == len(layouts):
        valid = False
        while not valid:
            coordinates = input('input FEN of layout. use O for pieces to be recommended:\n')
            valid = True
            if coordinates.count('/') != 7:
                print('not enough rows in FEN')
                valid = False
                continue
            for i,row in enumerate(coordinates.split('/')):
                total = 0
                for c in row:
                    try:
                        total += int(c)
                    except:
                        total += 1
                if total != 8:
                    print('not enough pieces/spaces in row %d'%(i+1))
                    valid = False
    else:
        coordinates = layouts[res]
    return coordinates