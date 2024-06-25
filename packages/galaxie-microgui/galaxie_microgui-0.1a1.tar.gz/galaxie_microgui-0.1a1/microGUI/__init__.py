

from microGUI.mainloop import MainLoop


# 1
from microGUI.Widgets import Widget

# 2
from microGUI.Widgets.Basic import Basic
from microGUI.Widgets.Timer import Timer

# 3
from microGUI.Widgets.bargraph import BarGraph
from microGUI.Widgets.calendar import Calendar
from microGUI.Widgets.clock import Clock
from microGUI.Widgets.Container import Container
from microGUI.Widgets.gauge import Gauge
from microGUI.Widgets.graphic import Graphic
from microGUI.Widgets.Label import Label
from microGUI.Widgets.meter import Meter
from microGUI.Widgets.mtrend import MTrend
from microGUI.Widgets.raw import Raw
from microGUI.Widgets.separator import Separator
from microGUI.Widgets.trend import Trend
from microGUI.Widgets.updown import UpDown

# 4
from microGUI.Widgets.bkgd import Bkgd
from microGUI.Widgets.client import Client
from microGUI.Widgets.compound import Compound
from microGUI.Widgets.disjoint import Disjoint
from microGUI.Widgets.fontsel import FontSel
from microGUI.Widgets.group import Group
from microGUI.Widgets.imagearea import ImageArea
from microGUI.Widgets.oscontainer import OsContainer
from microGUI.Widgets.pane import Pane
from microGUI.Widgets.panelgroup import PanelGroup
from microGUI.Widgets.printsel import PrintSel
from microGUI.Widgets.region import Region
from microGUI.Widgets.scrollarea import ScrollArea

APPLICATION_VERSION = "0.1a1"
APPLICATION_AUTHORS = "Tuuux, Mo"

mainloop = MainLoop()


__all__ = [
    "mainloop"
]


