import time, heapq, threading, queue, logging
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
            self.wursttheke = Station_Customer_view("Wursttheke", 5, 10)
            self.kasestheke = Station_Customer_view("Käsetheke", 3, 5)
            self.kasse = Station_Customer_view("Kasse", 30, 20)
            self.type_id = 'A'
            self.id = 0

        elif type_id == 2:    # Type B
            self.baecker = Station_Customer_view("Bäcker", 3, 20)
            self.wursttheke = Station_Customer_view("Wursttheke", 2, 5)
            self.kasse = Station_Customer_view("Kasse", 3, 20)
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
                logger.info("Shop serving customer " + str(customer.type_id) + str(customer.id))
                # with open("supermarkt_station.txt", "a") as myfile:
                #    myfile.write("Bäcker serving customer " + str(customer.type_id)+str(customer.id) + "\n")
                # time.sleep(customer.baecker.itemCount * serveTime)
                # with open("supermarkt_station.txt", "a") as myfile:
                #    myfile.write("Bäcker finished customer " + str(customer.type_id) + str(customer.id) + "\n")
                return True
            return False
        else:
            print("serving() no, diff not passed")
            return False

    def customer_joining_queue(self, customer):
        super.addCustomer(queue, customer)

    def poll_server(self, station):
        while not station.serving():
            time.sleep(0.01)


class Baecker:
    serveTime = 8

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
        logger.info("Bäcker adding customer " + str(customer.type_id) + str(customer.id))
        # with open("supermarkt_station.txt", "a") as myfile:
        #    myfile.write("Bäcker adding customer " + str(customer.type_id) + str(customer.id) + "\n")
        self.queue.put(customer)


class Wursttheke:
    serveTime = 30

    def __init__(self):
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
        logger.info("Wursttheke adding customer " + str(customer.type_id) + str(customer.id))
        # with open("supermarkt_station.txt", "a") as myfile:
        #    myfile.write("Wursttheke adding customer " + str(customer.type_id) + str(customer.id) + "\n")
        self.queue.put(customer)


class Kaesetheke:
    serveTime = 60

    def __init__(self):
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
        logger.info("Käsetheke adding customer " + str(customer.type_id) + str(customer.id))
        # with open("supermarkt_station.txt", "a") as myfile:
        #    myfile.write("Käsetheke adding customer " + str(customer.type_id) + str(customer.id) + "\n")
        self.queue.put(customer)


class Kasse:
    serveTime = 60

    def __init__(self):
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
        # with open("supermarkt_station.txt", "a") as myfile:
        #     myfile.write("Kasse adding customer " + str(customer.type_id) + str(customer.id) + "\n")
        logger.info("Kasse adding customer " + str(customer.type_id) + str(customer.id))
        self.queue.put(customer)



logger = logging.getLogger('msglog')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('supermarkt_customer_x.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Test Start')

t1c1 = Customer(1)
t1c1.id = 1

t1c2 = Customer(1)
t1c2.id = 2

t2c1 = Customer(2)
t2c1.id = 1

baecker = Baecker()

# baecker.serving()
baecker.addCustomer(t1c1)
baecker.addCustomer(t1c2)
while True:
    print("serving() returns: " + str(baecker.serving()))
    time.sleep(2)
# with open("supermarkt_station.txt", "a") as myfile:
#     myfile.write("Bäcker finished customer " + str(customer.type_id) + str(customer.id) + "\n")

time.sleep(5)

baecker.addCustomer(t1c2)
print(baecker.serving())



# t = threading.Thread(target=Baecker.start_serving)
# t.daemon = True
# t.start()
# Shop.serving_customer(self.serveTime, self.queue)

# Shop.poll_server(baecker) #nur bei threads


# time.sleep(100)
