from util import *
from . import object
from .arg import Arg

class Message:
    # TODO: figure out a way to remove global time offset
    base_time = None

    def __init__(self, abs_time, obj, sent, name, args):
        assert isinstance(abs_time, float) or isinstance(abs_time, int)
        assert isinstance(obj, object.Base)
        assert isinstance(sent, bool)
        assert isinstance(name, str)
        for arg in args:
            assert isinstance(arg, Arg.Base)
        if Message.base_time == None:
            Message.base_time = abs_time
        self.timestamp = abs_time - Message.base_time
        self.obj = obj
        self.sent = sent
        self.name = name
        self.args = args
        self.destroyed_obj = None

    def resolve(self, connection):
        if not self.obj.resolved():
            self.obj = self.obj.resolve(connection)
        if self.obj.type == 'wl_registry' and self.name == 'bind':
            assert isinstance(self.args[3], Arg.Object)
            self.args[3].set_type(self.args[1].value)
        if self.obj == connection.display and self.name == 'delete_id' and len(self.args) > 0:
            self.destroyed_obj = connection.look_up_most_recent(self.args[0].value, None)
            self.destroyed_obj.destroy(self.timestamp)
        for i, arg in enumerate(self.args):
            arg.resolve(connection, self, i)

    def used_objects(self):
        result = []
        for i in self.args:
            if isinstance(i, Arg.Object):
                result.append(i.obj)
        if self.destroyed_obj:
            result.append(self.destroyed_obj)
        return result

    def __str__(self):
        destroyed = ''
        if self.destroyed_obj:
            destroyed = (
                color(timestamp_color, ' -- ') +
                color('1;31', 'destroyed ') +
                str(self.destroyed_obj) +
                color(timestamp_color, ' after {:0.4f}s'.format(self.destroyed_obj.lifespan())))
        return (
            (color('37', '→ ') if self.sent else '') +
            str(self.obj) + ' ' +
            color(message_color, self.name) + color(timestamp_color, '(') +
            color(timestamp_color, ', ').join([str(i) for i in self.args]) + color(timestamp_color, ')') +
            destroyed +
            (color(timestamp_color, ' ↲') if not self.sent else ''))

    def show(self, out):
        out.show(color('37', '{:7.4f}'.format(self.timestamp)) + ' ' + str(self))

