from sympy.utilities.iterables import multiset_permutations
import subprocess

#Now, require that the king be betweent the two rooks and the bishops be on different colored squares:
def chessFilter(chessList):
    kingIsBetweenRooks = False
    isbetweenRooks = False
    bishopSum = 0
    for pos, i in enumerate(chessList):
        if i == 'R':
            isbetweenRooks = not isbetweenRooks
        if isbetweenRooks:
            if i == 'K':
                kingIsBetweenRooks = True
        
        if i == 'B':
            bishopSum += pos
    
    bishopsOnOppositeSquares = (bishopSum % 2 == 0)
    return kingIsBetweenRooks and bishopsOnOppositeSquares #no early exit, though that is definitely possible

#Now we inject these values into the tex file.
#The tex file has two iterators.
#The first is the piece locations. 

#The following is the complete latex for piece generation:

#\def\wholeCard{0/{0/\WhiteRookOnBlack,1/\WhiteKnightOnWhite,2/\WhiteBishopOnBlack,3/\WhiteQueenOnWhite,4/\WhiteKingOnBlack,5/\WhiteBishopOnWhite,6/\WhiteKnightOnBlack,7/\WhiteRookOnWhite}/0/7/4,1/{0/\WhiteRookOnBlack,1/\WhiteKnightOnWhite,2/\WhiteBishopOnBlack,3/\WhiteQueenOnWhite,4/\WhiteKingOnBlack,5/\WhiteBishopOnWhite,6/\WhiteKnightOnBlack,7/\WhiteRookOnWhite}/0/7/4,2/{0/\WhiteRookOnBlack,1/\WhiteKnightOnWhite,2/\WhiteBishopOnBlack,3/\WhiteQueenOnWhite,4/\WhiteKingOnBlack,5/\WhiteBishopOnWhite,6/\WhiteKnightOnBlack,7/\WhiteRookOnWhite}/0/7/4,3/{0/\WhiteRookOnBlack,1/\WhiteKnightOnWhite,2/\WhiteBishopOnBlack,3/\WhiteQueenOnWhite,4/\WhiteKingOnBlack,5/\WhiteBishopOnWhite,6/\WhiteKnightOnBlack,7/\WhiteRookOnWhite}/0/7/4}

def deteremineLatexString(pos, piece):
    #Here, given K Q R B N we map it to the latex string
    pieceMap = {'K' : '\\WhiteKingOn',
                'Q' : '\\WhiteQueenOn',
                'R' : '\\WhiteRookOn',
                'B' : '\\WhiteBishopOn',
                'N' : '\\WhiteKnightOn'}
    
    return pieceMap[piece] + ('Black' if (pos % 2 == 0) else 'White') #5050 shot of right

def generateIndividualTemplate(index, chessList):
    #And now I create the chess setup, with a position data
    kingPos = -1
    lRookPos = -1
    rRookPos = -1
    chessStr = '{'
    for pos,i in enumerate(chessList):
        if i == 'K':
            kingPos = pos
        if i == 'R':
            if lRookPos == -1:
                lRookPos = pos
            else:
                rRookPos = pos
        
        #double duty. Also generate the chess list:
        chessStr += str(pos)  + '/' + deteremineLatexString(pos, i)
        if pos < 7:
            chessStr += ','
    chessStr += '}'
    
    return str(index) + '/' + str(chessStr) + '/' + str(lRookPos) + '/' + str(rRookPos) + '/' + str(kingPos)


def generateCompleteTemplateAndSubIntoTex(index, chessPieces):
    return '\\def\\wholeCard{' + ",".join([generateIndividualTemplate(i, chessPieces[index + i]) for i in range(0, 4)]) + '}\n'


#The main part of the program. Here we take in the .tex file and generate 240 files based on it.

chessPieces = multiset_permutations('RRNNBBKQ')
chessPieces = list(filter(chessFilter, chessPieces))

referenceTex = open('chess_card.tex', 'r')
lines = referenceTex.readlines()

lineRef = -1
for pos, i in enumerate(lines):
    if '\\def\\wholeCard' in i:
        lineRef = pos
        break

#Now, we concatenate everything before and after:

beforeTexString = "".join(lines[:lineRef])
afterTexString = "".join(lines[lineRef + 1:])



for i in range(240):
    subStringIn = generateCompleteTemplateAndSubIntoTex(i, chessPieces)
    fileStr = 'chess_card' + str(i*4) + '.tex'
    with open('deckTex/' + fileStr, 'w+') as file:
        file.write(beforeTexString + subStringIn + afterTexString)