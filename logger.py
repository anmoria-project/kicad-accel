

# debug=0, info=1, warn=2, error=3
log_debug = 0
log_note = 1
log_warn = 2
log_error = 3
log_level_system = 1

def log(lvl, msg):
    global log_level_system
    prefix = ''
    if log_debug == lvl:
        prefix = "DEBUG: " + msg
    if log_note == lvl:
        prefix = "NOTE: " + msg
    if log_warn == lvl:
        prefix = "WARN: " + msg
    if log_error == lvl:
        prefix = "ERROR: " + msg

    if lvl < log_level_system:
        return
    else:
        print(prefix)