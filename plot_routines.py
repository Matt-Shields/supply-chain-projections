import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as txt
import os


def mysave(fig, froot, mode='png'):
    assert mode in ['png', 'eps', 'pdf', 'all']
    fileName, fileExtension = os.path.splitext(froot)
    padding = 0.1
    dpiVal = 200
    legs = []
    for a in fig.get_axes():
        addLeg = a.get_legend()
        if not addLeg is None: legs.append(a.get_legend())
    ext = []
    if mode == 'png' or mode == 'all':
        ext.append('png')
    if mode == 'eps':  # or mode == 'all':
        ext.append('eps')
    if mode == 'pdf' or mode == 'all':
        ext.append('pdf')

    for sfx in ext:
        fig.savefig(fileName + '.' + sfx, format=sfx, pad_inches=padding, bbox_inches='tight',
                    dpi=dpiVal, bbox_extra_artists=legs)


titleSize = 24  # 40 #38
axLabelSize = 20  # 38 #36
tickLabelSize = 18  # 30 #28
legendSize = tickLabelSize + 2
textSize = legendSize - 2
deltaShow = 4
linewidth = 4


def myformat(ax, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax):
        if mode.lower() == 'show':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize + 3 * deltaShow)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize + deltaShow + 6)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize + deltaShow + 6)

            myax.set_title(myax.get_title(), size=titleSize + deltaShow, weight='bold')
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.tick_params(labelsize=tickLabelSize + deltaShow)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(tickLabelSize + deltaShow)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(tickLabelSize + deltaShow)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

        elif mode.lower() == 'save':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize)

            myax.set_title(myax.get_title(), size=titleSize, weight='bold')
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize, weight='bold')
            myax.tick_params(labelsize=tickLabelSize)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(tickLabelSize)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(tickLabelSize)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

    if type(ax) == type([]):
        for i in ax: myformat(i)
    else:
        myformat(ax)


def initFigAxis():
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111)
    return fig, ax

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def stacked_bar_cumulative(x, y_zip,
                           fname=None, fig_in=None, ax_in=None, axR_in=None,  y1max=None, y2max=None,
                           width=None, order=1, single=True, cumulative_line=True,
                           myxlabel='Year', myylabel='Annual installed capacity, MW', myy2label='Cumulative capacity, MW',
                           mycumsumlabel='Cumulative deployment', cumsumline='-', linecol='k'):
    if ax_in:
        fig = fig_in
        axL = ax_in
    else:
        fig, axL = initFigAxis()
    data_num = 0
    for y, c, n in y_zip:
        if data_num == 0:
            try:
                axL.bar(x - order*width/2, y, width=width, color=c, edgecolor='k', label=n)
            except TypeError:
                # Width not defined
                axL.bar(x, y, color=c, edgecolor='k', label=n)
            y_total = np.copy(y)
        else:
            try:
                axL.bar(x - order*width/2, y, width=width, color=c, edgecolor='k', label=n, bottom=y_total)
            except TypeError:
                axL.bar(x, y,  color=c, edgecolor='k', label=n, bottom=y_total)
            y_total += y
        data_num+=1
    if y1max:
        axL.set_ylim([0, y1max])

    if cumulative_line is True:
        if axR_in:
            axR = axR_in
        else:
            axR = axL.twinx()

        axR.plot(x, np.cumsum(y_total), cumsumline, color=linecol, label=mycumsumlabel)

    xticks=x
    xv = [x.min(), x.max() + 1]
    axL.set_xticks(xticks)

    axL.set_xticklabels([str(m) for m in xticks], rotation=90)
    axL.set_xlabel(myxlabel)
    axL.set_ylabel(myylabel)
    axL.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # axL.grid()
    # yv = np.array( axL.get_ylim() )
    axL.set_xlim(xv)
    if cumulative_line is True:
        axR.set_xlim(xv)
        axR.set_ylabel(myy2label)
        axR.set_ylim([0, y2max])
        axR.get_yaxis().set_major_formatter(
            mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if single == True:
        axL.legend(loc='upper left')

    if fname:
        if cumulative_line is True:
            myformat([axL, axR])
            mysave(fig, fname)
            plt.close()
            return axL, axR
        else:
            myformat(axL)
            mysave(fig, fname)
            plt.close()
            return axL



def bar_cumulative_comp(x, y1_zip, y2_zip, fname,
                         y1max=10000, y2max=50001, width=None):
    fig, ax = initFigAxis()
    # Plot first set
    axL1, axR1 = stacked_bar_cumulative(x, y1_zip, y1max=y1max, y2max=y2max, single=False, fig_in=fig, ax_in=ax, width=width,
                           mycumsumlabel='Cumulative deployment (30 GW target)', cumsumline='-', linecol='#0B5E90')
    # Plot second set
    axL2, axR2 = stacked_bar_cumulative(x, y2_zip, y1max=y1max, y2max=y2max, single=False,  order=-1,
                                        fig_in=fig, ax_in=ax, axR_in=axR1, width=width,
                                      mycumsumlabel='Cumulative deployment (conservative)', cumsumline='--', linecol='#3D6321')

    # Combine legends
    linesL2, labelsL2 = axL2.get_legend_handles_labels()
    linesR2, labelsR2 = axR2.get_legend_handles_labels()
    axR2.legend(linesL2+linesR2, labelsL2+labelsR2, loc='upper left')
    axL2.set_xlim(x.min()-width, x.max()+width)
    if fname:
        myformat([axL2, axR2])
        mysave(fig, fname)
        plt.close()
#TODO: stacked bar line for deployment + jobs
def stacked_bar_line(x, y_bar_zip, y_line_zip,
                           fname=None, y1max=None, y2max=None,
                           width=None, order=1, single=True,
                           myxlabel='Year', myylabel='Annual installed capacity, MW', myy2label='Cumulative capacity, MW',
                           mycumsumlabel='Cumulative deployment', cumsumline='-', linecol='k'):

    fig, axL = initFigAxis()
    data_num = 0
    for y, c, n in y_bar_zip:
        if data_num == 0:
            try:
                axL.bar(x - order*width/2, y, width=width, color=c, edgecolor='k', label=n)
            except TypeError:
                # Width not defined
                axL.bar(x, y, color=c, edgecolor='k', label=n)
            y_total = np.copy(y)
        else:
            try:
                axL.bar(x - order*width/2, y, width=width, color=c, edgecolor='k', label=n, bottom=y_total)
            except TypeError:
                axL.bar(x, y,  color=c, edgecolor='k', label=n, bottom=y_total)
            y_total += y
        data_num+=1
    if y1max:
        axL.set_ylim([0, y1max])

    axR = axL.twinx()
    for y, c, n in y_line_zip:
        axR.plot(x, y, cumsumline, color=c, label=n)

    xticks=x
    xv = [x.min(), x.max() + 1]
    axL.set_xticks(xticks)
    axL.set_xticklabels([str(m) for m in xticks], rotation=90)
    axL.set_xlabel(myxlabel)
    axL.set_ylabel(myylabel)

    # axL.grid()
    # yv = np.array( axL.get_ylim() )
    axL.set_xlim(xv)
    axR.set_xlim(xv)
    axR.set_ylabel(myy2label)
    axR.set_ylim([0, y2max])

    linesL, labelsL = axL.get_legend_handles_labels()
    linesR, labelsR = axR.get_legend_handles_labels()
    axR.legend(linesL+linesR, labelsL+labelsR, loc='upper left')


    if fname:
        myformat([axL, axR])
        mysave(fig, fname)
        plt.close()

    return axL, axR

def line_plots(x, y_zip, fname, myylabel, myxlabel='Year'):
    fig, ax = initFigAxis()

    for y, c, n in y_zip:
        ax.plot(x, y, color=c, label=n)

    ax.legend(loc='upper left')

    xticks=x
    xv = [x.min(), x.max() + 1]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(m) for m in xticks], rotation=90)
    ax.set_xlabel(myxlabel)
    ax.set_ylabel(myylabel)

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax

