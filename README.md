# StealthimFileStorage

## 使用

> 本程序仅在 Linux 下进行测试，建议使用 docker image 运行

建议去从 Github Actions 下载最新版本而不是 Releases

程序第一次运行时会创建 `config.toml` (docker-compose: `cfg/config.toml`)。此时你应该编辑一些基础配置。

### 小工具

在 docker image 的全局安装中可以使用 `python -m stimfstool` 调用命令行工具。

```bash
python -m stimfstool reload  # 重载配置
python -m stimfstool usage   # 查看用量
```

> 注：重载配置时请勿更改包括 host，port，storgae 等关键参数
>
> 常见的可以重载的参数是 `usage.total`。
>
> 这在让节点变成只读模式时非常有用。
>
> usage.total 并不是强制的，因此你应该在设备存储的基础上预留出至少 20-100 个 block。

## 构建

本程序使用 Makefile(for linux) 管理编译。使用 poetry 管理依赖。

```bash
# 下载依赖
poetry install --with=dev
# 进入虚拟环境
poetry env activate
# 构建 proto
make proto
```

然后可以正常使用 `poetry run main.py` 运行程序。
