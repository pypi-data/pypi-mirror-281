from typing import Union
from PySide6.QtWidgets import QStackedWidget, QWidget
from ..core.objects.routes import Routes
from ..core import AbstractWidget


class StackedWidget(AbstractWidget, QStackedWidget):
    def __init__(self, 
                 *,
                 children: Union[list[QWidget], Routes, dict] = None,
                 **kwargs):
        QStackedWidget.__init__(self)
        super().__init__(**kwargs)

        if not children:
            return

        if isinstance(children, (Routes, dict)):
            self.routes = Routes("/", **children) if isinstance(children, dict) else children
            self.routes._set_stacked(self)
            for route, child in children.items():
                self.routes.add(route, child)
        else:
            for child in children:
                self.addWidget(child)