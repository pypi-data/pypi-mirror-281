from accions import *
from asyncio import run


value = run(MultiWalk("181.232.180.7","ConextVM",["1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.4194312960"],True))
print(value['0'])