## AutoFig

### Execution examples

```sh
python main.py --config configs/config1x2.yaml --output "assets/1x2.pdf"
python main.py --config configs/config1x3.yaml --output "assets/1x3.pdf"
python main.py --config configs/config1x4.yaml --output "assets/1x4.pdf"
python main.py --config configs/config2x4.yaml --output "assets/2x4.pdf"
python main.py --config configs/config2x4_single.yaml --output "assets/2x4_single.pdf"
```
Check the outputs in assets directory

### Config Example

```yaml
layout: 
  num_row: 1
  num_col: 4
  margin: 0.1
font:
  size: 20
  type: Arial
images:
  - assets/sample01.jpg
  - assets/sample01.jpg
  - assets/sample01.jpg
  - assets/sample01.jpg
labels:
    - (a) Ours
    - (b) Method1
    - (C) Method2
    - (d) Method3
```
