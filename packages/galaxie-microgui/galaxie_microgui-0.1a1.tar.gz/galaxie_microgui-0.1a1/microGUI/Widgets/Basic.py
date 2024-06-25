from microGUI.Widgets.Widget import Widget


class Basic(Widget):
    """
    A superclass of basic resources for most widgets.

    The :class:`~microGUI.Widgets.Basic.Basic` superclass provides basic resources for all widgets.

    It provides the fundamental events for:
     - getting/losing focus activating button press
     - release
     - repeat

    Also, Basic supports:
     - toggle buttons
     - autohighlighting

    and provides properties for:
     - margins
     - bevel colors
     - outline and inline colors
     - draw color
     - fill color
     - fill pattern.

    """
    def __init__(self):
        super().__init__()
