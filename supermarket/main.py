import time
from heapq import heappush, heappop, heapify
import threading
import queue
import logging
from datetime import datetime, timedelta


class StationCustomerView:
    def __init__(self, station_type, item_count, max_queue_size):
        self.station_type = station_type
        self.item_count = item_count
        self.max_queue_size = max_queue_size


class Customer:
    def __init__(self, type_id):
        self.id = 0
        self.start_time = datetime(2000, 1, 1)
        self.end_time = datetime(2000, 1, 1)
        self.busy = False
        self.first_time_here = True
        self.current_state = ''
        self.skipped_station = False
        self.station_sequence_lock = threading.Lock()

        if type_id == 1:    # Type A
            self.baecker = StationCustomerView('Bäcker', 10, 10)
            self.wursttheke = StationCustomerView('Wursttheke', 5, 10)
            self.kaesetheke = StationCustomerView('Käsetheke', 3, 5)
            self.kasse = StationCustomerView('Kasse', 30, 20)
            self.station_sequence = ['Bäcker', 'Wursttheke', 'Käsetheke', 'Kasse']
            self.type_id = 'A'

        elif type_id == 2:    # Type B
            self.baecker = StationCustomerView('Bäcker', 3, 20)
            self.wursttheke = StationCustomerView('Wursttheke', 2, 5)
            self.kasse = StationCustomerView('Kasse', 3, 20)
            self.station_sequence = ['Wursttheke', 'Kasse', 'Bäcker']
            self.type_id = 'B'

    def supervise(self, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse, logger_supermarket_station,
                  logger_supermarket_customer):
        if self.busy:
            return
        elif self.first_time_here:
            self.start_time = datetime.now()
            self.first_time_here = False
        self.station_sequence_lock.acquire()
        if len(self.station_sequence) > 0:
            if self.station_sequence[0] == 'Bäcker':
                self.current_state = 'Bäcker'
                self.busy = True
                tmp_baecker.add_customer(self, logger_supermarket_station)
                logger_supermarket_customer.info(self.type_id + str(self.id) + ' Queueing at Bäcker')
            elif self.station_sequence[0] == 'Wursttheke':
                self.current_state = 'Wursttheke'
                self.busy = True
                tmp_wursttheke.add_customer(self, logger_supermarket_station)
                logger_supermarket_customer.info(self.type_id + str(self.id) + ' Queueing at Wursttheke')
            elif self.station_sequence[0] == 'Käsetheke':
                self.current_state = 'Käsetheke'
                self.busy = True
                tmp_kaesetheke.add_customer(self, logger_supermarket_station)
                logger_supermarket_customer.info(self.type_id + str(self.id) + ' Queueing at Käsetheke')
            elif self.station_sequence[0] == 'Kasse':
                self.current_state = 'Kasse'
                self.busy = True
                tmp_kasse.add_customer(self, logger_supermarket_station)
                logger_supermarket_customer.info(self.type_id + str(self.id) + ' Queueing at Kasse')
        else:
            self.end_time = datetime.now()
        self.station_sequence_lock.release()

    def makeunbusy(self):
        self.busy = False


class Shop:

    @staticmethod
    def serving_items(shop_object):
        serving_until = shop_object.serving_until

        if serving_until > datetime.now():
            return True
        else:
            return False


def serving_customer(self, tmp_supermarket, logger_supermarket_station):
    if Shop.serving_items(self):
        return 0, ''

    now = datetime.now()
    diff = now - self.last_served

    if diff.seconds >= self.serve_time:
        if not self.queue.empty():
            customer = self.queue.get()
            tmpstr = str(customer.type_id) + str(customer.id)
            if self.name == 'Bäcker':
                tmptime = customer.baecker.item_count * self.serve_time
            if self.name == 'Kasse':
                tmptime = customer.kasse.item_count * self.serve_time
            if self.name == 'Käsetheke':
                tmptime = customer.kaesetheke.item_count * self.serve_time
            if self.name == 'Wursttheke':
                tmptime = customer.wursttheke.item_count * self.serve_time
            heappush(tmp_supermarket.heap, (datetime.now() + timedelta(0, tmptime), tmpstr, self.name))
            self.serving_until = datetime.now() + timedelta(0, tmptime)
            logger_supermarket_station.info(self.name + ' serving customer ' + tmpstr)
            return tmptime, tmpstr
        return 0, ''
    else:
        return 0, ''


