## AutoFig

Automatic figure generator such as image grids.

### Examples

#### Single row example
```sh
python main.py --config configs/config1x4.yaml 
```
<figure>
<img src="autofig/assets/config1x4.jpg" alt="fail" style="width:100%">
</figure>


#### Multiple rows example 
```sh
python main.py --config configs/config2x4.yaml 
```
<figure>
<img src="autofig/assets/config2x4.jpg" alt="fail" style="width:100%">
</figure>

#### Multiple rows example with single row label
```sh
python main.py --config configs/config2x4_single.yaml 
```

<figure>
<img src="autofig/assets/config2x4_single.jpg" alt="fail" style="width:100%">
</figure>

#### Multiple rows example with single row label and ylabel
```sh
python main.py --config configs/config2x4_ylab.yaml 
```

<figure>
<img src="autofig/assets/config2x4_ylab.jpg" alt="fail" style="width:100%">
</figure>
