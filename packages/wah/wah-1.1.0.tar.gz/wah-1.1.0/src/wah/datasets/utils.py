import random

import torch
from torch.utils.data import Subset

from ..typing import (
    Dataset,
    Literal,
    Optional,
    Tensor,
    Tuple,
)

__all__ = [
    "mean_and_std",
    "portion_dataset",
]


def mean_and_std(
    dataset: Dataset,
    data_shape: Literal[
        "CHW",
        "HWC",
        "HW",
    ] = "CHW",
) -> Tuple[Tensor, Tensor]:
    """
    Computes the mean and standard deviation of the dataset.

    ### Parameters
    - `dataset` (Dataset):
      The dataset for which to compute the mean and standard deviation.
      Note that the dataset must contain data of type `torch.Tensor` for computation.
    - `data_shape` (str):
      The shape format of the data in the dataset. Defaults to "CHW".
        - "CHW": Channels-Height-Width
        - "HWC": Height-Width-Channels
        - "HW": Height-Width (grayscale images)

    ### Returns
    - Tensor:
      The mean value of the dataset.
    - Tensor:
      The standard deviation of the dataset.

    ### Raises
    - ValueError:
      If an unsupported data_shape is provided.

    ### Notes
    - The dataset must contain data of type `torch.Tensor` for computation.
      For instance, use `torchvision.transforms.ToTensor()` to transform PIL Image data into tensor format.
    - The data is converted to float32 before computing mean and standard deviation.

    ### Example
    ```python
    import wah

    dataset = Dataset(...)    # data is RGB image
    mean, std = wah.datasets.mean_and_std(
        dataset=dataset,
        data_shape="CHW",
    )
    # mean.shape: torch.Size([3])
    # std.shape: torch.Size([3])
    ```
    """
    data = []

    for x in dataset:
        if isinstance(x, tuple):
            x: Tensor = x[0]

        data.append(x.unsqueeze(dim=0))

    data = torch.cat(data, dim=0).to(torch.float32)

    if data_shape == "CHW":
        dim_to_reduce = (0, 2, 3)
    elif data_shape == "HWC":
        dim_to_reduce = (0, 1, 2)
    elif data_shape == "HW":
        dim_to_reduce = (0, 1, 2)
    else:
        raise ValueError(f"Unsupported data_shape: {data_shape}")

    mean = data.mean(dim=dim_to_reduce)
    std = data.std(dim=dim_to_reduce)

    return mean, std


def portion_dataset(
    dataset: Dataset,
    portion: float,
    balanced: Optional[bool] = True,
    random_sample: Optional[bool] = False,
) -> Dataset:
    """
    Creates a subset of the given dataset based on the specified portion.

    ### Parameters
    - `dataset` (Dataset):
      The dataset from which to create the subset.
    - `portion` (float):
      The portion of the dataset to include in the subset. Must be in range (0, 1].
    - `balanced` (bool, optional):
      Whether to create a balanced subset.
      If True, the subset will have a balanced number of samples from each class.
      Defaults to True.
    - `random_sample` (bool, optional):
      Whether to randomly sample the indices.
      If False, the subset will include the first `portion` of the dataset.
      Defaults to False.

    ### Returns
    - `Dataset`:
      A subset of the original dataset based on the specified portion.

    ### Raises
    - `AssertionError`:
      If `portion` is not in range (0, 1].
    - `AssertionError`:
      If `balanced` is True and the dataset does not have targets.

    ### Notes
    - When `balanced` is True, the dataset must have a 'targets' attribute containing the labels for balancing.
    - When `random_sample` is True, the function will randomly select samples.
      This can lead to different subsets on different runs.

    ### Example
    ```python
    import wah

    dataset = Dataset(...)
    subset = wah.datasets.portion_dataset(
        dataset=dataset,
        portion=0.8,
        balanced=True,
        random_sample=False,
    )
    # len(subset) == len(dataset) * 0.8
    ```
    """
    assert 0 < portion <= 1, f"Expected 0 < portion <= 1, got {portion}"

    if balanced:
        assert hasattr(
            dataset, "targets"
        ), f"Unable to create a balanced dataset as there are no targets in the dataset."

        targets = dataset.targets
        classes = list(set(targets))

        indices = []

        for c in classes:
            c_indices = [i for i, target in enumerate(targets) if target == c]
            num_c = int(len(c_indices) * portion)

            if random_sample:
                c_indices = random.sample(c_indices, num_c)

            else:
                c_indices = c_indices[:num_c]

            indices += c_indices

    else:
        num_data = int(len(dataset) * portion)

        if random_sample:
            indices = random.sample([i for i in range(len(dataset))], num_data)

        else:
            indices = [i for i in range(len(dataset))][:num_data]

    return Subset(dataset, indices)