class Baecker:
    def __init__(self, speedup):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = 'Bäcker'
        self.serve_time = 10 / speedup
        self.skip_count = 0
        self.successful_customer = []
        self.busy = False

    def serving(self, tmp_supermarket, logger_supermarket_station):
        for item in tmp_supermarket.heap:
            if self.name == item[2]:
                return
        tmp = serving_customer(self, tmp_supermarket, logger_supermarket_station)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer, logger_supermarket_station):
        if self.get_queue_size() < customer.baecker.max_queue_size:
            logger_supermarket_station.info('Bäcker adding customer ' + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)
        else:
            self.skip_count += 1
            customer.skipped_station = True
            customer.station_sequence.remove('Bäcker')
            customer.makeunbusy()


class Wursttheke:
    def __init__(self, speedup):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = 'Wursttheke'
        self.serve_time = 30 / speedup
        self.skip_count = 0
        self.successful_customer = []
        self.busy = False

    def serving(self, tmp_supermarket, logger_supermarket_station):
        for item in tmp_supermarket.heap:
            if self.name == item[2]:
                return
        tmp = serving_customer(self, tmp_supermarket, logger_supermarket_station)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer, logger_supermarket_station):
        if self.get_queue_size() < customer.wursttheke.max_queue_size:
            logger_supermarket_station.info('Wursttheke adding customer ' + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)
        else:
            self.skip_count += 1
            customer.skipped_station = True
            customer.station_sequence.remove('Wursttheke')
            customer.makeunbusy()


class Kaesetheke:
    def __init__(self, speedup):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = 'Käsetheke'
        self.serve_time = 60 / speedup
        self.skip_count = 0
        self.successful_customer = []
        self.busy = False

    def serving(self, tmp_supermarket, logger_supermarket_station):
        for item in tmp_supermarket.heap:
            if self.name == item[2]:
                return
        tmp = serving_customer(self, tmp_supermarket, logger_supermarket_station)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer, logger_supermarket_station):
        if self.get_queue_size() < customer.kaesetheke.max_queue_size:
            logger_supermarket_station.info('Käsetheke adding customer ' + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)
        else:
            self.skip_count += 1
            customer.skipped_station = True
            customer.station_sequence.remove('Käsetheke')
            customer.makeunbusy()


class Kasse:
    def __init__(self, speedup):
        self.queue = queue.Queue()
        self.last_served = datetime(2000, 1, 1)
        self.serving_until = datetime(2000, 1, 1)
        self.name = 'Kasse'
        self.serve_time = 5 / speedup
        self.skip_count = 0
        self.successful_customer = []
        self.busy = False

    def serving(self, tmp_supermarket, logger_supermarket_station):
        for item in tmp_supermarket.heap:
            if self.name == item[2]:
                return
        tmp = serving_customer(self, tmp_supermarket, logger_supermarket_station)
        if tmp[0] != 0:
            self.last_served = datetime.now()
        return

    def get_queue_size(self):
        return self.queue.qsize()

    def add_customer(self, customer, logger_supermarket_station):
        if self.get_queue_size() < customer.kasse.max_queue_size:
            logger_supermarket_station.info('Kasse adding customer ' + str(customer.type_id) + str(customer.id))
            self.queue.put(customer)
        else:
            self.skip_count += 1
            customer.skipped_station = True
            customer.station_sequence.remove('Kasse')
            customer.makeunbusy()


