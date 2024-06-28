import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
import copy
from scipy.optimize import curve_fit
from scipy.interpolate import griddata
from matplotlib.colors import to_rgba

def __get_bar_data(input_list, bin_tuple_list):
    # bin_tuple_list is a list of tuples, each tuple contains the start and end of a bin
    res = []
    for i in range(len(bin_tuple_list)):
        if i == 0:
            end = bin_tuple_list[i]
            start = -999
        elif i == len(bin_tuple_list) - 1:
            start = bin_tuple_list[i]
            end = 999999
        else:
            start, end = bin_tuple_list[i][0], bin_tuple_list[i][1]
        count = 0
        for j in range(len(input_list)):
            if start <= input_list[j] < end:
                count += 1
        res.append(count)
    return res

def __find_bin_ind(val, bin_ticks, min_val = 0, max_val = 999999):
    if min_val <= val < bin_ticks[0]:
        return 0
    elif val >= bin_ticks[-1]:
        return len(bin_ticks)
    else:
        for i in range(len(bin_ticks) - 1):
            temp_tick = bin_ticks[i]
            if temp_tick <= val < bin_ticks[i + 1]:
                return i + 1
    

def __analyze_cross_relationship(data, key1, key2, key1_ticks = None, key2_ticks = None, x_scale = 1, y_scale = 1):
    """
    Analyzes the cross-relationship between two variables in a list of dictionaries.

    :param data: List of dictionaries containing the data.
    :param key1: The first key in the dictionaries to analyze.
    :param key2: The second key in the dictionaries to analyze.
    :return: A dictionary with keys as tuple pairs of values from key1 and key2, and values as their frequency.
    """
    pair_frequency = {}
    
    for entry in data:
        # Extract the values associated with key1 and key2
        value1 = entry.get(key1) / x_scale
        value2 = entry.get(key2) / y_scale
        
        # Skip entries where either key is missing
        if value1 is None or value2 is None:
            continue
        
        # Create a tuple from the two values
        if key1_ticks is None or key2_ticks is None:
            key_pair = (value1, value2)
        else:
            key_pair = (__find_bin_ind(value1, key1_ticks), __find_bin_ind(value2, key2_ticks))
        if key_pair[0] is None:
            print(value1)
        # Increment the count for this key pair in the dictionary
        if key_pair in pair_frequency:
            pair_frequency[key_pair] += 1
        else:
            pair_frequency[key_pair] = 1

    return pair_frequency

def __generate_ticklabels(tick_bins, is_close_1, is_close_2):
        res = []
        if not is_close_1:
            res.append(f'<{tick_bins[0]}')
        for i in range(len(tick_bins) - 1):
            res.append(f'{tick_bins[i]}-{tick_bins[i + 1]}')
        if not is_close_2:
            res.append(f'>{tick_bins[-1]}')
        return res

