# Installation and Project SetUp

In this chapter, we install FastAPI, starting with a minimal setup.

### 1. Virtual Environment Creation

Begin by creating a virtual environment using the built-in Python module `venv`. If you already have Python installed, you might not need to install it separately. However, on Linux, installation may be necessary based on your distribution. In your commandline or terminal, type the following command.

```
python3 -m venv env
```

This command generates a virtual environment in the specified folder (in our example, `env`). This folder is an isolated Python environment that separates the dependencies of our project from the system-wide Python installation.

Activate the virtual environment using the following commands:

On Linux or macOS:

```
source env/bin/activate
```

On Windows:

```
env\Scripts\activate
```

Once activated, your command line will indicate the active virtual environment:

On Linux or macOS:

```
(env) yourusername@yourmachine$
```

On Windows:

```
(env) C:\users\YourUsername>
```

### 2. Directory Structure

At this point, your directory structure should look like this:

```
└── env
```

### 3. Installing FastAPI

Now, let us install FastAPI within the virtual environment. We shall install FastAPI using `pip` with the following command.

```
(env) pip install "fastapi[standard]"
```

### 4. Freeze Dependencies

Freeze the installed dependencies into a `requirements.txt` file to track the exact versions of our dependencies so that we can easily reproduce them in the future.

```
(env) pip freeze > requirements.txt
```

### 5. Confirm the installation

Let us confirm our FastAPI installation by running the following command.

```
(env) fastapi --version
FastAPI CLI version: 0.0.2
```

This command will show us the version of the FastAPI CLI—the FastAPI command-line interface. The `fastapi` command shall help us run and manage our app as we shall see in the coming chapters.

If the version has been displayed, then we are sure that FastAPI has been installed in our virtual environment.

## Conclusion

By following these steps, you have successfully set up a virtual environment, and installed FastAPI, frozen the dependencies to reproduce the project in the future and you have verified your installation using the `fastapi` CLI command. This structured approach ensures a clean and manageable development environment for our FastAPI project. Next, we shall create a simple web server and create our first API routes.