class Supermarket:
    def __init__(self, speedup):
        self.heap_lock = threading.Lock()
        self.event_queue_lock = threading.Lock()
        self.heap = []
        self.active_customer_list = []
        self.customer_list = []
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
        self.A11 = Customer(1)
        self.A12 = Customer(1)
        self.A13 = Customer(1)
        self.A14 = Customer(1)
        self.A15 = Customer(1)
        self.A16 = Customer(1)
        self.A17 = Customer(1)
        self.A18 = Customer(1)
        self.A19 = Customer(1)
        self.A20 = Customer(1)
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
        self.A11.id = 11
        self.A12.id = 12
        self.A13.id = 13
        self.A14.id = 14
        self.A15.id = 15
        self.A16.id = 16
        self.A17.id = 17
        self.A18.id = 18
        self.A19.id = 19
        self.A20.id = 20
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
        self.B11 = Customer(2)
        self.B12 = Customer(2)
        self.B13 = Customer(2)
        self.B14 = Customer(2)
        self.B15 = Customer(2)
        self.B16 = Customer(2)
        self.B17 = Customer(2)
        self.B18 = Customer(2)
        self.B19 = Customer(2)
        self.B20 = Customer(2)
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
        self.B11.id = 11
        self.B12.id = 12
        self.B13.id = 13
        self.B14.id = 14
        self.B15.id = 15
        self.B16.id = 16
        self.B17.id = 17
        self.B18.id = 18
        self.B19.id = 19
        self.B20.id = 20
        self.customer_list = [self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7, self.A8, self.A9, self.A10,
                              self.A11, self.A12, self.A13, self.A14, self.A15, self.A16, self.A17, self.A18, self.A19,
                              self.A20, self.B1, self.B2, self.B3, self.B4, self.B5, self.B6, self.B7, self.B8, self.B9,
                              self.B10, self.B11, self.B12, self.B13, self.B14, self.B15, self.B16, self.B17, self.B18,
                              self.B19, self.B20,
                              ]
        self.event_queue = self.initiate_event_queue(speedup)

    def check_if_finished_at_station(self, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                     logger_supermarket_station, logger_supermarket_customer):
        if len(self.heap) > 0:
            x = self.heap[0]
            if x[0] < datetime.now():
                self.heap_lock.acquire()
                y = heappop(self.heap)
                self.heap_lock.release()
                logger_supermarket_station.info(y[2] + ' finished customer' + y[1])
                logger_supermarket_customer.info(y[1] + ' finished at' + y[2])
                eval('self.' + y[1] + '.station_sequence.pop(0)')
                eval('self.' + y[1] + '.makeunbusy()')
                if y[2] == 'Bäcker':
                    tmp_baecker.successful_customer.append(y[1])
                elif y[2] == 'Wursttheke':
                    tmp_wursttheke.successful_customer.append(y[1])
                elif y[2] == 'Käsetheke':
                    tmp_kaesetheke.successful_customer.append(y[1])
                elif y[2] == 'Kasse':
                    tmp_kasse.successful_customer.append(y[1])

    def initiate_event_queue(self, speedup):
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
        event_list.append((datetime.now() + timedelta(seconds=2000) / speedup, self.A11))
        event_list.append((datetime.now() + timedelta(seconds=2200) / speedup, self.A12))
        event_list.append((datetime.now() + timedelta(seconds=2400) / speedup, self.A13))
        event_list.append((datetime.now() + timedelta(seconds=2600) / speedup, self.A14))
        event_list.append((datetime.now() + timedelta(seconds=2800) / speedup, self.A15))
        event_list.append((datetime.now() + timedelta(seconds=3000) / speedup, self.A16))
        event_list.append((datetime.now() + timedelta(seconds=3200) / speedup, self.A17))
        event_list.append((datetime.now() + timedelta(seconds=3400) / speedup, self.A18))
        event_list.append((datetime.now() + timedelta(seconds=3600) / speedup, self.A19))
        event_list.append((datetime.now() + timedelta(seconds=3800) / speedup, self.A20))
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
        event_list.append((datetime.now() + timedelta(seconds=601) / speedup, self.B11))
        event_list.append((datetime.now() + timedelta(seconds=661) / speedup, self.B12))
        event_list.append((datetime.now() + timedelta(seconds=721) / speedup, self.B13))
        event_list.append((datetime.now() + timedelta(seconds=781) / speedup, self.B14))
        event_list.append((datetime.now() + timedelta(seconds=841) / speedup, self.B15))
        event_list.append((datetime.now() + timedelta(seconds=901) / speedup, self.B16))
        event_list.append((datetime.now() + timedelta(seconds=961) / speedup, self.B17))
        event_list.append((datetime.now() + timedelta(seconds=1021) / speedup, self.B18))
        event_list.append((datetime.now() + timedelta(seconds=1081) / speedup, self.B19))
        event_list.append((datetime.now() + timedelta(seconds=1141) / speedup, self.B20))
        for item in event_list:
            heappush(event_queue, item)
        event_queue.sort()
        return event_queue

    def supermarket_supervisor(self, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                               logger_supermarket_station, logger_supermarket_customer):
        while True:
            if len(self.event_queue) > 0 and self.event_queue[0][0] <= datetime.now():  # appending customer to active_customer_list
                self.event_queue_lock.acquire()
                customer = heappop(self.event_queue)[1]
                self.event_queue_lock.release()
                self.active_customer_list.append(customer)
            else:                                                                            # supervising the customers
                for item in self.active_customer_list:
                    if item.end_time == datetime(2000, 1, 1):
                        item.supervise(tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                       logger_supermarket_station, logger_supermarket_customer)
                    else:                                                  # removing customer from active_customer_list
                        self.active_customer_list.remove(item)
                break

    def print_stats(self, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse, speedup, simulation_start,
                    logger_supermarket):
        avg_time = timedelta()
        total_customers = len(self.customer_list)
        skip_count = 0
        customer_time_in_shop_list = []
        for customer in self.customer_list:
            customer_time_in_shop_list.append((customer.end_time - customer.start_time) * speedup)
            if customer.skipped_station:
                skip_count += 1
        for customer_time in customer_time_in_shop_list:
            avg_time = avg_time + customer_time
        avg_time = avg_time / len(customer_time_in_shop_list)
        logger_supermarket.info('Simulationsende: ' + str(datetime.now() - simulation_start))
        logger_supermarket.info('Anzahl Kunden: ' + str(total_customers))
        logger_supermarket.info('Anzahl vollständige Einkäufe: ' + str(total_customers - skip_count))
        logger_supermarket.info('Mittlere Einkaufsdauer: ' + str(avg_time))
        print('Simulationsende: ' + str(datetime.now() - simulation_start))
        print('Anzahl Kunden: ' + str(total_customers))
        print('Anzahl vollständige Einkäufe: ' + str(total_customers - skip_count))
        print('Mittlere Einkaufsdauer: ' + str(avg_time))
        if tmp_baecker.skip_count == 0:
            logger_supermarket.info('Drop percentage at Bäcker: 00.0')
            print('Drop percentage at Bäcker: 00.0')
        else:
            logger_supermarket.info('Drop percentage at Bäcker: ' + str(tmp_baecker.skip_count /
                                                                        (len(tmp_baecker.successful_customer) +
                                                                         tmp_baecker.skip_count) * 100))
            print('Drop percentage at Bäcker: ' + str(tmp_baecker.skip_count / (len(tmp_baecker.successful_customer) +
                                                                                tmp_baecker.skip_count) * 100))
        if tmp_wursttheke.skip_count == 0:
            logger_supermarket.info('Drop percentage at Wursttheke: 00.0')
            print('Drop percentage at Wursttheke: 00.0')
        else:
            logger_supermarket.info('Drop percentage at Wursttheke: ' + str(tmp_wursttheke.skip_count /
                                                                            (len(tmp_wursttheke.successful_customer) +
                                                                             tmp_wursttheke.skip_count) * 100))
            print('Drop percentage at Wursttheke: ' + str(tmp_wursttheke.skip_count /
                                                          (len(tmp_wursttheke.successful_customer) +
                                                           tmp_wursttheke.skip_count) * 100))
        if tmp_kaesetheke.skip_count == 0:
            logger_supermarket.info('Drop percentage at Käsetheke: 00.0')
            print('Drop percentage at Käsetheke: 00.0')
        else:
            logger_supermarket.info('Drop percentage at Käsetheke: ' + str(tmp_kaesetheke.skip_count /
                                                                           (len(tmp_kaesetheke.successful_customer) +
                                                                            tmp_kaesetheke.skip_count) * 100))
            print('Drop percentage at Käsetheke: ' + str(tmp_kaesetheke.skip_count /
                                                         (len(tmp_kaesetheke.successful_customer) +
                                                          tmp_kaesetheke.skip_count) * 100))
        if tmp_kasse.skip_count == 0:
            logger_supermarket.info('Drop percentage at Kasse: 00.0')
            print('Drop percentage at Kasse: 00.0')
        else:
            logger_supermarket.info('Drop percentage at Kasse: ' + str(tmp_kasse.skip_count /
                                                                       (len(tmp_kasse.successful_customer) +
                                                                        tmp_kasse.skip_count) * 100))
            print('Drop percentage at Kasse: ' + str(tmp_kasse.skip_count / (len(tmp_kasse.successful_customer) +
                                                                             tmp_kasse.skip_count) * 100))
        # print('Bäcker: ' + str(len(tmp_baecker.successful_customer)) + ' skipped: ' + str(
        #     tmp_baecker.skip_count))
        # print('Wursttheke: ' + str(len(tmp_wursttheke.successful_customer)) + ' skipped: ' + str(
        #     tmp_wursttheke.skip_count))
        # print('Käsetheke: ' + str(len(tmp_kaesetheke.successful_customer)) + ' skipped: ' + str(
        #     tmp_kaesetheke.skip_count))
        # print('Kasse: ' + str(len(tmp_kasse.successful_customer)) + ' skipped: ' + str(
        #     tmp_kasse.skip_count))


