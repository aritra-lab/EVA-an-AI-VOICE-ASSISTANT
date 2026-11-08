import os

def shutdown_pc():
    os.system("shutdown /s /t 2")
    return "SHUTTING DOWN YOUR COMPUTER."

def restart_pc():
    os.system("shutdown /r /t 2")
    return "RESTARTING YOUR COMPUTER."

def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "LOCKING YOUR COMPUTER."

def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "PUTTING THE COMPUTER TO SLEEP."