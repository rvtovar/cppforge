# cppforge

`cppforge` is a powerful and user-friendly CLI tool designed to simplify the creation, management, and building of C++ projects. With support for C++ classes, modules, generators, build automation, and Docker development environments, `cppforge` streamlines your C++ development workflow.

---

## Features
- **Generate C++ Classes**: Quickly create class header and implementation files.
- **C++20 Modules**: Automate the creation of module-based classes and implementation files.
- **Build Automation**: Parse and use `CMakePresets.json` to generate, build, and run projects.
- **Preset Management**: Organize multiple build configurations with ease.
- **Customized Docker Containers**: Spin up development environments for isolated and reproducible builds.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Configuration](#configuration)
- [License](#license)

---

## Installation

### Clone the Repository:
```bash
git clone https://github.com/<your-username>/cppforge.git
cd cppforge
```

### Install with `pip`:
Make sure you have Python 3.7+ and `pip` installed.

```bash
pip install -e .
```

---

## Usage

Run `cppforge` with the desired command:

```bash
cppforge [COMMAND] [ARGS...]
```

For example:
```bash
cppforge new MyProject
```

Get help for available commands:
```bash
cppforge -h
```

---

## Commands

### **Project Commands**
- `new`: Create a new C++ project with support for CMake.
   ```bash
   cppforge new MyProject
   ```

   Options:
   - `--prod`: Create the project in release mode.

### **Class Creation Commands**
- `class`: Generate a header and implementation file for your class.
   ```bash
   cppforge class ClassName
   ```

   Options:
   - `--module`: Generate a C++ module-based class instead of traditional files.

### **Module Commands**
- `module`: Generate a C++ module interface file.
   ```bash
   cppforge module ModuleName
   ```

### **Build Commands**
- **Generate and Build**:
   ```bash
   cppforge generate --preset <CMakePreset>
   ```
   - `--export-compile-commands`: Export a `compile_commands.json` file for tools like clangd.
- **Build Only**:
   ```bash
   cppforge build --preset <CMakePreset>
   ```
- **Run Only**:
   ```bash
   cppforge run --preset <CMakePreset> --executable <PathToExecutable>
   ```

- **Build and Run**:
   ```bash
   cppforge build-run --preset <CMakePreset> --executable <PathToExecutable>
   ```

### **Docker Commands**
- `spinup`: Spin up a development Docker container for building and testing.
   ```bash
   cppforge spinup
   ```

### **Setup Commands**
- `setup`: Set up the default configuration for `cppforge`.
   ```bash
   cppforge setup
   ```

---

## Configuration
`cppforge` uses a configuration file to define default settings. The configuration file `cppforge.yaml` is located in `~/.config/cppforge/`.

### Example Configuration (`~/.config/cppforge/cppforge.yaml`):
```yaml
docker:
  docker_compose_file: "docker-compose.yml"
  default_container_name: "cpp-dev"

cmake:
  presets_path: "CMakePresets.json"
  default_generator: "Ninja"
```

---

## Development Setup

1. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

3. **Test the CLI**:
   ```bash
   cppforge -h
   ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
