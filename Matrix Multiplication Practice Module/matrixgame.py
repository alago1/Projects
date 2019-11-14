import tkinter as tk
import random
from numpy import dot
import time

class MainWindow:

    def __init__(self, root):
        #Window Set up
        self._root = root
        self._root.state('zoomed')
        self._root.title('Multiplying Game')


        # combobox_font = font.Font(family='Arial', size=15)
        # self._root.option_add("*TCombobox*Listbox*Font", combobox_font)

        #Widget Initialization
        window_canvas = tk.Canvas(self._root, bg='#FF8000', highlightthickness=0, height=100)

        instruction_canvas = tk.Canvas(window_canvas, bg='#FF8000', highlightthickness=0, width=150, height=80)

        problem_frame = tk.Frame(window_canvas)
        problem_title = tk.Canvas(problem_frame, bg='#FF8000', highlightthickness=0, width=90, height=20)
        self._num_problems = 20
        self._number_problems_text = tk.Canvas(problem_frame, bg='#FF00FF', highlightbackground='#646464', width=80, height=40)

        level_frame = tk.Frame(window_canvas)
        level_title = tk.Canvas(level_frame, bg='#FF8000', highlightthickness=0, width=50, height=20)
        self._level_number = 1
        self._level_text = tk.Canvas(level_frame, bg='#FF00FF', highlightbackground='#646464', width=30, height=40)

        # pixel = tk.PhotoImage(width=1, height=1)
        start_button = tk.Button(window_canvas, text='Start Time Trial', width=13, height=2, command=lambda:print('START BUTTON', self.start_time_trial()))

        self._current_problem_frame = tk.Frame(self._root)
        self._answer_current_problem = self.render_problem(self._current_problem_frame)

        check_answer_frame = tk.Frame(self._root)
        self._dne_boolean_variable = tk.BooleanVar()
        self._dne_checkbutton = tk.Checkbutton(check_answer_frame, text='Product Does Not Exist \n(Toggle: Q)', variable=self._dne_boolean_variable)
        check_answer_button = tk.Button(check_answer_frame, text='Check Answer', width=12, height=2, command=lambda:print('CHECK ANSWER BUTTON:', self.check_answer()))

        self._timer_canvas = tk.Canvas(self._root, bg='#FF8000', highlightthickness=0)
        self._timeStarted = False # change to True when start is pressed
        self._endTimer = True # change to False when start is pressed
        self._startTime = time.time() # reset when start is pressed
        self._timer_label = tk.Label(self._timer_canvas, text='Time: 00:00', font=('Courier', 30, 'underline'), bg='#FF8000')

        problem_counter_frame = tk.Canvas(self._root, bg='#FF8000', highlightthickness=0)
        self._num_correct_answers = 0
        self._correct_answer_counter = tk.Label(problem_counter_frame, text='#Correct: 0', font=('Courier', 20), bg='#FF8000')
        self._current_streak = 0
        self._current_streak_counter = tk.Label(problem_counter_frame, text='Current Streak: 0', font=('Courier', 15), bg='#FF8000')
        self._num_wrong_answers = 0
        self._wrong_answer_counter = tk.Label(problem_counter_frame, text='#Wrong: 0', font=('Courier', 20), bg='#FF8000')

        #Grid Set up
        window_canvas.grid(row=0, column=0, sticky='new', columnspan=2)

        instruction_canvas.grid(row=0, column=0)

        problem_frame.grid(row=0, column=1, padx=0, pady=50)
        problem_title.grid(row=0, column=0)
        self._number_problems_text.grid(row=1, column=0, sticky='ew')

        level_frame.grid(row=0, column=2, padx=50, pady=50)
        level_title.grid(row=0, column=0)
        self._level_text.grid(row=1, column=0, sticky='ew')

        start_button.grid(row=0, column=3, sticky='w', pady=(20, 0))

        self._current_problem_frame.grid(row=1, column=0, sticky='new')

        check_answer_frame.grid(row=1, column=1, sticky='new')
        self._dne_checkbutton.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        check_answer_button.grid(row=1, column=0, padx=10, pady=10)

        self._timer_canvas.grid(row=3, column=0, columnspan=2, sticky='nsew')
        self._timer_label.grid(row=0, column=0, sticky='nsew', pady=(20, 0), padx=10)

        problem_counter_frame.grid(row=4, column=0, columnspan=2, sticky='nsew')
        self._correct_answer_counter.grid(row=0, column=0, sticky='nsw', padx=10)
        self._current_streak_counter.grid(row=1, column=0, sticky='nsw', padx=20)
        self._wrong_answer_counter.grid(row=2, column=0, sticky='nsw', padx=10, pady=(0, 10))


        #Widget Post-Initialization Configuration
        instruction_canvas.create_text(20, 30, text='Click Number \n  Boxes to \n customize:', font=('Arial', 8, 'bold'), anchor='nw')

        problem_title.create_text(0, 0, text='# of Problems', font=('Arial', 10, 'bold'), anchor='nw')
        self._num_problems_textID = self._number_problems_text.create_text(23, 0, text='20', font=('Arial', 28, 'bold'), anchor='nw', fill='#FFFF00')

        level_title.create_text(7, 0, text='Level', font=('Arial', 10, 'bold'), anchor='nw')
        self._level_textID = self._level_text.create_text(15, 0, text='1', font=('Arial', 28, 'bold'), anchor='nw', fill='#FFFF00')


        #Grid Resizing
        # self._root.grid_rowconfigure(0, weight=1)
        # self._root.grid_columnconfigure(0, weight=1)
        # self._root.grid_rowconfigure(1, weight=1)


        #Key Bindings
        self._number_problems_text.bind('<Button-1>', self.change_number_problems)
        self._level_text.bind('<Button-1>', self.change_level)

        self._dne_checkbutton.bind('<Key-q>', self.toogle_dne_check_on_entry)
        self._dne_checkbutton.bind('<Return>', self.check_answer)
        check_answer_button.bind('<Key-q>', self.toogle_dne_check_on_entry)
        check_answer_button.bind('<Return>', self.check_answer)


    def change_number_problems(self, event):
        if not self._timeStarted:
            if self._num_problems == 80:
                self._num_problems = 100
                self._number_problems_text.itemconfig(self._num_problems_textID, text=str(self._num_problems))
                self._number_problems_text.move(self._num_problems_textID, -13, 0)
            elif self._num_problems == 100:
                self._num_problems = 20
                self._number_problems_text.itemconfig(self._num_problems_textID, text=str(self._num_problems))
                self._number_problems_text.move(self._num_problems_textID, 13, 0)
            else:
                self._num_problems += 20
                self._number_problems_text.itemconfig(self._num_problems_textID, text=str(self._num_problems))

    def change_level(self, event):
        if not self._timeStarted:
            if self._level_number == 5:
                self._level_number = 1
            else:
                self._level_number += 1
            self._level_text.itemconfig(self._level_textID, text=str(self._level_number))

            self.next_problem()

    def generate_problem(self):
        # 5% chance of the problem having no solution
        isUndefined = (int(100*random.random()) <= 10)
        if self._level_number == 1:
            dim = [1, 2]
            mag = range(6)
        elif self._level_number == 2:
            dim = [1, 2, 3]
            mag = range(10)
        elif self._level_number == 3:
            dim = [2, 3, 4]
            mag = range(11)
        elif self._level_number == 4:
            dim = [2, 3, 4]
            mag = range(13)
        else:
            dim = [3, 4]
            mag = range(20)

        if isUndefined:
            d1, d4 = random.choice(dim), random.choice(dim)
            tmp = dim.copy()
            random.shuffle(tmp)
            d2, d3 = tmp[0:2]

        d1, d2, d4 = [random.choice(dim) for x in range(3)]
        # avoid 1x1 matrices
        if self._level_number == 2:
            if d1 == 1 and d2 == 1:
                tmp = dim.copy()[1:]
                toss = int(100*random.random())
                if toss < 50:
                    d1 = random.choice(tmp)
                else:
                    d2 = random.choice(tmp)
            if d2 == 1 and d4 == 1:
                tmp = dim.copy()[1:]
                toss = int(100*random.random())
                if toss < 50:
                    d2 = random.choice(tmp)
                else:
                    d4 = random.choice(tmp)

        if not isUndefined:
            d3 = d2

        matrix1 = Matrix(d1, d2, [(-1)**int(2*random.random())*random.choice(mag) for x in range(d1*d2)])
        matrix2 = Matrix(d3, d4, [(-1)**int(2*random.random())*random.choice(mag) for x in range(d3*d4)])
        answer = matrix1.product(matrix2)
        # print(matrix1, matrix2, answer)
        return matrix1, matrix2, answer

    def render_problem(self, problem_frame):
        m1, m2, ans = self.generate_problem()

        m1_frame = tk.Frame(problem_frame, bg='#FF8000')
        m2_frame = tk.Frame(problem_frame, bg='#FF8000')
        equal_sign_frame = tk.Frame(problem_frame, bg='#FF8000')
        ans_frame = tk.Frame(problem_frame, bg='#FF8000')

        #print(m1.matrixForm)
        open_bracket_one = tk.Canvas(m1_frame, width=50, height=60*m1.nRows)
        open_bracket_one.grid(row=0, column=0, rowspan=m1.nRows, padx=(10, 0), sticky='ns')
        open_bracket_one.create_text(0, 0, text='[', anchor='nw', font=('Courier', 45*m1.nRows))
        for i in range(m1.nRows):
            for j in range(m1.nCols):
                text = tk.Canvas(m1_frame, width=50, height=50)
                text.grid(row=i, column=j+1, padx=10, pady=10)
                text.create_text(10, 10, text=str(m1.matrixForm[i][j]), anchor='nw', font=30)
        close_bracket_one = tk.Canvas(m1_frame, width=50, height=60*m1.nRows)
        close_bracket_one.grid(row=0, column=m1.nCols+1, rowspan=m1.nRows, padx=(0, 10), sticky='ns')
        close_bracket_one.create_text(0, 0, text=']', anchor='nw', font=('Courier', 45*m1.nRows))

        #print(m2.matrixForm)
        open_bracket_two = tk.Canvas(m2_frame, width=50, height=60*m2.nRows)
        open_bracket_two.grid(row=0, column=0, rowspan=m2.nRows, sticky='ns')
        open_bracket_two.create_text(0, 0, text='[', anchor='nw', font=('Courier', 45*m2.nRows))
        for i in range(m2.nRows):
            for j in range(m2.nCols):
                text = tk.Canvas(m2_frame, width=50, height=50)
                text.grid(row=i, column=j+1, padx=10, pady=10)
                text.create_text(10, 10, text=str(m2.matrixForm[i][j]), anchor='nw', font=30)
        close_bracket_two = tk.Canvas(m2_frame, width=50, height=60*m2.nRows)
        close_bracket_two.grid(row=0, column=m2.nCols+1, rowspan=m2.nRows, padx=(0, 10), sticky='ns')
        close_bracket_two.create_text(0, 0, text=']', anchor='nw', font=('Courier', 45*m2.nRows))

        equal_sign = tk.Canvas(equal_sign_frame, width=50, height=50)
        equal_sign.grid(row=0, column=m2.nCols+2)
        equal_sign.create_text(10, 0, text='=', anchor='nw', font=('Courier', 30))


        open_bracket_three = tk.Canvas(ans_frame, width=50, height=60*m1.nRows)
        open_bracket_three.grid(row=0, column=0, rowspan=m1.nRows, sticky='ns')
        open_bracket_three.create_text(0, 0, text='[', anchor='nw', font=('Courier', 45*m1.nRows))
        stringVariables = [[None for col in range(m2.nCols)] for row in range(m1.nRows)]
        entries = [[None for col in range(m2.nCols)] for row in range(m1.nRows)]
        for i in range(m1.nRows):
            for j in range(m2.nCols):
                string = tk.StringVar()
                #string.trace("w", self.toogle_dne_check_on_entry)
                stringVariables[i][j] = string
                entry = tk.Entry(ans_frame, textvariable=string, width=4, font=30)
                entry.grid(row=i, column=j+1, padx=10)
                entry.bind('<Return>', self.check_answer)
                entry.bind('<Key-q>', self.toogle_dne_check_on_entry)
                entries[i][j] = entry
        entries[0][0].focus()
        close_bracket_three = tk.Canvas(ans_frame, width=50, height=60*m1.nRows)
        close_bracket_three.grid(row=0, column=m2.nCols+1, rowspan=m1.nRows, sticky='ns')
        close_bracket_three.create_text(0, 0, text=']', anchor='nw', font=('Courier', 45*m1.nRows))

        m1_frame.grid(row=0, column=0, sticky='w')
        m2_frame.grid(row=0, column=1, sticky='w')
        equal_sign_frame.grid(row=0, column=2, sticky='w')
        ans_frame.grid(row=0, column=3, sticky='w')

        problem_frame.grid_rowconfigure(0, weight=1)

        print(ans.matrixForm if ans is not None else 'Does Not Exist')
        self._answer_string_variables = stringVariables
        self._answer_entries = entries
        return ans

    def next_problem(self):
        for child_frame in self._current_problem_frame.winfo_children():
            child_frame.destroy()
        self._dne_boolean_variable.set(False)

        self._answer_current_problem = self.render_problem(self._current_problem_frame)

    def check_answer(self, event=None):
        errors = list()
        if self._dne_boolean_variable.get():
            if self._answer_current_problem is not None:
                errors.append(-1)
        elif self._answer_current_problem is None:
            errors.append(-1)
        else:
            index = 0
            for i in range(self._answer_current_problem.nRows):
                for j in range(self._answer_current_problem.nCols):
                    if self._answer_string_variables[i][j].get() != str(self._answer_current_problem.matrixForm[i][j]):
                        errors.append(index)
                    index += 1


        if len(errors) == 0:
            self.update_correct()
        else:
            self.update_wrong()


        if not self._timeStarted:
            if len(errors) != 0:
                print('Errors: ', errors)
                self.display_errors(errors)
            else:
                self.next_problem()
        else:
            if len(errors) == 0:
                if self._num_correct_answers == self._num_problems:
                    self.end_time_trial()
                else:
                    self.next_problem()
            else:
                print('Errors: ', errors)
                self.display_errors(errors)

    def display_errors(self, errors):
        if -1 in errors:
            self._dne_checkbutton.configure(bg='red')
        else:
            self._dne_checkbutton.configure(bg='#F0F0F0')

        index = 0
        for i in range(self._answer_current_problem.nRows):
            for j in range(self._answer_current_problem.nCols):
                if index in errors:
                    self._answer_entries[i][j].configure(bg='red')
                else:
                    self._answer_entries[i][j].configure(bg='white')
                index += 1

    def update_correct(self):
        self._num_correct_answers += 1
        self._current_streak += 1

        self._correct_answer_counter.configure(text='#Correct: ' + str(self._num_correct_answers), bg='green')
        self._current_streak_counter.configure(text='Current Streak: ' + str(self._current_streak), bg='green')

        self._wrong_answer_counter.configure(bg='#FF8000')

    def update_wrong(self):
        self._num_wrong_answers += 1
        self._current_streak = 0

        self._wrong_answer_counter.configure(text='#Wrong: ' + str(self._num_wrong_answers), bg='red')
        self._current_streak_counter.configure(text='Current Streak: ' + str(self._current_streak), bg='red')

        self._correct_answer_counter.configure(bg='#FF8000')

    def start_time_trial(self):
        self._timeStarted = True
        self._endTimer = False
        self._startTime = time.time()
        self.update_timer()

        self._num_correct_answers = 0
        self._correct_answer_counter.configure(text='#Correct: 0', bg='#FF8000')
        self._current_streak = 0
        self._current_streak_counter.configure(text='Current Streak: 0', bg='#FF8000')
        self._num_wrong_answers = 0
        self._wrong_answer_counter.configure(text='#Wrong: 0', bg='#FF8000')
        self._timer_label.configure(bg='#FF8000')

        self.next_problem()

    def update_timer(self):
        if not self._endTimer:
            minutes, seconds = divmod(time.time()-self._startTime, 60)
            self._timer_label.configure(text='Time: {:0>2}:{:0>2}'.format(int(minutes), int(seconds)))
            self._root.after(1000, self.update_timer)

    def end_time_trial(self):
        self._timeStarted = False
        self._endTimer = True

        self._timer_label.configure(bg='#D4AF37')

    def toogle_dne_check_on_entry(self, event=None):
        self._dne_boolean_variable.set(not self._dne_boolean_variable.get())

        return "break"

class Matrix:

    def __init__(self, d1, d2, nums):
        self.nRows = d1
        self.nCols = d2
        self.values = nums
        matrix = [[0 for y in range(self.nCols)] for x in range(self.nRows)]
        index = 0
        for i in range(self.nRows):
            for j in range(self.nCols):
                matrix[i][j] = self.values[index]
                index += 1
        self.matrixForm = matrix

    def product(self, matrix2):
        if self.nCols != matrix2.nRows:
            return None

        matrixResult = dot(self.matrixForm, matrix2.matrixForm)
        #print('matrixResult', matrixResult)

        numResult = [0 for x in range(len(matrixResult)*len(matrixResult[0]))]
        index = 0
        for i in range(len(matrixResult)):
            for j in range(len(matrixResult[0])):
                numResult[index] = matrixResult[i][j]
                index += 1

        return Matrix(self.nRows, matrix2.nCols, numResult)


if __name__ == '__main__':
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
