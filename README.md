# toy-car

## 文件夹说明

### 概述

```bash
├── car                       # 快捷命令
├── config.ini                # toy-car 配置文件
├── control                   # 目录：手动控制相关
│   ├── Car.py                # 读取配置文件，判断_Cmd.py或_View.py
│   ├── _Cmd.py               # 基于命令行的采集工具
│   ├── GetChar.py            # 类文件：实时获取输入字符
│   └── _View.py              # 基于图形化界面的采集工具
├── html                      # nginx图片服务器目录
│   ├── data                  # 训练测试使用数据
│   ├── index.html            # 网页文件
│   └── rwby.jpg              # 测试图片
├── network                   # 网络模型文件夹
│   ├── _AutoAcc.py           # 使用OpenVINO加速的寻路程序
│   ├── _Auto.py              # 使用Raspberry Pi CPU的寻路程序
│   ├── Car.py                # 读取配置文件，判断_Auto.py或_AutoAcc.py
│   ├── model                 # 模型文件
│   │   ├── model.bin         # 计算棒使用，包含权重和偏差二进制数据。
│   │   ├── model.mapping     # 计算棒使用，映射文件
│   │   ├── model.onnx        # onnx格式网络数据文件
│   │   ├── model.pth         # pytorch格式网络数据文件
│   │   └── model.xml         # 计算棒使用，描述网络拓扑。
│   ├── Net.py                # 网络模型
│   ├── pytorch2onnx.py       # pytorch格式转onnx格式
│   └── Train.py              # 模型训练文件
├── README.md                 # 说明文件
└── tools                     # 工具目录
    └── check.py              # 移除空文件
```

执行`./car init`后生成完整目录，增加目录：

```bash
├── html
│   └── data                  # 网络训练测试使用数据
│       ├── a                 # 左转方向数据
│       ├── d                 # 右转方向数据
│       └── w                 # 直行方向数据
└─ network
    └── model
```

### 一些文件详细说明

#### `car`

详情请使用`./car help`

```bash
help
usage:
car               -- Simplified operation
| ./car init      -- init basic folder
| ./car help      -- help infomation
| ./car camera    -- adjust car camera by computer
| ./car start     -- control car by computer
| ./car check     -- check if picture is empty
| ./car train     -- train network
| ./car auto      -- control car by network
| ./car clean     -- clean useless image and model
V
         _____________________________ 
        |                             |
        | q w                       p |
        | a   d              h j k l  |
        |                             |
        |                             |
        |            _____            |
        |           |space|           |
        |            -----            |
        |_____________________________|

    w:  car start, adjust direction to forward
    a:  car start, adjust direction to left
    d:  car start, adjust direction to right
    h:  car camera, adjust camera left
    j:  car camera, adjust camera down
    k:  car camera, adjust camera up
    l:  car camera, adjust camera right
    p:  car auto, stop toy-car
    q:  car start/auto, end program
space:  car start/auto, forward then stop; stop then forward
```

#### `config.ini`

`Pin`: 相应引脚

- `CameraH`：水平方向调节舵机
- `CameraV`：垂直方向调节舵机
- `MotorA`：电机接口
- `MotorB`：电机接口
- `Direction`：方向控制舵机

`Car`: 电机（Motor）速度和舵机（Servo）转向角度

- `Speed`：速度控制
- `Left`：左转角度
- `Right`：右转角度


`Network`:

- `BatchSize`：一次处理数量
- `Data`：训练数据目录
- `Epoch`： 训练更新次数
- `LearnRate`: 学习率
- `Model`： 模型存放位置
- `OpenVINO`：Intel Neural Compute Stick 2是否可用（`True`可用，`False`不可用）

`View`:

- `View`：图形化界面是否可用（`True`可用，`False`不可用）

## 主要依赖库

- [gpiozero](https://gpiozero.readthedocs.io/en/stable/)
- [numpy](https://pypi.org/project/numpy/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [Pillow](https://pypi.org/project/Pillow/)
- [pytorch](https://pytorch.org/)中的[torch](https://github.com/pytorch/pytorch)与[torchvision](https://github.com/pytorch/vision.git)

## 其它

### 配置`nginx`图片服务器

安装`nginx`

```bash
sudo apt install nginx
```

编辑配置文件`/etc/nginx/sites-available/default`

```bash
sudo vim /etc/nginx/sites-available/default
```

增加内容，其中`root`位置具体到项目可能有所不同。

```conf
location /images/ {
    root /home/pi/toy-car/html;
    autoindex on;
}

location /data/ {
    root /home/pi/toy-car/html;
    autoindex on;
}
```

可选：nginx 默认时间是`UTC`，修改为本地

编辑文件`/etc/nginx/nginx.conf`，在`http`内加入

```conf
autoindex_localtime on;
```

### 安装`pytorch`

`pytorch`官网没有`arm`版本，可以在网上找别人打包的`.whl`文件（我打包的[raspberry-torch](https://gitee.com/mrsoymilk/raspberry-torch)）或者手动编译安装。下面是手动安装过程：

#### `swap`扩容

不扩容的话会非常慢，导致异常的失败。

1. 暂时停止 swap

```bash
sudo dphys-swapfile swapoff
```

2. 修改 swap 大小

编辑文件：`/etc/dphys-swapfile`，修改`CONF_SWAPSIZE`

扩容至至少 1G（我选择了 2G）

```bash
CONF_SWAPSIZE=1024
```

3. 应用修改

```bash
sudo dphys-swapfile setup
```

4. 启动 swap

```bash
sudo dphys-swapfile swapon
```

#### 安装依赖

```bash
sudo apt install libopenblas-dev libblas-dev m4 cmake python3-yaml libatlas-base-dev
```

#### 编译`pytorch`

##### 编译`torch`

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

可选：在`./dist`目录下生成`.whl`文件

```bash
sudo -E python3 setup.py bdist_wheel
```

##### 编译`torchvision`

获取`torchvision`

```bash
git clone https://github.com/pytorch/vision.git
```

编译（可以直接使用`install`，默认构建）

```bash
sudo -E python3 setup.py build
sudo -E python3 setup.py install
```

可选：在`./dist`目录下生成`.whl`文件

```bash
sudo -E python3 setup.py bdist_wheel
```

