"""Nature风格论文绘图模板"""
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'figure.dpi': 150, 'savefig.dpi': 300,
    'lines.linewidth': 1.5,
})
colors = {'blue':'#0077BB','red':'#EE7733','green':'#009988'}
color_cycle = ['#0077BB','#EE7733','#009988','#CC3311']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_cycle)
