import subprocess
import datetime
from send_email import *

ts_now = '{:%Y-%m-%d_%H%M%S}'.format(datetime.datetime.now())
file_with_ts = 'attachment_' + ts_now + '.pdf'

subprocess.run(["scan-pdf/src/scan-pdf", "--flatbed", "--color-mode", "color", file_with_ts])

subprocess.run(["ocrmypdf", "-r", "--rotate-pages-threshold", "6", "-O", "3", file_with_ts, file_with_ts])

send_email(file_with_ts, ts_now)