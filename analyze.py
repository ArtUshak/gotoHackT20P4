import pandas
import numpy
import matplotlib as plt

data_filename = 'data.csv'

def load_structure(course_id):
    return pandas.read_csv('../data_stepic/course-' + str(course_id) + '-structure.csv')

def load_events(course_id):
    return pandas.read_csv('../data_stepic/course-' + str(course_id) + '-events.csv')

events = load_events(7)
