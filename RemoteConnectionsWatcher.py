# by DFT 2023-08-23
import psutil
import colorama
import time
from tabulate import tabulate

colorama.init()

SLEEP = 2

DEBUG = False

totalConns = 0

remote_ip_detected = []


def scan():

    global remote_ip_detected, DEBUG

    result = []

    for p in psutil.pids():

        try:

            proc = psutil.Process(p)

            name = proc.name()

            conns = proc.connections()

            has_conns = int(len(conns) > 0)

            remote_connection = []

            if has_conns:

                for conn in conns:
                    
                    if conn.raddr:

                        r_ip = str(conn.raddr.ip)

                        r_port = str(conn.raddr.port)

                        if r_ip != "127.0.0.1" and r_ip != "0.0.0.0" and r_ip != "::":

                            r_ip_color = "\033[91m" + r_ip + "\033[0m"

                            if [r_ip_color] not in remote_ip_detected:

                                remote_ip_detected.append([r_ip_color])

                            remote_connection_row = "\033[91m" + r_ip + "\033[96m:\033[2m" + r_port + "\033[0m"

                            if remote_connection_row not in remote_connection:

                                remote_connection.append(remote_connection_row)
                
            if len(remote_connection):
                
                remote_connection.sort()
                
                for connection in remote_connection:
                    
                    result.append(["\033[2m" + str(p), "\033[96m" + name + "\033[0m", connection])
                    
        except Exception as e:
            if DEBUG:
                print("An exception has been thrown.", "\n\033[31mException\033[0m->", e, "Don't mind, let's keep walking.")

    remote_ip_detected.sort()
    
    print("\033[2J")
    
    print(tabulate(result, headers=['\033[96mPID', 'PROCESS NAME', 'REMOTE CONNECTION\033[0m']), "\n")
    
    print(tabulate(remote_ip_detected, headers=["\033[96mREMOTE IPS\033[0m"], tablefmt="grid"))
    
    print("\033[31m", "IPS DETECTED", len(remote_ip_detected), "\033[0m")

    result = []
    
    print(result, "\033[94m", time.ctime(), "\033[0m")
    

while True:

    scan()

    time.sleep(SLEEP)
