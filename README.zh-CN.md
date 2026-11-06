# Plumbline

**用于研究 LLM 代码审查的基准与分析工具。**

Plumbline 研究审查模型如何识别代码问题、将发现归因到架构规则，以及作出批准／拒绝判决。仓库包含代码变更、模型审查、来源核验标注、提示词和实验结果复算脚本，对应研究 **Flagging Is Not Naming: Mention, Attribution, and Verdicts in LLM Code Review**。

## 快速开始

使用 Python 3.11+，分析过程仅依赖标准库，直接读取仓库中的数据：

```sh
git clone https://github.com/ghosttt0/plumbline.git
cd plumbline
python reproduce.py
python -m unittest discover -s tests -v
python verify.py
```

结果写入 `outputs/summary.json` 与 `outputs/verification.json`，包括实验规模、批准率、逐问题精确率、规则归因率和重复采样一致性。

## 数据与实验

基准覆盖 rentomatic、full-stack-fastapi-template 和 Saleor 三个 Python 代码库：

- 66 个主实验条目：原始网格 33 个，扩展集 33 个。
- 836 条主实验审查：396 条核心审查、132 条 GPT 复核、308 条扩展审查。
- 660 个不同的审查 cell；扩展集 leak 条目包含重复采样。
- 686 条审查带有最终逐问题标注。
- 配对埋入 pilot 另有 18 个条目、72 条审查，单独统计。

评价分别记录构造提及、设计规则归因、问题真实性和审查判决；标注按论文所述的真人双盲编码与仲裁流程开展。

## 使用入口

- `data/`：条目、完整 diff、审查文本、最终标注和 pilot 数据。
- `prompts/`：架构上下文与审查者提示词。
- `materials/`：上游仓库、冻结提交及必要源码快照。
- `expected/`：结果核对使用的参考值。
- `tests/`：数据关联、数值和提示词渲染测试。
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md)：字段、标注类别和统计口径。

按 `release_id` 关联主实验审查与标注，按 `review_id` 关联 pilot 审查与标注。查看某个条目的提示词：

```sh
python render_prompt.py D2-a bare
```

`MANIFEST.json` 提供文件 SHA-256 校验。上游源码保留 `licenses/` 中的原始许可证。完整英文说明见 [README.md](README.md)。
