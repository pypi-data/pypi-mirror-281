from accions import *
from asyncio import run


value = run(MultiWalk("","CM",[""],True,True))
print(value['0'][0])