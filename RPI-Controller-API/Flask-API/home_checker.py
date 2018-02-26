import nmap
import threading

class HomeCheck():
    def __init__(self):
        self.riv = False
        self.ethan = False
        self.nm = nmap.PortScanner()
        self.THREAD_COUNT = 6
        self.results = [(False, False)] * self.THREAD_COUNT
        self.threads = [None] * self.THREAD_COUNT

    def start_scan(self):
        self.nm.scan(hosts='192.168.1.1/24', arguments='-n -sP')
        self.nm.command_line()

    def check_if_home(self, place):
        for h in self.nm.all_hosts():
            if 'mac' in self.nm[h]['addresses']:
                if(self.nm[h]['addresses']['mac'] == 'EC:9B:F3:EE:51:4B'):
                    self.riv = True
                if(self.nm[h]['addresses']['mac'] == 'B4:F1:DA:EA:28:DB'):
                    self.ethan = True
        self.results[place] = (self.riv,self.ethan)

    def get_home(self):
        self.start_scan()
        for i in range(0, self.THREAD_COUNT):
            self.threads[i] = FuncThread(self.check_if_home, i)
        for i in range(0, self.THREAD_COUNT):
            self.threads[i].start()
        for i in range(0, self.THREAD_COUNT):
            self.threads[i].join()

        riv_total = 0
        ethan_total = 0
        for riv,ethan in self.results:
            riv_total += int(riv)
            ethan_total += int(ethan)
        return (riv_total > 0, ethan_total > 0)

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

h = HomeCheck()
res = h.get_home()
print res

