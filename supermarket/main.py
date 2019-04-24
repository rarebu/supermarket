import time
from heapq import heappush, heappop, heapify
import threading
import queue
import logging
from datetime import datetime, timedelta

speedup = 40


class StationCustomerView:
    def __init__(self, station_type, item_count, max_queue_size):
        self.station_type = station_type
        self.item_count = item_count
        self.max_queue_size = max_queue_size


class Customer:
    def __init__(self, type_id):

        if type_id == 1:    # Type A
            self.baecker = StationCustomerView("Bäcker", 10, 10)
            self.wursttheke = StationCustomerView("Wursttheke", 5, 10)
            self.kaesetheke = StationCustomerView("Käsetheke", 3, 5)
            self.kasse = StationCustomerView("Kasse", 30, 20)
            self.station_sequence = ["Bäcker", "Wursttheke", "Käsetheke", "Kasse"]
            self.busy = False
            self.type_id = 'A'
            self.id = 0
            self.start_time = datetime(2000, 1, 1)
            self.end_time = datetime(2000, 1, 1)
            self.first_time_here = True

        elif type_id == 2:    # Type B
            self.baecker = StationCustomerView("Bäcker", 3, 20)
            self.wursttheke = StationCustomerView("Wursttheke", 2, 5)
            self.kasse = StationCustomerView("Kasse", 3, 20)
            self.station_sequence = ["Wursttheke", "Kasse", "Bäcker"]
            self.busy = False
            self.type_id = 'B'
            self.id = 0
            self.start_time = datetime(2000, 1, 1)
            self.end_time = datetime(2000, 1, 1)
            self.first_time_here = True

    def supervise(self):
        if self.busy:
            return
        elif self.first_time_here:
            self.start_time = datetime.now()
            self.first_time_here = False

        if len(self.station_sequence) > 0:
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
        else:
            self.end_time = datetime.now()

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
                heappush(supermarket.heap, (datetime.now() + timedelta(0, tmptime), tmpstr, shop_object.name))
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
        self.serve_time = 10 / speedup
        self.skip_count = 0
        self.successful_customer = []

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
        else:
            self.skip_count += 1
            customer.station_sequence.remove("Bäcker")
            customer.makeunbusy()


class Wursttheke:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Wursttheke"
        self.serve_time = 30 / speedup
        self.skip_count = 0
        self.successful_customer = []

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
        else:
            self.skip_count += 1
            customer.station_sequence.remove("Wursttheke")
            customer.makeunbusy()


class Kaesetheke:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Käsetheke"
        self.serve_time = 60 / speedup
        self.skip_count = 0
        self.successful_customer = []

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
        else:
            self.skip_count += 1
            customer.station_sequence.remove("Käsetheke")
            customer.makeunbusy()


class Kasse:
    def __init__(self):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = "Kasse"
        self.serve_time = 5 / speedup
        self.skip_count = 0
        self.successful_customer = []

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
        else:
            self.skip_count += 1
            customer.station_sequence.remove("Kasse")
            customer.makeunbusy()


