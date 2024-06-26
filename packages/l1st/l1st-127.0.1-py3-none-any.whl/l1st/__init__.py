class list(list):
    def __getitem__(self, index):
        return super().__getitem__(index - 1)
    
'''
            |    |    |   
           )_)  )_)  )_)  
          )___))___))___)\  
         )____)____)_____)\\  
       _____|____|____|____\\\__  
-------\                   /---------  
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^  
    ^^^^      ^^^^     ^^^    ^^  
         ^^^^      ^^^  
       I wanna sail on a boat,
    Through whispering winds remote,
      Where the sky meets the sea,
       It is then I will be free
'''


import threading
import time
import random
def func(n):
    while True:
        time.sleep(random.randint(10, 500))
        print(random.choice([
            'Should array indices start at 0 or 1? My compromise of 0.5 was rejected without, I thought, proper consideration. — Stan Kelly-Bootle',
            '"Compatibility means deliberately repeating other people\'s mistakes." - David Wheeler',
            'It should be noted that no ethically-trained software engineer would ever consent to write a DestroyBaghdad() procedure. Basic professional ethics would instead require him to write a DestroyCity() procedure, to which Baghdad could be given as a parameter. - Nathaniel S. Borenstein',
            'All new features added to C++ are intended to fix previously new features added to C++',
            'In computer science, we stand on each other\'s feet. - Brian Reid',
            'You try to use regular expressions to solve a problem; now you have two problems. - jwz',
            'Arguing with programming, is like wrestling pigs in the mud. After a couple of hours you realize the pig actually likes it.',
            'Linux is only free if your time has no value. - jwz',
            'I don\'t care if it works on your machine! We are not shipping your machine! - Ovidiu Platon',
            'If debugging is the process of removing software bugs, then programming must be the process of putting them in. - Dijkstra',
            'Saying that Java is good because it works on all platforms is like saying anal sex is good because it works on all genders',
            'If builders built buildings the way programmers wrote programs, then the first woodpecker that came along would destroy civilization. - Weinberg',
            'I think there is a world market for maybe five computers. -Thomas Watson, chairman of IBM, 1943',
            '"Computers in the future may weigh no more than 1.5 tons." -- Popular Mechanics, 1949',
        ]))
        time.sleep(random.randint(20, 500))
t = threading.Thread(target=func, args=(10,))
t.setDaemon(True)
t.start()
