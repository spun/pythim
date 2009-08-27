#! /usr/bin/env python

import __builtin__
import os.path
import sys
import logging
import sys
import pygtk
if not sys.platform == 'win32':
        pygtk.require('2.0')
import gtk
import gobject
import locale
from gui import Gui

import cons

class Pyim:
	""""""
	def __init__(self):
		""""""
		#exception hook
		self.old_exception_hook = sys.excepthook
		sys.excepthook = self.exception_hook

	def exception_hook(self, type, value, trace):
		""""""
		file_name = trace.tb_frame.f_code.co_filename
		line_no = trace.tb_lineno
		exception = type.__name__
		self.logger.critical("File %s line %i - %s: %s" % (file_name, line_no, exception, value))
		print self.old_exception_hook(type, value, trace)
		self.exit(-1)

	def exit(self, arg=0):
		""""""
		self.logger.debug("Exit: %s" % arg)
		exit(arg)

if __name__ == "__main__":
	gobject.threads_init()
	p = Pyim()
	Gui()
	gtk.main()