def plot_bar_plots(list_of_lists, tuple_range_list, titles = '', ylabels='', bar_color='blue', bar_edgecolor='black', fig_size=(10, 6), tick_fontname='Arial',
                    tick_fontsize=12, title_fontsize=14, label_fontsize=14, line_color='red', show_all_xticklabels=True, bar_width = 1,
                    line_style='--', line_width=2, is_legend=False, unit='m', is_fixed_y_range=True, y_range=[0, 20], is_mean_value = False,
                    is_scaled=False, scale_factor=10, save_path='', is_show=False, is_save=True, transparent_bg=True, horizontal = True, 
                    convert_minute = True, hspace=0.05):
    '''
    This function is used to plot multiple bar plots in one figure. The input data should be a list of lists, where each list contains the data for one bar plot.
    
    Parameters:
    list_of_lists: list of lists, the input data for the bar plots
    tuple_range_list: list of tuples, the range of each bar
    titles: str or list of str, the title of each bar plot, if it is empty, no title will be shown
    ylabels: str or list of str, the y label of each bar plot, if it is empty, no y label will be shown
    bar_color: str, the color of the bars
    bar_edgecolor: str, the edge color of the bars
    fig_size: tuple, the size of the figure
    tick_fontname: str, the font name of the ticks
    tick_fontsize: int, the font size of the ticks
    title_fontsize: int, the font size of the titles
    label_fontsize: int, the font size of the labels
    line_color: str, the color of the mean line
    show_all_xticklabels: bool, whether to show all x tick labels
    bar_width: float, the width of the bars
    line_style: str, the style of the mean line
    line_width: float, the width of the mean line
    is_legend: bool, whether to show the legend
    unit: str, the unit of the data
    is_fixed_y_range: bool, whether to fix the y range
    y_range: list, the y range
    is_mean_value: bool, whether to show the mean value
    is_scaled: bool, whether to scale the data
    scale_factor: float, the scale factor
    save_path: str, the path to save the figure
    is_show: bool, whether to show the figure
    is_save: bool, whether to save the figure
    transparent_bg: bool, whether to set the background to be transparent
    horizontal: bool, whether to plot the bar horizontally
    convert_minute: bool, whether to convert the x tick labels to minutes
    hspace: float, the space between subplots
    
    Returns:
    None
    
    If you want to customize the plot, you can modify the code in this function.
    
    '''
    
    n = len(list_of_lists)
    w, h = fig_size
    
    if is_fixed_y_range and y_range is None:
        max_bar_value = 0
        for data in list_of_lists:
            if is_scaled:
                data = np.array(data) / scale_factor
            bars = __get_bar_data(data, tuple_range_list)
            max_bar_value = max(max_bar_value, bars.max())
        y_range = [0, max_bar_value * 1.05]
    
    fig, axs = plt.subplots(n, 1, figsize=(w, h * n))

    for i, data in enumerate(list_of_lists):
        if is_scaled:
            data = np.array(data) / scale_factor
        
        bar_positions = np.arange(len(tuple_range_list))
        bars = __get_bar_data(data, tuple_range_list)  # This function needs to be defined to get bar data
        bars = np.array(bars) / np.sum(bars) * 100
        if horizontal:
            axs[i].barh(bar_positions, bars, color=bar_color, edgecolor=bar_edgecolor)
        else:
            axs[i].bar(bar_positions, bars, color=bar_color, edgecolor=bar_edgecolor, width=bar_width)
        
        # Calculate and plot the mean line
        if is_mean_value:
            mean_value = np.mean(data)
            axs[i].axvline(mean_value, color=line_color, linestyle=line_style, linewidth=line_width, label=f'Mean: {mean_value:.2f} {unit}')
        
        temp_title = titles if titles == None or isinstance(titles, str) else titles[i]
        if temp_title:
            axs[i].set_title(temp_title, fontsize=title_fontsize, fontname=tick_fontname)
        
        x_tick_labels = []
        convert_factor = 1 if not convert_minute else 60
        for j in range(len(tuple_range_list)):
            if j == len(tuple_range_list) - 1:
                if tuple_range_list[j]/60 >= 1:
                    x_tick_labels.append(f'>{round(tuple_range_list[j]/convert_factor)}')
                else:
                    x_tick_labels.append(f'>{tuple_range_list[j]/convert_factor}')
            elif j == 0:
                if tuple_range_list[j]/60 >= 1:
                    x_tick_labels.append(f'<{round(tuple_range_list[j]/convert_factor)}')
                else:
                    x_tick_labels.append(f'<{tuple_range_list[j]/convert_factor}')
                
            else:
                if tuple_range_list[j][0]/60 >= 1:
                    x_tick_labels.append(f'{round(tuple_range_list[j][0]/convert_factor)}-{round(tuple_range_list[j][1]/convert_factor)}')
                elif tuple_range_list[j][1]/60 >= 1:
                    x_tick_labels.append(f'{tuple_range_list[j][0]/convert_factor}-{round(tuple_range_list[j][1]/convert_factor)}')
                else:
                    x_tick_labels.append(f'{tuple_range_list[j][0]/convert_factor}-{tuple_range_list[j][1]/convert_factor}')
        
        if horizontal:
            axs[i].set_yticks(bar_positions)
            axs[i].set_yticklabels(x_tick_labels,fontsize=tick_fontsize, fontname=tick_fontname)
            # Also needs to make the tick label orientation align with y
            axs[i].tick_params(axis='y', rotation=45)
        else:
            if i == len(list_of_lists) - 1:
                # last x label for each bar should be the range of tuple, also consider that the last tuple should be >, the first should be >
                axs[i].set_xticks(bar_positions)
                axs[i].set_xticklabels(x_tick_labels, fontsize=tick_fontsize, fontname=tick_fontname)
        if i < len(list_of_lists) - 1:
            axs[i].set_xticks([])
        
        if isinstance(ylabels, list) and ylabels[i]:
            axs[i].set_ylabel(ylabels[i], fontsize=label_fontsize, fontname=tick_fontname)
        
        if is_legend:
            axs[i].legend(loc="upper left")
        
        axs[i].grid(False)
        axs[i].tick_params(axis='both', which='major', labelsize=tick_fontsize)
        
        if not show_all_xticklabels and i != n - 1:
            axs[i].set_xticklabels([])
        if is_fixed_y_range:
            axs[i].set_ylim(y_range) if not horizontal else axs[i].set_xlim(y_range)
        if transparent_bg:
            axs[i].patch.set_alpha(0)

    plt.tight_layout()
    plt.subplots_adjust(hspace=hspace)
    if is_show:
        plt.show()
    if is_save:
        if save_path:
            fig.savefig(save_path, dpi=600, transparent=transparent_bg)
        else:
            print("Please provide a valid path to save the figure.")

