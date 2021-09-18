import shutil
import os

def modify_geo(out_file_name, shape_name):
    # Modify the geo file generated by FreeCAD according to my needs.
    # out_file_name: Name of the final geo file.
    # shape_name: Name of the shape generated with FreeCAD.

    # Current directory.
    current_dir = os.getcwd()
    current_dir = current_dir + '/'

    # FreeCAD generates the geo file in /tmp.
    # Copy the geo file from /tmp to the current directory.
    shutil.copyfile('/tmp/shape2mesh.geo', current_dir + out_file_name + '.geo.copy')

    # Copy the brep file from /tmp to the current directory.
    brep = '/tmp/' + shape_name + '_Geometry.brep'
    shutil.copyfile(brep, current_dir + out_file_name + '.brep')

    # Remove blank lines in geo file.
    with open(current_dir + out_file_name + '.geo.copy', 'r') as inFile, open(out_file_name + '.geo', 'w') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)

    # Remove temporary geo file.
    os.remove(out_file_name + '.geo.copy')

    # Open the geo file to read.
    with open(out_file_name + '.geo', 'r') as file :
        filedata = file.readlines()

    # Remove unnecessary lines.
    filedata = [line for line in filedata if not 'SaveAll' in line]
    filedata = [line for line in filedata if not 'Save' in line]
    filedata = [line for line in filedata if not 'Mesh  3' in line]
    filedata = [line for line in filedata if not 'Coherence' in line]
    filedata = [line for line in filedata if not 'Mesh.CharacteristicLengthMin' in line]
    filedata = [line for line in filedata if not 'Mesh.CharacteristicLengthMax' in line]
    filedata = [line for line in filedata if not 'Mesh.Optimize' in line]
    filedata = [line for line in filedata if not 'Mesh.OptimizeNetgen' in line]
    filedata = [line for line in filedata if not 'Mesh.High' in line]
    filedata = [line for line in filedata if not 'Geometry.Tolerance' in line]
    filedata = [line for line in filedata if not '//' in line]

    # These are replacements for certain parameters and also additions. For example, I want Mesh.Format to be specifically 1.
    for i, line in enumerate(filedata):
        if 'Mesh.Format' in line:
            filedata[i] = 'Mesh.Format = 1;\n'
        if 'Mesh.Algorithm =' in line:
            filedata[i] = 'Mesh.Algorithm = 1;\n'
        if 'Mesh.Algorithm3D =' in line:
            filedata[i] = 'Mesh.Algorithm3D = 10;\n'
        if 'ElementOrder' in line:
            filedata[i] = 'Mesh.ElementOrder = 1;\n'
            filedata[i-1] = filedata[i-1] + '\n'
        if 'Save' in line:
            filedata[i] =  "Save \"" + out_file_name + ".msh\";"
        if 'Merge' in line:
            filedata[i] =  "Merge \"" + out_file_name + ".brep\";\n\n"
        if 'mg_wall' in line:
            import re
            regex = r"\{(.*?)\}"
            matches = re.findall(regex, line, re.MULTILINE | re.DOTALL)
            filedata[i] = filedata[i].replace("\"mg_wall\"", "1")
        if 'mg_symmetry' in line:
            filedata[i] = filedata[i].replace("\"mg_symmetry\"", "12")
        if 'mg_farfield' in line:
            filedata[i] = filedata[i].replace("\"mg_farfield\"", "9")
        if 'mg_interog' in line:
            filedata[i] = filedata[i].replace("\"mg_interog\"", "11")
        if 'mg_volume' in line:
            filedata[i] = filedata[i].replace("\"mg_volume\"", "4")

    # Add custom parameters to the file.
    filedata.append('Mesh.MshFileVersion = 2.2;\n')
    filedata.append('Mesh.MeshSizeExtendFromBoundary = 0;\n')
    filedata.append('Mesh.RandomFactor = 1e-6;\n\n')
    filedata.append('lc = 10;\n')
    filedata.append('Field[1] = Distance;\n')
    filedata.append('Field[1].SurfacesList = {' + matches[0] + '};\n')
    filedata.append('Field[1].NumPointsPerCurve = 200;\n')
    filedata.append('Field[2] = MathEval;\n')
    filedata.append('Field[2].F = Sprintf("F1/5 + %g", lc);\n')
    filedata.append('Background Field = 2;\n')

    # Write all of the above to the output file.
    with open(out_file_name + '.geo', 'w') as file:
        for line in filedata:
            file.write(line)
