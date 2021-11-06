import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime
import numpy as np

class Plot():
    @staticmethod
    def _plot(df, x_col, y_col, figsize=None, xlab='Time', ylab='Value', ax=None):
        if ax is None:
            _, ax = plt.subplots(figsize=figsize)
        
        # X
        x = np.arange(len(df))
        x_txt = list(df[x_col])
        
        # Y
        y = list(df[y_col])
        y_txt = ['${:.2f}'.format(yi) for yi in y]
        print(len(x_txt))
        print(len(y_txt))
        print(len(x))
        print(len(y))
        
        # Plot
        ax.plot(x, y)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_xticks([])

        # Make interactive
        mplcursors.cursor(ax, hover=True).connect('add', lambda sel: Plot._plot_annotate(sel, x_txt, y_txt))
        plt.show(block=False)

    @staticmethod
    def _plot_annotate(sel, x_txt, y_txt):
        label = sel.artist.get_label()
        x = int(round(sel.target.index))
        sel.annotation.set_text(f'{label}\n{x_txt[x]}\n{y_txt[label][x]}')
