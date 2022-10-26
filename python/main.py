import sys
from boardgame import Boardgame

def run(path):
    boardgame = Boardgame(path)
    possible,message = boardgame.find_soulution()
    sys.stdout.write(message)
    if possible:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    path = sys.argv[1]
    run(path)