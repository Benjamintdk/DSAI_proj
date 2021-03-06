# AUTOGENERATED! DO NOT EDIT! File to edit: 05_train.ipynb (unless otherwise specified).

__all__ = ['TagLineLoss', 'splitter_func', 'predict_one_batch']

# Internal Cell

from transformers import DistilBertTokenizer
from fastai.data.core import DataLoaders
from fastai.vision.all import *
from .dataset import *
from .model import *
from fastai.vision import *
from torch import nn
from pandas import DataFrame
import torch

# Cell

class TagLineLoss(nn.Module):

    def __init__(self):
        super(TagLineLoss, self).__init__()
        self.criterion = torch.nn.CrossEntropyLoss()

    def forward(self, output, target):
        return self.criterion(input=output, target=target)

# Cell

def splitter_func(model: nn.Module):
    return [params(model.cnn_encoder),
            params(model.text_encoder),
            params(model.meta_encoder),
            params(model.decoder)]

# Internal Cell

def load_model(model_path: str, **kwargs):
    model = TaglinePredictorModel(**kwargs)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    model.to("cpu")
    return model

# Cell

def predict_one_batch(tokenizer,
                      dls,
                      mode: str,
                      model_path: str) -> DataFrame:

    if mode != "train":
        x, y = dls.valid.one_batch()
    else:
        x, y = dls.train.one_batch()
    model = load_model(model_path=model_path, vocab_size=30522, meta_features=x[3].shape[-1])
    x = model(x)
    preds = torch.argmax(x, dim=1)
    results = {"preds" : [tokenizer.decode(p) for p in preds], "labels" : [tokenizer.decode(t) for t in y]}
    return pd.DataFrame.from_dict(results)