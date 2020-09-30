# toy-car

## 文件夹说明

### 概述

```bash
toy-car
├── car                         # 快捷命令
├── config.ini                  # toy-car配置文件
├── control                     # 目录：手动控制相关
│   ├── CameraAdjust.py         # 调节相机
│   ├── CarCamera.py            # 类文件：相机
│   ├── Car.py                  # toy-car主程序
│   ├── GetChar.py              # 类文件：实时获取输入字符
│   ├── static                  # flask项目目录
│   │   ├── favicon.png         # 网页图标
│   │   └── style.css           # 网页样式文件
│   └── templates               # flask项目目录
│       └── index.html          # 网页文件
├── html                        # nginx图片服务器目录
│   └── index.html              # 网页文件
├── network                     # 机器学习网络目录
│   ├── CarAuto.py              # toy-car自动驾驶主程序
│   ├── Net.py                  # 机器学习网络模型
│   └── Network.py              # 机器学习网络训练程序
├── README.md                   # 说明文件
└── tools                       # 工具目录
    ├── change.py               # 图像变换程序
    ├── sendtar.py              # raspberry pi发送压缩包程序
    └── train_test_split.py     # 拆分训练集与测试集（7:3）
```

执行`./car init`后生成完整目录，增加目录：

```bash
├── html
│   ├── data                    # 机器学习网络使用数据
│   │   ├── test                # 测试数据
│   │   │   ├── a               # 左转方向数据
│   │   │   ├── d               # 右转方向数据
│   │   │   └── w               # 无转动方向数据
│   │   └── train               # 训练数据
│   │       ├── a               # 左转方向数据
│   │       ├── d               # 右转方向数据
│   │       └── w               # 无转动方向数据
│   └── images                  # toy-car原始数据
│       ├── a                   # 左转方向图片
│       ├── d                   # 右转方向图片
│       └── w                   # 无转动方向图片
├── network
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
| ./car sendtar   -- send tar archive to remote Host
| ./car movetar   -- extra tar archive to ./html/images/, use in remote
| ./car split     -- split original image to train(0.7) and test(0.3)
| ./car change    -- change original image to 32x32 for network
| ./car train     -- train network
| ./car dragon    -- ./car movetar, split, change, train, send model
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
    q:  car start/auto, end program, should use with Ctrl + c
space:  car start/auto, toy-car forward
```

#### `config.ini`

`Pin`: 相应引脚

`Car`: 电机（Motor）速度和舵机（Servo）转向角度

`Camera`: 相机拍摄图像尺寸和调整相机支架参数（抖动过大，未使用）

`Picture`: 机器学习网络使用图像尺寸

`Target`:

- `Host`: 远程主机（用于发送压缩包，raspberry pi 训练速度太慢）
- `File`: 原始数据文件夹

`Network`:

- `Train`: 训练集目录
- `Test`: 测试集目录
- `Epoch`: 训练更新次数
- `LearnRate`: 学习率
- `Model`: 模型存放位置

## 主要依赖库

- [Flask](https://pypi.org/project/Flask/)
- [gpiozero](https://gpiozero.readthedocs.io/en/stable/)
- [numpy](https://pypi.org/project/numpy/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [picamera](https://picamera.readthedocs.io/en/release-1.13/)
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
