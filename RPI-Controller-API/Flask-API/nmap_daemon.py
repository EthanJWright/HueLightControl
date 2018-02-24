import nmap
nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.1/24', arguments='-n -sP')
nm.command_line()

file = open('home.txt', 'w')

def check_if_home():
    riv, ethan = False, False
    for h in nm.all_hosts():
        if 'mac' in nm[h]['addresses']:
            if(nm[h]['addresses']['mac'] == 'EC:9B:F3:EE:51:4B'):
                riv = True
            if(nm[h]['addresses']['mac'] == 'B4:F1:DA:EA:28:DB'):
                ethan = True
    return riv,ethan
report = [' is not home.', ' is home.']
for i in range(0,6):
    riv,ethan = check_if_home()
    if(riv and ethan):
        file.write("Ethan and River are Home.")
        print("Ethan and River are Home.")
        file.close()
        exit()
file.write("Ethan" + report[int(ethan)] + "\n" + "River" + report[int(riv)])
print "Ethan" + report[int(ethan)] + "\n" + "River" + report[int(riv)]

