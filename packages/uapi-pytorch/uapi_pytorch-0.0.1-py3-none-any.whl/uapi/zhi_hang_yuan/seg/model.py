# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: PaddlePaddle Authors
"""
import logging
import os
import torch
import torch.nn as nn
from pathlib import Path
from torch import optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from sklearn.metrics import mean_squared_error
import h5py
from scipy.io import savemat

from uapi.uapi.base import BaseModel, BaseResult
from uapi.uapi.base.utils.subprocess import CompletedProcess
from uapi.uapi.utils.util import get_device
from .unet import UNet
from .dataset import MatDataset, check_dataset

import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class SegModel(BaseModel):
    """ Semantic Segmentation Model """

    def check_dataset(self,
                      dataset_dir=None,
                      dataset_type=None,
                      mode='fast'):
        """check dataset

        Args:
            dataset_dir (str, optional): the dataset directory. Defaults to None.
            dataset_type (str, optional): the dataset type. Defaults to None.
            mode (str, optional): the dataset mode. Defaults to 'fast'.

        Returns:
            CompletedProcess
        """
        return check_dataset(dataset_dir, dataset_type, mode)

    def train(self,
              batch_size: int=None,
              learning_rate: float=None,
              epochs_iters: int=None,
              ips: str=None,
              device: str='gpu',
              resume_path: str=None,
              dy2st: bool=False,
              amp: str='OFF',
              num_workers: int=None,
              use_vdl: bool=True,
              save_dir: str=None,
              **kwargs) -> CompletedProcess:
        """train self

        Args:
            batch_size (int, optional): the train batch size value. Defaults to None.
            learning_rate (float, optional): the train learning rate value. Defaults to None.
            epochs_iters (int, optional): the train epochs value. Defaults to None.
            ips (str, optional): the ip addresses of nodes when using distribution. Defaults to None.
            device (str, optional): the running device. Defaults to 'gpu'.
            resume_path (str, optional): the checkpoint file path to resume training. Train from scratch if it is set
                to None. Defaults to None.
            dy2st (bool, optional): Enable dynamic to static. Defaults to False.
            amp (str, optional): the amp settings. Defaults to 'OFF'.
            num_workers (int, optional): the workers number. Defaults to None.
            use_vdl (bool, optional): enable VisualDL. Defaults to True.
            save_dir (str, optional): the directory path to save train output. Defaults to None.

        Returns:
           CompletedProcess: the result of training subprocess execution.
        """
        self.config.update_batch_size (batch_size, 'train')
        self.config.update_learning_rate(learning_rate)
        self.config.update_epochs_iters(epochs_iters)

        device = get_device(device)
        logging.info(f'Using device {device}')

        # 1. Create model
        # Change here to adapt to your data
        # n_channels=3 for RGB inputs
        # n_classes is the number of probabilities you want to get per pixel
        model = UNet(n_channels=1, n_classes=1, bilinear=False)
        model = model.to(memory_format=torch.channels_last)

        logging.info(f'Network:\n'
                     f'\t{model.n_channels} input channels\n'
                     f'\t{model.n_classes} output channels (classes)\n'
                     f'\t{"Bilinear" if model.bilinear else "Transposed conv"} upscaling')

        pretrained_weights = self.config.get_pretrained_weights()

        if pretrained_weights:
            state_dict = torch.load(pretrained_weights, map_location=device)
            model.load_state_dict(state_dict)
            logging.info(f'Model loaded from {pretrained_weights}')

        model.to(device=device)

        # 2. Create dataset
        train_set = MatDataset(self.config.get_dataset_dir(), "train.txt")
        val_set = MatDataset(self.config.get_dataset_dir(), "val.txt")

        # 3. Create data loaders
        train_loader = DataLoader(train_set, shuffle=True, batch_size=batch_size, num_workers=os.cpu_count(), pin_memory=True)
        val_loader = DataLoader(val_set, shuffle=False, drop_last=True,
                                batch_size=self.config.get_batch_size(mode='evaluate'),
                                num_workers=os.cpu_count(), pin_memory=True)

        amp = False if amp == 'OFF' or amp is None else True
        logging.info(f'''Starting training:
                Epochs:          {epochs_iters}
                Batch size:      {batch_size}
                Learning rate:   {learning_rate}
                Training size:   {len(train_set)}
                Validation size: {len(val_set)}
                Checkpoints:     {save_dir}
                Device:          {device.type}
                Mixed Precision: {amp}
            ''')

        # 4. Set up the optimizer, the loss, the learning rate scheduler and the loss scaling for AMP
        # optimizer = optim.RMSprop(model.parameters(),
        #                          lr=learning_rate, weight_decay=weight_decay, momentum=momentum, foreach=True)
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-8)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5)
        grad_scaler = torch.cuda.amp.GradScaler(enabled=amp)
        criterion = nn.MSELoss()
        global_step = 0
        best_score = 100
        best_model_dir = os.path.join(save_dir, 'best_model')
        if not os.path.exists(best_model_dir):
            os.makedirs(best_model_dir)
        best_filename = best_model_dir + "/model.pth"

        # 5. Begin training
        for epoch in range(1, epochs_iters + 1):
            model.train()
            epoch_loss = 0
            with tqdm(total=len(train_set), desc=f'Epoch {epoch}/{epochs_iters}', unit='img') as pbar:
                for batch in train_loader:
                    inputs, targets = batch[0], batch[1]

                    assert inputs.shape[1] == model.n_channels, \
                        f'Network has been defined with {model.n_channels} input channels, ' \
                        f'but loaded inputs have {inputs.shape[1]} channels. Please check that ' \
                        'the inputs are loaded correctly.'

                    inputs = inputs.to(device=device, dtype=torch.float32)
                    targets = targets.to(device=device, dtype=torch.float32)

                    optimizer.zero_grad()

                    with torch.autocast(device.type if device.type != 'mps' else 'cpu', enabled=amp):
                        masks_pred = model(inputs)
                        loss = criterion(masks_pred, targets)

                    grad_scaler.scale(loss).backward()
                    grad_scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    grad_scaler.step(optimizer)
                    grad_scaler.update()

                    pbar.update(inputs.shape[0])
                    global_step += 1
                    epoch_loss += loss.item()
                    pbar.set_postfix(**{'loss (batch)': loss.item()})

            # Evaluation round
            if epoch % self.config.get_eval_interval() == 0:
                model.eval()
                dice_score = 0
                with torch.no_grad():
                    with torch.autocast(device.type if device.type != 'mps' else 'cpu', enabled=amp):
                        for batch in tqdm(val_loader, total=len(val_loader), desc='Validation round', unit='batch', leave=False):
                            inputs, targets = batch[0], batch[1]

                            # move images and labels to correct device and type
                            inputs = inputs.to(device=device, dtype=torch.float32)
                            targets = targets.to(device=device, dtype=torch.float32)

                            # predict the mask
                            calculated = model(inputs)
                            targets = torch.flatten(torch.squeeze(targets), 0)
                            calculated = torch.flatten(torch.squeeze(calculated), 0)

                            dice_score += mean_squared_error(calculated.cpu(), targets.cpu())
                        val_score = dice_score / max(len(val_loader), 1)
                        scheduler.step(val_score)
                logging.info('Validation score: {}'.format(val_score))

                if val_score < best_score:
                    best_score = val_score
                    torch.save(model.state_dict(), best_filename)

            if save_dir and epoch > epochs_iters - 3:
                Path(save_dir).mkdir(parents=True, exist_ok=True)
                state_dict = model.state_dict()
                # state_dict['mask_values'] = dataset.mask_values
                torch.save(state_dict, os.path.join(save_dir, 'checkpoint_epoch{}.pth'.format(epoch)))
                logging.info(f'Checkpoint {epoch} saved!')

    def evaluate(self,
                 weight_path: str,
                 batch_size: int=None,
                 ips: str=None,
                 device: str='gpu',
                 amp: str='OFF',
                 num_workers: int=None,
                 **kwargs):
        """evaluate self using specified weight

        Args:
            weight_path (str): the path of model weight file to be evaluated.
            batch_size (int, optional): the batch size value in evaluating. Defaults to None.
            ips (str, optional): the ip addresses of nodes when using distribution. Defaults to None.
            device (str, optional): the running device. Defaults to 'gpu'.
            amp (str, optional): the AMP setting. Defaults to 'OFF'.
            num_workers (int, optional): the workers number in evaluating. Defaults to None.

        Returns:
            CompletedProcess: the result of evaluating subprocess execution.
        """

        device = get_device(device)
        model = UNet(n_channels=1, n_classes=1, bilinear=False)
        model = model.to(memory_format=torch.channels_last)
        state_dict = torch.load(weight_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device=device)

        val_set = MatDataset(self.config.get_dataset_dir(), "val.txt")

        # 3. Create data loaders
        if batch_size is None:
            batch_size = self.config.get_batch_size(mode='evaluate')
        loader_args = dict(batch_size=batch_size, num_workers=os.cpu_count(), pin_memory=True)
        dataloader = DataLoader(val_set, shuffle=False, drop_last=True, **loader_args)
        model.eval()
        num_val_batches = len(dataloader)
        print(num_val_batches)
        dice_score = 0
        amp = False if amp == 'OFF' or amp is None else True
        # iterate over the validation set
        with torch.no_grad():
            with torch.autocast(device.type if device.type != 'mps' else 'cpu', enabled=amp):
                for i, batch in enumerate(dataloader):
                    inputs, targets = batch[0], batch[1]

                    # move images and labels to correct device and type
                    inputs = inputs.to(device=device, dtype=torch.float32)
                    targets = targets.to(device=device, dtype=torch.float32)

                    # predict the mask
                    calculated = model(inputs)
                    targets = torch.flatten(torch.squeeze(targets), 0)
                    calculated = torch.flatten(torch.squeeze(calculated), 0)

                    # compute the Dice score
                    dice_score += mean_squared_error(calculated.cpu(), targets.cpu())
        mse = dice_score / max(num_val_batches, 1)
        return BaseResult(metrics={"MSE": format(mse, '.4f')})

    def predict(self,
                weight_path: str,
                input_path: str,
                device: str='gpu',
                save_dir: str=None,
                **kwargs):
        """predict using specified weight

        Args:
            weight_path (str): the path of model weight file used to predict.
            input_path (str): the path of image file to be predicted.
            device (str, optional): the running device. Defaults to 'gpu'.
            save_dir (str, optional): the directory path to save predict output. Defaults to None.

        Returns:
            CompletedProcess: the result of predicting subprocess execution.
        """
        device = get_device(device)
        model = UNet(n_channels=1, n_classes=1, bilinear=False)
        state_dict = torch.load(weight_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device=device)

        model.eval()  # 设置为评估模式
        # 创建一个示例输入
        with h5py.File(input_path, 'r') as mat_file:
            image = mat_file['data'][:]
            image = torch.tensor(image, dtype=torch.float32)
            image = torch.unsqueeze(image, 0)

        batch_t = torch.unsqueeze(image, 0)
        batch_t = batch_t.to(device, non_blocking=True)

        with torch.no_grad():
            out = model(batch_t)
            out = torch.squeeze(out).cpu().numpy()

        savemat(os.path.join(save_dir, 'predict.mat'), {'data': out})

    def export(self, weight_path: str, save_dir: str,
               **kwargs):
        """export the dynamic model to static model

        Args:
            weight_path (str): the model weight file path that used to export.
            save_dir (str): the directory path to save export output.

        Returns:
            CompletedProcess: the result of exporting subprocess execution.
        """
        device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        model = UNet(n_channels=1, n_classes=1, bilinear=False)
        state_dict = torch.load(weight_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device=device)

        model.eval()  # 设置为评估模式
        # 创建一个示例输入
        input_shape = self.config.get_input_shape()
        example_input = torch.rand(1, input_shape[0], input_shape[1], input_shape[2])
        example_input = example_input.to(device, non_blocking=True)

        # 使用torch.jit.trace来跟踪模型的执行并生成静态图模型
        traced_model = torch.jit.trace(model, example_input)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 保存静态图模型
        traced_model.save(os.path.join(save_dir, 'inference.pt'))
        return BaseResult()

    def infer(self,
              model_dir: str,
              input_path: str,
              device: str='gpu',
              save_dir: str=None,
              **kwargs):
        """predict image using infernece model

        Args:
            model_dir (str): the directory path of inference model files that would use to predict.
            input_path (str): the path of image that would be predict.
            device (str, optional): the running device. Defaults to 'gpu'.
            save_dir (str, optional): the directory path to save output. Defaults to None.

        Returns:
            CompletedProcess: the result of infering subprocess execution.
        """