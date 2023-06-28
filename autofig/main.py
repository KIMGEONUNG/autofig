import matplotlib.pyplot as plt
import argparse
from mpl_toolkits.axes_grid1 import ImageGrid
from omegaconf import OmegaConf
from PIL import Image
from os.path import join, dirname, basename
from glob import glob
import os
import shutil
import re


def load_config(config_path):
    config = OmegaConf.load(config_path)
    return config


def gen_custom_config(
    row,
    col,
    path_imgs=None,
    labels=None,
    ylabels=None,
    tag=None,
):
    config = OmegaConf.load(join(dirname(__file__), 'configs/autofig.yaml'))
    config.layout.num_col = col
    config.layout.num_row = row

    total = col * row

    if tag:
        config.name = tag

    images = ["%Black" for j in range(row) for i in range(col)]
    if path_imgs:
        images = (path_imgs + images)[:total]
    config.images = images

    if labels is None:
        config.labels = [
            "(" + chr(ord('a') + i) + ")" if j == row - 1 else ''
            for j in range(row) for i in range(col)
        ]
    else:
        config.labels = labels

    if ylabels is None:
        config.ylabels = [
            "(" + chr(ord('A') + j) + ")" if i == 0 else '' for j in range(row)
            for i in range(col)
        ]
    else:
        config.ylabels = ylabels

    config_str = OmegaConf.to_yaml(config)

    path = f'autofig.{tag}.yaml' if tag else 'autofig.yaml'
    assert not os.path.exists(path)
    with open(path, 'w') as file:
        file.write(config_str)
    return path


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--config', default='autofig.yaml')
    p.add_argument('-g', '--gen_config', type=str, default=None)
    p.add_argument('--img', type=str, nargs='+', default=None)
    p.add_argument('-s', '--size', type=int, default=None)
    p.add_argument('--output', default=None)
    p.add_argument('--tag', default=None)

    p.add_argument('-x', type=str, default=None)
    p.add_argument('-y', type=str, default=None)
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


def parse2convention(paths):
    ls = []
    for path in paths:
        string, _ = os.path.splitext(path)
        info = {}
        info['%0'] = path
        for value in string.split('-'):
            key_val = value.split(':')
            if len(key_val) == 1:
                info[key_val[0]] = ''
            elif len(key_val) == 2:
                info[key_val[0]] = key_val[1]
            else:
                raise AssertionError
        ls.append(info)
    return ls


def extract_labels(names, x, y):
    rows = sorted(list(set([i[y] for i in names])))
    cols = sorted(list(set([i[x] for i in names])))
    n_total = len(names)
    n_row = len(rows)
    n_col = len(cols)

    labelx = [
        "(" + chr(ord('a') + i) + ") " + x + " " + cols[i] if j == n_row -
        1 else '' for j in range(n_row) for i in range(n_col)
    ]

    labely = [
        y + " " + rows[j] if i == 0 else '' for j in range(n_row)
        for i in range(n_col)
    ]

    return labelx, labely


def cal_row_col(names, x, y):
    row = len(set([i[y] for i in names]))
    col = len(set([i[x] for i in names]))
    return row, col


MACROS = {
    "%Black": Image.new("RGB", (512, 512)),
}


def mk_figure(config, args):
    num_total = config.layout.num_col * config.layout.num_row
    assert num_total == len(config.images)

    # PADDING WITH LAST ONE
    config.labels = [
        config.labels[min(len(config.labels) - 1, i)] for i in range(num_total)
    ]
    config.ylabels = [
        config.ylabels[min(len(config.ylabels) - 1, i)]
        for i in range(num_total)
    ]

    images = [
        MACROS[p] if p[0] == "%" else Image.open(p) for p in config.images
    ]
    if args.size:
        tmp = []
        for image in images:
            w, h = image.size
            ratio = args.size / h
            w_, h_ = int(ratio * w), int(ratio * h)
            tmp.append(image.resize((w_, h_)))
        images = tmp

    labels = [a for a in config.labels]
    ylabels = [a for a in config.ylabels]
    if config.all_caption:
        plot_w_allcaption(images, labels, config)
    else:
        plot_images(images, labels, ylabels, config)

    path_output = f"{config.name}.{config.format}" if args.output is None else args.output
    plt.savefig(path_output, dpi=150, bbox_inches="tight")


def main():
    print('Started autofig')
    args = parse()
    if args.gen_config:
        pattern = re.compile(r'(\d+)x(\d+)')
        match = pattern.search(args.gen_config)
        assert match
        row = int(match.group(1))
        col = int(match.group(2))
        gen_custom_config(row, col, args.img, tag=args.tag)
        return
    elif args.x is not None and args.y is not None and args.img is not None:
        # To sort, we should parse the string into dictionary
        x, y = args.x, args.y
        data = parse2convention(args.img)
        data_sorted = list(sorted(data, key=lambda a: (a[y], a[x])))
        names = [item["%0"] for item in data_sorted]
        row, col = cal_row_col(data_sorted, x, y)
        labelx, labely = extract_labels(data_sorted, x, y)
        path = gen_custom_config(row, col, names, labelx, labely,
                          tag=args.tag)  # sould define row and col
        config = load_config(path)
        mk_figure(config, args)
    else:
        assert os.path.exists(args.config)
        config = load_config(args.config)
        mk_figure(config, args)
    print('Finished autofig')


if __name__ == "__main__":
    main()
