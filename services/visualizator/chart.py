from matplotlib import pyplot as plt


class Chart:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax

        fig.set_figheight(15)
        fig.set_figwidth(15)

    def draw(self, x, y, title, *args, **kwargs):
        self.ax.clear()
        self.ax.plot(x, y, *args, **kwargs)
        self.ax.grid()
        self.ax.set_title(title, color='w', fontsize=12, fontweight='bold')
        self.ax.set_xlabel('Time', color='w', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Temperature', color='w', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, color='w', fontsize=12, fontweight='bold')
        plt.yticks(color='w', fontsize=12, fontweight='bold')
