#!/bin/bash

python main.py --config configs/config1x2.yaml --output "assets/1x2.pdf"
python main.py --config configs/config1x3.yaml --output "assets/1x3.pdf"
python main.py --config configs/config1x4.yaml --output "assets/1x4.pdf"
python main.py --config configs/config2x4.yaml --output "assets/2x4.pdf"
python main.py --config configs/config2x4_single.yaml --output "assets/2x4_single.pdf"