class Thread:
    @staticmethod
    def t_check_if_finished_at_station(tmp_supermarket, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                       logger_supermarket_station, logger_supermarket_customer):
        while True:
            tmp_supermarket.check_if_finished_at_station(tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                                         logger_supermarket_station, logger_supermarket_customer)

    @staticmethod
    def t_supermarket_supervisor(tmp_supermarket, tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                 logger_supermarket_station, logger_supermarket_customer):
        while True:
            tmp_supermarket.supermarket_supervisor(tmp_baecker, tmp_wursttheke, tmp_kaesetheke, tmp_kasse,
                                                   logger_supermarket_station, logger_supermarket_customer)

    @staticmethod
    def t_station_serving(tmp_station, tmp_supermarket, logger_supermarket_station):
        while True:
            tmp_station.serving(tmp_supermarket, logger_supermarket_station)


class Simulation:
    def __init__(self, speedup):
        self.simulation_start = datetime.now()
        self.speedup = speedup
        self.baecker = Baecker(speedup)
        self.kaesetheke = Kaesetheke(speedup)
        self.wursttheke = Wursttheke(speedup)
        self.kasse = Kasse(speedup)
        self.supermarket = Supermarket(speedup)
        self.formatter = logging.Formatter('%(asctime)s - %(message)s')
        self.formatter2 = logging.Formatter('%(message)s')
        self.logger_supermarket_station = self.setup_logger('supermarket_station', 'supermarket_station.txt')
        self.logger_supermarket_customer = self.setup_logger('supermarket_customer', 'supermarket_customer.txt')
        self.logger_supermarket = self.setup_logger('supermarket', 'supermarket.txt')

    def simulate_with_threads(self):
        thread = Thread

        t_check_if_finished_at_station = threading.Thread(target=thread.t_check_if_finished_at_station,
                                                          args=(self.supermarket, self.baecker, self.wursttheke,
                                                                self.kaesetheke, self.kasse,
                                                                self.logger_supermarket_station,
                                                                self.logger_supermarket_customer))
        t_check_if_finished_at_station.daemon = True
        t_check_if_finished_at_station.start()

        t_supermarket_supervisor = threading.Thread(target=thread.t_supermarket_supervisor,
                                                    args=(self.supermarket, self.baecker, self.wursttheke,
                                                          self.kaesetheke, self.kasse, self.logger_supermarket_station,
                                                          self.logger_supermarket_customer))
        t_supermarket_supervisor.daemon = True
        t_supermarket_supervisor.start()

        t_serving_kaesetheke = threading.Thread(target=thread.t_station_serving,
                                                args=(self.kaesetheke, self.supermarket,
                                                      self.logger_supermarket_station))
        t_serving_kaesetheke.daemon = True
        t_serving_kaesetheke.start()

        t_serving_baecker = threading.Thread(target=thread.t_station_serving, args=(self.baecker, self.supermarket,
                                                                                    self.logger_supermarket_station))
        t_serving_baecker.daemon = True
        t_serving_baecker.start()

        t_serving_kasse = threading.Thread(target=thread.t_station_serving, args=(self.kasse, self.supermarket,
                                                                                  self.logger_supermarket_station))
        t_serving_kasse.daemon = True
        t_serving_kasse.start()

        t_serving_wursttheke = threading.Thread(target=thread.t_station_serving, args=(self.wursttheke,
                                                                                       self.supermarket,
                                                                                       self.logger_supermarket_station))
        t_serving_wursttheke.daemon = True
        t_serving_wursttheke.start()

        while True:
            # print(list(self.supermarket.heap))
            finished = self.check_if_simulation_has_finished()
            if finished:
                break
            time.sleep(1 / self.speedup)

    def check_if_simulation_has_finished(self):
        if len(self.supermarket.heap) == 0:
            for customer in self.supermarket.customer_list:
                # print(customer.type_id + str(customer.id) + ' ' + ' ' + str(customer.station_sequence))
                if len(customer.station_sequence) != 0:
                    return False
            self.supermarket.print_stats(self.baecker, self.wursttheke, self.kaesetheke, self.kasse, self.speedup,
                                         self.simulation_start, self.logger_supermarket)
            return True

    def simulate_with_list(self):
        while True:
            self.supermarket.check_if_finished_at_station(self.baecker, self.wursttheke, self.kaesetheke, self.kasse,
                                                          self.logger_supermarket_station,
                                                          self.logger_supermarket_customer)
            self.supermarket.supermarket_supervisor(self.baecker, self.wursttheke, self.kaesetheke, self.kasse,
                                                    self.logger_supermarket_station, self.logger_supermarket_customer)
            self.kaesetheke.serving(self.supermarket, self.logger_supermarket_station)
            self.baecker.serving(self.supermarket, self.logger_supermarket_station)
            self.kasse.serving(self.supermarket, self.logger_supermarket_station)
            self.wursttheke.serving(self.supermarket, self.logger_supermarket_station)
            # print(list(self.supermarket.heap))
            finished = self.check_if_simulation_has_finished()
            if finished:
                break
            time.sleep(1 / self.speedup)

    def setup_logger(self, name, log_file, level=logging.INFO):
        open('supermarket_customer.txt', 'w').close()
        open('supermarket_station.txt', 'w').close()
        open('supermarket.txt', 'w').close()
        handler = logging.FileHandler(log_file)
        if name == 'supermarket':
            handler.setFormatter(self.formatter2)
        else:
            handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger


# Simulation(speedup=30).simulate_with_list()
Simulation(speedup=100).simulate_with_threads()
