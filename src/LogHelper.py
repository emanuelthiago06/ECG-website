from datetime import date

colors = {
    "HEADER": '\033[95m',
    "NORMALLOG": '\033[94m',
    "OK": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m'
}


def writeLog(type_msg, msg):
    f = open("log.txt", "a")
    f.write(str(date.today()) + " | " + type_msg + " | " + msg + "\n")
    f.close()


def processing(msg, active_flag=1, save_log=0):
    if active_flag:
        print(colors["NORMALLOG"] + msg + colors["ENDC"])
        if save_log:
            writeLog("Processing", msg)


def success(msg, active_flag=1, save_log=0):
    if active_flag:
        print(colors["OK"] + msg + colors["ENDC"])
        if save_log:
            writeLog("Processing", msg)


def warning(msg, active_flag=1, save_log=0):
    if active_flag:
        print(colors["WARNING"] + msg + colors["ENDC"])
        if save_log:
            writeLog("Processing", msg)


def error(msg, active_flag=1, save_log=0):
    if active_flag:
        print(colors["FAIL"] + msg + colors["ENDC"])
        if save_log:
            writeLog("Processing", msg)
