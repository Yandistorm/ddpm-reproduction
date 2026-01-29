@echo off
REM Windows环境快速设置脚本

echo ========================================
echo DDPM环境设置脚本
echo ========================================

REM 检查Python
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境
echo.
echo [1/4] 创建虚拟环境...
if not exist venv (
    python -m venv venv
    echo 虚拟环境创建成功
) else (
    echo 虚拟环境已存在
)

REM 激活虚拟环境
echo.
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo.
echo [3/4] 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo [4/4] 安装依赖包...
pip install -r requirements.txt

echo.
echo ========================================
echo 环境设置完成！
echo ========================================
echo.
echo 下一步:
echo 1. 准备数据集到 ./data/images 目录
echo 2. 运行测试: python scripts\test_model.py
echo 3. 开始训练: python train.py
echo.
pause
