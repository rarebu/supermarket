import time, heapq, threading, queue
from collections import deque


class Customer:

    def __init__(self, type_id):

        if type_id == 1:    # Type A
            self.baecker_items = 10
            self.baecker_max_queue_to_service = 10
            self.wurst_items = 5
            self.wurst_max_queue_to_service = 10
            self.kaese_items = 3
            self.kaese_max_queue_to_service = 5
            self.kasse_items = 30
            self.kasse_max_queue_to_service = 20
            self.type_id = 'A'
            self.id = 0

        elif type_id == 2:    # Type B
            self.baecker_items = 3
            self.baecker_max_queue_to_service = 20
            self.wurst_items = 2
            self.wurst_max_queue_to_service = 5
            self.kasse_items = 3
            self.kasse_max_queue_to_service = 20
            self.type_id ='B'
            self.id = 0


class Shop:

    def baecker(self, b_queue):
        while(True):
            if not b_queue.empty():
                customer = b_queue.get()
                with open("supermarkt_station.txt", "a") as myfile:
                    myfile.write("Bäcker serving customer " + str(customer.type_id)+str(customer.id) + "\n")
                time.sleep(customer.baecker_items * 1)
                with open("supermarkt_station.txt", "a") as myfile:
                    myfile.write("Bäcker finished customer " + str(customer.type_id) + str(customer.id) + "\n")


class Simulation:

    t1c1 = Customer(1)
    t1c1.id = 1

    t1c2 = Customer(1)
    t1c2.id = 2

    t2c1 = Customer(2)
    t2c1.id = 2

    b_queue = queue.Queue()

    b_queue.put(t1c1)
    with open("supermarkt_station.txt", "a") as myfile:
        myfile.write("Bäcker adding customer " + str(t1c1.type_id) + str(t1c1.id) + "\n")

    shop = Shop()

    # shop.baecker(b_queue)
    t = threading.Thread(target=shop.baecker, args=[b_queue])
    t.daemon = True
    t.start()
    time.sleep(5)
    b_queue.put(t1c2)
    with open("supermarkt_station.txt", "a") as myfile:
        myfile.write("Bäcker adding customer " + str(t1c2.type_id) + str(t1c2.id) + "\n")


    time.sleep(100)
