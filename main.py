import matplotlib.pyplot as plt
import argparse
from omegaconf import OmegaConf
from PIL import Image


def load_config(config_path):
    config = OmegaConf.load(config_path)
    return config


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='configs/config2x4_label.yaml')
    return p.parse_args()


def plot_images(images, labels, config):
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

    for i in range(len(images)):
        axs[i].imshow(images[i])

        # REMOVE ORDER COLOR
        color_spine = 'white'
        axs[i].spines['bottom'].set_color(color_spine)
        axs[i].spines['top'].set_color(color_spine)
        axs[i].spines['right'].set_color(color_spine)
        axs[i].spines['left'].set_color(color_spine)

        # REMOVE TICKS
        if labels[i] is None:
            axs[i].axis('off')
            axs[i].axis('tight')
            axs[i].axis('image')
        else:
            axs[i].tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
            )
            axs[i].set_xlabel(labels[i], fontsize=20, fontname=config.font.type)

    plt.tight_layout(pad=config.layout.margin, rect=(0, 0, 1, 1))
    plt.savefig(config.output, dpi=150, bbox_inches="tight")


def main():
    args = parse()
    config = load_config(args.path)
    assert config.layout.num_col * config.layout.num_row == len(
        config.images) == len(config.labels)
    images = [Image.open(p) for p in config.images]
    labels = [a for a in config.labels]
    plot_images(images, labels, config)


if __name__ == "__main__":
    main()
