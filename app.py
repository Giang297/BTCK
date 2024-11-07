# app.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from collections import defaultdict
import logging
import os
import random

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')
logging.basicConfig(level=logging.DEBUG)

file_path = 'school_schedule_data.xlsx'
teacher_schedules = {}
class_schedules = {}
subject_schedule = {}

def load_data_from_excel(file_path):
    try:
        teachers_df = pd.read_excel(file_path, sheet_name='teachers')
        teacher_schedule_df = pd.read_excel(file_path, sheet_name='teacher_schedule')
        classes_df = pd.read_excel(file_path, sheet_name='classes')
        class_schedule_df = pd.read_excel(file_path, sheet_name='class_schedule')
        subject_schedule_df = pd.read_excel(file_path, sheet_name='subject_schedule')
    except FileNotFoundError:
        logging.error("Excel file not found.")
        raise Exception("Excel file not found.")
    
    teachers = {}
    teacher_subjects = {}
    for _, row in teachers_df.iterrows():
        username = row['Username']
        subject = row.get('Subject')
        teachers[username] = {
            'name': row['Teacher Name'],
            'password': row['Password']
        }
        if subject:
            teacher_subjects[username] = subject

    classes = {}
    for _, row in classes_df.iterrows():
        classes[row['Username']] = {
            'name': row['Class Name'],
            'password': row['Password']
        }

    teacher_schedules = defaultdict(lambda: {day: {'morning': {}, 'afternoon': {}} for day in ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6']})
    for _, row in teacher_schedule_df.iterrows():
        teacher_name = row['Teacher Name']
        day = row['Day']
        period = row.get('Period')
        subject = row.get('Subject')
        
        if pd.isna(teacher_name) or pd.isna(day) or pd.isna(period) or pd.isna(subject):
            logging.warning(f"Incomplete row in teacher_schedule: {row}")
            continue

        period_type = 'morning' if period <= 5 else 'afternoon'
        period_number = f"Period {period if period <= 5 else period - 5}"
        teacher_schedules[teacher_name][day][period_type][period_number] = subject

    class_schedules = defaultdict(lambda: {day: {'morning': {}, 'afternoon': {}} for day in ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6']})
    for _, row in class_schedule_df.iterrows():
        class_name = row['Class Name']
        day = row['Day']
        period = row.get('Period')
        subject = row.get('Subject')
        teacher = row.get('Teacher')

        if pd.isna(class_name) or pd.isna(day) or pd.isna(period) or pd.isna(subject) or pd.isna(teacher):
            logging.warning(f"Incomplete row in class_schedule: {row}")
            continue

        period_type = 'morning' if period <= 5 else 'afternoon'
        period_number = f"Period {period if period <= 5 else period - 5}"
        class_schedules[class_name][day][period_type][period_number] = f"{subject} ({teacher})"

    subject_schedule = {}
    for _, row in subject_schedule_df.iterrows():
        subject = row['Môn học']
        weekly_periods = row['Số tiết/tuần']
        if pd.isna(subject) or pd.isna(weekly_periods):
            logging.warning(f"Incomplete row in subject_schedule: {row}")
            continue
        subject_schedule[subject] = weekly_periods
    
    return teachers, teacher_schedules, classes, class_schedules, subject_schedule, teacher_subjects

def load_data():
    global teacher_schedules, class_schedules, subject_schedule, teacher_subjects
    teachers, teacher_schedules, classes, class_schedules, subject_schedule, teacher_subjects = load_data_from_excel(file_path)
    return teachers, classes

teachers, classes = load_data()

def reset_class_schedules(class_schedules):
    for class_name in class_schedules:
        for day in ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6']:
            class_schedules[class_name][day] = {'morning': {}, 'afternoon': {}}

def auto_schedule(class_schedules, subject_schedule, teacher_subjects, days=['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6'], periods_per_day=10):
    reset_class_schedules(class_schedules)
    reset_class_schedules(teacher_schedules)

    afternoon_only_subjects = {"Thể Dục", "Nghệ Thuật", "Tin học"}
    consecutive_subjects = {"Thể Dục", "Tin học"}

    for class_name, schedule in class_schedules.items():
        remaining_subjects = subject_schedule.copy()
        
        for day in days:
            subject_count_per_day = defaultdict(int)
            period = 1
            
            while period <= periods_per_day:
                period_type = 'morning' if period <= 5 else 'afternoon'
                period_number = f"Period {period if period <= 5 else period - 5}"

                if remaining_subjects:
                    available_subjects = [
                        subject for subject, periods_left in remaining_subjects.items() 
                        if periods_left > 0 and subject_count_per_day[subject] < 2
                    ]
                    if available_subjects:
                        subject = random.choice(available_subjects)

                        if subject in afternoon_only_subjects and period_type == 'morning':
                            period += 1
                            continue

                        if subject in consecutive_subjects:
                            next_period_number = f"Period {period + 1 if period < 5 else period - 4}"
                            if period % 5 != 0 and next_period_number not in schedule[day][period_type]:
                                teacher_username = next((teacher for teacher, subj in teacher_subjects.items() if subj == subject), None)
                                if teacher_username:
                                    teacher_name = teachers[teacher_username]['name']

                                    if teacher_schedules[teacher_name][day][period_type].get(period_number) is None and \
                                       teacher_schedules[teacher_name][day][period_type].get(next_period_number) is None:
                                        schedule[day][period_type][period_number] = f"{subject} ({teacher_name})"
                                        schedule[day][period_type][next_period_number] = f"{subject} ({teacher_name})"
                                        teacher_schedules[teacher_name][day][period_type][period_number] = f"{subject} ({class_name})"
                                        teacher_schedules[teacher_name][day][period_type][next_period_number] = f"{subject} ({class_name})"
                                        
                                        remaining_subjects[subject] -= 2
                                        subject_count_per_day[subject] += 2
                                        if remaining_subjects[subject] <= 0:
                                            del remaining_subjects[subject]

                                        period += 2
                                        continue
                        else:
                            teacher_username = next((teacher for teacher, subj in teacher_subjects.items() if subj == subject), None)
                            if teacher_username:
                                teacher_name = teachers[teacher_username]['name']

                                if teacher_schedules[teacher_name][day][period_type].get(period_number) is None:
                                    schedule[day][period_type][period_number] = f"{subject} ({teacher_name})"
                                    teacher_schedules[teacher_name][day][period_type][period_number] = f"{subject} ({class_name})"
                                    
                                    remaining_subjects[subject] -= 1
                                    subject_count_per_day[subject] += 1
                                    if remaining_subjects[subject] == 0:
                                        del remaining_subjects[subject]

                period += 1

    return class_schedules

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        elif username in teachers and teachers[username]['password'] == password:
            session['teacher_name'] = teachers[username]['name']
            return redirect(url_for('teacher_dashboard'))
        elif username in classes and classes[username]['password'] == password:
            session['class_name'] = classes[username]['name']
            return redirect(url_for('class_dashboard'))
        else:
            return render_template('login.html', message="Đăng nhập thất bại! Sai tài khoản hoặc mật khẩu.")
    return render_template('login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        auto_schedule(class_schedules, subject_schedule, teacher_subjects)
    selected_teacher = request.args.get('teacher')
    selected_class = request.args.get('class')
    teacher_schedule = teacher_schedules.get(selected_teacher, {})
    class_schedule = class_schedules.get(selected_class, {})
    return render_template(
        'admin_dashboard.html',
        teacher_names=list(teacher_schedules.keys()),
        class_names=list(class_schedules.keys()),
        selected_teacher=selected_teacher,
        teacher_schedule=teacher_schedule,
        selected_class=selected_class,
        class_schedule=class_schedule
    )

@app.route('/run_schedule', methods=['POST'])
def run_schedule():
    try:
        logging.info("Bắt đầu quá trình phân lịch tự động")
        global class_schedules
        class_schedules = auto_schedule(class_schedules, subject_schedule, teacher_subjects)
        logging.info("Phân lịch thành công")
        return jsonify({'status': 'success', 'message': 'Phân lịch thành công!', 'schedule': class_schedules}), 200
    except Exception as e:
        logging.error("Lỗi khi phân lịch: %s", str(e))
        return jsonify({'status': 'error', 'message': f"Có lỗi xảy ra: {str(e)}"}), 500

@app.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_name = session.get('teacher_name')
    if not teacher_name:
        return redirect(url_for('login'))
    schedule = teacher_schedules.get(teacher_name, {})
    return render_template('schedule.html', schedule=schedule, role=teacher_name)

@app.route('/class_dashboard')
def class_dashboard():
    class_name = session.get('class_name')
    if not class_name:
        return redirect(url_for('login'))
    schedule = class_schedules.get(class_name, {})
    return render_template('schedule.html', schedule=schedule, role=class_name)

@app.route('/logout')
def logout():
    session.pop('teacher_name', None)
    session.pop('class_name', None)
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
