# toy-car

## 主要库

- gpiozero
- torch
- torchvision
- pynput
- picamera

### 安装pytorch

#### swap扩容

1. 暂时停止swap

```bash
sudo dphys-swapfile swapoff
```

2. 修改swap大小

编辑文件：`/etc/dphys-swapfile`，修改`CONF_SWAPSIZE`

扩容至至少1G

```bash
CONF_SWAPSIZE=1024
```

3. 应用修改

```bash
sudo dphys-swapfile setup
```

4. 启动swap

```bash
sudo dphys-swapfile swapon
```

#### 安装依赖

```bash
sudo apt install libopenblas-dev libblas-dev m4 cmake python3-yaml libatlas-base-dev
```

#### pytorch部分

##### torch

获取`pytorch`

```bash
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
git submodule sync
git submodule update --init --recursive
```

设置环境变量

```bash
export USE_CUDA=0
export USE_MKLDNN=0
export USE_NNPACK=0
export USE_QNNPACK=0
export USE_DISTRIBUTED=0
export USE_NUMPY=1
export NO_CUDA=1
export NO_DISTRIBUTED=1
export NO_MKLDNN=1
export NO_NNPACK=1
export ONNX_ML=1
export MAX_JOBS=3
```

编译（可以直接使用`install`，默认构建）

```bash
sudo -E python3 setup.py build
sudo -E python3 setup.py install
```

可选：生成`.whl`文件，在`./dist`目录下

```bash
sudo -E python3 setup.py bdist_wheel
```

##### vision

```bash
git clone https://github.com/pytorch/vision.git
```

编译（可以直接使用`install`，默认构建）

```bash
sudo -E python3 setup.py build
sudo -E python3 setup.py install
```

可选：生成`.whl`文件

```bash
sudo -E python3 setup.py bdist_wheel
```

## 引脚说明

### 超声波模块

- Trig: GPIO 20
- Echo: GPIO 21

### 摄像机模块

- 纵向舵机: GPIO 3
- 横向舵机: GPIO 2

### 方向模块

GPIO 4

### 动力模块

- GPIO 7
- GPIO 8


## 其他

批量删除空文件

```bash
find . -name '*' -type f -size 0c | xargx -n 1 rm -f
```
