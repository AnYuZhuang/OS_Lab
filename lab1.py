import multiprocessing
import random
import time
import numpy as np

def thread_func(start_point,end_point,matA,matB,result_queue):
    dictionary={}
    for row in range(start_point, end_point):
        dictionary[row] = np.matmul(matA[row], matB)
    result_queue.put(dictionary)

def main():
    start_time=time.time()
    # Generate queue for communication
    s=100
    processes = 10
    process_number=s//processes
    matA = np.random.randint(10, size = (s, s))
    matB = np.random.randint(10, size = (s, s))

    result = np.zeros((matA.shape[0], matB.shape[1]))   

    total = s/processes
    result_queue = multiprocessing.Manager().Queue()
    jobs = []
    new_list=[]
    for i in range(processes):
        process = multiprocessing.Process(target = thread_func, args = (int(i*total),int(i*total + total),matA,matB,result_queue))
        jobs.append(process)
    
    for process in jobs:
        process.start()

    for process in jobs:
        process.join()
    
    while not result_queue.empty():
        result = result_queue.get()
        for k in list(result):
            obj=result[k].tolist()
            new_list.append(obj)
        #print(result)
    end_time=time.time()
    print('Time:',end_time - start_time)
    print('Answer is correct:', np.all(np.matmul(matA, matB) == new_list))
    
if __name__ == "__main__":
    main()



