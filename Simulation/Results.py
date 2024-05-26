import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Results:
    def __init__(self):
        # initialize arrays for each size
        self.under_five = []
        self.five_ten = []
        self.ten_fifteen = []
        self.fifteen_twenty = []
        self.over_twenty = []

    def calculate_statistics(self):
        means = [np.mean(self.under_five),np.mean(self.five_ten),np.mean(self.ten_fifteen),np.mean(self.fifteen_twenty),np.mean(self.over_twenty)]
        sds = [np.std(self.under_five),np.std(self.five_ten),np.std(self.ten_fifteen),np.std(self.fifteen_twenty),np.std(self.over_twenty)]
        minimums = [min(self.under_five),min(self.five_ten),min(self.ten_fifteen),min(self.fifteen_twenty),min(self.over_twenty)]
        maximums = [max(self.under_five),max(self.five_ten),max(self.ten_fifteen),max(self.fifteen_twenty),max(self.over_twenty)]

        return means, sds, minimums, maximums

    def draw_boxplot(self, title):
        # Prepare data for seaborn
        data = {
            '< 5': self.under_five,
            '5-10': self.five_ten,
            '10-15': self.ten_fifteen,
            '15-20': self.fifteen_twenty,
            '> 20': self.over_twenty
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
        plt.show()

