import torch
import torch.nn.functional as F
from torch import nn

from ...typing import Tensor

__all__ = [
    "UNet",
]


class DoubleConv(nn.Module):
    """(Conv2d => BN => ReLU) * 2"""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        mid_channels: int = None,
    ) -> None:
        super().__init__()

        if not mid_channels:
            mid_channels = out_channels

        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(
        self,
        x: Tensor,
    ) -> Tensor:
        return self.double_conv(x)


class Down(nn.Module):
    """Downscaling (maxpool) => DoubleConv"""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ) -> None:
        super().__init__()

        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels),
        )

    def forward(
        self,
        x: Tensor,
    ) -> Tensor:
        return self.maxpool_conv(x)


class Up(nn.Module):
    """Upscaling => DoubleConv"""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        bilinear: bool = True,
    ) -> None:
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)

        else:
            self.up = nn.ConvTranspose2d(
                in_channels,
                in_channels // 2,
                kernel_size=2,
                stride=2,
            )
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(
        self,
        x1: Tensor,
        x2: Tensor,
    ) -> Tensor:
        x1 = self.up(x1)

        # input is CHW
        diffH = x2.size()[2] - x1.size()[2]
        diffW = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffW // 2, diffW - diffW // 2, diffH // 2, diffH - diffH // 2])
        # if you have padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd

        x = torch.cat([x2, x1], dim=1)

        return self.conv(x)


class OutConv(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ) -> Tensor:
        super().__init__()

        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(
        self,
        x: Tensor,
    ) -> Tensor:
        return self.conv(x)


class UNet(nn.Module):
    """
    [**UNet**](https://arxiv.org/abs/1505.04597) model for image segmentation.

    ### Parameters
    - `num_channels` (int):
      The number of input channels.
    - `num_classes` (int):
      The number of output classes.
    - `bilinear` (bool, optional):
      Whether to use bilinear upsampling. Defaults to False.
    """

    def __init__(
        self,
        num_channels: int,
        num_classes: int,
        bilinear: bool = False,
    ) -> None:
        """
        - `num_channels` (int):
        The number of input channels.
        - `num_classes` (int):
        The number of output classes.
        - `bilinear` (bool, optional):
        Whether to use bilinear upsampling. Defaults to False.
        """
        super().__init__()

        self.num_channels = num_channels
        self.num_classes = num_classes
        self.bilinear = bilinear

        self.in_conv = DoubleConv(num_channels, 64)

        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        factor = 2 if bilinear else 1
        self.down4 = Down(512, 1024 // factor)

        self.up1 = Up(1024, 512 // factor, bilinear)
        self.up2 = Up(512, 256 // factor, bilinear)
        self.up3 = Up(256, 128 // factor, bilinear)
        self.up4 = Up(128, 64, bilinear)

        self.out_conv = OutConv(64, num_classes)

    def forward(
        self,
        x: Tensor,
    ) -> Tensor:
        x1 = self.in_conv(x)

        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)

        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)

        logits = self.out_conv(x)

        return logits
