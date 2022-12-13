import pandas as pd
import argparse
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (12, 4)

# colors
green = '#D33D35'
darkblue = '#2251BD'
yellow = '#F5D406'
red = '#f7394c'
lightblue = '#22A3BD'
turqoise = '#22BDB1'
lila = '#7C129C'
gray = 'dimgray'
black = 'black'
red_heart1 = '#B30808'
red_heart2 = '#D60A0A'
magenta = '#781C42'
orange = '#F46B21'
darkgray = '#4a4a4a'
bluegreen = '#00a3b5'

color_lines = bluegreen
color_markers = darkgray


def create_dataframe(path_to_csv_data):
    # import csv data
    # BPM; pulse data; resting BPM; time; exercise intensity
    # headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
    # df = pd.read_csv('data_log/data_log-21_12_21-1444.csv', sep=';', names=headers)
    df = pd.read_csv(path_to_csv_data, sep=';')

    filepath = path_to_csv_data.split('.')[0]

    return df, filepath


def create_plot(df, show_plot=False, save_plot=False, save_path="somefilename"):
    # test modifications
    #df["exercise_intensity"].replace({1: 0}, inplace=True)
    #df.at[6522, 'exercise_intensity'] = -1
    #df.at[6666, 'exercise_intensity'] = 1  # exercise start
    #df.at[7066, 'exercise_intensity'] = 10

    # - get first entry with resting BPM
    first_resting_BPM_index = df[df.resting_BPM != -1].first_valid_index()

    # get resting BPM and calc boundaries
    resting_BPM = df.at[first_resting_BPM_index, 'resting_BPM']
    upper_boundary = resting_BPM * 1.3
    lower_boundary = resting_BPM * 1.2

    # - normalize time to start of exercise
    df["time"] = df["time"] - df.at[first_resting_BPM_index, 'time']

    # get indices of markers
    idx_up = df.index[df['exercise_intensity'] == 1].tolist()
    idx_down = df.index[df['exercise_intensity'] == -1].tolist()
    idx_same = df.index[df['exercise_intensity'] == 0].tolist()

    # idx_down, idx_same = [4000], [5000]

    # create plot
    fig, ax = plt.subplots()

    # BPM boundary lines
    plt.axhline(y=upper_boundary, linewidth=1, color=gray, linestyle='--', label='exercise BPM boundaries')
    plt.axhline(y=lower_boundary, linewidth=1, color=gray, linestyle='--')
    plt.axhline(y=resting_BPM, linewidth=1, color=gray, linestyle=':', label='resting BPM')

    # BPM data
    ax.plot(df.time, df.BPM, '-', linewidth=1, color=color_lines, label='recorded BPM')

    # action evaluation markers
    ax.plot(df.time, df.BPM, '^', markevery=idx_up, label='higher exercise intensity',
            markersize=4,  # color=color_lines,  # 10
            mfc=color_markers, mec=color_markers, markeredgewidth=1.5)
    ax.plot(df.time, df.BPM, 'v', markevery=idx_down, label='lower exercise intensity',
            markersize=4,   # color=color_lines,  # 11
            mfc=color_markers, mec=color_markers, markeredgewidth=1.5)
    ax.plot(df.time, df.BPM, 'o', markevery=idx_same, label='same exercise intensity',
            markersize=5,   # color=color_lines,
            mfc=color_markers, mec=color_markers, markeredgewidth=1)

    # axis settings
    # - limits
    ax.set_xlim(left=-20)
    ax.set_ylim(50, 100)

    # - custom ticks
    #ax.get_yticklabels()
    #plt.yticks(list(plt.yticks()[0]) + [resting_BPM, upper_boundary, lower_boundary])
    ax2 = ax.twinx()
    ax2.set_yticks([resting_BPM, upper_boundary, lower_boundary])
    ax2.set_ylim(50, 100)

    for i in range(0, 3):
        ax2.get_yticklabels()[i].set_color(color_lines)
        # ax2.get_yticklabels()[i].set_fontweight('bold')

    # - labels
    ax.set_xlabel('time (s)')
    ax.set_ylabel('heartbeats per minute (BPM)')

    # legend
    ax.legend(loc="lower right", ncol=2, fontsize='small', markerscale=0.8)

    if save_plot:
        plt.savefig(save_path + ".png", dpi=300)
        print("Saved plot to: % s" % save_path + ".png")

    if show_plot:
        seconds = 5
        print("Showing plot for " + str(seconds) + " seconds")
        plt.show(block=False)
        plt.pause(seconds)
        plt.close()


def create_plot_from_path(csv_path, show_plot=False, save_plot=True):
    df, file_path = create_dataframe(csv_path)
    create_plot(df, show_plot=show_plot, save_plot=save_plot, save_path=file_path)


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-p", "--path", help="Path to csv file")

    # Read arguments from command line
    args = parser.parse_args()

    if args.path:
        print("Processing: % s" % args.path)
        dataframe, path = create_dataframe(args.path)
        create_plot(dataframe, show_plot=False, save_plot=True, save_path=path)
