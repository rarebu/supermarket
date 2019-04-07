import time, heapq, threading, queue
from collections import deque
from datetime import datetime


class Station_Customer_view:

    def __init__(self, stationType, itemCount, maxQueueSize):
        self.stationType = stationType
        self.itemCount = itemCount
        self.maxQueueSize = maxQueueSize


class Customer:

    def __init__(self, type_id):

        if type_id == 1:    # Type A
            self.baecker = Station_Customer_view("Bäcker", 10, 10)
            self.wurst_items = 5
            self.wurst_max_queue_to_service = 10
            self.kaese_items = 3
            self.kaese_max_queue_to_service = 5
            self.kasse_items = 30
            self.kasse_max_queue_to_service = 20
            self.type_id = 'A'
            self.id = 0

        elif type_id == 2:    # Type B
            self.baecker = Station_Customer_view("Bäcker", 3, 20)
            self.wurst_items = 2
            self.wurst_max_queue_to_service = 5
            self.kasse_items = 3
            self.kasse_max_queue_to_service = 20
            self.type_id ='B'
            self.id = 0


class Shop:
    def serving_customer(queue, serveTime, lastServed):
        now = datetime.now()
        diff = now - lastServed
        print("serving() diff.seconds " + str(diff.seconds) + " serveTime " + str(serveTime))
        if (diff.seconds >= serveTime):
            print("serving() yes, diff passed")
            print("serving() queue: ", queue.qsize())
            if not queue.empty():
                customer = queue.get()
                print("serving() customer " + str(customer.type_id)+str(customer.id))
                with open("supermarkt_station.txt", "a") as myfile:
                    myfile.write("Bäcker serving customer " + str(customer.type_id)+str(customer.id) + "\n")
                # time.sleep(customer.baecker.itemCount * serveTime)
                with open("supermarkt_station.txt", "a") as myfile:
                    myfile.write("Bäcker finished customer " + str(customer.type_id) + str(customer.id) + "\n")
            return True
        else:
            print("serving() no, diff not passed")
            return False

    def customer_joining_queue(self, customer):
        super.addCustomer(queue, customer)

    def poll_server(self, station):
        while not station.serving():
            time.sleep(0.01)


class Baecker:
    serveTime = 1

    def __init__(self):
        print("State init")
        self.queue = queue.Queue()
        self.lastServed = datetime(2000, 1, 1)

    def serving(self):
        if Shop.serving_customer(self.queue, self.serveTime, self.lastServed):
            self.lastServed = datetime.now()
            return True
        else:
            return False

    def getQueueSize(self, queue):
        return queue.len()

    def addCustomer(self, customer):
        print("State added")
        with open("supermarkt_station.txt", "a") as myfile:
            myfile.write("Bäcker adding customer " + str(customer.type_id) + str(customer.id) + "\n")
        self.queue.put(customer)


t1c1 = Customer(1)
t1c1.id = 1

t1c2 = Customer(1)
t1c2.id = 2

t2c1 = Customer(2)
t2c1.id = 2

baecker = Baecker()

# baecker.serving()
baecker.addCustomer(t1c1)
while True:
    print("serving() returns: " + str(baecker.serving()))
    time.sleep(1)
# with open("supermarkt_station.txt", "a") as myfile:
#     myfile.write("Bäcker finished customer " + str(customer.type_id) + str(customer.id) + "\n")

time.sleep(5)

baecker.addCustomer(t1c2)
baecker.serving()



# t = threading.Thread(target=Baecker.start_serving)
# t.daemon = True
# t.start()
# Shop.serving_customer(self.serveTime, self.queue)

# Shop.poll_server(baecker) #nur bei threads


# time.sleep(100)