def area_plots(x, y_zip, fname, myylabel, myxlabel='Year'):
    fig, ax = initFigAxis()

    yBase = np.zeros(len(x))
    leglist = []
    hand = []
    ht = []
    for y, c, n in y_zip:
        yPlot = yBase + y
        ax.plot(x,yPlot, 'k')
        ax.fill_between(x, list(yBase), list(yPlot), color=c, alpha=0.5, label=n)
    # #     # leglist.append(Rectangle((0, 0), 1, 1, color=colors[i]))  # creates rectangle patch for legend use.
    # #     # if legpos == 'text':
    # #     #     ht.append(ax.text(2041, (0.1 * (yPlot - yBase) + yBase)[i2040], labels[i], color=colors[-1]))
        yBase = yPlot
    ax.legend(loc='upper left')

    xticks=x
    xv = [x.min(), x.max() + 1]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(m) for m in xticks], rotation=90)
    ax.set_xlabel(myxlabel)
    ax.set_ylabel(myylabel)
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax

def line_plots2(x, y_zip, fname, ymax=None, title=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year',
                n_moving_average=3):
    fig, ax = initFigAxis()

    y_fill = []
    for y, c, l, n, lbl in y_zip:
        # ax.scatter(x, y, color=c, linestyle=l, marker=m, label=n)
        # if n_moving_average:
        x_avg = x[n_moving_average-1:]
        y_avg = moving_average(y, n_moving_average)
        _leg = str(n_moving_average)+' year moving average for ' + lbl + ' domestic content'
        ax.plot(x_avg, y_avg, color=c, linestyle=l, label=_leg)
        y_fill.append(y_avg)

    ax.fill_between(x_avg, y_fill[0], y_fill[1], alpha=0.5, linewidth=0)

    if ymax:
        ax.set_ylim([0, ymax])

    ax.legend(loc='upper left')

    xticks=x
    xv = [x.min(), x.max() + 1]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(m) for m in xticks], rotation=90)
    ax.set_xlabel(myxlabel)
    ax.set_ylabel(myylabel)
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # ax.set_title(title)

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax

