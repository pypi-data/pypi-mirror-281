from typing import Union
from PySide6.QtWidgets import QLayout, QLayoutItem, QWidget
from PySide6.QtCore import (
    QSize, 
    QPoint, 
    Qt, 
    QRect, 
    QPropertyAnimation, 
    QParallelAnimationGroup
)

from ..core import AbstractQObject
from ..utils.alignment import Alignment


class _FlowLayout(QLayout):
    """ Flow layout """

    def __init__(self, 
                 parent=None, 
                 enable_animation: bool = False,
                 enable_tight: bool = False,
                 animation: QPropertyAnimation = None):
        """
        Parameters
        ----------
        parent:
            parent window or layout

        enable_animation: bool
            whether to add moving animation

        enable_tight: bool
            whether to use the tight layout when widgets are hidden
        """

        super().__init__(parent)

        self._items: list[QLayoutItem] = []
        self._anis: list[QPropertyAnimation] = []
        self._aniGroup = QParallelAnimationGroup(self)
        self._verticalSpacing = 10
        self._horizontalSpacing = 10
        self.enable_animation = enable_animation
        self.enable_tight = enable_tight
        self._custom_animation = animation

    def setAnimationEnabled(self, on: bool) -> None:
        self.enable_animation = on

    def setTightEnabled(self, on: bool) -> None:
        self.enable_tight = on

    def addItem(self, item):
        self._items.append(item)

    def addWidget(self, w):
        super().addWidget(w)

        if not self.enable_animation:
            return

        if self._custom_animation is not None:
            ani = self._custom_animation.__new__(QPropertyAnimation)
            ani.__init__(w, b"geometry")
            ani.setEndValue(QRect(QPoint(0, 0), w.size()))
        else:
            ani = QPropertyAnimation(w, b"geometry")
            ani.setEndValue(QRect(QPoint(0, 0), w.size()))
            ani.setDuration(300)

        w.setProperty('flowAni', ani)

        self._anis.append(ani)
        self._aniGroup.addAnimation(ani)

    def count(self):
        return len(self._items)

    def itemAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self._items):
            item = self._items[index]
            ani = item.widget().property('flowAni')
            if ani:
                self._anis.remove(ani)
                self._aniGroup.removeAnimation(ani)
                ani.deleteLater()

            return self._items.pop(index).widget()

        return None

    def removeWidget(self, widget):
        for i, item in enumerate(self._items):
            if item.widget() is widget:
                return self.takeAt(i)

    def removeAllWidgets(self):
        """ remove all widgets from layout """
        while self._items:
            self.takeAt(0)

    def takeAllWidgets(self):
        """ remove all widgets from layout and delete them """
        while self._items:
            w = self.takeAt(0)
            if w:
                w.deleteLater()

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        """ get the minimal height according to width """
        return self._doLayout(QRect(0, 0, width, 0), False)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._doLayout(rect, True)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        m = self.contentsMargins()
        size += QSize(m.left()+m.right(), m.top()+m.bottom())

        return size

    def setVerticalSpacing(self, spacing: int):
        """ set vertical spacing between widgets """
        self._verticalSpacing = spacing

    def verticalSpacing(self):
        """ get vertical spacing between widgets """
        return self._verticalSpacing

    def setHorizontalSpacing(self, spacing: int):
        """ set horizontal spacing between widgets """
        self._horizontalSpacing = spacing

    def horizontalSpacing(self):
        """ get horizontal spacing between widgets """
        return self._horizontalSpacing

    def _doLayout(self, rect: QRect, move: bool):
        """ adjust widgets position according to the window size """
        margin = self.contentsMargins()
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        rowHeight = 0
        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for i, item in enumerate(self._items):
            if item.widget() and not item.widget().isVisible() and self.enable_tight:
                continue

            nextX = x + item.sizeHint().width() + spaceX

            if nextX - spaceX > rect.right() and rowHeight > 0:
                x = rect.x() + margin.left()
                y = y + rowHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                rowHeight = 0

            if move:
                if not self.enable_animation:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
                else:
                    self._anis[i].stop()
                    self._anis[i].setEndValue(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            rowHeight = max(rowHeight, item.sizeHint().height())

        if self.enable_animation:
            self._aniGroup.stop()
            self._aniGroup.start()

        return y + rowHeight - rect.y()


class FlowLayout(AbstractQObject, _FlowLayout):
    def __init__(self,
                 *,
                 children: list[Union[QWidget,
                                      QLayoutItem,
                                      Alignment]] = None,
                 enable_animation: bool = False,
                 enable_tight: bool = False,
                 animation: QPropertyAnimation = None,
                 **kwargs) -> None:
        _FlowLayout.__init__(self, None, enable_animation, enable_tight, animation)
        super().__init__(**kwargs)

        if not children:
            return

        for child in children:
            if isinstance(child, Alignment):
                _widget = child.child
                if isinstance(_widget, QWidget):
                    self.addWidget(_widget)
                elif isinstance(_widget, QLayoutItem):
                    self.addItem(_widget)

                self.setAlignment(_widget, child.alignment)

            elif isinstance(child, QLayoutItem):
                self.addItem(child)

            elif isinstance(child, QWidget):
                self.addWidget(child)