def draw_cat_bar_curveplots(main_result, other_data_list, bar_colors=None, bar_thickness=0.8, bar_edge_color='black', line_color='black', 
                       y_range=None, figsize=(10, 6), line_thickness=1, tick_fontsize=10, tick_fontname='sans-serif', x_tick_interval=1, is_show=False, 
                       is_save=True, save_path=''):
    '''
    This function is used to draw bar plots with multiple curve plots with a line plot for each dataset.
    
    Parameters:
    main_result: dict, the main result for the stacked bar plot
    other_data_list: list of dict, the other datasets for the line plots
    bar_colors: list, the colors for the bars
    bar_thickness: float, the thickness of the bars
    bar_edge_color: str, the edge color of the bars
    line_color: str, the color of the line plots
    y_range: list, the y range for each subplot
    figsize: tuple, the size of the figure
    line_thickness: float or list, the thickness of the line plots
    tick_fontsize: int, the font size of the ticks
    tick_fontname: str, the font name of the ticks
    x_tick_interval: int, the interval of the x ticks
    is_show: bool, whether to show the figure
    is_save: bool, whether to save the figure
    save_path: str, the path to save the figure
    
    Returns:
    None
    
    If you want to customize the plot, you can modify the code in this function.
    
    
    '''
    def prepare_data(result):
        dates = list(result.keys())
        values = list(result.values())
        return pd.DataFrame(values, index=pd.to_datetime(dates))
    
    def is_number(variable):
        return isinstance(variable, (int, float))

    main_df = prepare_data(main_result)
    all_series = [prepare_data(data) for data in other_data_list]

    fig, axes = plt.subplots(len(all_series) + 1, 1, figsize=figsize, sharex=True)

    # If bar_colors are not provided, use a default color list
    if bar_colors is None:
        bar_colors = ['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c', '#984ea3']

    # Plot the main result as a stacked bar plot
    bottom_series = None
    for i, col in enumerate(main_df.columns):
        color = bar_colors[i % len(bar_colors)]
        axes[0].bar(main_df.index, main_df[col], bottom=bottom_series, color=color, edgecolor=bar_edge_color, width=bar_thickness, label=col)
        if bottom_series is None:
            bottom_series = main_df[col]
        else:
            bottom_series += main_df[col]

    axes[0].tick_params(axis='x', labelsize=tick_fontsize)
    axes[0].tick_params(axis='y', labelsize=tick_fontsize)
    for tick in axes[0].get_xticklabels():
        tick.set_fontname(tick_fontname)
    for tick in axes[0].get_yticklabels():
        tick.set_fontname(tick_fontname)
    if y_range:
        axes[0].set_ylim(y_range[0])
    axes[0].legend()

    # Plot each additional dataset as a line plot
    for idx, series in enumerate(all_series, start=1):
        axes[idx].plot(series.index, series.values, color=line_color)
        axes[idx].tick_params(axis='x', labelsize=tick_fontsize)
        axes[idx].tick_params(axis='y', labelsize=tick_fontsize)
        for tick in axes[idx].get_xticklabels():
            tick.set_fontname(tick_fontname)
        for tick in axes[idx].get_yticklabels():
            tick.set_fontname(tick_fontname)
        if y_range:
            axes[idx].set_ylim(y_range[idx])
        if line_thickness is not None:
            if is_number(line_thickness):
                axes[idx].plot(series.index, series.values, color=line_color, linewidth=line_thickness)
            else:
                axes[idx].plot(series.index, series.values, color=line_color, linewidth=line_thickness[idx - 1])

    # Set date format on x-axis and set tick interval for all subplots
    axes[-1].xaxis.set_major_locator(mdates.DayLocator(interval=x_tick_interval))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    fig.autofmt_xdate()  # Auto format x-axis dates for better appearance

    fig.tight_layout()
    if is_show:
        plt.show()
    if is_save:
        if save_path:
            fig.savefig(save_path, dpi=600)
        else:
            print("Please provide a valid path to save the figure.")
            
