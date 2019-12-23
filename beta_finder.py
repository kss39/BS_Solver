from pathlib import Path
import data_fetcher as df

blocks = df.fetch(Path('./resources/paper_data/p1.csv'))

for b in blocks:
    print(b.reg(50, 0.01))
