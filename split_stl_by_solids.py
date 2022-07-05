import os
import re
import sys

def split_stl_by_solids(filename, create_dir=True):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    filename_splited = os.path.splitext(filename)

    directory = ''
    if create_dir:
        directory = filename + r'_solids'
        if not os.path.exists(directory):
            os.makedirs(directory)

    solid_lines = []
    for line in lines:
        match_solid_start = re.fullmatch(r'solid component([0-9_]+):solid([0-9_]+)\n', line)
        match_solid_stop = re.fullmatch(r'endsolid component([0-9_]+):solid([0-9_]+)\n', line)
        if match_solid_start is not None:
            print(match_solid_start.group(0))
            solid_lines = []
            solid_lines.append(line)
            component_no = match_solid_start.group(1)
            solid_no = match_solid_start.group(2)
        elif match_solid_stop is not None:
            solid_lines.append(line)
            solid_filename = os.path.join(directory, filename_splited[0] + '_comp{:s}'.format(component_no) + '_solid{:s}'.format(solid_no) + filename_splited[1] )
            with open(solid_filename, 'w') as file:
                for solid_line in solid_lines:
                    file.write('{:s}'.format(solid_line))
        else:
            solid_lines.append(line)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Wrong syntax! Please use: "python split_stl_by_solids.py <filename>"')
    else:
        split_stl_by_solids(sys.argv[1])
