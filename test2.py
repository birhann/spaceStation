import ftplib

FTP_HOST = "192.168.137.178"
FTP_USER = "esp32"
FTP_PASS = "esp32"
# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"
# local file name you want to upload
filename = "zipdosyasi.zip"
print("---------")
with open(filename, "rb") as file:
    # use FTP's STOR command to upload the file
    ftp.storbinary(f"STOR {filename}", file)

ftp.dir()
ftp.quit()


# data = b'<62319>,<  2>,<15:08:21>,<00:00:00>,<   0.00>,<  0.0>,<  0.0>,<0>,<0.25>,<0.000000>,<0.000000>,<  0.0>,< BEKLEMEDE>,<   0>,<   0>,<   0>,<DONUS>,<VIDEO>,<0.0>;\r\n'
# # telemetry = [i.strip() for i in ]
# telemetry = [i[1:-1].strip() for i in data.decode("utf-8").split(",")[0:-1]]
# print(telemetry)
