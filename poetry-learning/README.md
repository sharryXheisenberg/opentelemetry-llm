# Poetry Information

- Many peoples think they can handle everything with pip and venv. This works for small scripts, but it becomes messy once your project grows

- **Poetry** solves this problem by giving you one clean workflow for managing Python projects from start to finish. Poetry brings structure to your project. It automates package management, creates virtual environments independently, and prepares your project for building and publishing

- Modern Python projects need many moving parts. You install libraries from PyPI, update them over time, track versions to keep the project stable, and share those versions with your team. You also need to package your project if you want others to use it

- The traditional way of using `requirements.txt` and `pip install` does not solve everything

- Poetry brings all these pieces together. It uses one file, `pyproject.toml`, to define everything. It installs packages in a clean **virtual environment**. It **locks** versions to avoid surprises. And it can build and publish your package with a couple of commands.

#### **Add the packages by using poetry**

```bash
poetry add <package_name>
```

#### **Run python program by using Poetry**

```bash
poetry run python main.py
```

#### **You can enter the environment**

```bash
poetry shell
```

### **Understanding pyproject.toml**

- The `pyproject.toml` file holds the data that defines your project. Poetry fills this file when you add or remove dependencies.

- This single file replaces `setup.py`, `requirements.txt`, and many manual steps. Poetry acts as a manager for everything inside it

### **The Lock File**
   - One of the quietly powerful features of Poetry is the lock file. When you add a package, Poetry writes exact versions to `poetry.lock`. This file ensures your project behaves the same across machines.


- Anyone who wants to run your project only needs to run use this command:-

```bash
poetry install
```
