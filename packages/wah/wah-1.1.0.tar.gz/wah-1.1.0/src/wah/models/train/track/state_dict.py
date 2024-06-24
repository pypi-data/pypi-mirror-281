import os

import torch

from ....typing import (
    Module,
    SummaryWriter,
)

__all__ = [
    "save",
]


def save(
    model: Module,
    epoch: int,
    every_n_epochs: int,
    tensorboard: SummaryWriter,
) -> None:
    if epoch % every_n_epochs == 0:
        ckpt_dir = os.path.join(tensorboard.log_dir, "checkpoints")
        os.makedirs(ckpt_dir, exist_ok=True)

        # epoch = str(epoch).zfill(4)
        fname = f"epoch={epoch}.ckpt"

        torch.save(
            model.state_dict(),
            os.path.join(ckpt_dir, fname),
        )
