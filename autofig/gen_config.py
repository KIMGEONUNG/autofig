from omegaconf import OmegaConf
from os.path import join, dirname, basename
import yaml


def gen_custom_config(
    row,
    col,
):
    config = OmegaConf.load(join(dirname(__file__), 'configs/autofig.yaml'))
    config.layout.num_col = col
    config.layout.num_row = row

    total = col * row

    config.images = ["${Black}" for j in range(row) for i in range(col)]
    config.labels = [
        "(" + chr(ord('a') + i) + ")" if j == row - 1 else ''
        for j in range(row) for i in range(col)
    ]
    config.ylabels = [
        "(" + chr(ord('A') + j) + ")" if i == 0 else '' for j in range(row)
        for i in range(col)
    ]

    config_str = OmegaConf.to_yaml(config)
    with open('autofig.yaml', 'w') as file:
        file.write(config_str)


def main():
    gen_custom_config(
        row=2,
        col=3,
    )


if __name__ == "__main__":
    main()