class Supermarket:
    def __init__(self):
        self.heap = []
        self.active_customer_list = []
        self.A1 = Customer(1)
        self.A2 = Customer(1)
        self.A3 = Customer(1)
        self.A4 = Customer(1)
        self.A5 = Customer(1)
        self.A6 = Customer(1)
        self.A7 = Customer(1)
        self.A8 = Customer(1)
        self.A9 = Customer(1)
        self.A10 = Customer(1)
        self.A1.id = 1
        self.A2.id = 2
        self.A3.id = 3
        self.A4.id = 4
        self.A5.id = 5
        self.A6.id = 6
        self.A7.id = 7
        self.A8.id = 8
        self.A9.id = 9
        self.A10.id = 10
        self.B1 = Customer(2)
        self.B2 = Customer(2)
        self.B3 = Customer(2)
        self.B4 = Customer(2)
        self.B5 = Customer(2)
        self.B6 = Customer(2)
        self.B7 = Customer(2)
        self.B8 = Customer(2)
        self.B9 = Customer(2)
        self.B10 = Customer(2)
        self.B1.id = 1
        self.B2.id = 2
        self.B3.id = 3
        self.B4.id = 4
        self.B5.id = 5
        self.B6.id = 6
        self.B7.id = 7
        self.B8.id = 8
        self.B9.id = 9
        self.B10.id = 10
        self.event_queue = self.initiate_event_queue()

    def check_if_finished_at_station(self):
        if len(supermarket.heap) > 0:
            x = supermarket.heap[0]
            if x[0] < datetime.now():
                y = heappop(supermarket.heap)
                logger.info(y[2] + ' finished serving ' + y[1])
                eval('self.' + y[1] + '.station_sequence.pop(0)')
                eval('self.' + y[1] + '.makeunbusy()')
                if y[2] == "Bäcker":
                    baecker.successful_customer.append(y[1])
                elif y[2] == "Wursttheke":
                    wursttheke.successful_customer.append(y[1])
                elif y[2] == "Käsetheke":
                    kaesetheke.successful_customer.append(y[1])
                elif y[2] == "Kasse":
                    kasse.successful_customer.append(y[1])

    def initiate_event_queue(self):
        heapify(self.heap)
        event_queue = []
        event_list = []
        event_list.append((datetime.now() + timedelta(seconds=0) / speedup, self.A1))
        event_list.append((datetime.now() + timedelta(seconds=200) / speedup, self.A2))
        event_list.append((datetime.now() + timedelta(seconds=400) / speedup, self.A3))
        event_list.append((datetime.now() + timedelta(seconds=600) / speedup, self.A4))
        event_list.append((datetime.now() + timedelta(seconds=800) / speedup, self.A5))
        event_list.append((datetime.now() + timedelta(seconds=1000) / speedup, self.A6))
        event_list.append((datetime.now() + timedelta(seconds=1200) / speedup, self.A7))
        event_list.append((datetime.now() + timedelta(seconds=1400) / speedup, self.A8))
        event_list.append((datetime.now() + timedelta(seconds=1600) / speedup, self.A9))
        event_list.append((datetime.now() + timedelta(seconds=1800) / speedup, self.A10))
        event_list.append((datetime.now() + timedelta(seconds=1) / speedup, self.B1))
        event_list.append((datetime.now() + timedelta(seconds=61) / speedup, self.B2))
        event_list.append((datetime.now() + timedelta(seconds=121) / speedup, self.B3))
        event_list.append((datetime.now() + timedelta(seconds=181) / speedup, self.B4))
        event_list.append((datetime.now() + timedelta(seconds=241) / speedup, self.B5))
        event_list.append((datetime.now() + timedelta(seconds=301) / speedup, self.B6))
        event_list.append((datetime.now() + timedelta(seconds=361) / speedup, self.B7))
        event_list.append((datetime.now() + timedelta(seconds=421) / speedup, self.B8))
        event_list.append((datetime.now() + timedelta(seconds=481) / speedup, self.B9))
        event_list.append((datetime.now() + timedelta(seconds=541) / speedup, self.B10))
        for item in event_list:
            heappush(event_queue, item)
        event_queue.sort()
        return event_queue

    def supermarket_supervisor(self, event_queue):
        while True:
            if len(event_queue) > 0 and event_queue[0][0] <= datetime.now():  # appending customer to active_customer_list
                customer = heappop(event_queue)[1]
                self.active_customer_list.append(customer)
                str(customer.type_id)
            else:  # supervising the customers
                for item in self.active_customer_list:
                    if item.end_time == datetime(2000, 1, 1):
                        item.supervise()
                    else:  # removing customer from active_customer_list
                        self.active_customer_list.remove(item)
                break;


