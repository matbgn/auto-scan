#!/usr/bin/env python3

import subprocess
import datetime
from send_email import send_email
import os
from dotenv import load_dotenv

load_dotenv()

ts_now = '{:%Y-%m-%d_%H%M%S}'.format(datetime.datetime.now())
file_with_ts = 'attachment_' + ts_now + '.pdf'

try:
    batch_total = int(os.environ['BATCH_TOTAL'])
except KeyError:
    batch_total = 1

total_range = list(reversed(range(batch_total + 1)))
total_range.insert(0, 0)

while batch_total > 0:
    source_file = "source" + str(total_range[batch_total]) + ".pdf"

    if os.environ['SCAN_MODE'] == 'ADF':
        print('ADF scanning mode')
        subprocess.run(["scan-pdf/src/scan-pdf", "--color-mode", "color", source_file])
        # subprocess.run(["scanimage", "-b", "-d", "hpaio:/net/OfficeJet_Pro_7740_series?ip=192.168.8.100", "--source=ADF", "--resolution", "300", "--mode", "Color", "--format=pnm"])
        # subprocess.run(["convert", "-depth", "4", "-density", "300", "-compress", "zip", "out*.pnm", file_with_ts])
    elif os.environ['SCAN_MODE'] == 'Duplex':
        print('Duplex scanning mode')
        subprocess.run(["scan-pdf/src/scan-pdf", "--duplex", "--color-mode", "color", source_file])
    else:
        print('Flatbed scanning mode')
        subprocess.run(["scan-pdf/src/scan-pdf", "--flatbed", "--color-mode", "color", source_file])

    subprocess.run(["ocrmypdf", "-r", "--rotate-pages-threshold", "6", "-O", "3", source_file, source_file])

    input("Press Enter to continue...") if batch_total > 1 else None

    batch_total = batch_total - 1


subprocess.run(f'pdfunite source*.pdf {file_with_ts}', shell=True)

send_email(file_with_ts, ts_now)

subprocess.run(f'rm -rf *.pdf', shell=True)