def line_plots4(x, y_zip, fname, ymax=None, myylabel='Jobs, Full-Time Equivalents', myxlabel='Year',
                n_moving_average=3):
    fig1, ax1 = initFigAxis()
    fig2, ax2 = initFigAxis()

    y_fill1 = []
    y_fill2 = []
    x_avg = x[n_moving_average - 1:]

    for y, c, l, n, lbl in y_zip:
        if 'Moderate' in n:
            y_avg1 = moving_average(y, n_moving_average)
            _leg = str(n_moving_average) + ' year moving average for ' + lbl + ' domestic content'
            ax1.plot(x_avg, y_avg1, color=c, linestyle=l, label=_leg)
            y_fill1.append(y_avg1)
            fname1 = fname+'Moderate'
        elif 'Significant' in n:
            y_avg2= moving_average(y, n_moving_average)
            _leg = str(n_moving_average) + ' year moving average for ' + lbl + ' domestic content'
            ax2.plot(x_avg, y_avg2, color=c, linestyle=l, label=_leg)
            y_fill2.append(y_avg2)
            fname2 = fname+'Significant'

    ax1.fill_between(x_avg, y_fill1[0], y_fill1[1], color='tab:gray', alpha=0.5, linewidth=0)
    ax2.fill_between(x_avg, y_fill2[0], y_fill2[1], color='tab:gray', alpha=0.5, linewidth=0)

    for a in [ax1, ax2]:
        if ymax:
            a.set_ylim([0, ymax])

        a.legend(loc='upper left')

        xticks=x
        xv = [x.min(), x.max() + 1]
        a.set_xticks(xticks)
        a.set_xticklabels([str(m) for m in xticks], rotation=90)
        a.set_xlabel(myxlabel)
        a.set_ylabel(myylabel)
        a.get_yaxis().set_major_formatter(
            mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        if fname:
            myformat(a)
            if a==ax1:
                mysave(fig1, fname1)
            elif a==ax2:
                mysave(fig2, fname2)
            plt.close()

    return ax1, ax2

def line_plotsGDP(x, y_zip, fname, ymax=None, title=None, myylabel='$ Million', myxlabel='Year',
                  n_moving_average=3):
    fig, ax = initFigAxis()

    y_fill=[]
    for y, c, l, n, lbl in y_zip:
        x_avg = x[n_moving_average - 1:]
        y_avg = moving_average(y, n_moving_average)
        _leg = str(n_moving_average) + ' year moving average for ' + lbl + ' domestic content'
        ax.plot(x_avg, y_avg, color=c, linestyle=l, label=_leg)
        y_fill.append(y_avg)

    ax.fill_between(x_avg, y_fill[0], y_fill[1], alpha=0.5, linewidth=0)

    if ymax:
        ax.set_ylim([0, ymax])

    ax.legend(loc='upper left')

    xticks=x
    xv = [x.min(), x.max() + 1]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(m) for m in xticks], rotation=90)
    ax.set_xlabel(myxlabel)
    ax.set_ylabel(myylabel)
    # ax.set_title(title)
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax

def area_plotsv2(x, y_zip, fname, ymax = None, title='100% Domestic Content, Baseline Scenario', myylabel='Jobs, Full Time Equivalents', myxlabel='Year'):
    fig, ax = initFigAxis()

    yBase = np.zeros(len(x))
    leglist = []
    hand = []
    ht = []
    for y, c, n in y_zip:
        yPlot = yBase + y
        ax.plot(x,yPlot, 'k')
        ax.fill_between(x, list(yBase), list(yPlot), color=c, alpha=0.5, label=n)
    # #     # leglist.append(Rectangle((0, 0), 1, 1, color=colors[i]))  # creates rectangle patch for legend use.
    # #     # if legpos == 'text':
    # #     #     ht.append(ax.text(2041, (0.1 * (yPlot - yBase) + yBase)[i2040], labels[i], color=colors[-1]))
        yBase = yPlot
    ax.legend(loc='upper left')

    xticks=x
    xv = [x.min(), x.max() + 1]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(m) for m in xticks], rotation=90)
    ax.set_xlabel(myxlabel)
    ax.set_ylabel(myylabel)

    if ymax:
        ax.set_ylim([0, ymax])

    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # ax.set_title(title)
    ax.legend(loc='center left', bbox_to_anchor=(1.04, 0.7),
          fancybox=True, shadow=True, ncol=1)

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax

def pie_plot(y, c, n, fname=None):
    fig, ax = initFigAxis()

    y_pie = y / np.sum(y)
    _dict = {}
    _c_dict={}
    for name, val, col in zip(n, y_pie, c):
        _val = np.round(100*val, 1)
        _leg = (name + ' (' + str(_val) + '%)')
        _dict[_leg] = _val
        _c_dict[col] = _val

    sort_dict = {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1])}
    sort_c_dict = {k: v for k, v in sorted(_c_dict.items(), key=lambda item: item[1])}

    wedges, texts = ax.pie(sort_dict.values(), colors=sort_c_dict.keys())
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.legend(wedges[::-1], list(sort_dict.keys())[::-1],
              loc='center left',
              bbox_to_anchor=(0.9, 0, 0.5, 1))

    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles=handles[::-1],
    #            labels=labels[::-1])

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ax
