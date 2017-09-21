import os

__folderdest = "backup"

config = {
    # FTP
    "host": "localhost",
    "port": 54218,
    "user": "GeekPrueba",
    "pass": '',
    "route": "\\",
    "folderdest": __folderdest,
    "dest": os.path.join(os.getcwd(), __folderdest)
}
