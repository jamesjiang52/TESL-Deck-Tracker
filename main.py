import sys
import copy
from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from common import *
from decode import decode


class DeckWindow(QtWidgets.QMainWindow):
    def __init__(self, deck):
        QtWidgets.QMainWindow.__init__(self)
        
        self.setPalette(QtGui.QPalette(QtCore.Qt.darkGray))
        self.setWindowTitle("Deck Tracker")

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            #QtCore.Qt.FramelessWindowHint
        )
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)

        self._deck_original = copy.deepcopy(deck)
        self._deck_current = copy.deepcopy(deck)

        self.update_window(adjust_size=True)

    def update_window(self, adjust_size=False):
        widget_main = QtWidgets.QWidget()
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        widget_cards = QtWidgets.QWidget()
        layout_cards = QtWidgets.QHBoxLayout()
        layout_cards.setSpacing(0)
        layout_cards.setContentsMargins(0, 0, 0, 0)
        
        widget_costs = QtWidgets.QWidget()
        layout_costs = QtWidgets.QVBoxLayout()
        layout_costs.setSpacing(0)
        layout_costs.setContentsMargins(0, 0, 0, 0)

        widget_counts = QtWidgets.QWidget()
        layout_counts = QtWidgets.QVBoxLayout()
        layout_counts.setSpacing(0)
        layout_counts.setContentsMargins(0, 0, 0, 0)
        
        """
        widget_percents = QtWidgets.QWidget()
        layout_percents = QtWidgets.QVBoxLayout()
        layout_percents.setSpacing(0)
        layout_percents.setContentsMargins(0, 0, 0, 0)
        """

        widget_names = QtWidgets.QWidget()
        layout_names = QtWidgets.QVBoxLayout()
        layout_names.setSpacing(0)
        layout_names.setContentsMargins(0, 0, 0, 0)
        
        widget_rarities = QtWidgets.QWidget()
        layout_rarities = QtWidgets.QVBoxLayout()
        layout_rarities.setSpacing(0)
        layout_rarities.setContentsMargins(0, 0, 0, 0)
        
        remaining = len(self._deck_current.Cards)
        if remaining == 0:
            remaining = 1

        i = 0
        while i < len(self._deck_original.Cards):
            card = self._deck_original.Cards[i]
            
            color = get_color_from_attributes_single(card.Attributes)
            
            label_cost = QtWidgets.QLabel("{0:2d}".format(card.Cost).ljust(3))
            label_cost.setAutoFillBackground(True)
            label_cost.setPalette(QtGui.QPalette(QtCore.Qt.darkBlue))
            layout_costs.addWidget(label_cost)
            
            label_count = QtWidgets.QPushButton(
                "{0}/{1}".format(
                    self._deck_current.Counts[card.Name],
                    self._deck_original.Counts[card.Name]
                )
            )
            label_count.setPalette(QtGui.QPalette(color))
            label_count.setFixedWidth(45)
            label_count.setEnabled(False)
            layout_counts.addWidget(label_count)
            
            """
            label_percent = QtWidgets.QPushButton(
                "{0:10.2f}% ".format(
                    100*self._deck_current.Counts[card.Name]/remaining
                )
            )
            label_percent.setPalette(QtGui.QPalette(color))
            label_percent.setStyleSheet("text-align:right")
            label_percent.setFont(QtGui.QFont("Sans-Serif", pointSize=12, weight=50))
            label_percent.setFixedWidth(90)
            label_percent.setEnabled(False)
            layout_percents.addWidget(label_percent)
            """

            button_name = QtWidgets.QPushButton(card.Name.rjust(len(card.Name) + 1))
            button_name.clicked.connect(partial(self.clicked, card=card))
            button_name.setPalette(QtGui.QPalette(color))
            button_name_palette = button_name.palette()
            button_name_palette.setColor(
                QtGui.QPalette.ColorGroup.All,
                QtGui.QPalette.ColorRole.ButtonText,
                button_name_palette.color(
                    QtGui.QPalette.ColorGroup.Disabled,
                    QtGui.QPalette.ColorRole.ButtonText
                )
            )
            button_name.setPalette(button_name_palette)
            button_name.setStyleSheet("text-align:left")
            button_name.setFont(QtGui.QFont("Sans-Serif", pointSize=10, weight=50))
            layout_names.addWidget(button_name)
            
            color = get_rarity_color(card.Rarity)
                
            label_rarity = QtWidgets.QLabel("")
            label_rarity.setAutoFillBackground(True)
            label_rarity.setPalette(QtGui.QPalette(color))
            label_rarity.setFixedWidth(5)
            layout_rarities.addWidget(label_rarity)

            i += self._deck_original.Counts[card.Name]

        widget_costs.setLayout(layout_costs)
        #widget_percents.setLayout(layout_percents)
        widget_counts.setLayout(layout_counts)
        widget_names.setLayout(layout_names)
        widget_rarities.setLayout(layout_rarities)

        layout_cards.addWidget(widget_costs)
        layout_cards.addWidget(widget_names)
        layout_cards.addWidget(widget_rarities)
        layout_cards.addWidget(widget_counts)
        #layout_cards.addWidget(widget_percents)
        widget_cards.setLayout(layout_cards)

        """
        button_reset = QtWidgets.QPushButton("Reset")
        button_reset.clicked.connect(self.reset_cards)
        button_reset.setFont(QtGui.QFont("Sans-Serif", pointSize=10, weight=50))
        """

        self._lineedit_deck_code = QtWidgets.QLineEdit()
        self._lineedit_deck_code.setStyleSheet("background-color:white")
        self._lineedit_deck_code.setFont(QtGui.QFont("Sans-Serif", pointSize=8, weight=50))
        self._lineedit_deck_code.returnPressed.connect(self.new_deck)

        label_total = QtWidgets.QPushButton(
            "{0}/{1}".format(
                len(self._deck_current.Cards),
                len(self._deck_original.Cards)
            )
        )
        label_total.setFont(QtGui.QFont("Sans-Serif", pointSize=14, weight=75))
        label_total.setEnabled(False)
        label_total.setFixedHeight(40)

        widget_class_colors = QtWidgets.QWidget()
        layout_class_colors = QtWidgets.QHBoxLayout()
        layout_class_colors.setSpacing(0)
        layout_class_colors.setContentsMargins(0, 0, 0, 0)
        
        colors = get_color_from_attributes_multiple(self._deck_current.Attributes)
        for color in colors:
            label_color = QtWidgets.QPushButton("")
            label_color.setSizePolicy(
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.MinimumExpanding
            )
            label_color.setEnabled(False)
            label_color.setPalette(QtGui.QPalette(color))
            label_color.setFixedHeight(12)
            layout_class_colors.addWidget(label_color)
        widget_class_colors.setLayout(layout_class_colors)

        label_class_name = QtWidgets.QPushButton(self._deck_current.Class)
        label_class_name.setFont(QtGui.QFont("Sans-Serif", pointSize=12, weight=75))
        label_class_name.clicked.connect(self.reset_cards)
        label_class_name.setPalette(QtGui.QPalette(QtCore.Qt.gray))
        label_class_name_palette = label_class_name.palette()
        label_class_name_palette.setColor(
            QtGui.QPalette.ColorGroup.All,
            QtGui.QPalette.ColorRole.ButtonText,
            label_class_name_palette.color(
                QtGui.QPalette.ColorGroup.Disabled,
                QtGui.QPalette.ColorRole.ButtonText
            )
        )
        label_class_name.setPalette(label_class_name_palette)
        label_class_name.setFixedHeight(40)

        layout_main.addWidget(self._lineedit_deck_code)
        #layout_main.addWidget(button_reset)
        layout_main.addWidget(widget_class_colors)
        layout_main.addWidget(label_class_name)
        layout_main.addWidget(widget_cards)
        layout_main.addWidget(label_total)
        widget_main.setLayout(layout_main)

        self.setCentralWidget(widget_main)

        if adjust_size:
            widget_main.adjustSize()
            self.setFixedSize(widget_main.size())

    def reset_cards(self):
        self._deck_current = copy.deepcopy(self._deck_original)
        self.update_window()

    def new_deck(self):
        deck = decode(self._lineedit_deck_code.text())
        self._deck_original = copy.deepcopy(deck)
        self._deck_current = copy.deepcopy(deck)
        self.update_window(adjust_size=True)

    def clicked(self, card):
        if self._deck_current.Counts[card.Name] > 0:
            self._deck_current.Counts[card.Name] -= 1
            self._deck_current.Cards.remove(card)
        self.update_window()


__default_deck = Deck([])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    app.setFont(QtGui.QFont("Sans-Serif", pointSize=10, weight=75))
    mywindow = DeckWindow(__default_deck)
    mywindow.show()
    app.exec_()
