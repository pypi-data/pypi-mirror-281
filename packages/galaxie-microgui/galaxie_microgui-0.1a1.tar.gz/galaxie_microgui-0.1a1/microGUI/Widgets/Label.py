from microGUI.Widgets.Basic import Basic


class Label(Basic):
    """
    A text, bitmap, or image label.

    The Label class provides a text string, bitmap, or image for labeling other widgets. You can have text pop up in
    a balloon to provide further meaning to the label.

    .. seealso::
     - :py:class:`~microGUI.Widgets.Button.Button`
     - :py:attr:`~microGUI.Widgets.Button.Button.Text`
    """
    def __init__(self):
        Basic.__init__(self)
