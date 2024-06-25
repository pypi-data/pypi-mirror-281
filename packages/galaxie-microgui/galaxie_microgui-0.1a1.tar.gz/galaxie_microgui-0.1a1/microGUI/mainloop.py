
class MainLoop:

    def __init__(self):
        self.__running = None
        self.running = None

    @property
    def running(self) -> bool:
        """
        Gets or sets a value indicating whether the widget can accept data that the user drags onto it.

        :getter: Return ``true`` if the mainloop operations are running; otherwise, false. The default \
                 is ``false``.
        :setter: Sets running property
        :raise TypeError: When not set running with a bool type or None
        :type: bool
        """
        return self.__running

    @running.setter
    def running(self, value):
        if value is None:
            value = False
        if value is not None and not isinstance(value, bool):
            raise TypeError("'running' property value must be a bool type or None")
        if self.running != value:
            self.__running = value

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
