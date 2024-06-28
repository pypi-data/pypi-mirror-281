import numpy as np
import matplotlib.pyplot as plt
import warnings
from numpy.typing import NDArray
from matplotlib.colors import LinearSegmentedColormap
from typing import List, Optional, Tuple, Union, Sequence
from scipy.stats import gaussian_kde


# Type alias for a 2D numpy array of floats
Matrix = NDArray[np.float64]

# Global variable to track input format for correct warning in is_empty_or_nan().s
# Input format context is needed, due to cropping a shifted matrix.
# Can only be "preview" if draw_heatmap() is called with "preview" as matrix_format.
# All other draw_x() functions always use review format
_input_format = ""


def remove_empty_rows_and_columns(matrix: Matrix) -> Matrix:
    """ Removes empty rows and columns from a matrix. """
    if is_empty_or_nan(matrix):
        return matrix
    matrix = np.array(matrix, dtype=float)
    non_empty_rows = np.any(np.isfinite(matrix), axis=1)
    non_empty_cols = np.any(np.isfinite(matrix), axis=0)
    cleaned_matrix = matrix[non_empty_rows][:, non_empty_cols]

    return cleaned_matrix


def is_empty_or_nan(matrix: Matrix) -> bool:
    """ Checks if the matrix is empty or contains only NaN values. Returns True if either case is true. """
    global _input_format
    if _input_format != "preview":
        _input_format = "review"
    if matrix.size == 0:
        warnings.warn(f"Matrix is empty or contains only nan values in {_input_format} format!", UserWarning)
        return True
    if np.isnan(matrix).all():
        warnings.warn(f"Matrix is empty or contains only nan values in {_input_format} format!", UserWarning)
        return True
    return False


def crop_matrix(matrix: Matrix) -> Matrix:
    """
    Crops the matrix to remove the first and last few columns
    based on the formula: amount of columns removed on each side = rows - 1.
    Only to be called if object format and the passed format are not the same -> matrix is shifted.


    Example Input:
    [nan nan nan 4   5   6   7   8   9
     nan nan 3   4   5   6   7   8   nan
     nan 2   3   4   5   6   7   nan nan
     1   2   3   4   5   6   nan nan nan]

    Output:
                [4   5   6
                 4   5   6
                 4   5   6
                 4   5   6]
    """
    if is_empty_or_nan(matrix):
        return matrix
    matrix = matrix.astype(float)
    rows, cols = matrix.shape
    matrix = remove_empty_rows_and_columns(matrix[:, (rows - 1):-(rows - 1)])
    return matrix


def preview_to_review(matrix: Matrix) -> Matrix:
    """
    Converts a preview matrix to a review matrix.

    A preview matrix is defined as a matrix, where the first row in a column is the actual measured value on each
    timestamp and the rows below are the predictions made at that timestamp for the following timestamps

    A review matrix is defined as a matrix, where the first row in a column is the actual measured value on each
    timestamp and the rows below are the values that were predicted on the timestamps before to occur on that timestamp

    In practice, this function shifts each row to the right based on the formula: shift = index

    Example Input:
    [0   1   2   3   4   5   6   7   8   9
     1   2   3   4   5   6   7   8   9   10
     2   3   4   5   6   7   8   9   10  11
     3   4   5   6   7   8   9   10  11  12]

    Output:
    [0   1   2   3   4   5   6   7   8   9   nan nan nan
     nan 1   2   3   4   5   6   7   8   9   10  nan nan
     nan nan 2   3   4   5   6   7   8   9   10  11  nan
     nan nan nan 3   4   5   6   7   8   9   10  11  12]
    """
    if is_empty_or_nan(matrix):
        return matrix
    if matrix.shape[0] > matrix.shape[1]:
        warnings.warn(f"Matrix has no complete Columns in review format!", UserWarning)
    matrix = matrix.astype(float)
    rows, cols = matrix.shape
    new_matrix = np.array([[np.nan for _ in range(rows + cols - 1)] for _ in range(rows)])

    for i in range(rows):
        shift = i
        for j in range(cols):
            new_matrix[i][j + shift] = matrix[i][j]

    return new_matrix


