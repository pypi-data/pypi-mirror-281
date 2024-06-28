import pandas as pd


def get_matrix_from_excel(path):
    """ Read an Excel file and return its content as a 2D matrix."""
    # Read the Excel file
    df = pd.read_excel(path, header=None)

    # Convert the DataFrame to a 2D matrix
    matrix = df.values

    return matrix


if __name__ == "__main__":
    raise RuntimeError("This script is not intended to be run directly. Please import it as a module.")
