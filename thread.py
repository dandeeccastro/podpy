from threading import Thread

def mainRoutine(in_point):
    for i in range(0,25):
        shared_memory[in_point + i] = 7

shared_memory = []
threads = []

class MyThreads(Thread):
    shared_data = []
    def initiateSharedData():
        for i in range(0,100):
            MyThreads.shared_data.append(0)

    def alterSharedData(in_point):
        for i in range(0,25):
            MyThreads.shared_data[in_point + i] = 7

MyThreads.initiateSharedData()

for i in range(0,4):
    thread = MyThreads(target=MyThreads.alterSharedData,args=(25*i,) )
    threads.append( thread )
    del thread

for i in range(0,4):
    threads[i].start()

for i in range(0,4):
    threads[i].join()

print (MyThreads.shared_data)
