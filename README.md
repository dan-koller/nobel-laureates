# Nobel Laureates

A small reference project for creating pie charts, histograms and box charts and visualizing your data with Matplotlib.

## Requirements

-   Python3
-   Packages from `requirements.txt`

## Installation

1. Clone the repository

```bash
https://github.com/dan-koller/nobel-laureates
```

2. Create a virtual environment\*

```bash
python3 -m venv venv
```

3. Install the requirements\*

```bash
pip3 install -r requirements.txt
```

4. Run the script\*

```bash
python3 main.py
```

_\*) You might need to use `python` and `pip` instead of `python3` and `pip3` depending on your system._

## Usage

The script is currently set to plot a box chart for ages of getting the Nobel Prize for each category. However, you can easily change the plot type and the data to plot by changing the corresponding lines in the `main` function.

```python
def main():
    df = load_data()
    df = prepare_data(df)
    df = count_age(df)
    # plot_pie_chart(df)
    # plot_bar(df)
    box_plot(df)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
