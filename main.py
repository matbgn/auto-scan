#!/usr/bin/env python3

import subprocess
import datetime
import time

from send_email import send_email
import os
from dotenv import load_dotenv
from PIL import Image, ImageFile
import fnmatch

load_dotenv()

try:
    emails = os.environ['EMAIL_RECIPIENTS']
except KeyError:
    emails = "N/A"

try:
    subject = os.environ['SUBJECT']
except KeyError:
    subject = "N/A"

try:
    scan_mode = os.environ['SCAN_MODE']
except KeyError:
    scan_mode = "Flatbed"

try:
    paper_format = os.environ['PAPER_FORMAT']
except KeyError:
    paper_format = 'A4'

try:
    batch_total = int(os.environ['BATCH_TOTAL'])
except KeyError:
    batch_total = 1

try:
    paperless_location = os.environ['PAPERLESS_LOCATION']
except KeyError:
    paperless_location = './consume/'


def process_raw_images(_source_file):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for i in range(len(fnmatch.filter(os.listdir(), '*.pnm'))):
        tmpImg = Image.open(f"out{i + 1}.pnm")
        tmpImg = tmpImg.crop((0, 0, 2550, 3500))
        tmpImg.save(f"out{i + 1}.pdf")
    subprocess.run(f'pdfunite out*.pdf {_source_file}', shell=True)
    subprocess.run(f'rm -rf *.pnm', shell=True)


def main(_emails=emails, _subject=subject, _scan_mode=scan_mode, _paper_format=paper_format, _batch_total=batch_total,
         as_web_interface=False, is_local_scan=False):
    ts_now = '{:%Y-%m-%d_%H%M%S}'.format(datetime.datetime.now())
    file_with_ts = 'attachment_' + ts_now + '.pdf'

    total_range = list(reversed(range(_batch_total + 1)))
    total_range.insert(0, 0)

    while _batch_total > 0:
        source_file = "source" + str(total_range[_batch_total]) + ".pdf"

        if _scan_mode == 'ADF':
            print('ADF scanning mode')
            subprocess.run(["scanimage", "-b", "-d", "hpaio:/net/OfficeJet_Pro_7740_series?ip=192.168.8.100",
                            "--source=ADF", "--resolution", "300", "--mode", "Color", "--format=pnm"])
            process_raw_images(source_file)
        elif _scan_mode == 'Duplex':
            print('Duplex scanning mode')
            subprocess.run(["scanimage", "-b", "-d", "hpaio:/net/OfficeJet_Pro_7740_series?ip=192.168.8.100",
                            "--source=Duplex", "--resolution", "300", "--mode", "Color", "--format=pnm"])
            process_raw_images(source_file)
        else:
            print('Flatbed scanning mode')
            subprocess.run(["scan-pdf/src/scan-pdf", "--flatbed", "--color-mode", "color",
                            "--paper-format", _paper_format, source_file])

        subprocess.run(["ocrmypdf", "-r", "--rotate-pages-threshold", "6", "-O", "3", source_file, source_file])

        if _batch_total > 1:
            msg = "Press Enter to continue..."
            print(msg)
            time.sleep(5) if as_web_interface else input()

        else:
            pass

        _batch_total = _batch_total - 1

    subprocess.run(f'pdfunite source*.pdf {file_with_ts}', shell=True)

    send_email(_subject, _emails, file_with_ts, ts_now)

    if is_local_scan:
        subprocess.run(f'mv {file_with_ts} {paperless_location}', shell=True)

    subprocess.run(f'rm -rf *.pdf', shell=True)


if __name__ == '__main__':
    main()
