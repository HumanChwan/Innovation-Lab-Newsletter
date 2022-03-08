def DEBUG(*message):
    DEBUG_PRETEXT = "\033[33m[+] DEBUG:\033[37m"
    print(f'{DEBUG_PRETEXT} {message[0] if len(message) == 1 else message}')


def LOG(*message):
    LOG_PRETEXT = "\033[34m[+] LOG:\033[37m"
    print(f'{LOG_PRETEXT} {message[0] if len(message) == 1 else message}')


def ERROR(*message):
    ERROR_PRETEXT = "\033[31m[+] ERROR:\033[37m"
    print(f'{ERROR_PRETEXT} {message[0] if len(message) == 1 else message}')
