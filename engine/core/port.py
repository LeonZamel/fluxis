import abc


class Port(abc.ABC):
    def __init__(self, node):
        self.node = node
        self._data = None
        self.has_data = False


class OutPort(Port):
    def __init__(self, node):
        super().__init__(node)

    @property
    def data(self):
        raise Exception("Can't get data from out port")

    @data.setter
    def data(self, data):
        self.has_data = True
        self._data = data
        self.node.flow.send_from_port(self, data)


class InPort(Port):
    def __init__(self, node):
        super().__init__(node)
        # If the port is locked it will accept data but keep the old value locked
        self.locked = False

    @property
    def data(self):
        if self.has_data:
            if not self.locked:
                self.has_data = False
            return self._data
        else:
            raise ValueError("Port does not have data")

    @data.setter
    def data(self, data):
        self.has_data = True
        self._data = data
        self.node.notify_port_state_changed()
