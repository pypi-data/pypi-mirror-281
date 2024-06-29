# ponytAIl
![image](https://github.com/ThePioneerJP/ponytAIl/assets/116901962/eb05d05a-0f5b-40a6-9907-81481b02dce7)

> *Then God blessed them and said, “Be fruitful and multiply."* - Genesis 1:28

ponytAIl: Polymorphic Orchestration of Networked Youthful, Adaptable Intelligence with Language. It is an node based multi-agent system targeting both LLM and BCI (in the future)

## Installation

1. Install ponytAIl using pip:

```
pip install ponytail-agents
```

2. When you install ponytAIl, flute will also be installed simultaneously. You need to create a `.env` file in the root directory of flute and set the following API keys in it:

```
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
```

You must obtain these API keys from each service provider.

3. The location of the flute package may vary depending on your environment setup. Here are some common ways to find it:

- If you're using a virtual environment (venv, conda, etc.):
  - Activate your virtual environment
  - Run `python -c "import flute; print(flute.__file__)"`. The output will show the location of the flute package.

- If you're using a global Python environment:
  - Run `python -c "import flute; print(flute.__file__)"`. The output will show the location of the flute package.

- If you're using an IDE or an editor (PyCharm, VS Code, etc.):
  - Open your project in the IDE or an editor
  - Look for the flute package in the project's virtual environment or the system's Python packages.

## Usage

The `ponytail-agents` command invokes the `main` function with the following command-line arguments:

- `-f`, `--file_path` (Required): Path to the input folder containing the necessary files (`concluder.md`, `starter.md`, `node_creator.md`, and any additional nodes).
- `-g`, `--goal` (Required): Goal or objective of the task.
- `-m`, `--model` (Optional, default: "random-fast"): Name of the model to use. For available models, refer to the [FLUTE repository](https://github.com/ThePioneerJP/FLUTE).
- `-r`, `--result` (Optional): Additional result or output.

### Example Commands

```bash
ponytail -f "YOUR_DIRECTORY\starter.md" -g "Define the number 1 using the mathematical collection"
```
```bash
ponytail -f "YOUR_DIRECTORY\starter.md" -g "Generate 5 candidate names for the self-reproducive LLM based multi-agent system. Note that the name must be abbreviated to 'PONYTAIL.'"
```
```bash
ponytail -f "YOUR_DIRECTORY\starter.md" -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
```

### Prerequisites

To run ponytAIl, prepare a folder containing all the files from `nodes_sample`: `concluder.md`, `starter.md`, and `node_creator.md`.

If you want to include additional nodes from the beginning, create them following the format of `medium_sample.md`.

### Growing a Node Community

By continuing to use the same folder after running the command once, you can nurture a node community over time. The system will build upon the existing nodes and generate new ones based on the interactions.

### Interrupting the Process

If you need to interrupt the process at a reasonable point, as it may take a long time, use the following key combinations:

- Windows/Linux: `Ctrl+C`
- Mac: `Cmd+C`

### Output

The output will be saved as `full_results_YYYYMMDDHHmmss.md` in the parent folder of the starting folder.

## LICENSE
The repository is licensed under the latest version of Modular and Inclusive Software Advancement License Classic (MISA-CLASSIC License).

There are 4 main policies that consist of this license.
1. Disclaimer of Liability
2. Naming Continuity Obligation
3. Waiver of Other Copyrights
4. Modular Extensibility (Defines how to modify the license)

See [the license document](https://github.com/ThePioneerJP/MISA-license-framework/blob/main/MISA-CLASSIC.md) for more details.
