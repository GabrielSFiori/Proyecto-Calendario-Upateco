import tkinter as tk
import csv
from datetime import datetime, timedelta

days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

def show_week_events(start_date):
    root = tk.Tk()
    root.title('Agenda Semanal')
    root.geometry('1100x400+100+100')
    root.config(background="#E59866")
    root.resizable(False, False)

    day_frame = tk.Frame(root)
    day_frame.pack(pady=10)

    for day in days:
        tk.Label(day_frame, text=day, width=15, padx=24, pady=5, borderwidth=2, relief='groove',background='#9b9b9b').pack(side=tk.LEFT)

    event_frame = tk.Frame(root)
    event_frame.pack()

    with open('agenda.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        events = list(reader)

    week_start = start_date - timedelta(days=start_date.weekday())
    week_end = week_start + timedelta(days=6)
    week_events = [event for event in events if
                   datetime.strptime(event['Fecha'], '%d/%m/%Y').date() >= week_start.date() and
                   datetime.strptime(event['Fecha'], '%d/%m/%Y').date() <= week_end.date()]

    day_events = {}
    for event in week_events:
        day = datetime.strptime(event['Fecha'], '%d/%m/%Y').strftime('%A')
        if day == 'Monday':
            day = 'Lunes'
        elif day == 'Tuesday':
            day = 'Martes'
        elif day == 'Wednesday':
            day = 'Miércoles'
        elif day == 'Thursday':
            day = 'Jueves'
        elif day == 'Friday':
            day = 'Viernes'
        elif day == 'Saturday':
            day = 'Sábado'
        elif day == 'Sunday':
            day = 'Domingo'
        if day not in day_events:
            day_events[day] = []
        day_events[day].append(event) 

    def show_prev_week():
        nonlocal week_start, week_end
        week_start -= timedelta(days=7)
        week_end = week_start + timedelta(days=6)
        root.destroy()  # destroy the current window
        show_week_events(week_start)  # call show_week_events with updated start_date

    def show_next_week():
        nonlocal week_start, week_end
        week_start += timedelta(days=7)
        week_end = week_start + timedelta(days=6)
        root.destroy()  # destroy the current window
        show_week_events(week_start)  # call show_week_events with updated start_date

    prev_button = tk.Button(root, text='Semana anterior', command=show_prev_week,background='#9b9b9b',font=("bold italic 2",11))
    prev_button.pack(side=tk.LEFT, padx=10, pady=10)

    next_button = tk.Button(root, text='Próxima semana', command=show_next_week,background='#9b9b9b',font=("bold italic 2",11))
    next_button.pack(side=tk.LEFT, padx=10, pady=10)

    for day in days:
        if day in day_events:
            event_list = tk.Listbox(event_frame, width=23, height=15, borderwidth=2, relief='groove',background='#9b9b9b')
            for event in day_events[day]:
                event_list.insert(tk.END, event['Titulo'])
                event_list.insert(tk.END, event['Descripcion'])
                event_list.insert(tk.END, event['Fecha'])
                event_list.insert(tk.END, '')
            event_list.pack(side=tk.LEFT, padx=6, pady=10)
        else:
            date_no_events = week_start + timedelta(days=days.index(day))
            tk.Label(event_frame, text=f"{date_no_events.strftime('%d/%m/%Y')} - Sin eventos", width=19, padx=10,
                    pady=10, borderwidth=2, relief='groove').pack(side=tk.LEFT)

    root.mainloop()
