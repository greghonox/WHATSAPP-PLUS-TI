from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from os.path import isfile, basename
from tempfile import gettempdir
from ast import literal_eval
from webbrowser import get
from json import dump
from os import getcwd
from re import split

from scripts.whats_motor import *
from scripts.Padroes import *
from scripts.Log import *
import scripts.recursos


BRR = '\\'
DIRETORIO_SCRIPT = gettempdir()
TELEFONE_AJUDA = '19996147129'
ARQUIVO_LOG = DIRETORIO_SCRIPT + BRR + 'log.log'
ARQUIVO_MSG = DIRETORIO_SCRIPT + BRR + 'config.json'
__VERSION__ = '1.0'