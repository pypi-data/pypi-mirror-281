from enum import Flag, auto


class AnchorStyles(Flag):
    """
    Anchor flags for :class:`~microGUI.Widgets.Widget.Widget` resource :func:`microGUI.Widget.Arguments.anchor_flags`.

    Anchor flags specify how the widget is anchored to its parent.

   .. list-table:: **Enumerator**
      :widths: 25 75
      :header-rows: 0
      :class: tight-table

      * - **LeftAnchoredRight**
        - Anchors the widget's left extent to the right edge of its parent's canvas.
      * - **RightAnchoredRight**
        - Anchors the widget's right extent to the right edge of its parent's canvas.
      * - **TopAnchoredBottom**
        - Anchors the widget's top extent to the bottom edge of its parent's canvas.
      * - **BottomAnchoredBottom**
        - Anchors the widget's bottom extent to the bottom edge of its parent's canvas.
      * - **LeftAnchoredLeft**
        - Anchors the widget's left extent to the left edge of its parent's canvas.
      * - **RightAnchoredLeft**
        - Anchors the widget's right extent to the left edge of its parent's canvas.
      * - **TopAnchoredTop**
        - Anchors the widget's top extent to the top edge of its parent's canvas.
      * - **BottomAnchoredTop**
        - Anchors the widget's bottom extent to the top edge of its parent's canvas.
      * - **BalloonsOn**
        - If a child widget has been assigned a balloon, pop up the balloon as soon as the pointer passes over the
          child widget; otherwise delay the pop-up for 1.25 seconds.
      * - **Bottom**
        - The widget is anchored to the bottom edge of its container.
      * - **Left**
        - The widget is anchored to the left edge of its container.
      * - **NoWhere**
        - The widget is not anchored to any edges of its container.
      * - **Right**
        - The widget is anchored to the right edge of its container.
      * - **Top**
        - The widget is anchored to the top edge of its container.

    """
    LeftAnchoredRight = auto()
    RightAnchoredRight = auto()
    TopAnchoredBottom = auto()
    BottomAnchoredBottom = auto()
    LeftAnchoredLeft = auto()
    RightAnchoredLeft = auto()
    TopAnchoredTop = auto()
    BottomAnchoredTop = auto()
    BalloonsOn = auto()
    Bottom = BottomAnchoredBottom
    Left = LeftAnchoredLeft
    NoneAnchoredNone = auto()
    Right = RightAnchoredRight
    Top = TopAnchoredTop
    All = LeftAnchoredRight | RightAnchoredRight | TopAnchoredBottom | BottomAnchoredBottom | LeftAnchoredLeft | RightAnchoredLeft | TopAnchoredTop | BottomAnchoredTop | BalloonsOn


class BalloonPosition(Flag):
    """
    Indicates where the balloon with the :class:`~microGUI.Widgets.Label.Label`'s text pops up.

    Apply to :py:attr:`microGUI.Widgets.Label.Label.BalloonPosition` property.

   .. seealso::
    - :py:attr:`microGUI.Widgets.Label.Label.BalloonPosition`
    - :py:attr:`microGUI.Widgets.Label.Label.Arguments.balloon_position`

   .. list-table:: **Enumerator**
      :widths: 25 75
      :header-rows: 0
      :class: tight-table

      * - **Inplace**
        - keep :class:`~microGUI.Widgets.Label.Label` balloon inplace.
      * - **Top**
        - place :class:`~microGUI.Widgets.Label.Label` balloon to top.
      * - **Left**
        - place :class:`~microGUI.Widgets.Label.Label` balloon to left.
      * - **Right**
        - place :class:`~microGUI.Widgets.Label.Label` balloon to right.
      * - **Bottom**
        - place :class:`~microGUI.Widgets.Label.Label` balloon to bottom.
    """
    Inplace = auto()
    Top = auto()
    Left = auto()
    Right = auto()
    Bottom = auto()