def plot_histograms(list_of_lists, titles, xlabels='', ylabels='', bins=10, color='blue', edgecolor='black', fig_size=(10, 6), tick_fontname='Arial',
                    tick_fontsize=12, title_fontsize=14, label_fontsize=14, value_range=None, line_color='red', show_all_xticklabels=True,
                    line_style='--', line_width=2, is_legend=False, unit='m', is_log=False, is_log_x=False, is_fixed_y_range=False, 
                    y_range=None, is_mean_value = True,
                    is_scaled=False, scale_factor=10, save_path='', is_show=False, is_save=True, transparent_bg=True, hspace=0.1):
    
    '''
    This function is used to plot multiple histograms in one figure. The input data should be a list of lists, where each list contains the data for one histogram.
    
    Parameters:
    list_of_lists: list of lists, the input data for the histograms
    titles: list of str, the title of each histogram
    xlabels: str or list of str, the x label of each histogram, if it is empty, no x label will be shown
    ylabels: str or list of str, the y label of each histogram, if it is empty, no y label will be shown
    bins: int, the number of bins
    color: str, the color of the bars
    edgecolor: str, the edge color of the bars
    fig_size: tuple, the size of the figure
    tick_fontname: str, the font name of the ticks
    tick_fontsize: int, the font size of the ticks
    title_fontsize: int, the font size of the titles
    label_fontsize: int, the font size of the labels
    value_range: list, the range of the values
    line_color: str, the color of the mean line
    show_all_xticklabels: bool, whether to show all x tick labels
    line_style: str, the style of the mean line
    line_width: float, the width of the mean line
    is_legend: bool, whether to show the legend
    unit: str, the unit of the data
    is_log: bool, whether to plot the histogram in log scale
    is_log_x: bool, whether to plot the histogram in log scale for x axis
    is_fixed_y_range: bool, whether to fix the y range
    y_range: list, the y range
    is_mean_value: bool, whether to show the mean value
    is_scaled: bool, whether to scale the data
    scale_factor: float, the scale factor
    save_path: str, the path to save the figure
    is_show: bool, whether to show the figure
    is_save: bool, whether to save the figure
    transparent_bg: bool, whether to set the background to be transparent
    hspace: float, the space between subplots
    
    Returns:
    None
    
    If you want to customize the plot, you can modify the code in this function.
    
    '''
    
    n = len(list_of_lists)
    w, h = fig_size
    
    if is_fixed_y_range and y_range is None:
        max_frequency = 0
        for data in list_of_lists:
            if is_scaled:
                data = np.array(data) / scale_factor
            if is_log_x:
                min_data, max_data = min(data), max(data)
                bins = np.logspace(np.log10(min_data), np.log10(max_data), bins)
            hist, _ = np.histogram(data, bins=bins, range=value_range)
            max_frequency = max(max_frequency, hist.max())
        y_range = [0, max_frequency * 1.05]
    
    fig, axs = plt.subplots(n, 1, figsize=(w, h * n))

    for i, data in enumerate(list_of_lists):
        if is_scaled:
            data = np.array(data) / scale_factor
        
        if is_log_x:
            min_data, max_data = min(data), max(data)
            bins = np.logspace(np.log10(min_data), np.log10(max_data), bins)
            axs[i].hist(data, bins=bins, color=color, edgecolor=edgecolor, weights=np.ones_like(data) / len(data) * 100)
            axs[i].set_xscale('log')
        else:
            axs[i].hist(data, bins=bins, color=color, edgecolor=edgecolor, weights=np.ones_like(data) / len(data) * 100, range=value_range, log=is_log)
        
        # Calculate and plot the mean line
        if is_mean_value:
            mean_value = np.mean(data)
            axs[i].axvline(mean_value, color=line_color, linestyle=line_style, linewidth=line_width, label=f'Mean: {mean_value:.2f} {unit}')
        
        if titles[i]:
            axs[i].set_title(titles[i], fontsize=title_fontsize, fontname=tick_fontname)
        
        if xlabels[i]:
            axs[i].set_xlabel(xlabels[i], fontsize=label_fontsize, fontname=tick_fontname)
        else:
            axs[i].set_xticks([])
        
        if ylabels[i]:
            axs[i].set_ylabel(ylabels[i], fontsize=label_fontsize, fontname=tick_fontname)
        
        if is_legend:
            axs[i].legend(loc="upper left")
        
        axs[i].grid(False)
        axs[i].tick_params(axis='both', which='major', labelsize=tick_fontsize)
        
        if not show_all_xticklabels and i != n - 1:
            axs[i].set_xticklabels([])
        if is_fixed_y_range:
            axs[i].set_ylim(y_range)
        if transparent_bg:
            axs[i].patch.set_alpha(0)

    plt.tight_layout()
    plt.subplots_adjust(hspace=hspace)
    if is_show:
        plt.show()
    if is_save:
        if save_path:
            fig.savefig(save_path, dpi=600, transparent=transparent_bg)
        else:
            print("Please provide a valid path to save the figure.")
            
