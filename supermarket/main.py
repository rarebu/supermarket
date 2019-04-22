import time
import heapq
import threading
import queue
import logging
from datetime import datetime, timedelta


class Station_customer_view:
    def __init__(self, station_type, item_count, max_queue_size):
        self.station_type = station_type
        self.item_count = item_count
        self.max_queue_size = max_queue_size

class Customer:
    def __init__(self, type_id):

        if type_id == 1:    # Type A
            self.baecker = Station_customer_view("Bäcker", 10, 10)
            self.wursttheke = Station_customer_view("Wursttheke", 5, 10)
            self.kaesetheke = Station_customer_view("Käsetheke", 3, 5)
            self.kasse = Station_customer_view("Kasse", 30, 20)
            self.station_sequence = ["Bäcker", "Wursttheke", "Käsetheke", "Kasse"]
            self.busy = False
            self.type_id = 'A'
            self.id = 0

        elif type_id == 2:    # Type B
            self.baecker = Station_customer_view("Bäcker", 3, 20)
            self.wursttheke = Station_customer_view("Wursttheke", 2, 5)
            self.kasse = Station_customer_view("Kasse", 3, 20)
            self.station_sequence = ["Wursttheke", "Kasse", "Bäcker"]
            self.busy = False
            self.type_id = 'B'
            self.id = 0

    def supervise(self):
        if self.busy:
            return
        elif len(self.station_sequence) > 0:
            if self.station_sequence[0] == "Bäcker":
                self.current_state = "Bäcker"
                self.busy = True
                baecker.add_customer(self)
            elif self.station_sequence[0] == "Wursttheke":
                self.current_state = "Wursttheke"
                self.busy = True
                wursttheke.add_customer(self)
            elif self.station_sequence[0] == "Käsetheke":
                self.current_state = "Käsetheke"
                self.busy = True
                kaesetheke.add_customer(self)
            elif self.station_sequence[0] == "Kasse":
                self.current_state = "Kasse"
                self.busy = True
                kasse.add_customer(self)

    def makeunbusy(self):
        self.busy = False




class Shop:
    def serving_customer(shop_object):
        if Shop.serving_items(shop_object):
            return 0, ""

        now = datetime.now()
        diff = now - shop_object.last_served

        if diff.seconds >= shop_object.serve_time:
            if not shop_object.queue.empty():
                customer = shop_object.queue.get()
                tmpstr = str(customer.type_id) + str(customer.id)
                if shop_object.name == "Bäcker":
                    tmptime = customer.baecker.item_count * shop_object.serve_time
                if shop_object.name == "Kasse":
                    tmptime = customer.kasse.item_count * shop_object.serve_time
                if shop_object.name == "Käsetheke":
                    tmptime = customer.kaesetheke.item_count * shop_object.serve_time
                if shop_object.name == "Wursttheke":
                    tmptime = customer.wursttheke.item_count * shop_object.serve_time
                heapq.heappush(heap, (datetime.now() + timedelta(0, tmptime), tmpstr, shop_object.name))
                shop_object.serving_until = datetime.now() + timedelta(0, tmptime)
                logger.info(shop_object.name + " serving customer " + tmpstr)
                return tmptime, tmpstr
            return 0, ""
        else:
            return 0, ""

    @staticmethod
    def serving_items(shop_object):
        serving_until = shop_object.serving_until

        if serving_until > datetime.now():
            return True
        else:
            return False

    def customer_joining_queue(self, customer):
        super.add_customer(queue, customer)

    def poll_server(self, station):
        while not station.serving():
            time.sleep(0.01)


class Baecker:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Bäcker"
        self.serve_time = 10

    def serving(self, shop_object):
        tmp = Shop.serving_customer(shop_object)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer):
        if self.get_queue_size() < customer.baecker.max_queue_size:
            logger.info("Bäcker adding customer " + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)


class Wursttheke:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Wursttheke"
        self.serve_time = 30

    def serving(self, shop_object):
        tmp = Shop.serving_customer(shop_object)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer):
        if self.get_queue_size() < customer.wursttheke.max_queue_size:
            logger.info("Wursttheke adding customer " + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)


class Kaesetheke:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Käsetheke"
        self.serve_time = 60

    def serving(self, shop_object):
        tmp = Shop.serving_customer(shop_object)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer):
        if self.get_queue_size() < customer.kaesetheke.max_queue_size:
            logger.info("Käsetheke adding customer " + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)


class Kasse:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Kasse"
        self.serve_time = 5

    def serving(self, shop_object):
        tmp = Shop.serving_customer(shop_object)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer):
        if self.get_queue_size() < customer.kasse.max_queue_size:
            logger.info("Kasse adding customer " + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)


heap = []
heapq.heapify(heap)

logger = logging.getLogger('msglog')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('supermarkt_station_x.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Test Start')






baecker = Baecker()
kaesetheke = Kaesetheke()
wursttheke = Wursttheke()
kasse = Kasse()

A1 = Customer(1)
A2 = Customer(1)
A3 = Customer(1)
A4 = Customer(1)
A5 = Customer(1)
A6 = Customer(1)
A7 = Customer(1)
A8 = Customer(1)
A9= Customer(1)
A10 = Customer(1)
A1.id = 1
A2.id = 2
A3.id = 3
A4.id = 4
A5.id = 5
A6.id = 6
A7.id = 7
A8.id = 8
A9.id = 9
A10.id = 10

B1 = Customer(2)
B2 = Customer(2)
B3 = Customer(2)
B4 = Customer(2)
B5 = Customer(2)
B6 = Customer(2)
B7 = Customer(2)
B8 = Customer(2)
B9 = Customer(2)
B10 = Customer(2)
B1.id = 1
B2.id = 2
B3.id = 3
B4.id = 4
B5.id = 5
B6.id = 6
B7.id = 7
B8.id = 8
B9.id = 9
B10.id = 10

#baecker.add_customer(A1)
# baecker.add_customer(A2)
# baecker.add_customer(A3)
# baecker.add_customer(A4)
# baecker.add_customer(A5)
#
# baecker.add_customer(B1)
# baecker.add_customer(B2)
# baecker.add_customer(B3)
# baecker.add_customer(B4)
#
#kaesetheke.add_customer(A6)
# kaesetheke.add_customer(A7)
# kaesetheke.add_customer(A8)
# kaesetheke.add_customer(A9)
# kaesetheke.add_customer(A10)
#
#wursttheke.add_customer(B5)
# wursttheke.add_customer(B6)
# wursttheke.add_customer(B7)
# wursttheke.add_customer(B8)
# wursttheke.add_customer(B9)
# wursttheke.add_customer(B10)

#kasse.add_customer(B2)

while True:
    if len(heap) > 0:
        x = heap[0]
        if x[0] < datetime.now():
            y = heapq.heappop(heap)
            logger.info(y[2] + ' finished serving ' + y[1])
            eval(y[1] + '.station_sequence.pop(0)')
            eval(y[1] + '.makeunbusy()')
    A1.supervise()
    B1.supervise()
    kaesetheke.serving(kaesetheke)
    baecker.serving(baecker)
    kasse.serving(kasse)
    wursttheke.serving(wursttheke)
    print(list(heap))
    if len(heap) == 0:
        break
    time.sleep(1)


# t = threading.Thread(target=Baecker.start_serving)
# t.daemon = True
# t.start()
# Shop.serving_customer(self.serve_time, self.queue)

# Shop.poll_server(baecker) #nur bei threads
