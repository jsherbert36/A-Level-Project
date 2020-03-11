import math,pygame,random,sys,os
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PATH = sys.path[0]
import numpy as np


if __name__ == "__main__":
    exec(open(os.path.join(PATH,"GamePlay.py")).read())
    exec(open(os.path.join(PATH,"GameOver.py")).read())