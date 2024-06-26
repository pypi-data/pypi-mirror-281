import os

from typing import Union
from PySide6.QtCore import QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from ..core import QObjectDec


class UiLoader(QObjectDec, QUiLoader):
    '''
    UiLoader(
        ui="/path/to/file.ui",
        ...
    ) # -> QWidget
    '''

    def __init__(self, ui: Union[str, bytes, os.PathLike, QIODevice], **kwargs) -> QWidget:
        QUiLoader.__init__(self)
        super().__init__(**kwargs)

        return self.load(ui)