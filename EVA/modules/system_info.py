import platform
import psutil

def get_system_info():
    cpu = platform.processor()
    ram = round(psutil.virtual_memory().total / (1024**3), 2)

    return (
        f"Computer Name: {platform.node()}\n"
        f"System: {platform.system()}\n"
        f"Processor: {cpu}\n"
        f"RAM: {ram} GB"
    )