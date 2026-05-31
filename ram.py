import psutil

def get_ram_info():
    mem = psutil.virtual_memory()
    ram_val = mem.percent
    mem_used = round(mem.used / (1024**3), 1)
    mem_total = round(mem.total / (1024**3), 1)
    
    return ram_val, mem_used, mem_total