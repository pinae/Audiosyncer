#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gui import MainWindow
from correlate import correlate
import argparse
from PySide.QtGui import QApplication


def create_interface():
    app = QApplication([])
    window = MainWindow()
    app.exec_()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync better Audio files.")
    parser.add_argument('-c', '--clip',
                        help="Video or audio with low quality",
                        metavar='low_quality_clip',
                        type=str,
                        default='',
                        required=False)
    parser.add_argument('-a', '--audio',
                        help="Audio with better quality",
                        metavar='high_quality_audio',
                        type=str,
                        default='',
                        required=False)
    parser.add_argument('-o', '--out',
                        help="Filename for the mixed output",
                        metavar='output_filename',
                        type=str,
                        default='',
                        required=False)
    args = parser.parse_args()
    if not args.clip and not args.audio and not args.out:
        create_interface()
    elif args.clip and args.audio and args.out:
        correlate(args.clip, args.audio, args.out)
    else:
        parser.print_help()

