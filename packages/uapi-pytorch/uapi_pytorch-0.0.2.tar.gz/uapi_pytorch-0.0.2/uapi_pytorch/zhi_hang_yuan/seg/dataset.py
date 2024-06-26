import os
import h5py
import torch
from torch.utils.data import Dataset
from random import shuffle


class MatDataset(Dataset):
    def __init__(self, dataset_dir, txt_file):
        self.images = []
        self.annotations = []

        # 读取txt_file文件，构建图像路径和类别id的列表
        with open(os.path.join(dataset_dir, txt_file), 'r') as f:
            for line in f:
                image_path, annotations_path = line.strip().split()
                self.images.append(os.path.join(dataset_dir, image_path))
                self.annotations.append(os.path.join(dataset_dir, annotations_path))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        with h5py.File(self.images[idx], 'r') as mat_file:
            image = mat_file['data'][:]
            image = torch.tensor(image, dtype=torch.float32)
            image = torch.unsqueeze(image, 0)

        with h5py.File(self.annotations[idx], 'r') as mat_file:
            annotation = mat_file['data'][:]
            annotation = torch.tensor(annotation, dtype=torch.float32)
            annotation = torch.unsqueeze(annotation, 0)

        return image, annotation


def check_dataset(dataset_dir=None,
                  dataset_type=None,
                  mode='fast'):
    ds_meta = {'err_msg': "", 'res_flag': True}
    # 读取train.txt和val.txt文件
    for split in ['train', 'val']:
        if not os.path.exists(os.path.join(dataset_dir, f'{split}.txt')):
            ds_meta['res_flag'] = False
            ds_meta['err_msg'] += f"{split}.txt not found.\n"
            break

        with open(os.path.join(dataset_dir, f'{split}.txt'), 'r') as f:
            image_infos = f.readlines()

        for line in image_infos:
            parts = line.rstrip().split()
            if not os.path.exists(os.path.join(dataset_dir, parts[0])):
                ds_meta['res_flag'] = False
                ds_meta['err_msg'] += f"{parts[0]} not found.\n"
                image_infos.remove(line)
            if not os.path.exists(os.path.join(dataset_dir, parts[1])):
                ds_meta['res_flag'] = False
                ds_meta['err_msg'] += f"{parts[1]} not found.\n"
                if line in image_infos:
                    image_infos.remove(line)

        ds_meta[f'{split}.samples'] = len(image_infos)
        shuffle(image_infos)

    if not ds_meta['res_flag']:
        ds_meta["err_type"] = 0
        print(ds_meta['err_msg'])
        return ds_meta
    return ds_meta