def review_to_preview(matrix: Matrix) -> Matrix:
    """
    Converts a preview matrix to a review matrix.

    A review matrix is defined as a matrix, where the first row in a column is the actual measured value on each
    timestamp and the rows below are the values that were predicted on the timestamps before to occur on that timestamp

    A preview matrix is defined as a matrix, where the first row in a column is the actual measured value on each
    timestamp and the rows below are the predictions made at that timestamp for the following timestamps

    In practice, this function shifts each row to the right based on the formula: shift = rows - 1 - i

    Example Input:
    [0   1   2   3   4   5   6   7   8   9
     0   1   2   3   4   5   6   7   8   9
     0   1   2   3   4   5   6   7   8   9
     0   1   2   3   4   5   6   7   8   9]

    Output:
    [nan nan nan 0   1   2   3   4   5   6   7   8   9
     nan nan 0   1   2   3   4   5   6   7   8   9   nan
     nan 0   1   2   3   4   5   6   7   8   9   nan nan
     0   1   2   3   4   5   6   7   8   9   nan nan nan]
    """
    if is_empty_or_nan(matrix):
        return matrix
    if matrix.shape[0] > matrix.shape[1]:
        warnings.warn(f"Matrix has no complete Columns in preview format!", UserWarning)
    matrix = matrix.astype(float)
    rows, cols = matrix.shape
    new_matrix = np.array([[np.nan for _ in range(rows + cols - 1)] for _ in range(rows)])

    for i in range(rows):
        shift = rows - 1 - i
        for j in range(cols):
            new_matrix[i][j + shift] = matrix[i][j]

    return new_matrix


def get_deviation_matrix(matrix: Matrix) -> Matrix:
    """
    Calculates the deviation matrix.
    Inputs the original matrix and replaces every entry with its
    deviation from the entry in the first row within the same column.

    Example Input:
    [0  1  2  3  4  5  6  7  8  9
     1  2  3  4  5  6  7  8  9  10
     2  3  4  5  6  7  8  9  10 11
     3  4  5  6  7  8  9  10 11 12]

    Output:
    [0  0  0  0  0  0  0  0  0  0
     1  1  1  1  1  1  1  1  1  1
     2  2  2  2  2  2  2  2  2  2
     3  3  3  3  3  3  3  3  3  3]
    """
    if is_empty_or_nan(matrix):
        return matrix
    rows, cols = matrix.shape
    deviation_matrix = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] is np.nan:
                deviation_matrix[i, j] = np.nan
            else:
                deviation_matrix[i, j] = matrix[i, j] - matrix[0, j]

    return deviation_matrix


def get_gradient_position_zero(matrix: Matrix) -> float:
    """
    Maps the range between the lowest number in the matrix and the highest number in the matrix onto the range
    between 0 and 1 and returns the value corresponding to 0 in that range. Used for coloring the deviation_colormap.

    Example:
    if  15 => 1
    and -4 => 0
    then 0 => ~0.21
    """
    if is_empty_or_nan(matrix):
        return 0.5
    max_value = np.nanmax(matrix)
    min_value = np.nanmin(matrix)
    if max_value != min_value:
        position = 1 - (max_value / (max_value - min_value))
    else:
        position = 0.5
        warnings.warn("Matrix only contains identical numbers!", UserWarning)

    return position


def get_absolute_mean_deviation_list_by_forecast_depth(matrix: Matrix) -> List[float]:
    """
    Calculates the mean deviations (from the corresponding element in the
    first row) of every element of each row of the matrix and returns them as a list.
    Skips nan values.
    """
    if is_empty_or_nan(matrix):
        return []
    deviation_matrix = remove_empty_rows_and_columns(get_deviation_matrix(matrix))
    rows, cols = deviation_matrix.shape
    deviation_sum = 0
    deviation_list = []
    for i in range(rows):
        number_of_nan = 0
        for j in range(cols):
            if i != 0:
                if not np.isnan(deviation_matrix[i, j]):
                    deviation_sum += abs(deviation_matrix[i, j])
                else:
                    number_of_nan += 1
        if cols - number_of_nan > 0:
            deviation_list.append(deviation_sum / (cols - number_of_nan))
        else:
            warnings.warn("Matrix only contains identical numbers", UserWarning)
        deviation_sum = 0

    return deviation_list


