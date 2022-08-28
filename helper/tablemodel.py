from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        # for setting columns name
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Pokemon Name"
            return "Count"
        # for setting rows name
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return ""
