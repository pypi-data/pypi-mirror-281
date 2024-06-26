import logging
import time
import torch
import yaml

from parallel_wavegan.utils import load_model
from s3prl_vc.utils import read_hdf5


class Vocoder(object):
    def __init__(self, checkpoint, config, stats, trg_stats, device):
        self.device = device
        self.trg_stats = {
            "mean": trg_stats["mean"].to(self.device),
            "scale": trg_stats["scale"].to(self.device),
        }

        # load config
        with open(config) as f:
            self.config = yaml.load(f, Loader=yaml.Loader)

        # load model
        self.model = load_model(checkpoint, self.config)
        logging.info(f"Loaded model parameters from {checkpoint}.")
        self.model.remove_weight_norm()
        self.model = self.model.eval().to(device)

        # load stats for normalization
        self.stats = {
            "mean": torch.tensor(read_hdf5(stats, "mean"), dtype=torch.float).to(
                self.device
            ),
            "scale": torch.tensor(read_hdf5(stats, "scale"), dtype=torch.float).to(
                self.device
            ),
        }

    def decode(self, c):
        # normalize with vocoder stats
        c = (c - self.stats["mean"]) / self.stats["scale"]

        start = time.time()
        y = self.model.inference(c, normalize_before=False).view(-1)
        rtf = (time.time() - start) / (len(y) / self.config["sampling_rate"])
        logging.info(f"Finished waveform generation. (RTF = {rtf:.03f}).")
        return y, self.config["sampling_rate"]
