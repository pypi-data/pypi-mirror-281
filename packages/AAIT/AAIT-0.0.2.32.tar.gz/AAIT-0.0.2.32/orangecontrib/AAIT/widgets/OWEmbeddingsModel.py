import os
import sys
from sentence_transformers import SentenceTransformer

from Orange.widgets import widget
from Orange.widgets.utils.signals import Output

from PyQt5 import uic
from AnyQt.QtWidgets import QApplication, QLabel

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.llm import embeddings
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_local_store_path
else:
    from orangecontrib.AAIT.llm import embeddings
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path


class OWEmbeddingsModel(widget.OWWidget):
    name = "Model - Embeddings - MPNET"
    description = "Load the embeddings model all-mpnet-base-v2 from the AI Store"
    icon = "icons/owembeddingsmodel.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owembeddingsmodel.ui")
    want_control_area = False

    class Outputs:
        model = Output("Model", SentenceTransformer)

    def __init__(self):
        super().__init__()
        # Path management
        self.current_ows = ""
        local_store_path = get_local_store_path()
        model_name = "all-mpnet-base-v2"
        self.model_path = os.path.join(local_store_path, "Models", "NLP", model_name)

        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)

        # Data Management
        try:
            self.model = SentenceTransformer(self.model_path)
            self.Outputs.model.send(self.model)
        except:
            print("Model couldn't be found") #TODO
            self.Outputs.model.send(None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWEmbeddingsModel()
    my_widget.show()
    app.exec_()
