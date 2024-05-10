#! pip install matplotlib
#! pip install pandas

from typing import List
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd

# Constants
NUM_FRAMES = 100
INTERVAL = 100 # delay between frames in milliseconds

# Create some random data to plot:
df = pd.DataFrame({'Date': pd.date_range(start='1/1/2022', periods=NUM_FRAMES), 
                   'Value1': np.cumsum(np.random.randint(0, 2, NUM_FRAMES)), 
                   'Value2': np.cumsum(np.random.randint(0, 2, NUM_FRAMES))})
df.set_index('Date', inplace=True)

# Create new Figure and an Axes which fills it.
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Random Data over time")

# Create line object, initial plot
line, = ax.plot(df.index, df['Value1'])
line2, = ax.plot(df.index, df['Value2'])
lines = [line, line2]

def get_description_string(data: pd.DataFrame, idx: int) -> str:
    winner = data.columns[data.iloc[idx].argmax()]
    date_str = data.index[idx].strftime('%Y-%m-%d')
    return f'{date_str}: Winner {winner}'

def update_ani_frame(frame_num: int, data_lines: List[plt.Line2D]) -> List[plt.Line2D]:
    idx_ceil = frame_num+1 # np.index end is exclusive
    df, lines = data_lines
    for i, line in enumerate(lines):
        line.set_data(df.index[:idx_ceil], df[f'Value{i+1}'][:idx_ceil])
    desc_string = get_description_string(df, frame_num)
    ax.set_xlabel(desc_string)
    return lines

# Construct the animation, using the update function as the animation director.
ani = animation.FuncAnimation(fig, update_ani_frame, frames=NUM_FRAMES, fargs=[(df, lines)], interval=100)
ani.save('graphs/animated_line_chart.gif')
plt.show()