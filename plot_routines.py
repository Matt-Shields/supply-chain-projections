import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
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
                i.set_linewidth(4)
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
                i.set_linewidth(4)
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


def stacked_bar_cumulative(x, y_zip,
                           fname=None, fig_in=None, ax_in=None, xmax=None, ymax=None, width=None, order=1,
                           myxlabel='Year', myylabel='Installed capacity, MW', myy2label='Cumulative capacity, MW',
                           linecol='k'):
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
            y_total = y
        else:
            try:
                axL.bar(x - order*width/2, y, width=width, color=c, edgecolor='k', label=n, bottom=y_total)
            except TypeError:
                axL.bar(x, y,  color=c, edgecolor='k', label=n, bottom=y_total)
            y_total += y
        data_num+=1

    axR = axL.twinx()
    axR.plot(x, np.cumsum(y_total), '-', color=linecol)
    axR.set_yticks([])
    if order ==-1:
        if xmax:
            xticks = np.arange(x.min(), xmax + 1, 1, dtype=np.int_)
            xv = [x.min(), xmax +1]
        else:
            xticks=x
            xv = [x.min(), x.max() + 1]
        axL.set_xticks(xticks)
        axL.set_xticklabels([str(m) for m in xticks], rotation=90)
        axL.set_xlabel(myxlabel)
        axL.set_ylabel(myylabel)
        axL.legend()
        # axL.grid()
        # yv = np.array( axL.get_ylim() )
        axL.set_xlim(xv)
        #
        # axR = axL.twinx()
        # axR.plot(x, np.cumsum(y_total), '-', color=linecol)
        axR.set_xlim(xv)
        if ymax:
            axR.set_ylim([0,ymax])
            yRticks = np.arange(0, ymax, 10000, dtype=np.int_)
            axR.set_yticks(yRticks)
        axR.set_ylabel(myy2label)

    if fname:
        myformat([axL, axR])
        mysave(fig, fname)
        plt.close()

def bar_cumulative_comp(x, y1_zip, y2_zip, fname,fig, ax,
                        xmax=None, ymax=50001, width=None,
                        myxlabel='Year', myylabel='Installed capacity, MW', myy2label='Cumulative capacity, MW',
                        linecol='k'):
    # Plot first set
    stacked_bar_cumulative(x, y1_zip, fig_in=fig, ax_in=ax, width=width)
    stacked_bar_cumulative(x, y2_zip, ymax=ymax, order=-1, fig_in=fig, ax_in=ax, width=width)
    plt.show()



