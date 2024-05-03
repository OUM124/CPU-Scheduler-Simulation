

class Table:
    __header = []  # private class variable to store table header
    __data_rows = []  # private class variable to store table data
    __column_widths = []  # private class variable to store width of each column

    # Constructor to initialize the instance variables
    def __init__(self):
        self.__header = []
        self.__data_rows = []
        self.__column_widths = []
    
    # getter for  all atribute
    def getHeader(self):
        return self.__header
    
    def getDataRow(self):
        return self.__data_rows
    
    def getColumnWidths(self):
        return self.__column_widths

    # Method to set table header
    def setHeader(self, header):
        # check if header is list or dictionary
        if isinstance(header, list):
            self.__header = header
        elif isinstance(header, dict):
            self.__header = list(header.keys())

    # Method to add a row to the table
    def addRow(self, row):

        # If row is a dictionary, add values to the table data rows
        if isinstance(row, dict):
            if not self.__header:
                # If header is not set, set header as the keys of the dictionary
                self.__header = list(row.keys())
                self.__column_widths = [len(column) for column in self.__header]

            self.__data_rows.append(list(row.values()))
            self.__calculateColumnWidths(list(row.values()))
        
        # If row is a list, add the list as it is to the table data rows
        elif isinstance(row, list):
            if not self.__header:
                # If header is not set, set header as '-'
                self.__header = ['-' for i in row]
                self.__column_widths = [0 for i in row]

            self.__data_rows.append(row)
            self.__calculateColumnWidths(row)

        else:
            print("Error!")

    # Private method to calculate width of each column based on its data
    def __calculateColumnWidths(self, data):
        for i, cell in enumerate(data):
            width = len(str(cell))
            if width > self.__column_widths[i]:
                self.__column_widths[i] = width

    # Method to add multiple rows to the table
    def addData(self, data):

        # If data is a list containing multiple rows, add each row
        if isinstance(data, list):
            for row in data:
                self.addRow(row)

        # If data is a dictionary, add the dictionary as a row
        elif isinstance(data, dict):
            self.addRow(data)
        
        else:
            print("Error!")

    # Method to display the table
    def display(self):

        print()

        # create border horizontal
        border = '+'
        for i, width in enumerate(self.__column_widths):
            border += '-' * (width + 2) + '+'

        # Print table header
        print(border)

        print('|', end='')
        for i, column in enumerate(self.__header):
            print(' {:^{width}} |'.format(column, width=self.__column_widths[i]), end='')
        print()

        print(border)

        # Print data table rows
        for row in self.__data_rows:
            print('|', end='')
            for i, cell in enumerate(row):
                print(' {:^{width}} |'.format(cell, width=self.__column_widths[i]), end='')
            print()

        print(border)
        print()
