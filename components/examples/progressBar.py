
import re
import os
import ftplib
import ntpath

import sys
import time

local_path = "archive.zip"
remote_path = "/remote/path/archive.zip"

file = open(local_path, 'wb')

size = ftp.size(remote_path)

pbar = ProgressBar(widgets=widgets, maxval=size)
pbar.start()


def file_write(data):
    file.write(data)
    global pbar
    pbar += len(data)


ftp.retrbinary("RETR " + remote_path, file_write)
