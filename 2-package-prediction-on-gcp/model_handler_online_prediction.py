import io
import json
import logging
import os

import torch
import torchvision.transforms as T
from PIL import Image
from ts.torch_handler.base_handler import BaseHandler

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class ModelHandlerOnlinePrediction(BaseHandler):

    def __init__(self):
        super().__init__()
        self.idx_to_class = None
        self.top_k = None
        self.transform = None
        self.model = None
        self.device = None

    def initialize(self, context):
        """
        :param context: the TorchServe context. Can be used for customization model_name, model_dir, manifest, batch_size, gpu etc.
        :return:
        """
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        # Read model serialize/pt file
        serialized_file = manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)
        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt file")

        # load index to class file
        idx_to_class_filepath = os.path.join(model_dir, "index_to_name.json")
        if os.path.isfile(idx_to_class_filepath):
            with open(idx_to_class_filepath) as f:
                self.idx_to_class = json.load(f)
        else:
            logging.warning('Missing the index_to_name.json file. Inference output will not include class name.')

        self.model = torch.jit.load(model_pt_path, map_location=self.device)
        self.model.to(self.device)
        self.model.eval()

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        model_input = self.preprocess(data)
        model_output = self.inference(model_input)
        return self.postprocess(model_output)

    def preprocess(self, req):
        """
        :param req: The incoming request - here image bytes is in 'data' key.
        {'data': <image bytes>, 'top_k': 5}
        :return: preprocessed image as model input
        """
        self.top_k = int(req.get("top_k", 1))
        image = req.get("data")
        image = Image.open(io.BytesIO(image))
        transformed_image = self.transform(image)
        model_input = transformed_image.unsqueeze(0)
        return model_input.to(self.device)

    def inference(self, model_input):
        with torch.no_grad():
            model_output = self.model(model_input)  # logits
        return model_output

    def postprocess(self, output):
        proba = torch.exp(output)
        top_proba, top_label = proba.topk(self.top_k)
        top_proba = top_proba.detach().numpy().tolist()[0]
        top_label = top_label.detach().numpy().tolist()[0]

        if self.idx_to_class is not None:
            top_labels = [self.idx_to_class[str(lab)] for lab in top_label]
        else:
            top_labels = top_label

        output = {"proba": top_proba, "label": top_labels}
        return output
