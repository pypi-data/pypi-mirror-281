#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demo"""

import sys
from typing import List, Callable

import qtpy
from qtpy import QtCore, QtGui, QtWidgets as QtWid

import dvg_pyqt_controls as c

print(
    f"{qtpy.API_NAME:9s} "
    f"{qtpy.QT_VERSION}"  # pyright: ignore[reportPrivateImportUsage]
)

# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------


class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setWindowTitle("Demo: dvg_pyqt_controls")
        self.setGeometry(350, 50, 800, 660)
        self.setStyleSheet(c.SS_GROUP)

        # Adjust font size while keeping default font family
        self.main_font = QtGui.QFont(QtGui.QGuiApplication.font().family(), 9)
        self.setFont(self.main_font)  # Keep
        QtGui.QGuiApplication.setFont(self.main_font)  # Keep

        def build_group(
            create_control_fun: Callable[[], QtWid.QPushButton],
            N: int = 8,
            off_text: str = "Off",
            on_text: str = "On",
            **kwargs,
        ) -> QtWid.QGroupBox:

            buttons: List[QtWid.QPushButton] = []
            labels: List[QtWid.QLabel] = []

            for k in range(N):
                if k < 2:
                    checked = False
                    enabled = False
                elif k < 4:
                    checked = True
                    enabled = False
                elif k < 6:
                    checked = False
                    enabled = True
                else:
                    checked = True
                    enabled = True

                button_text = on_text if checked else off_text
                label_text = "Enabled & " if enabled else "Disabled & "
                label_text += "True" if checked else "False"

                p = {"text": button_text, "checked": checked}
                p = {**p, **kwargs}
                button = create_control_fun(**p)
                button.setEnabled(enabled)

                buttons.append(button)
                labels.append(QtWid.QLabel(text=label_text))

            # Make the text of the buttons change on click
            if N == 8:
                for idx in range(4, 8):
                    buttons[idx].clicked.connect(
                        lambda state, button=buttons[idx]: button.setText(
                            on_text if state else off_text
                        )
                    )

            # Put the buttons and labels in a grid
            grid = QtWid.QGridLayout()
            grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

            for idx, button in enumerate(buttons):
                row_idx = grid.rowCount()
                grid.addWidget(labels[idx], row_idx, 0)
                grid.addWidget(button, row_idx, 1)

            if create_control_fun.__name__ == "create_Relay_button":
                grid.setVerticalSpacing(0)

            # Put the grid in a group box
            descr = create_control_fun.__name__
            descr = descr.replace("create_", "")
            descr = descr.replace("_", " ")
            grpb = QtWid.QGroupBox(descr)
            grpb.setLayout(grid)

            return grpb

        # ----------------------------------------------------------------------
        #   LEDs
        # ----------------------------------------------------------------------

        p = {
            "stretch": 0,
            "alignment": QtCore.Qt.AlignmentFlag.AlignTop,
        }

        hbox_1 = QtWid.QHBoxLayout()
        hbox_1.addWidget(build_group(c.create_LED_indicator, 4, "0", "1"), **p)
        hbox_1.addWidget(build_group(c.create_LED_indicator_rect, 4), **p)
        hbox_1.addWidget(build_group(c.create_error_LED, 4, "0", "1"), **p)
        hbox_1.addWidget(build_group(c.create_tiny_LED, 4, "", ""), **p)
        hbox_1.addWidget(build_group(c.create_tiny_error_LED, 4, "", ""), **p)

        # ----------------------------------------------------------------------
        #   Buttons
        # ----------------------------------------------------------------------

        hbox_2 = QtWid.QHBoxLayout()
        hbox_2.addWidget(
            build_group(
                c.create_Relay_button,
                8,
                "0",
                "1",
            ),
            **p,
        )
        hbox_2.addWidget(
            build_group(
                c.create_Toggle_button,
                8,
                "False",
                "True",
                minimumWidth=80,
            ),
            **p,
        )
        hbox_2.addWidget(
            build_group(
                c.create_Toggle_button_2,
                8,
                "Off Okay",
                "!! ON !!",
                minimumWidth=80,
            ),
            **p,
        )
        hbox_2.addWidget(
            build_group(
                c.create_Toggle_button_3,
                8,
                "!! OFF !!",
                "On Okay",
                minimumWidth=80,
            ),
            **p,
        )

        # ----------------------------------------------------------------------
        #   Other style sheets
        # ----------------------------------------------------------------------

        hbox_3 = QtWid.QHBoxLayout()

        # SS_TEXTBOX_READ_ONLY
        qlin_1 = QtWid.QLineEdit("Normal")
        qlin_2 = QtWid.QLineEdit("Read-only")
        qpte_1 = QtWid.QPlainTextEdit("Normal")
        qpte_2 = QtWid.QPlainTextEdit("Read-only")
        qlin_2.setReadOnly(True)
        qpte_2.setReadOnly(True)
        for control in (qlin_1, qlin_2, qpte_1, qpte_2):
            control.setStyleSheet(c.SS_TEXTBOX_READ_ONLY)

        grid = QtWid.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        grid.addWidget(qlin_1, 0, 0)
        grid.addWidget(qlin_2, 1, 0)
        grid.addWidget(qpte_1, 2, 0)
        grid.addWidget(qpte_2, 3, 0)

        grpb = QtWid.QGroupBox("SS_TEXTBOX_READ_ONLY")
        grpb.setLayout(grid)

        hbox_3.addWidget(grpb)

        # SS_TEXTBOX_ERRORS
        qlin_1 = QtWid.QLineEdit("Normal")
        qlin_2 = QtWid.QLineEdit("Read-only --> ERROR")
        qpte_1 = QtWid.QPlainTextEdit("Normal")
        qpte_2 = QtWid.QPlainTextEdit("Read-only --> ERROR")
        qlin_2.setReadOnly(True)
        # qlin_2.setEnabled(False)
        qpte_2.setReadOnly(True)
        # qpte_2.setEnabled(False)
        for control in (qlin_1, qlin_2, qpte_1, qpte_2):
            control.setStyleSheet(c.SS_TEXTBOX_ERRORS)

        grid = QtWid.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        grid.addWidget(qlin_1, 0, 0)
        grid.addWidget(qlin_2, 1, 0)
        grid.addWidget(qpte_1, 2, 0)
        grid.addWidget(qpte_2, 3, 0)

        grpb = QtWid.QGroupBox("SS_TEXTBOX_ERRORS")
        grpb.setLayout(grid)

        hbox_3.addWidget(grpb)

        # SS_TITLE
        qlbl = QtWid.QLabel("QLabel using SS_TITLE")
        qlbl.setFont(QtGui.QFont("Verdana", 12))
        qlbl.setStyleSheet(c.SS_TITLE)

        # PyQt defaults
        grid = QtWid.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QtWid.QPushButton("Default QPushButton"), 0, 0)
        grid.addWidget(QtWid.QLineEdit("Default QLineEdit"), 1, 0)
        grid.addWidget(QtWid.QTextEdit("Default QTextEdit"), 2, 0)

        grpb = QtWid.QGroupBox("PyQt defaults using SS_GROUP_RECT")
        grpb.setStyleSheet(c.SS_GROUP_RECT)
        grpb.setLayout(grid)

        vbox_sub = QtWid.QVBoxLayout()
        vbox_sub.addWidget(qlbl)
        vbox_sub.addWidget(grpb)

        hbox_3.addLayout(vbox_sub)

        # -------------------------
        #   Round up full window
        # -------------------------

        hbox_1.addStretch()
        hbox_2.addStretch()
        hbox_3.addStretch()

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox_1, stretch=0)
        vbox.addLayout(hbox_2, stretch=0)
        vbox.addLayout(hbox_3, stretch=0)
        vbox.addStretch()


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    if qtpy.PYQT6 or qtpy.PYSIDE6:
        sys.argv += ["-platform", "windows:darkmode=0"]

    app = QtWid.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