def add_empty_strings(input_list: List[str], matrix, object_format: str, input_format: str) -> List[str]:
    """
    Adds a number of empty strings to the beginning or end of a list, depending on which format is the original format.
    If the object format is preview and the input format is review, the empty strings are added to the end.
    If the object format is review and the input format is preview, the empty strings are added to the beginning.
    The number of empty strings is determined by the number of rows in the matrix.

    Args:
        input_list (List[str]): List to which empty strings are added.
        matrix (Matrix): Matrix used to determine the number of empty strings.
        object_format (str): Format of the instance of the object ("preview" or "review").
        input_format (str): Format of the input ("preview" or "review").

    Returns:
        List[str]: List with added empty strings.

    """
    rows, cols = matrix.shape
    empty_strings = [''] * (rows - 1)

    if object_format == "preview" and input_format == "review":
        output_list = input_list + empty_strings
    elif object_format == "review" and input_format == "preview":
        output_list = empty_strings + input_list
    else:
        output_list = input_list

    return output_list


def configure_format_dependent_parameters(
        object_format: str,
        input_format: str,
        cropped: bool,
        review_timestamps: List[str],
        preview_timestamps: List[str],
        review_matrix: Matrix,
        preview_matrix: Matrix,
        deviation: bool
) -> Tuple[Matrix, List[str]]:
    """
    Configures matrix and timestamps based on format scenario.
    Created to avoid redundancy, because almost the same configuration steps are needed for both
    the draw_heatmap() and draw_heatmap_deviation() functions.

    Args:
        object_format (str): Format of the object ("preview" or "review").
        input_format (str): Format of the input ("preview" or "review").
        cropped (bool): Whether the matrix should be cropped.
        review_timestamps (List[str]): List of review timestamps.
        preview_timestamps (List[str]): List of preview timestamps.
        review_matrix (Matrix): Review matrix.
        preview_matrix (Matrix): Preview matrix.
        deviation (bool): Determines whether the function was called for the purpose of configuring a deviation matrix

    Returns:
        Tuple[Matrix, List[str]]: Configured matrix and timestamps.
    """
    if input_format == "review":
        matrix = review_matrix
        timestamps = review_timestamps
    elif input_format == "preview":
        matrix = preview_matrix
        timestamps = preview_timestamps
    else:
        raise ValueError(f"Format {input_format} not valid! Choose either preview or review!")

    if input_format != object_format and cropped:
        matrix = crop_matrix(matrix)
    elif input_format != object_format and not cropped:
        if object_format == "review":
            timestamps = review_timestamps
        elif object_format == "preview":
            timestamps = preview_timestamps
        if not deviation and timestamps != []:
            timestamps = add_empty_strings(timestamps, matrix, object_format, input_format)

    return matrix, timestamps


def set_heatmap_parameters(
        ax: plt.Axes,
        title: str,
        x_axis: str,
        y_axis: str,
        tick_labels: bool,
        timestamps: List[str]
) -> plt.Axes:
    """
    Sets the heatmap parameters for a plot.
    Created to avoid redundancy, because the same colormap parameters need to be set for both
    the draw_heatmap() and draw_heatmap_deviation() functions.

    Args:
        ax (plt.Axes): Matplotlib Axes object.
        title (str): Title of the plot.
        x_axis (str): Label for the x-axis.
        y_axis (str): Label for the y-axis.
        tick_labels (bool): Whether to display tick labels.
        timestamps (List[str]): List of timestamps.

    Returns:
        plt.Axes: Matplotlib Axes object with updated parameters.
    """
    ax.set_title(title)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_aspect('equal', adjustable='box')

    if tick_labels and timestamps != []:
        more_spacing = len(timestamps) > 14
        if more_spacing:
            timestamps = timestamps[::2]
            ax.set_xticks(np.arange(0, len(timestamps) * 2, 2))
        else:
            ax.set_xticks(np.arange(len(timestamps)))
        ax.set_xticklabels([String for String in timestamps], rotation=45)

    return ax


