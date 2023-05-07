import random

def get_response(message: str) -> str:
    p_message = message.lower()
    if 'ambatukam' in p_message:
        return 1
    if "พศิน" in message:
        return 2
    if p_message == '_read':
        return 'read'
    else:
        pass