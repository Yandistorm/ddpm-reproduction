@echo off
echo ========================================
echo Git 快速设置和推送脚本
echo ========================================
echo.

REM 配置Git用户信息（如果还没配置）
echo [1/4] 配置Git用户信息...
git config --global user.name "YourName"
git config --global user.email "your.email@example.com"
echo 请手动修改上面的用户名和邮箱！
echo.

REM 提交代码
echo [2/4] 提交代码...
git commit -m "DDPM复现项目初始化"
echo.

REM 添加远程仓库
echo [3/4] 添加GitHub远程仓库...
echo 请先在GitHub创建仓库，然后运行：
echo git remote add origin https://github.com/你的用户名/仓库名.git
echo.

REM 推送代码
echo [4/4] 推送到GitHub...
echo git branch -M main
echo git push -u origin main
echo.

echo ========================================
echo 完成！
echo ========================================
pause
