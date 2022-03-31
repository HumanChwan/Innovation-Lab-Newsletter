def DEBUG(*message):
    debug_pretext = "\033[33m[+] DEBUG:\033[37m"
    print(f'{debug_pretext} {message[0] if len(message) == 1 else message}')


def LOG(*message):
    log_pretext = "\033[34m[+] LOG:\033[37m"
    print(f'{log_pretext} {message[0] if len(message) == 1 else message}')


def ERROR(*message):
    error_pretext = "\033[31m[+] ERROR:\033[37m"
    print(f'{error_pretext} {message[0] if len(message) == 1 else message}')
