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
            self.type_id = 'A'
            self.id = 0

        elif type_id == 2:    # Type B
            self.baecker = Station_customer_view("Bäcker", 3, 20)
            self.wursttheke = Station_customer_view("Wursttheke", 2, 5)
            self.kasse = Station_customer_view("Kasse", 3, 20)
            self.type_id ='B'
            self.id = 0


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

        print(shop_object.name + " serving until: " + str(serving_until))
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
        return tmp

    def get_queue_size(self, queue):
        return queue.len()

    def add_customer(self, customer):
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
        return tmp

    def get_queue_size(self, queue):
        return queue.len()

    def add_customer(self, customer):
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
        return tmp

    def get_queue_size(self, queue):
        return queue.len()

    def add_customer(self, customer):
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
        return tmp

    def get_queue_size(self, queue):
        return queue.len()

    def add_customer(self, customer):
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

t1c1 = Customer(1)
t1c2 = Customer(1)
t1c3 = Customer(1)
t1c4 = Customer(1)
t1c5 = Customer(1)
t1c6 = Customer(1)
t1c7 = Customer(1)
t1c8 = Customer(1)
t1c9= Customer(1)
t1c10 = Customer(1)
t1c1.id = 1
t1c2.id = 2
t1c3.id = 3
t1c4.id = 4
t1c5.id = 5
t1c6.id = 6
t1c7.id = 7
t1c8.id = 8
t1c9.id = 9
t1c10.id = 10

t2c1 = Customer(2)
t2c2 = Customer(2)
t2c3 = Customer(2)
t2c4 = Customer(2)
t2c5 = Customer(2)
t2c6 = Customer(2)
t2c7 = Customer(2)
t2c8 = Customer(2)
t2c9 = Customer(2)
t2c10 = Customer(2)
t2c1.id = 1
t2c2.id = 2
t2c3.id = 3
t2c4.id = 4
t2c5.id = 5
t2c6.id = 6
t2c7.id = 7
t2c8.id = 8
t2c9.id = 9
t2c10.id = 10

baecker = Baecker()
kaesetheke = Kaesetheke()
wursttheke = Wursttheke()
kasse = Kasse()

baecker.add_customer(t1c1)
baecker.add_customer(t1c2)
baecker.add_customer(t1c3)
baecker.add_customer(t1c4)
baecker.add_customer(t1c5)

baecker.add_customer(t2c1)
baecker.add_customer(t2c2)
baecker.add_customer(t2c3)
baecker.add_customer(t2c4)

kaesetheke.add_customer(t1c6)
kaesetheke.add_customer(t1c7)
kaesetheke.add_customer(t1c8)
kaesetheke.add_customer(t1c9)
kaesetheke.add_customer(t1c10)

wursttheke.add_customer(t2c5)
wursttheke.add_customer(t2c6)
wursttheke.add_customer(t2c7)
wursttheke.add_customer(t2c8)
wursttheke.add_customer(t2c9)
wursttheke.add_customer(t2c10)

while True:
    if len(heap) > 0:
        x = heap[0]
        if x[0] < datetime.now():
            y = heapq.heappop(heap)
            logger.info(y[2] + ' finished serving ' + y[1])
    print(kaesetheke.serving(kaesetheke))
    print(baecker.serving(baecker))
    print(wursttheke.serving(wursttheke))
    print(list(heap))
    time.sleep(1)


# t = threading.Thread(target=Baecker.start_serving)
# t.daemon = True
# t.start()
# Shop.serving_customer(self.serve_time, self.queue)

# Shop.poll_server(baecker) #nur bei threads
