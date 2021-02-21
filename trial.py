#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ale_python_interface import ALEInterface

ale = ALEInterface()

rom_file = str.encode('这里写path')
ale.loadROM(rom_file)