# Class to plot forecast data
class ForecastPlotter:
    """
        Can plot forecast data in various formats.

        Attributes:
            review_matrix (Matrix): Forecast matrix in review format.
            preview_matrix (Matrix): Forecast matrix in preview format.
            review_timestamps (List[str]): List of timestamps corresponding to the review matrix.
            preview_timestamps (List[str]): List of timestamps corresponding to the preview matrix.
            matrix_format (str): The format of the matrix given when instantiating, either "review" or "preview".
            fig (plt.Figure): The matplotlib figure object used for plotting.
            ax (plt.Axes): The matplotlib axes object used for plotting.
            plot_string (str): A string describing the currently drawn plot. Only used in the __str__ method.
        """

    def __init__(self, matrix: Matrix, matrix_format: str = "review", timestamps: List[str] = None) -> None:
        """
        Initializes the ForecastPlotter with a given matrix, format and timestamps. Review chosen as default format,
        because it is expected to be the more commonly used format.

        Args:
            matrix (Matrix): Matrix of forecast data.
            matrix_format (str): The format of the matrix, either "review" or "preview".
            timestamps (List[str], optional): List of timestamps corresponding to the matrix.

        Raises:
            ValueError: If the provided matrix_format is not valid.
        """
        if timestamps is None:
            timestamps = []
        self.review_timestamps = []
        self.preview_timestamps = []

        if matrix_format == "review":
            self.review_matrix = matrix
            self.preview_matrix = review_to_preview(matrix)
            self.review_timestamps = timestamps
        elif matrix_format == "preview":
            self.preview_matrix = matrix
            self.review_matrix = preview_to_review(matrix)
            self.preview_timestamps = timestamps
        else:
            raise ValueError(f"Object format {matrix_format} not valid! Choose either preview or review!")
        self.matrix_format = matrix_format

        self._adjust_timestamps()
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.plot_string = ""
        self.plotted = False

    def __str__(self) -> str:
        """
        Returns:
            str: A string representation of the ForecastPlotter instance.
        """
        matrix_str = f"Matrix:\n{self.review_matrix if self.matrix_format == 'review' else self.preview_matrix}"
        timestamps_str = \
            f"Timestamps:\n{self.review_timestamps if self.matrix_format == 'review' else self.preview_timestamps}"
        format_str = f"Format: {self.matrix_format}"
        plot_str = f"Currently drawn plots: \n{self.plot_string}"

        return f"{matrix_str}\n\n{timestamps_str}\n\n{format_str}\n\n{plot_str}"

    def new_fig_ax(self):
        """
        Creates a new figure and axes object.
        Used to enable further use of the same instance after a plot has been drawn.
        Can also be called by Users to create multiple Plots in one plot() call.
        """
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.plotted = False

    def _adjust_timestamps(self):
        """
        Adjusts the timestamps based on the matrix format.
        """
        if not self.review_timestamps and not self.preview_timestamps:
            pass
        else:
            if self.matrix_format == "review":
                rows, cols = self.review_matrix.shape
                self.preview_timestamps = self.review_timestamps[rows - 1:]
            elif self.matrix_format == "preview":
                rows, cols = self.preview_matrix.shape
                self.review_timestamps = self.preview_timestamps[:cols - rows + 1]

    def add_column(self, column: NDArray[np.float64], timestamp: str = "") -> None:
        """
        Adds a column to the matrix and updates the timestamps accordingly.

        Args:
            column (NDArray[np.float64]): The column to be added.
            timestamp (str, optional): The timestamp corresponding to the new column.
        """
        try:
            if self.matrix_format == "review":
                self.review_matrix = np.column_stack((self.review_matrix, column))
                self.preview_matrix = review_to_preview(self.review_matrix)
                self.review_timestamps.append(timestamp)
            elif self.matrix_format == "preview":
                self.preview_matrix = np.column_stack((self.preview_matrix, column))
                self.review_matrix = preview_to_review(self.preview_matrix)
                self.preview_timestamps.append(timestamp)
        except ValueError:
            raise ValueError("Number of entries in the new column exceeds number of rows in the matrix!")

        self._adjust_timestamps()

    def remove_column(self, columns: int = 1) -> None:
        """
        Removes a specified number of columns from the matrix and updates the timestamps accordingly.

        Args:
            columns (int, optional): The number of columns to remove. Defaults to 1.

        Raises:
            ValueError: If there are no more columns to remove.
        """
        for i in range(columns):

            if self.matrix_format == "review":
                if self.review_matrix.shape[1] <= 1:
                    raise ValueError("Amount of columns to be removed exceeds the amount of columns in the matrix!")
                self.review_matrix = np.delete(self.review_matrix, 0, axis=1)
                self.preview_matrix = review_to_preview(self.review_matrix)
                if self.review_timestamps:
                    del self.review_timestamps[0]

            elif self.matrix_format == "preview":
                if self.preview_matrix.shape[1] <= 1:
                    raise ValueError("Amount of columns to be removed exceeds the amount of columns in the matrix!")
                self.preview_matrix = np.delete(self.preview_matrix, 0, axis=1)
                self.review_matrix = preview_to_review(self.preview_matrix)
                if self.preview_timestamps:
                    del self.preview_timestamps[0]

        self._adjust_timestamps()

    def draw_heatmap(
            self,
            matrix_format: str = "review",
            colors_list: Optional[List[Tuple[int, str]]] = None,
            title: str = "Forecast Data",
            colormap_name: str = "Measured Value",
            x_axis: str = "Timestamps",
            y_axis: str = "Forecast Depth",
            cropped: bool = False,
            missing_color: str = 'white',
            tick_labels: bool = True
    ) -> None:
        """
        Adds a heatmap of the forecast data to this instances ax object.

        Args:
            matrix_format (str, optional): The format to be used, either "review" or "preview". Defaults to "review",
                because it is expected to be the more commonly used format.
            colors_list ([List[Tuple[int, str]]], optional): List of color thresholds and corresponding colors.
                Default value is set in Code.
            title (str, optional): Title of the heatmap. Defaults to "Forecast Data".
            colormap_name (str, optional): Label for the colorbar. Defaults to "Measured Value".
            x_axis (str, optional): Label for the x-axis. Defaults to "Timestamps".
            y_axis (str, optional): Label for the y-axis. Defaults to "Forecast Depth".
            cropped (bool, optional): Whether to crop the matrix for plotting. Defaults to True.
            missing_color (str, optional): Color for missing data. Defaults to 'white'.
            tick_labels (bool, optional): Whether to display tick labels. Defaults to True.

        Raises:
            ValueError: If matrix values are beyond the set color limits. Color limits are determined by colors_list.
        """
        global _input_format
        _input_format = matrix_format

        if self.plotted:
            self.new_fig_ax()

        matrix, timestamps = configure_format_dependent_parameters(
            self.matrix_format,
            matrix_format,
            cropped,
            self.review_timestamps,
            self.preview_timestamps,
            self.review_matrix,
            self.preview_matrix,
            deviation=False
        )

        # Default colors are purple, blue, green, yellow, orange, red
        if colors_list is None:
            colors_list = [(-10, 'purple'), (0, 'blue'), (10, 'green'), (20, 'yellow'), (30, 'orange'), (40, 'red')]

        # Thresholds are the first element of each tuple in colors_list
        thresholds = [item[0] for item in colors_list]

        # Get the minimum and maximum values of the colors_list
        min_value = min(colors_list, key=lambda x: x[0])[0]
        max_value = max(colors_list, key=lambda x: x[0])[0]

        self.ax = set_heatmap_parameters(self.ax, title, x_axis, y_axis, tick_labels, timestamps)
        if max_value >= np.nanmax(matrix, initial=0) and np.nanmin(matrix, initial=0) >= min_value:
            if not is_empty_or_nan(matrix):
                # Normalize the colors_list to the range of the matrix values
                normalized_colors_list = [((key - min_value) / (max_value - min_value), value) for key, value in
                                          colors_list]
                # Create a colormap from the normalized colors_list
                cm = LinearSegmentedColormap.from_list("Custom", normalized_colors_list)

                # Create the colorbar and parameterize it and the colormap
                cbar = self.fig.colorbar(
                    self.ax.imshow(matrix, cmap=cm, vmin=min(thresholds), vmax=max(thresholds),
                                   interpolation='nearest'),
                    ax=self.ax
                )
                cbar.set_label(colormap_name)
                cm.set_bad(color=missing_color)

                self.plot_string += f"Heatmap in {matrix_format} format\n"

        else:
            # If the matrix values are beyond the set color limits, raise an error
            message = f"Matrix values are beyond the set limits: {min_value} and {max_value}:\n"
            if min_value > np.nanmin(matrix):
                message += f"The lowest number below the limit is: {np.nanmin(matrix)}\n"
            elif max_value < np.nanmax(matrix):
                message += f"The highest number above the limit is: {np.nanmax(matrix)}"
            raise ValueError(message)

    def draw_heatmap_deviation(
            self,
            colors: Optional[List[str]] = None,
            title: str = "Deviations from measured Value",
            colormap_name: str = "Deviation",
            x_axis: str = "Day",
            y_axis: str = "Forecast Depth",
            cropped: bool = True,
            missing_color: str = 'white',
            tick_labels: bool = True
    ) -> None:
        """
        Adds a deviation heatmap to this instances ax object. This heatmap is based on the deviation of the forecast
        values from the measured values. The deviation is calculated by subtracting the measured value from the forecast
        value. The measured values are stored in the first row of each matrix and the forecast values in the following
        rows.

        Args:
            colors ([List[int, str]], optional): List of colors to be used. Default set in function.
            title (str, optional): Title of the heatmap. Defaults to "Deviation from measured Value".
            colormap_name (str, optional): Label for the colorbar. Defaults to "Deviation".
            x_axis (str, optional): Label for the x-axis. Defaults to "Timestamps".
            y_axis (str, optional): Label for the y-axis. Defaults to "Forecast Depth".
            cropped (bool, optional): Whether to crop the matrix for plotting. Defaults to True.
            missing_color (str, optional): Color for missing data. Defaults to 'white'.
            tick_labels (bool, optional): Whether to display tick labels. Defaults to True.

        Raises:
            ValueError: If colors has an uneven number of elements.
        """
        if self.plotted:
            self.new_fig_ax()

        # Default colors are blue, white, red
        if colors is None:
            colors = ['blue', 'white', 'red']

        # Check if colors has an uneven number of elements
        if len(colors) % 2 == 0:
            raise ValueError("Number of colors for deviation Matrix must be uneven")

        matrix, timestamps = configure_format_dependent_parameters(
            self.matrix_format,
            "review",
            cropped,
            self.review_timestamps,
            self.preview_timestamps,
            get_deviation_matrix(self.review_matrix),
            get_deviation_matrix(self.preview_matrix),
            True
        )
        min_deviation = np.nanmin(matrix, initial=0)
        max_deviation = np.nanmax(matrix, initial=0)

        num_colors = len(colors)
        middle_index = num_colors // 2  # Integer division, rounded down

        if min_deviation >= 0:
            # All values are non-negative
            colors_differential = [(i / (num_colors - 1), colors[i]) for i in range(num_colors)]
        elif max_deviation <= 0:
            # All values are non-positive
            colors_differential = [(i / (num_colors - 1), colors[i]) for i in range(num_colors)]
        else:
            # Mixed positive and negative values
            zero_gradient_position = get_gradient_position_zero(matrix)
            colors_differential = []

            for i in range(num_colors):
                if i == middle_index:
                    colors_differential.append((zero_gradient_position, colors[i]))
                else:
                    pos = i / (num_colors - 1)
                    colors_differential.append((pos, colors[i]))

        cm = LinearSegmentedColormap.from_list("Custom", colors_differential)
        cbar = self.fig.colorbar(self.ax.imshow(matrix, cmap=cm), ax=self.ax)
        cbar.set_label(colormap_name)
        cm.set_bad(color=missing_color)

        self.ax = set_heatmap_parameters(self.ax, title, x_axis, y_axis, tick_labels, timestamps)

        self.plot_string += "Heatmap Deviation\n"

    def draw_dod(
            self,
            title: str = "Mean absolute deviation by forecast depth",
            x_axis: str = "Forecast depth",
            y_axis: str = "Mean deviation (absolute Value)",
            color: str = "blue"
    ) -> None:
        """
        Adds a line plot depicting the mean absolute deviation for
        each forecast depth level to this instances ax object.

        Args:
            title (str, optional): Title of the plot. Defaults to "Mean absolute deviation by forecast depth".
            x_axis (str, optional): Label for the x-axis. Defaults to "Forecast depth".
            y_axis (str, optional): Label for the y-axis. Defaults to "Mean deviation (absolute Value)".
            color (str, optional): Color of the plot line. Defaults to "blue".

        """
        if self.plotted:
            self.new_fig_ax()

        deviation_list = get_absolute_mean_deviation_list_by_forecast_depth(self.review_matrix)

        self.ax.plot(deviation_list, color=color)
        self.ax.set_title(title)
        self.ax.set_xlabel(x_axis)
        self.ax.set_ylabel(y_axis)
        self.ax.invert_xaxis()

        self.plot_string += "Deviation over Depth\n"

    def draw_histogram(
            self,
            title: str = 'Forecast Deviation density',
            x_axis: str = 'Deviation',
            y_axis: str = 'Density',
            color: str = 'skyblue',
            center_line: bool = True,
            center_line_color: str = 'yellow',
            center_line_style: str = '--',
            pdf: bool = True,
            pdf_color: str = 'red',
            bins: Union[str, int, Sequence] = 'auto'
    ) -> None:
        """
        Adds a histogram of the density values of different deviation ranges to this instances ax object.

        Args:
            title (str, optional): Title of the plot. Defaults to 'Forecast Deviation density'.
            x_axis (str, optional): Label for the x-axis. Defaults to 'Deviation'.
            y_axis (str, optional): Label for the y-axis. Defaults to 'Density'.
            color (str, optional): Color of the histogram bars. Defaults to 'skyblue'.
            center_line (bool, optional): Whether to show a center line at deviation 0. Defaults to True.
            center_line_color (str, optional): Color of the center line. Defaults to 'yellow'.
            center_line_style (str, optional): Style of the center line. Defaults to '--'.
            pdf (bool, optional): Whether to plot the probability density function. Defaults to True.
            pdf_color (str, optional): Color of the PDF plot. Defaults to 'red'.
            bins (Union[str, int, Sequence], optional): Number of bins or bin edges for the histogram.
                Defaults to 'auto'.

        Raises:
            ValueError: If the object format is not valid.
        """
        if self.plotted:
            self.new_fig_ax()

        # Get appropriate matrix
        if self.matrix_format == "review":
            matrix = remove_empty_rows_and_columns(get_deviation_matrix(self.review_matrix))
        elif self.matrix_format == "preview":
            matrix = remove_empty_rows_and_columns(get_deviation_matrix(crop_matrix(self.review_matrix)))
        else:
            raise ValueError(f"Object format \'{self.matrix_format}\' not valid! Choose either preview or review!")

        # Remove first row of matrix
        if matrix.shape[0] > 0:
            matrix = matrix[1:]
        else:
            warnings.warn("Matrix has no forecast rows!", UserWarning)

        # Creates one dimensional array of all values in the matrix to feed hist() function
        flattened_values = matrix.flatten()
        self.ax.hist(flattened_values, bins=bins, color=color, density=True)

        # Creates line at deviation 0 if center_line is True
        if center_line:
            self.ax.axvline(x=0, color=center_line_color, linestyle=center_line_style)

        # Create mask that doesn't contain nan values
        mask = ~np.isnan(flattened_values)

        # Apply mask
        flattened_values = flattened_values[mask]

        if flattened_values.size > 0:

            # Creates probability density function if pdf is True, flattened_values has more than one entry and all
            # entries are not the same
            if pdf and flattened_values.size > 1 and not np.all(flattened_values == flattened_values[0]):
                kde = gaussian_kde(flattened_values, bw_method='scott')
                x = np.linspace(np.min(flattened_values), np.max(flattened_values), 1000)
                p = kde(x)
                self.ax.plot(x, p, color=pdf_color, linewidth=2)
            if np.all(flattened_values == flattened_values[0]):
                warnings.warn("Cannot create probability density function. All values in the matrix are the same!",
                              UserWarning)

        self.ax.set_title(title)
        self.ax.set_xlabel(x_axis)
        self.ax.set_ylabel(y_axis)

        self.plot_string += "Histogram\n"

    @property
    def get_fig(self) -> plt.Figure:
        """
        Returns:
            plt.Axes: Matplotlib figure object.
        """
        return self.fig

    @property
    def get_ax(self) -> plt.Axes:
        """
        Returns:
            plt.Axes: Matplotlib axes object.
        """
        return self.ax

    def plot(self) -> None:
        """ Show the created plot using matplotlib and adjust the object plot_string."""
        plt.tight_layout()
        plt.show()
        self.plotted = True

        newline_indices = [i for i, char in enumerate(self.plot_string) if char == '\n']

        # If there are fewer than two newlines, return the string as is
        if len(newline_indices) >= 1:
            # Get the index of the second to last newline
            second_last_newline_index = newline_indices[-1]

            # Extract and return the part of the string after the second to last newline
            self.plot_string = self.plot_string[second_last_newline_index + 1:]
        global _input_format
        _input_format = ""


if __name__ == "__main__":
    raise RuntimeError("This script is not intended to be run directly. Please import it as a module.")
