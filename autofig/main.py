import matplotlib.pyplot as plt
import argparse
from mpl_toolkits.axes_grid1 import ImageGrid
from omegaconf import OmegaConf
from PIL import Image
from os.path import join, dirname, basename
from glob import glob
import os
import shutil


def load_config(config_path):
    config = OmegaConf.load(config_path)
    return config


def gen_configs(arg):
    path = join(dirname(__file__), "configs")
    for path_f in glob(join(path, "*.yaml")):
        file = basename(path_f)
        if not os.path.exists(file):
            shutil.copy(path_f, file)
            print(f"Copy from {path_f} to {file}")


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--config', default='autofig.yaml')
    p.add_argument('-g', '--gen_config', action='store_true')
    p.add_argument('--output', default=None)
    return p.parse_args()


def plot_w_allcaption(images, labels, config):
    coef_col = 5
    coef_row = 5.5
    figsize = (
        config.layout.num_col * coef_col,
        config.layout.num_row * coef_row,
    )
    fig, axs = plt.subplots(
        config.layout.num_row,
        config.layout.num_col,
        figsize=figsize,
    )
    axs = axs.reshape(-1)

    for ax, im, label in zip(axs, images, labels):
        ax.imshow(im)
        # REMOVE ORDER COLOR
        color_spine = 'white'
        ax.spines['bottom'].set_color(color_spine)
        ax.spines['top'].set_color(color_spine)
        ax.spines['right'].set_color(color_spine)
        ax.spines['left'].set_color(color_spine)

        # REMOVE TICKS
        ax.tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            right=False,
            labelleft=False,
            labelbottom=False,
        )
        ax.set_xlabel(label,
                      fontsize=config.font.size,
                      fontname=config.font.type)

    plt.tight_layout(pad=config.layout.margin, rect=(0, 0, 1, 1))


def plot_images(images, labels, ylabels, config):
    coef_col = 5
    coef_row = 5.5
    figsize = (
        config.layout.num_col * coef_col,
        config.layout.num_row * coef_row,
    )

    fig = plt.figure(figsize=figsize)
    grid = ImageGrid(fig,
                     111,
                     nrows_ncols=(config.layout.num_row,
                                  config.layout.num_col),
                     axes_pad=config.layout.margin)

    for ax, im, label, ylabel in zip(grid, images, labels, ylabels):
        ax.imshow(im)

        # REMOVE ORDER COLOR
        color_spine = 'white'
        ax.spines['bottom'].set_color(color_spine)
        ax.spines['top'].set_color(color_spine)
        ax.spines['right'].set_color(color_spine)
        ax.spines['left'].set_color(color_spine)

        ax.tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            right=False,
            labelleft=False,
            labelbottom=False,
        )

        if label is not None:
            ax.set_xlabel(label,
                          fontsize=config.font.size,
                          fontname=config.font.type)
        if ylabel is not None:
            ax.set_ylabel(ylabel,
                          fontsize=config.font.size,
                          fontname=config.font.type)


def extract_name(path):
    return path.split('/')[-1].split('.')[0]


def main():
    print('Started autofig')
    args = parse()
    if args.gen_config:
        gen_configs()
    else:
        config = load_config(args.config)
        assert config.layout.num_col * config.layout.num_row == len(
            config.images) == len(config.labels) == len(config.ylabels)
        images = [Image.open(p) for p in config.images]
        labels = [a for a in config.labels]
        ylabels = [a for a in config.ylabels]
        if config.all_caption:
            plot_w_allcaption(images, labels, config)
        else:
            plot_images(images, labels, ylabels, config)

        path_output = f"{extract_name(args.config)}.{config.format}" if args.output is None else args.output
        plt.savefig(path_output, dpi=150, bbox_inches="tight")
    print('Finished autofig')


if __name__ == "__main__":
    main()
