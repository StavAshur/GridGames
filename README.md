# Grid and Agent Simulation

This repository contains a Python simulation of a grid with agents that move according to different strategies.

## Prerequisites

Before you start, make sure you have the following installed on your laptop:
- Python 3.x
- pip (Python package installer)

## Step-by-Step Instructions

### 1. Install Python

1. Open your web browser and go to the Python website.
2. Click on the "Downloads" tab.
3. Click on the "Download Python 3.x.x" button (the latest version).
4. Once the download is complete, open the installer and follow the instructions to install Python.

### 2. Install pip

pip is usually installed with Python by default. To check if pip is installed, open the Terminal app (you can find it in Applications > Utilities) and type:

```sh
pip --version

If you see a version number, pip is installed. If not, follow these steps:

1. Download the `get-pip.py` file by clicking here.
2. Open the Terminal app.
3. Navigate to the folder where you downloaded `get-pip.py` (e.g., Downloads folder):

```sh
cd ~/Downloads
```

4. Run the following command to install pip:

```sh
python3 get-pip.py
```

### 3. Clone the Repository

1. Open the Terminal app.
2. Navigate to the folder where you want to save the repository (e.g., Desktop):

```sh
cd ~/Desktop
```

3. Clone the repository using the following command:

```sh
git clone <repository_url>
```

Replace `<repository_url>` with the URL of your repository.

### 4. Install Required Packages

Navigate to the cloned repository folder:

```sh
cd <repository_folder>
```

Replace `<repository_folder>` with the name of the cloned repository folder.

Install the required packages using pip:

```sh
pip install matplotlib networkx
```

### 5. Run the Simulation

1. Make sure you are in the repository folder in the Terminal.
2. Run the simulation using the following command:

```sh
python3 simulation.py
```

The simulation will start, and you will see a grid with two agents moving around. The grid will update every 0.3 seconds.

## Troubleshooting

### Problem: `pip` command not found

If you get an error saying `pip: command not found`, make sure you have installed pip correctly. Follow the steps in the "Install pip" section above.

### Problem: `matplotlib` or `networkx` not installed

If you get an error saying `ModuleNotFoundError: No module named 'matplotlib'` or `No module named 'networkx'`, make sure you have installed the required packages. Run the following command:

```sh
pip install matplotlib networkx
```

### Problem: `python3` command not found

If you get an error saying `python3: command not found`, make sure you have installed Python 3 correctly. Follow the steps in the "Install Python" section above.

## Conclusion

You should now have the simulation running on your Apple laptop. If you encounter any issues or have any questions, feel free to ask for help. Enjoy the simulation!
```
