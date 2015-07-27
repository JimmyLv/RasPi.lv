import commands
import os


def get_CPU_temp():
    CPU_temp_file = open( "/sys/class/thermal/thermal_zone0/temp" )
    CPU_temp = CPU_temp_file.read()
    CPU_temp_file.close()
    return float(CPU_temp)/1000

def get_GPU_temp():
    GPU_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return float(GPU_temp)

# Return % of CPU used by user as a character string
def get_CPU_use():
    cpu_used = os.popen("top -n1")
    for cpu_line in cpu_used:
        if cpu_line[:3]=="%Cp":
            cpu_line_used=cpu_line.split(":")[1].split(",")[0].split(" ")[-2]
            return cpu_line_used

# Return RAM information (unit=kb) in a list                                       
# Index 0: total RAM                                                               
# Index 1: used RAM                                                                 
# Index 2: free RAM  
def get_RAM_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return line.split()[1:4]

def get_RAM_use():
    RAM_stats = get_RAM_info()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)

    return float("%.3f"%(RAM_used*100/RAM_total))

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def get_Disk_info():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
