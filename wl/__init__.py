'''
Module handles the internal representation of Wayland messages and data
Also it parses Wayland protocol XML files and uses them to add additional context
(such as the names of message arguments)
'''

from .connection import Connection
from .object import Object
from .message import Message
from .arg import Arg
