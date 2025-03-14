import csv
import os

DATABASE_CONFIG = {
    'students': "students.csv",
    'instructors': "instructors.csv",
    'courses': "courses.csv",
    'enrollments': "enrollments.csv"
}

class DatabaseManager:
    @staticmethod
    def initialize():
        tables = {
            'students': ['student_id', 'name', 'email', 'password'],
            'instructors': ['instructor_id', 'name', 'email', 'password'],
            'courses': ['course_id', 'title', 'instructor_id'],
            'enrollments': ['student_id', 'course_id', 'grade'],
        }

        for table, headers in tables.items():
            path = DATABASE_CONFIG[table]
            if not os.path.exists(path):
                with open(path, 'w') as csvfile:
                    csvfile.write(','.join(headers) + '\n')


    @staticmethod
    def get_file_path(table_name):
        return DATABASE_CONFIG.get(table_name)

    @staticmethod
    def get_next_id(table_name):
        filename = DatabaseManager.get_file_path(table_name)
        if not os.path.exists(filename):
            return 1

        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if not rows:
                return 1
            last_id = int(rows[-1][f"{table_name[:-1]}_id"])
            return last_id + 1



    @staticmethod
    def save(table_name, obj):
        filename = DatabaseManager.get_file_path(table_name)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(obj.to_dict().values())

    @staticmethod
    def update(table_name, obj, key, value):
        filename = DatabaseManager.get_file_path(table_name)
        records = DatabaseManager.fetch_all(table_name)
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=obj.to_dict().keys())
            writer.writeheader()
            for record in records:
                if record[key] == value:
                    writer.writerow(obj.to_dict())
                else:
                    writer.writerow(record)

    @staticmethod
    def delete(table_name, key, value):
        filename = DatabaseManager.get_file_path(table_name)
        records = DatabaseManager.fetch_all(table_name)
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=records[0].keys())
            writer.writeheader()
            for record in records:
                if record[key] != value:
                    writer.writerow(record)

    @staticmethod
    def fetch_all(table_name):
        filename = DatabaseManager.get_file_path(table_name)
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)

    @staticmethod
    def filter_records(table_name, key, value):
        filename = DatabaseManager.get_file_path(table_name)
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader if row[key] == value]

    @staticmethod
    def is_user_registered(email, user_type):
        table_name = f"{user_type}s"
        filename = DatabaseManager.get_file_path(table_name)
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email:
                    return True
        return False