def plot_polylines(df, x, ys, line_styles=None, line_widths=None, line_colors=None, legends=None, show_legend=True,
                   marker_colors=None, figsize=(10, 6), x_tick_interval=1, markers=None, y_label = None,
                   show_grid=True, font_name='Arial', font_size=12, save_path=None, dpi=600, y_range = None):
    """
    Plots multiple lines from a DataFrame using column indices for x and ys with customizable font settings
    and an option to save the figure.

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    x (int): Index of the column to use as x-axis.
    ys (list of int): List of indices of columns to plot on the y-axis.
    line_styles (dict): Dictionary mapping column indices to line styles.
    line_widths (dict): Dictionary mapping column indices to line widths.
    line_colors (dict): Dictionary mapping column indices to line colors.
    legends (list): Optional list of legend labels.
    marker_colors (dict): Dictionary mapping column indices to marker colors.
    figsize (tuple): Figure size.
    x_tick_interval (int): Interval between x-ticks.
    markers (dict): Dictionary mapping column indices to markers.
    show_grid (bool): Whether to show grid.
    font_name (str): Font name for all text elements.
    font_size (int): Font size for all text elements.
    save_path (str): Path to save the figure. If None, the figure is not saved.
    dpi (int): The resolution in dots per inch of the saved figure.
    
    Returns:
    None
    
    """
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Set global font properties
    plt.rcParams.update({'font.size': font_size, 'font.family': font_name})

    for y in ys:
        plt.plot(df.iloc[:, x], df.iloc[:, y],
                 linestyle=line_styles.get(y, '-'),  # Default to solid line
                 linewidth=line_widths.get(y, 2),    # Default line width
                 color=line_colors.get(y, 'blue'),   # Default line color
                 marker=markers.get(y, ''),          # Default no markers
                 markerfacecolor=marker_colors.get(y, 'blue'))  # Default marker color

    # Set x-ticks interval
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xticks(rotation=0)
    plt.xlabel(df.columns[x])
    y_label = "Percent (%)" if y_label is None else y_label
    plt.ylabel(y_label)
    plt.title("")
    if show_grid:
        plt.grid(True)

    # Legend using column names or provided custom legends
    legend_labels = [df.columns[y] for y in ys] if not legends else legends
    if show_legend:
        plt.legend(legend_labels)
    
    if y_range:
        plt.ylim(y_range)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=dpi)
        print(f"Figure saved to {save_path} at {dpi} dpi.")
    plt.show()
    
