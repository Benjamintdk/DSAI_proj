# AUTOGENERATED! DO NOT EDIT! File to edit: 04_model.ipynb (unless otherwise specified).

__all__ = ['cnn_encoder', 'text_encoder', 'meta_encoder', 'decoder', 'TaglinePredictorModel']

# Internal Cell

from transformers import DistilBertModel, DistilBertTokenizer
from .dataset import *
from torch import nn
from fastai.data.core import DataLoaders
from functools import partial
from PIL import Image
import torchvision.models as models
import torch

# Internal Cell

def freeze_all_but_layer(m, layer):
    if not isinstance(m, layer):
        if hasattr(m, 'weight') and m.weight is not None:
            m.weight.requires_grad_(False)
        if hasattr(m, 'bias') and m.bias is not None:
            m.bias.requires_grad_(False)

# Cell

def cnn_encoder(pretrained: bool, in_channels: int, out_channels: int):
    model = models.resnet18(pretrained=pretrained)
    last_layers = [nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, padding=1, bias=False), nn.AdaptiveAvgPool2d(1)]
    model = nn.Sequential(*list(model.children())[:-2], *last_layers)
    img_freeze_fn = partial(freeze_all_but_layer, layer=nn.BatchNorm2d)
    model.apply(img_freeze_fn)
    return model

# Cell

def text_encoder(model_type: str):
    model = DistilBertModel.from_pretrained(model_type)
    text_freeze_fn = partial(freeze_all_but_layer, layer=nn.LayerNorm)
    model.apply(text_freeze_fn)
    return model

# Cell

def meta_encoder(in_channels: int, out_channels: int):
    model = [nn.Linear(in_features=in_channels, out_features=out_channels),
             nn.Dropout(0.3)]
    return nn.Sequential(*model)

# Cell

def decoder(cur_len: int, max_seq_len: int, hidden_dim: int, vocab_size: int):
    layers = [nn.Conv1d(in_channels=cur_len, out_channels=max_seq_len, kernel_size=1, stride=1),
              nn.ReLU(),
              nn.Linear(in_features=hidden_dim, out_features=vocab_size),
              nn.Softmax(dim=-1),
              nn.Dropout(0.3)]
    return nn.Sequential(*layers)

# Cell

class TaglinePredictorModel(nn.Module):

    def __init__(self, vocab_size: int, meta_features: int):
        super(TaglinePredictorModel, self).__init__()
        self.cnn_encoder = cnn_encoder(pretrained=True, in_channels=512, out_channels=768)
        self.text_encoder = text_encoder(model_type='distilbert-base-uncased')
        self.meta_encoder = meta_encoder(in_channels=meta_features, out_channels=768)
        self.decoder = decoder(cur_len=83, max_seq_len=10, hidden_dim=768, vocab_size=vocab_size)
        print("Model is created!")

    def forward(self, x: list):
        poster_feature = self.cnn_encoder(x[0]).squeeze(-1).permute(0, 2, 1)
        backdrop_feature = self.cnn_encoder(x[1]).squeeze(-1).permute(0, 2, 1)
        text_feature = self.text_encoder((x[2])).last_hidden_state
        meta_feature = self.meta_encoder(x[3]).unsqueeze(1)

        combined_feature = torch.cat((poster_feature, backdrop_feature, text_feature, meta_feature), dim=1)
        output = self.decoder(combined_feature)
        return output.permute(0, 2, 1)