import os

def make_table(grid, header=True):
    cell_width = [2 + max([len(str(row[i])) for row in grid]) for i, val in enumerate(grid[0])]
    filled = [[' '+str(val).ljust(width-1) for width, val in zip(cell_width, row)] for row in grid]
    rst = '\t+' + '+'.join(['-'*width for width in cell_width]) + '+\n'
    for i, row in enumerate(filled):
        rst += '\t|' + '|'.join([val for val in row]) + '|\n'
        if i == 0 and header:
            rst += '\t+' + '+'.join(['='*width for width in cell_width]) + '+\n'
        else:
            rst += '\t+' + '+'.join(['-'*width for width in cell_width]) + '+\n'

    return rst


def fits_info_table(info):
    info.insert(0, ('No.', 'Name', 'Type', 'Cards', 'Dimensions', 'Format', ''))
    return make_table([row[:-1] for row in info])

def fits_header_table(header, keys):
    table = [[key, header[key], header.comments[key]]for key in keys]
    table.insert(0, ['Key', 'Value', 'Comments'])
    return make_table(table)

class ReportChapter(object):

    def __init__(self, title):
        self.title = title
        self.content = ''
        self.add_section(title)

    def add_section(self, title):
        self.content += title+'\n'
        self.content += '='*len(title)+'\n\n'

    def add_subsection(self, title):
        self.content += title+'\n'
        self.content += '-'*len(title)+'\n\n'

    def add_table(self, table_title, rows):
        self.content += ".. table:: "+table_title+'\n\n'
        self.content += make_table(rows)
        self.content += '\n'

    def add_text(self, content, extra_newline=True):
        self.content += content+'\n'
        if extra_newline:
            self.content += '\n'

    def add_equation(self, equation, label=None):
        self.content += ".. math::"+'\n'
        if label:
            self.content += '\t'+":label: "+label+'\n'

        self.content += '\n\t'+equation+'\n\n'


    def print_chapter(self):
        print(self.content)

    def write(self, output_file):
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(output_file, 'w') as f:
            f.write(self.content)
