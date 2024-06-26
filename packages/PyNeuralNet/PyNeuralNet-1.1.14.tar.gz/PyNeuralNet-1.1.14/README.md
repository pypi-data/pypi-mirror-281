PyNeuralNet
============

Welcome to the PyNeuralNet repository! PyNeuralNet is a python library for prototyping and building neural networks. PyNeuralNet uses PyTorch as a computational backend for deep learning models.

## Installation

1. First, make sure you have Python installed on your system.
2. Use this pip command to install the latest version of package.
   ```bash
   pip install pyneuralnet
   ```

## Usage
```python
from pyneuralnet import train

dataset_loader = 'local'
root_dir = 'path/to/root_diractory'
metadata_file = 'path/to/meta_info_file.txt'
network = 'usrcnn'
batchs = 4

train(datasetloader, metadata_file, root_dir, epochs=25, batch_size=batchs, network=network)

```
- Parameters
   - dataset_loader: Type of dataset loader, there is two type of dataloaders (locally - `local` and from internet - `internet`). In this example, it is set to 'local'.
   - metadata_file: Path to the metadata file. If you load your dataset from internet you should type an url like [this](https://itzloghotxd.github.io/machine-learning-datasets/image-datasets/div2k/meta-info/meta_info_DIV2K_valid_HR.txt).
   - root_dir: Path to the root directory where the dataset is located. If you load your dataset from internet you should type an url like [this](https://itzloghotxd.github.io/machine-learning-datasets/image-datasets/div2k/), example [image](https://itzloghotxd.github.io/machine-learning-datasets/image-datasets/div2k/DIV2K_valid_HR/0864.png).
   - network: Neural network architecture to be used (e.g., 'usrcnn'). There are 6 type of networks(for now) which are based on `Convolutional Neural Network` e.g., `usrcnn`, `esrcnn`, `bsrcnn`, `isrcnn`, `rsrcnn` and `srcnn`.
   - epochs: Number of training epochs.
   - batch_size: Size of each training batch.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, follow these steps:
1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

## License

This project is licensed under the [MIT License](https://github.com/ItzLoghotXD/PyNeuralNet/blob/main/LICENSE) - see the LICENSE file for details.

## Contact

Feel free to reach out to me at **loghot.gamerz.official@gmail.com** if you have any questions or feedback!
Or just open an [issue](https://github.com/ItzLoghotXD/PyNeuralNet/issues) on PyNeuralNet's github page.

Happy coding! 🚀
