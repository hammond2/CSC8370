'''
Homework 6
Student name: Jiawei Sun
'''
import socket
import threading
import queue
import sys

# Set default timeout for socket
socket.setdefaulttimeout(0.05)
# Take input parameters form command line one by one
IP = sys.argv[1]
low = int(sys.argv[2])
upper = int(sys.argv[3])

q = queue.Queue()

'''
Method name: threads()
Input: Nothing.
Output: Nothing.
This method is used to process threads to connect port that in queue in order.
'''
def threads():
    while True:
        currentjob = q.get()
        connecting(currentjob)
        # Close this task when currentjob is finished
        q.task_done()


# With this lock we can avoid print errors of other threads
lock = threading.Lock()

'''
Method name: scan()
Input: a thread.
Output: Print information of port id if this port is open.
This method takes a thread as input, and then try to connect it to see if it's open. 
After successfully connection, it would disconnect the port.
'''
def connecting(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = s.connect((IP, port))
        # With this lock we can avoid print errors of these information
        with lock:
            print('port', port, 'is open')
        # Disconnect if there was a successful connection as the question said
        connection.close()
    except:
        pass


# Create at most 500 threads to use
for x in range(500):
    thread = threading.Thread(target=threads)
    thread.daemon = True
    thread.start()

# To make sure every port from lower bound to upper bound can be scanned
for currentjob in range(low, upper + 1):
    q.put(currentjob)
q.join()
