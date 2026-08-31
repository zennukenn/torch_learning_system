# Environment report

检查时间：2026-09-01（Asia/Shanghai）

## 已观察事实

| 项目 | 结果 | 影响 |
|---|---|---|
| OS | WSL2, Ubuntu 22.04.2, Linux 6.6.87.2 | 适合 Linux 源码阅读与开发 |
| CPU | Intel Core i9-13980HX, WSL 可见 32 logical CPUs | 编译并行度高，但受内存约束 |
| RAM | 7.6 GiB，可用约 6.3 GiB | 完整 PyTorch 构建风险较高 |
| Swap | 2.0 GiB，检查时已使用约 1.1 GiB | 大型 C++ 编译可能发生 OOM/严重换页 |
| Disk | `/home/quanyx` 可用约 892 GiB | 源码、build tree、ccache 空间充足 |
| GPU | `nvidia-smi` 报 `GPU access blocked by the operating system` | 当前不能进行 CUDA runtime 实验 |
| CUDA toolkit | `nvcc` 11.8 | 不能据此推断兼容当前 PyTorch；需按目标 tag 官方要求重配 |
| Python | 3.10.12 | 可建立隔离学习环境 |
| Compiler | GCC/G++ 11.4 | 具备 C++20 基础能力；最终按目标 tag 构建检查 |
| Missing | `cmake`, `ninja`, `gdb` 未找到 | Phase 0 需要补齐 |
| Python torch | 未安装 | 尚不能运行基线 eager/dispatcher 实验 |

## 环境关卡

Agent 在获得明确授权后才安装或修改环境。先按以下顺序诊断：

1. 查 Windows 主机物理内存和 `.wslconfig`，目标至少给 WSL 16 GiB；完整 CUDA 构建更适合 24–32 GiB 或以上。具体值以主机资源为限。
2. 在 Windows/WSL 两侧诊断 NVIDIA driver、WSL GPU 映射和 `nvidia-smi`；在修复前采用 CPU-first。
3. 为目标 stable tag 创建独立 Python 环境，避免污染系统 Python。
4. 按该 tag 的 `README.md`、`CONTRIBUTING.md` 和依赖元数据确定 CMake、Ninja、编译器、CUDA/cuDNN 组合。
5. 先安装或构建可运行的 CPU 版本，验证小测试和增量开发；再启用 CUDA。
6. 使用低并发作为 8 GiB 内存下的临时策略，并监控峰值内存；不要直接以 32 jobs 构建。

## 待采集

- Windows 版本、主机物理内存、GPU 型号和 driver 版本；
- `.wslconfig` 的 memory/swap 设置；
- 目标 tag 的构建依赖与 CUDA 支持矩阵；
- VS Code C++ 扩展、Python 环境管理方式；
- 是否能在另一台 Linux/CUDA 机器运行硬件或 GPU 实验。

不得把“有 `nvcc`”等同于“PyTorch CUDA 可用”，也不得把 WSL 报错直接归因于某一个原因；必须用进一步证据诊断。
