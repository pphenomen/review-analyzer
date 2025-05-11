class ButtonStyles:
    @staticmethod
    def default() -> str:
        return """
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1c1c1c, stop:1 #3c3c3c
                );
                color: #ffffff;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background: #2d2d2d;
            }
        """

    @staticmethod
    def rounded() -> str:
        return """
            QPushButton {
                font-size: 18px;
                padding: 10px;
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1c1c1c,
                    stop:1 #3c3c3c
                );
                color: #ffffff;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: #2d2d2d;
            }
        """

class GroupBoxStyles:
    @staticmethod
    def default() -> str:
        return """
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """

class FrameStyles:
    @staticmethod
    def default() -> str:
        return """
            background-color: #ffffff;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        """

class LabelStyles:
    @staticmethod
    def review_text() -> str:
        return "font-size: 18px; color: #333333;"

    @staticmethod
    def star() -> str:
        return "font-size: 20px; color: #FFD700;"

    @staticmethod
    def description() -> str:
        return """
            color: #505050;
            text-align: center;
            margin-bottom: 100px;
        """
    
    @staticmethod
    def filter_text() -> str:
        return "font-size: 16px; padding: 6px;"

class DragDropStyles:
    @staticmethod
    def drag_area() -> str:
        return """
            border: 2.5px dashed #333333;
            border-radius: 10px;
            background-color: #C0C0C0;
        """

    @staticmethod
    def drag_text() -> str:
        return """
            font-size: 18px; 
            color: #4A4A4A; 
            border: none;
        """
