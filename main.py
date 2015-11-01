#!/usr/bin/env python

from audi import launcher
from settings import config

app = launcher.create_app(conf=config)
