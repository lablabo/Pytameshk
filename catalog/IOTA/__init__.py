from __future__ import absolute_import, division, print_function, unicode_literals

from argparse import ArgumentParser
from pprint import pprint
from sys import argv
from typing import Text

from requests.exceptions import ConnectionError
from six import text_type

from iota import BadApiResponse, StrictIota, __version__


class controller:

    def __init__(self, action, libraries):
        print("Start IOTA")



