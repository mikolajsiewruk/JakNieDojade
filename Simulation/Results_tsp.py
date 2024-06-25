import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Results_tsp:
    def __init__(self):
        # initialize arrays for each size
        self.under_ten = []
        self.ten_thirteen = []
        self.thirteen_sixteen = []
        self.sixteen_nineteen = []
        self.over_nineteen = []
        self.num_under_ten = 0
        self.num_ten_thirteen = 0
        self.num_thirteen_sixteen = 0
        self.num_sixteen_nineteen = 0
        self.num_over_nineteen = 0
        self.under_ninety = []
        self.ninety_hundred = []
        self.hundred_hundredten = []
        self.hundredten_hundredtwenty = []
        self.over_hundredtwenty = []
        self.num_under_ninety = 0
        self.num_ninety_hundred = 0
        self.num_hundred_hundredten = 0
        self.num_hundredten_hundredtwenty = 0
        self.num_over_hundredtwenty = 0

    def calculate_statistics(self, marker):
        if marker == 0:
            means = [np.mean(self.under_ten), np.mean(self.ten_thirteen), np.mean(self.thirteen_sixteen), np.mean(self.sixteen_nineteen), np.mean(self.over_nineteen)]
            sds = [np.std(self.under_ten), np.std(self.ten_thirteen), np.std(self.thirteen_sixteen), np.std(self.sixteen_nineteen), np.std(self.over_nineteen)]
            minimums = [min(self.under_ten), min(self.ten_thirteen), min(self.thirteen_sixteen), min(self.sixteen_nineteen), min(self.over_nineteen)]
            maximums = [max(self.under_ten), max(self.ten_thirteen), max(self.thirteen_sixteen), max(self.sixteen_nineteen), max(self.over_nineteen)]

            return means, sds, minimums, maximums
        else:
            means = [np.mean(self.under_ninety), np.mean(self.ninety_hundred), np.mean(self.hundred_hundredten),
                     np.mean(self.hundredten_hundredtwenty), np.mean(self.over_hundredtwenty)]
            sds = [np.std(self.under_ninety), np.std(self.ninety_hundred), np.std(self.hundred_hundredten),
                   np.std(self.hundredten_hundredtwenty), np.std(self.over_hundredtwenty)]
            minimums = [min(self.under_ninety), min(self.ninety_hundred), min(self.hundred_hundredten),
                        min(self.hundredten_hundredtwenty), min(self.over_hundredtwenty)]
            maximums = [max(self.under_ninety), max(self.ninety_hundred), max(self.hundred_hundredten),
                        max(self.hundredten_hundredtwenty), max(self.over_hundredtwenty)]

            return means, sds, minimums, maximums
    def draw_boxplot(self, title, filename, marker):
        # Prepare data for seaborn
        if marker == 0:
            data = {
                '< 10': self.under_ten,
                '10-13': self.ten_thirteen,
                '13-16': self.thirteen_sixteen,
                '16-19': self.sixteen_nineteen,
                '> 19': self.over_nineteen
            }

            # Convert data to long-form DataFrame for seaborn
            import pandas as pd
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))

            # Melt DataFrame to long-form
            df_melted = df.melt(var_name='Distance', value_name='Time')

            # Create the boxplot
            plt.figure(figsize=(10, 7))
            sns.boxplot(x='Distance', y='Time', data=df_melted)
            plt.title(title)
            plt.savefig(filename)
            plt.close()

        else:
            data = {
                '< 90': self.under_ninety,
                '90-100': self.ninety_hundred,
                '100-110': self.hundred_hundredten,
                '110-120': self.hundredten_hundredtwenty,
                '> 120': self.over_hundredtwenty
            }
            # Convert data to long-form DataFrame for seaborn
            import pandas as pd
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))

            # Melt DataFrame to long-form
            df_melted = df.melt(var_name='Number of stops', value_name='Time')

            # Create the boxplot
            plt.figure(figsize=(10, 7))
            sns.boxplot(x='Number of stops', y='Time', data=df_melted)
            plt.title(title)
            plt.savefig(filename)
            plt.close()


