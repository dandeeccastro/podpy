from threading import Thread

def mainRoutine(in_point):
    for i in range(0,25):
        shared_memory[in_point + i] = 7

shared_memory = []
threads = []

for i in range(0,100):
    shared_memory.append(0)

for i in range(0,4):
    threads.append( Thread(target=mainRoutine,args=(25*i,) ) )

for i in range(0,4):
    threads[i].start()

for i in range(0,4):
    threads[i].join()

print (shared_memory)
