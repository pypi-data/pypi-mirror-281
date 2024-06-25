from microGUI.Widgets import AnchorStyles


class Widget:
    """
    Widget is the fundamental superclass. All widgets belong to a subclass of Widget.

    .. seealso:: dynamic_widget_caste()
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__AllowDrop = None
        self.AllowDrop = None

        self.__Anchor = None
        self.Anchor = None

        self.__BevelWidth = None
        self.BevelWidth = None

    @property
    def AllowDrop(self):
        """
        Gets or sets a value indicating whether the widget can accept data that the user drags onto it.

        .. seealso::
         - DragEventArgs
         - DragOver
         - DragDrop
         - DragEnter
         - DragLeave
         - DoDragDrop

        :getter: Return ``true`` if drag-and-drop operations are allowed in the widget; otherwise, ``false``.
                 The default is ``false``.
        :setter: Sets AllowDrop property
        :raise TypeError: When not set AllowDrop with a bool type or None
        :type: bool
        """
        return self.__AllowDrop

    @AllowDrop.setter
    def AllowDrop(self, value):
        if value is None:
            value = False
        if value is not None and not isinstance(value, bool):
            raise TypeError("'AllowDrop' property value must be a bool type or None")
        if self.AllowDrop != value:
            self.__AllowDrop = value

    @property
    def Anchor(self):
        """
        Gets or sets a value indicating whether the widget can accept data that the user drags onto it.

        Exemple
        =======

        .. code-block:: python
          :emphasize-lines: 2

          widget = Widget()
          widget.Anchor = ( Widgets.AnchorStyles.Bottom | Widgets.AnchorStyles.Right )

        .. attention::
         Use the Widget.Anchor property to define how a widget is automatically resized as its parent widget is \
         resized. Anchoring a widget to its parent widget ensures that the anchored edges remain in the same \
         position relative to the edges of the parent widget when the parent widget is resized. \
         You can anchor a widget to one or more edges of its container. For example, if you have a Container \
         with a Button whose microGUI.Widgets.Button.Anchor property value is set to microGUI.Widgets.AnchorStyles.Top
         and :py:class:`microGUI.Widgets.AnchorStyles.Bottom`, \
         the microGUI.Widgets.Button is stretched to maintain the anchored distance to the top and bottom edges of the \
         :py:class:`~microGUI.Widgets.Container.Container` as the Height of the \
         :py:class:`~microGUI.Widgets.Container.Container` is increased.

        .. seealso::
         - :py:class:`microGUI.Widgets.AnchorStyles`
         - Dock
         - Layout

        :getter: Return ``True`` if drag-and-drop operations are allowed in the widget; otherwise, ``False``.
                 The default is ``False``.
        :setter: Sets :py:attr:`~microGUI.Widgets.Widget.Widget.Anchor` property
        :raise TypeError: When not set AllowDrop with a bool type or None
        :type: A bitwise combination of the Flags :py:class:`microGUI.Widgets.AnchorStyles` values.
        """
        return self.__Anchor

    @Anchor.setter
    def Anchor(self, value):
        if value is None:
            value = AnchorStyles.NoneAnchoredNone
        if value is not None and not isinstance(value, AnchorStyles):
            raise TypeError("'Anchor' property value must be a AnchorStyles type or None")
        if self.Anchor != value:
            self.__Anchor = value

    @property
    def BevelWidth(self):
        """
        Gets or sets the bevel width of the widget.

        .. attention::
         The width of the widget's bevel if the widget is highlighted and is to draw a bevel.

        .. seealso::
         - :py:class:`microGUI.Widgets.Widget.ThisFlagsHighlighted`
         - :py:class:`microGUI.Widgets.Basic.ThisFlags.Basic`

        :getter: The bevel width of the widget in chars.
        :setter: Sets :py:attr:`~microGUI.Widgets.Widget.Widget.BevelWidth` property
        :raise TypeError: When not set BevelWidth with a int type or None
        :type: int
        """
        return self.__BevelWidth

    @BevelWidth.setter
    def BevelWidth(self, value):
        if value is None:
            value = 0
        if value is not None and not isinstance(value, int):
            raise TypeError("'BevelWidth' property value must be a int type or None")
        if self.BevelWidth != value:
            self.__BevelWidth = value

    def get(self):
        """
        Returns the stored pointer.

        :return: self from widget point of view
        :rtype: Widget
        """
        return self

    # def Contains(self, widget) -> bool:
    #     """
    #     Retrieves a value indicating whether the specified widget is a child of the widget.
    #
    #     :Example:
    #
    #     def MakeLabelVisible():
    #         if main_window.Contains(label1):
    #             label1.BringToFront()
    #
    #
    #     .. seealso:: BringToFront() Send
    #
    #     :param widget: The Widget to evaluate
    #     :type widget: Widget
    #     :return: ``true`` if the specified widget is a child of the widget; otherwise, ``false``.
    #     :rtype: bool
    #     """
    #     raise NotImplemented
