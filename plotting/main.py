import csv
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        lst = list(tuple(line) for line in reader)
        return lst


def plot_all_in_directory(directory):
    sorted_files = sorted(os.listdir(directory))
    for file in sorted_files:
        path = os.path.join(directory, file)
        if path.__contains__("total-results") or path.__contains__("graphs"):
            continue
        rows = read_csv(path)
        count_and_message_size = rows.pop(0)
        header = rows.pop(0)
        sorted_rows = sorted(rows)
        columns = list(map(list, zip(*sorted_rows)))
        plt.figure()
        plt.plot(list(map(divide_by_1000, convert_to_int(columns[0]))), convert_to_int(columns[1]), linewidth=0.5, marker='o',
                 markerfacecolor='blue', markersize=1, linestyle='dashed')
        plt.ylim(ymin=0)
        plt.xlabel(header[0])
        plt.ylabel(header[1])
        plt.suptitle(file[:-4])
        plt.title(count_and_message_size[0] + count_and_message_size[1] +
                  " " + count_and_message_size[2] + count_and_message_size[3])
        plt.gcf().autofmt_xdate()


def divide_by_1000(number):
    return number / 1000


def save_plots_to_pdf(filename):
    p = PdfPages(filename)

    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(p, format='pdf')
    p.close()


def convert_to_int(array):
    return list(map(int, array))


if __name__ == '__main__':
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    print("Directory of csvs with data is ", sys.argv[1])
    plot_all_in_directory(sys.argv[1])
    save_plots_to_pdf(sys.argv[1] + "/graphs.pdf")
