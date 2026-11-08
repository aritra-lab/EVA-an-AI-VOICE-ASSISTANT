COMMAND_HANDLERS = []

def register(handler):
    COMMAND_HANDLERS.append(handler)

def process(command):
    for handler in COMMAND_HANDLERS:
        if handler(command):
            return True

    return False