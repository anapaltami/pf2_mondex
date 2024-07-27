import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from src.config import PAIZO_LOGO, AZORA_LOGO


class LegalTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # paizo logo
        paizo_pixmap = QPixmap(str(PAIZO_LOGO))
        if paizo_pixmap.isNull():
            logging.error("Failed to load Paizo logo")
        else:
            paizo_pixmap = paizo_pixmap.scaledToHeight(150, Qt.SmoothTransformation)
        paizo_label = QLabel()
        paizo_label.setPixmap(paizo_pixmap)
        paizo_label.setAlignment(Qt.AlignCenter)

        # azora law logo
        azora_pixmap = QPixmap(str(AZORA_LOGO))
        if azora_pixmap.isNull():
            logging.error("Failed to load Azora Law logo")
        else:
            azora_pixmap = azora_pixmap.scaledToHeight(150, Qt.SmoothTransformation)
        azora_label = QLabel()
        azora_label.setPixmap(azora_pixmap)
        azora_label.setAlignment(Qt.AlignCenter)

        legal_heading = QLabel("Legal License Notes:")
        legal_heading.setAlignment(Qt.AlignCenter)
        legal_heading.setFont(QFont('Arial', 24, QFont.Bold))

        # legal license notes
        legal_text = QLabel(
            "This product is licensed under the ORC License located at the Library of Congress at TX 9-307-067 and "
            "available online at various locations. All warranties are disclaimed as set forth therein.\n\n"
            "This product is based on the following Licensed Material: PF2 Monster Dex, © 2024, Developed by "
            "Anastasia Altamirano.\n\n"
            "If you use our Licensed Material in your own published works, please credit us as follows: "
            "PF2 Monster Dex, © 2024, Developed by Anastasia Altamirano.\n\n"
            "Reserved Material elements in this product include, but may not be limited to: "
            "Specific characters, world lore.\n\n"
            "The following elements are owned by the Licensor and would otherwise constitute Reserved Material and "
            "are hereby designated as Licensed Material: General monster statblocks, game rules, and mechanics.\n"
        )
        legal_text.setWordWrap(True)
        legal_text.setAlignment(Qt.AlignCenter)

        h_layout = QHBoxLayout()
        h_layout.addWidget(paizo_label)
        h_layout.addWidget(legal_text)
        h_layout.addWidget(azora_label)

        layout.addWidget(legal_heading)
        layout.addLayout(h_layout)
        self.setLayout(layout)