logger = logging.getLogger('msglog')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('supermarkt_station_x.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
baecker = Baecker()
kaesetheke = Kaesetheke()
wursttheke = Wursttheke()
kasse = Kasse()
supermarket = Supermarket()

while True:
    supermarket.check_if_finished_at_station()
    supermarket.supermarket_supervisor(supermarket.event_queue)
    kaesetheke.serving(kaesetheke)
    baecker.serving(baecker)
    kasse.serving(kasse)
    wursttheke.serving(wursttheke)
    print(list(supermarket.heap))
    if len(supermarket.heap) == 0:
        print("Successful Customers at Bäcker: " + str(len(baecker.successful_customer)))
        print("Customers that skipped Bäcker: " + str(baecker.skip_count))
        print("Successful Customers at Wursttheke: " + str(len(wursttheke.successful_customer)))
        print("Customers that skipped Wursttheke: " + str(wursttheke.skip_count))
        print("Successful Customers at Käsetheke: " + str(len(kaesetheke.successful_customer)))
        print("Customers that skipped Käsetheke: " + str(kaesetheke.skip_count))
        print("Successful Customers at Kasse: " + str(len(kasse.successful_customer)))
        print("Customers that skipped Kasse: " + str(kasse.skip_count))
        print("Customer A1 time spent in Supermarket: " + str((supermarket.A1.end_time - supermarket.A1.start_time) * speedup))
        print("Customer A2 time spent in Supermarket: " + str((supermarket.A2.end_time - supermarket.A2.start_time) * speedup))
        print("Customer A3 time spent in Supermarket: " + str((supermarket.A3.end_time - supermarket.A3.start_time) * speedup))
        print("Customer A4 time spent in Supermarket: " + str((supermarket.A4.end_time - supermarket.A4.start_time) * speedup))
        print("Customer A5 time spent in Supermarket: " + str((supermarket.A5.end_time - supermarket.A5.start_time) * speedup))
        print("Customer A6 time spent in Supermarket: " + str((supermarket.A6.end_time - supermarket.A6.start_time) * speedup))
        print("Customer A7 time spent in Supermarket: " + str((supermarket.A7.end_time - supermarket.A7.start_time) * speedup))
        print("Customer A8 time spent in Supermarket: " + str((supermarket.A8.end_time - supermarket.A8.start_time) * speedup))
        print("Customer A9 time spent in Supermarket: " + str((supermarket.A9.end_time - supermarket.A9.start_time) * speedup))
        print("Customer A10 time spent in Supermarket: " + str((supermarket.A10.end_time - supermarket.A10.start_time) * speedup))
        print("Customer B1 time spent in Supermarket: " + str((supermarket.B1.end_time - supermarket.B1.start_time) * speedup))
        print("Customer B2 time spent in Supermarket: " + str((supermarket.B2.end_time - supermarket.B2.start_time) * speedup))
        print("Customer B3 time spent in Supermarket: " + str((supermarket.B3.end_time - supermarket.B3.start_time) * speedup))
        print("Customer B4 time spent in Supermarket: " + str((supermarket.B4.end_time - supermarket.B4.start_time) * speedup))
        print("Customer B5 time spent in Supermarket: " + str((supermarket.B5.end_time - supermarket.B5.start_time) * speedup))
        print("Customer B6 time spent in Supermarket: " + str((supermarket.B6.end_time - supermarket.B6.start_time) * speedup))
        print("Customer B7 time spent in Supermarket: " + str((supermarket.B7.end_time - supermarket.B7.start_time) * speedup))
        print("Customer B8 time spent in Supermarket: " + str((supermarket.B8.end_time - supermarket.B8.start_time) * speedup))
        print("Customer B9 time spent in Supermarket: " + str((supermarket.B9.end_time - supermarket.B9.start_time) * speedup))
        print("Customer B10 time spent in Supermarket: " + str((supermarket.B10.end_time - supermarket.B10.start_time) * speedup))
        break
    time.sleep(1 / speedup)


# t = threading.Thread(target=Baecker.start_serving)
# t.daemon = True
# t.start()
# Shop.serving_customer(self.serve_time, self.queue)

# Shop.poll_server(baecker) #nur bei threads
