# Streamlit Template for Data Visualizations

Welcome to the **Streamlit Template** repository! This template is designed to help you quickly create and deploy interactive data visualization apps using Streamlit.

## Overview

This project provides a simple Streamlit application with multiple sections, main components are :
- **GitHub Repo:** You need a GitHub repo that contains your application.
- **requirements.txt:** Contains all packages (and their version) that you use in your project, e.g. `numpy==2.2.4`
- **app.py:** The main Python file that contains your Streamlit code.

## Features

- **Modular Design:** The app is divided into multiple containers for clarity using `st.container()`
- **Interactive Visualizations:** Easily display various types of visualizations.
- **Quick Deployment:** Perfect as a starting point for more complex projects.

## Getting Started

### Prerequisites

- Python 3.7 or later
- Pip

### Installation

1. **Run locally:**

- Clone the repository (in order to have it on your computer)

   ```bash
   git clone https://github.com/yourusername/streamlit_da.git
   cd streamlit_da

- Use pip to install all pacakges in the requirements.txt

  ```python
  pip install -r requirements.txt

- Run the following command inside the project directory :

  ```bash
  streamlit run app.py

1. **Deploy using Streamlit Cloud:**
  - Log in to Streamlit Community Cloud and link your GitHub repository.
  - [Link text](https://streamlit.io/cloud)
    - Create App -> Connect to GH
    - Main file : is the same python file that contains your Streamlit code : "app.py"