def plot_time_histogram(histogram, color='blue', edgecolor='black', fig_size=(10, 6),
                        tick_fontname='Arial', tick_fontsize=12, title_fontsize=14, 
                        label_fontsize=14, y_range=None, line_color='red', 
                        show_all_xticklabels=True, x_ticklabel_interval=30, 
                        x_ticklabel_format='HH:MM', is_legend=False, save_path='', 
                        is_show=False, is_save=True, transparent_bg=True):
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=fig_size)
    
    # Prepare data
    dates = list(histogram.keys())
    values = list(histogram.values())
    
    # Plotting the bar chart
    ax.bar(dates, values, color=color, edgecolor=edgecolor)
    
    # Set y-axis limits if specified
    if y_range:
        ax.set_ylim(y_range)
    
    # Set x-ticks format
    if x_ticklabel_format.lower() == 'hh:mm':
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    elif x_ticklabel_format.lower() == 'yyyy-mm-dd':
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    # Set the interval for x-tick labels
    if show_all_xticklabels:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=x_ticklabel_interval))
    else:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    
    # Customize tick labels
    ax.tick_params(axis='both', labelsize=tick_fontsize, labelcolor='black')
    plt.xticks(fontname=tick_fontname)
    plt.yticks(fontname=tick_fontname)
    
    # Set title and labels
    ax.set_title('Histogram of Time Ranges', fontsize=title_fontsize)
    ax.set_xlabel('Date', fontsize=label_fontsize)
    ax.set_ylabel('Frequency', fontsize=label_fontsize)
    
    # Legend
    if is_legend:
        ax.legend()
    
    # Save plot
    if is_save:
        if save_path:
            plt.savefig(save_path, transparent=transparent_bg, bbox_inches='tight', dpi=600)
    
    # Show plot
    if is_show:
        plt.show()
    
    # Close plot to free memory
    plt.close()

