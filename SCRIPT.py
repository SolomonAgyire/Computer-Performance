import psutil
import wmi
import csv
from datetime import datetime
from time import time

# Define the performance metrics to be measured (Windows equivalents)
METRICS = [
    "cpu_percent",
    "memory_percent",
    "disk_io_counters",
    "net_io_counters",
     "graphics_name",
    "graphics_ram_size",
     "graphics_DeviceID"
    
]

# Set the test duration (in seconds)
DURATION = 600
c = wmi.WMI()

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Sample every second
    return cpu_usage


def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    return memory_usage

def get_disk_io():
    disk_io = psutil.disk_io_counters()
    return disk_io

def get_network_io():
    net_io = psutil.net_io_counters()
    return net_io
def get_graphics_name():
    for graphics in c.Win32_VideoController():
        graphics_name=graphics.name
    return graphics_name    
def get_graphics_ID():
    for ID in c.Win32_VideoController():
        graphics_ID=ID.DeviceID
    return graphics_ID   
def get_graphics_size():
    for ram in c.Win32_VideoController():
        graphics_size=ram.AdapterRAM
        if graphics_size is None:
            graphics_size=0
        else:
            # Convert bytes to GB
            graphics_size = ram.AdapterRAM / (1024 ** 3)  
    return graphics_size 
           

def collect_performance_data():
    start_time = time()  # Record starting time
    results = {}
    for metric in METRICS:
        if metric == "cpu_percent":
            data = get_cpu_usage()
        elif metric == "memory_percent":
            data = get_memory_usage()
        elif metric == "disk_io_counters":
            data = get_disk_io()
        elif metric == "net_io_counters":
            data = get_network_io()
        elif metric =="graphics_name" :
            data=get_graphics_name()     
        elif metric == "graphics_DeviceID":
            data=get_graphics_ID()
          
        elif metric =="graphics_ram_size":
            data = get_graphics_size() 
             
             
        results[metric] = data
    end_time = time()  # Record ending time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    results["completion_time"] = elapsed_time  # Add elapsed time to results
    return results

def write_to_csv(results):
    column_names = list(results.keys())
    with open("performance_data.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        writer.writerow(results)

def main():
    performance_data = collect_performance_data()
    write_to_csv(performance_data)
    print(f"Performance data written to performance_data.csv (completed in {performance_data['completion_time']:.2f} seconds)")
    
if __name__ == "__main__":
    main()
