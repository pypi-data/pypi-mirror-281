import copy
import numpy as np

import torch
import torch.nn as nn
from torch.optim import Adam
from sklearn.model_selection import StratifiedKFold

class simple_model(nn.Module):
    def __init__(self, X):
        super(simple_model, self).__init__()
        self.weights = nn.ParameterList(
            [nn.Parameter(torch.ones(x_each.shape[1], 1) / x_each.shape[1]) for x_each in X])

    def forward(self, x):
        x_total_score = []
        for idx, x_each in enumerate(x):
            x_score = x_each @ torch.clamp(self.weights[idx], min=0)
            x_total_score.append(x_score)
        x_total_score = torch.cat(x_total_score, dim=-1)
        return x_total_score


def base_classifier(X_train_now, label_list, shot, y_train_num):
    criterion = nn.CrossEntropyLoss()
    if shot // len(label_list) == 1:
        model = simple_model(X_train_now)
        opt = Adam(model.parameters(), lr=1e-2)
        for _ in range(200):
            opt.zero_grad()
            outputs = model(X_train_now)
            preds = outputs.argmax(dim=1).numpy()
            acc = (np.array(y_train_num) == preds).sum() / len(preds)
            if acc == 1:
                break
            loss = criterion(outputs, torch.tensor(y_train_num))
            loss.backward()
            opt.step()
    else:
        if shot // len(label_list) <= 2:
            n_splits = 2
        else:
            n_splits = 4

        kfold = StratifiedKFold(n_splits=n_splits, shuffle=True)
        model_list = []
        for fold, (train_ids, valid_ids) in enumerate(kfold.split(X_train_now[0], y_train_num)):
            model = simple_model(X_train_now)
            opt = Adam(model.parameters(), lr=1e-2)
            X_train_now_fold = [x_train_now[train_ids] for x_train_now in X_train_now]
            X_valid_now_fold = [x_train_now[valid_ids] for x_train_now in X_train_now]
            y_train_fold = y_train_num[train_ids]
            y_valid_fold = y_train_num[valid_ids]

            max_acc = -1
            for _ in range(200):
                opt.zero_grad()
                outputs = model(X_train_now_fold)
                loss = criterion(outputs, torch.tensor(y_train_fold))
                loss.backward()
                opt.step()

                valid_outputs = model(X_valid_now_fold)
                preds = valid_outputs.argmax(dim=1).numpy()
                acc = (np.array(y_valid_fold) == preds).sum() / len(preds)
                if max_acc < acc:
                    max_acc = acc
                    final_model = copy.deepcopy(model)
                    if max_acc >= 1:
                        break
            model_list.append(final_model)

        sdict = model_list[0].state_dict()
        for key in sdict:
            sdict[key] = torch.stack([model.state_dict()[key] for model in model_list], dim=0).mean(dim=0)

        model = simple_model(X_train_now)
        model.load_state_dict(sdict)
    return model