def plot_2D_heatmap(pair_frequency, x_bin_ticks, y_bin_ticks, fig_size=(10, 8), title='Cross Relationship Heatmap', title_fontsize=16,
                 xlabel='Variable 1', ylabel='Variable 2', label_fontsize=14, tick_fontsize=12, vmin = None, vmax = None,
                 cmap='viridis', cbar_label='Frequency', save_path='', is_show=True, x_ticklabel_left_close = False, x_ticklabel_right_close = False,
                 y_ticklabel_top_close = False, y_ticklabel_bottom_close = False,is_annotate = False, is_percent = False,
                 xtick_rotation=0, ytick_rotation=0, xticklabels=None, yticklabels=None):
    """
    Plots a heatmap of the frequency of tuple pairs.

    :param pair_frequency: Dictionary with keys as tuple pairs of values and values as their frequency.
    :param fig_size: Size of the figure.
    :param title: Title of the heatmap.
    :param title_fontsize: Font size for the title.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param label_fontsize: Font size for labels.
    :param tick_fontsize: Font size for tick labels.
    :param cmap: Color map of the heatmap.
    :param vmin: Minimum value for the color bar.
    :param vmax: Maximum value for the color bar.
    :param is_percent: Whether to show the frequency as a percentage.
    :param cbar_label: Label for the color bar.
    :param save_path: Path to save the figure.
    :param is_show: Whether to display the plot.
    :param x_ticklabel_left_close: Whether to close the left side of x-tick labels.
    :param x_ticklabel_right_close: Whether to close the right side of x-tick labels.
    :param y_ticklabel_top_close: Whether to close the top side of y-tick labels.
    :param y_ticklabel_bottom_close: Whether to close the bottom side of y-tick labels.
    :param is_annotate: Whether to annotate the heatmap with the frequency values.
    :param xtick_rotation: Rotation angle of x-tick labels.
    :param ytick_rotation: Rotation angle of y-tick labels.
    :param xticklabels: Custom labels for the x-axis ticks.
    :param yticklabels: Custom labels for the y-axis ticks.
    """
    index = list(range(0, len(x_bin_ticks) - 1))
    columns = list(range(0, len(y_bin_ticks) - 1))
    
    if not x_ticklabel_left_close:
        columns.append(columns[-1] + 1)
    if not x_ticklabel_right_close:
        columns.append(columns[-1] + 1)
    if not y_ticklabel_top_close:
        index.append(index[-1] + 1)
    if not y_ticklabel_bottom_close:
        index.append(index[-1] + 1)
    # print(index)
    # print(columns)
    # Create a DataFrame from the pair_frequency
    data = np.zeros((len(columns), len(index)))
    for (var1, var2), freq in pair_frequency.items():
        i = index.index(var1)
        j = columns.index(var2)
        data[j, i] = freq
    
    if is_percent:
        data = data / np.sum(data) * 100
        
    df = pd.DataFrame(data, index=columns, columns=index)

    # Plotting
    plt.figure(figsize=fig_size)
    if vmin is None or vmax is None:
        heatmap = sns.heatmap(df, annot=is_annotate, fmt=".0f", cmap=cmap, linewidths=.5, 
                          cbar_kws={'label': cbar_label})
    else:
        heatmap = sns.heatmap(df, annot=is_annotate, fmt=".0f", cmap=cmap, linewidths=.5, vmin=vmin, vmax=vmax,
                          cbar_kws={'label': cbar_label})
    plt.title(title, fontsize=title_fontsize)
    plt.xlabel(xlabel, fontsize=label_fontsize)
    plt.ylabel(ylabel, fontsize=label_fontsize)
    
    
    # Custom or default tick labels
    if xticklabels is None:
        xticklabels = __generate_ticklabels(x_bin_ticks, x_ticklabel_left_close, x_ticklabel_right_close)
        
    plt.xticks(ticks=np.arange(len(index)) + 0.5, labels=xticklabels, rotation=xtick_rotation, fontsize=tick_fontsize)
    if yticklabels is None:
        yticklabels = __generate_ticklabels(y_bin_ticks, y_ticklabel_top_close, y_ticklabel_bottom_close)
        
    plt.yticks(ticks=np.arange(len(columns)) + 0.5, labels=yticklabels, rotation=ytick_rotation, fontsize=tick_fontsize)
    # Save the plot
    if save_path:
        plt.savefig(save_path, bbox_inches='tight',dpi=600)
    
    # Show the plot
    if is_show:
        plt.show()
    plt.close()