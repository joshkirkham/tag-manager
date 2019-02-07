"""
The log process is responsible for managing the log files in db_files/log
"""
import os
import datetime


class LogP:
    def __init__(self, log_file_path, log_file_max_size, log_buffer_size):
        """
        :param log_file_path:    path to the log file in the database
        :param log_file_max_size:   Maximum number of entries in the log file
        :param log_buffer_size: Number of log entries to buffer before writing to the log file
        """
        self.log_file_path = log_file_path
        self.log_file_max_size = log_file_max_size

        self.log_buffer_size = log_buffer_size
        self.log_buffer = []

        if not os.path.isfile(log_file_path):
            file = open(log_file_path, 'a')
            file.close()
        self.log("logP started with file " + str(self.log_file_path))




    def write_buffer_to_file(self):
        """Appends the contents of the log buffer to a file"""
        curr_contents = self.get_log_file_string()

        # Remove old log entries to make room for the buffer
        if len(curr_contents) + len(self.log_buffer) < self.log_file_max_size:
            file = open(self.log_file_path, 'a')
        else:
            file = open(self.log_file_path, 'w')
            file.writelines(curr_contents[len(self.log_buffer):])

        # Write the contents of the log buffer to the log file
        file.writelines(self.log_buffer)
        file.close()

        # Empty the log buffer
        del(self.log_buffer)
        self.log_buffer = []




    def log(self, item):
        """ Prints a string to the log file along with the currrent time"""
        self.log_buffer.append(self.get_time() + item + '\n')

        if len(self.log_buffer) >= self.log_buffer_size:
            self.write_buffer_to_file()


    def get_time(self):
        """:return: The current date and time as a string"""
        return str(datetime.datetime.now())[0:19] + " "


    def get_log_file_string(self):
        """:return: The contents of the log file as a string"""
        file = open(self.log_file_path, 'r')
        log_contents = file.readlines()
        file.close()
        return log_contents


    def close(self):
        """Store any buffered data to prepare for the process being ended"""
        self.write_buffer_to_file()

