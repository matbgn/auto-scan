import subprocess
import datetime
from send_email import send_email
import os
from dotenv import load_dotenv

load_dotenv()

ts_now = '{:%Y-%m-%d_%H%M%S}'.format(datetime.datetime.now())
file_with_ts = 'attachment_' + ts_now + '.pdf'

if os.environ['SCAN_MODE'] == 'ADF':
    print('ADF scanning mode')
    subprocess.run(["scan-pdf/src/scan-pdf", "--color-mode", "color", file_with_ts])
elif os.environ['SCAN_MODE'] == 'Duplex':
    print('Duplex scanning mode')
    subprocess.run(["scan-pdf/src/scan-pdf", "--duplex", "--color-mode", "color", file_with_ts])
else:
    print('Flatbed scanning mode')
    subprocess.run(["scan-pdf/src/scan-pdf", "--flatbed", "--color-mode", "color", file_with_ts])

subprocess.run(["ocrmypdf", "-r", "--rotate-pages-threshold", "6", "-O", "3", file_with_ts, file_with_ts])

send_email(file_with_ts, ts_now)