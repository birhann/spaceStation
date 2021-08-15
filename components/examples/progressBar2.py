from glob import glob
import os
import ftplib
import ntpath
from tqdm import tqdm

ntpath.basename("a/b/c")


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


FileTransferList = [y for x in os.walk(
    '/tmp/rippedMovies') for y in glob(os.path.join(x[0], '*.mkv'))]

global ftp


def FTP_GLOB_transfer(URL, UserName, Password):
    ftp = ftplib.FTP(URL, UserName, Password)   # connect to host, default port
    print URL, UserName, Password
    for file in FileTransferList:
        FileName = path_leaf(file)
        filesize = os.path.getsize(file)
        print file
        TheFile = open(file, 'r')
        with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc='Uploading......', total=filesize) as tqdm_instance:
            ftp.storbinary('STOR ' + FileName, TheFile, 2048,
                           callback=lambda sent: tqdm_instance.update(len(sent)))
        TheFile.close()
    ftp.quit()
    ftp = None
