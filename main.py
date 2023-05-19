import tkinter as tk
import matplotlib
from tkinter import messagebox, filedialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algorithms

matplotlib.use('Agg')


class ClippingApp:

    def __init__(self):
        self.master = tk.Tk()
        self.master.title('Clipping algorithms')
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.resizable(width=False, height=False)

        self.scale = range(0, 100)

        self.figure = plt.figure(figsize=(7, 7), dpi=100)
        plt.grid(linewidth=0.5, which='both', axis='both', color='gray', linestyle='--')
        plt.ylabel('y')
        plt.xlabel('x')

        plt.axis('equal')

        self.canvas = FigureCanvasTkAgg(self.figure)
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack(side=tk.RIGHT, padx=10)

        self.alg_var = tk.StringVar(value="l")

        radiobutton1 = tk.Radiobutton(self.options_frame, text="Liang Barsky", variable=self.alg_var,
                                      value="l")
        radiobutton1.select()
        radiobutton1.pack()

        tk.Radiobutton(self.options_frame, text='Cyrus Beck', variable=self.alg_var, value="c").pack()

        tk.Button(self.options_frame, text='Build', command=self.clip).pack()

        self.filepath = None

    def start(self):
        self.master.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()
            plt.close()

    def ask_file(self):
        self.filepath = filedialog.askopenfilename(initialdir='.', filetypes=[("Text files", "*.txt")])

    def clear_canvas(self):
        plt.clf()
        plt.grid(linewidth=0.5, which='both', axis='both', color='gray', linestyle='--')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.axis('equal')

    def parse_file1(self):
        with open(self.filepath, 'r') as file:
            data = file.read()
            split_data = data.split()
            num = int(split_data[0])
            del split_data[0]
            k = 0
            res = []
            for _ in range(num):
                res.append(
                    [int(split_data[k]), int(split_data[k + 1]), int(split_data[k + 2]), int(split_data[k + 3])])
                k += 4
            res1 = [int(split_data[-4]), int(split_data[-3]), int(split_data[-2]), int(split_data[-1])]
            return res, res1

    def parse_file2(self):
        with open(self.filepath, 'r') as file:
            data = file.read()
            split_data = data.split()

            num = int(split_data[0])
            res = []
            clip_polygon = []
            k = 1
            for _ in range(num):
                res.append(
                    [int(split_data[k]), int(split_data[k + 1]), int(split_data[k + 2]), int(split_data[k + 3])])
                k += 4

            num = int(split_data[k])
            k += 1
            for _ in range(num):
                clip_polygon.append((int(split_data[k]), int(split_data[k + 1])))
                k += 2

            return res, clip_polygon


    def clip(self):
        if self.alg_var.get() == 'l':
            self.process_liang_barsky()
        else:
            self.process_cyrus_beck()


    def process_cyrus_beck(self):
        self.ask_file()
        if self.filepath == None or self.filepath == '':
            messagebox.showerror(message='file is not chosen', title='Error')
            return

        self.clear_canvas()
        lines, clip_polygon = self.parse_file2()

        # new_lines = []
        # for line in lines:
        #     new_lines.append(algorithms.cyrus_beck_algorithm([[line[0],
        #                                                 line[1]],
        #                                                 [line[2],
        #                                                 line[3]]],
        #                                                 clip_polygon))


        # self.draw_polygon(clip_polygon, 'black', 3)

        # for line in lines:
        #     plt.plot([line[0], line[2]], [line[1], line[3]], color='red', linewidth=2)
        
        # for new_line in new_lines:
        #     if new_line == None:
        #         continue
        #     plt.plot([new_line[0], new_line[2]], [new_line[1], new_line[3]], color='green', linewidth=4)
        #     plt.plot(*new_line[4].exterior.xy, color='red')
        #     # plt.plot(*new_line, color='green', linewidth=4)
        #     # plt.plot(*int_line.xy)

        new_lines = []
        for line in lines:
            new_lines.append(algorithms.cyrus_beck_algorithm(line[0],
                                                        line[1],
                                                        line[2],
                                                        line[3],
                                                        clip_polygon))


        self.draw_polygon(clip_polygon, 'black', 3)

        for line in lines:
            plt.plot([line[0], line[2]], [line[1], line[3]], color='red', linewidth=2)
        
        for new_line in new_lines:
            if new_line == None:
                continue
            plt.plot([new_line[0], new_line[2]], [new_line[1], new_line[3]], color='green', linewidth=4)


        plt.title('Cyrus Beck')
        self.canvas.draw()


    def process_liang_barsky(self):
        try:
            self.ask_file()
            if self.filepath == None or self.filepath == '':
                messagebox.showerror(message='file is not chosen', title='Error')
                return

            self.clear_canvas()

            lines, clip_rectangle = self.parse_file1()
            new_lines = []
            for line in lines:
                new_lines.append(algorithms.liang_barsky(line[0],
                                                         line[1],
                                                         line[2],
                                                         line[3],
                                                         clip_rectangle[0],
                                                         clip_rectangle[1],
                                                         clip_rectangle[2],
                                                         clip_rectangle[3]))

            for line in lines:
                plt.plot([line[0], line[2]], [line[1], line[3]], color='red', linewidth=2)

            for line in new_lines:
                if line != None:
                    plt.plot([line[0], line[2]], [line[1], line[3]], color='green', linewidth=4)

            self.draw_clip_rectangle(clip_rectangle[0], clip_rectangle[1], clip_rectangle[2], clip_rectangle[3])
            plt.title('Liang Barskiy')
            self.canvas.draw()

        except:
            messagebox.showerror(message='file is wrong(1)', title='Error')

    def draw_clip_rectangle(self, x_min, y_min, x_max, y_max):
        plt.plot([x_min, x_max], [y_min, y_min], color='black', linewidth=3)
        plt.plot([x_max, x_max], [y_min, y_max], color='black', linewidth=3)
        plt.plot([x_min, x_max], [y_max, y_max], color='black', linewidth=3)
        plt.plot([x_min, x_min], [y_min, y_max], color='black', linewidth=3)


    def draw_polygon(self, polygon, color, linewidth):
        for i in range(len(polygon)):
            plt.plot([polygon[i-1][0], polygon[i][0]], [polygon[i-1][1], polygon[i][1]], color=color, linewidth=linewidth)


if __name__ == "__main__":
    ClippingApp().start()
