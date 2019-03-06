import re
import csv

FLOAT_EXPR = r'[-+]?[0-9]*\.?[0-9]*'
STR_MATCH_KLABEL = r'\s*(?:\s*'+ FLOAT_EXPR + r'){3}\s*!\s*(\w)'
STR_MATCH_FERMI = r'^\s*E-fermi\s*:\s*(' + FLOAT_EXPR + r')'
STR_MATCH_ISPIN = r'ISPIN  =      (\d)'
STR_MATCH_KPOINT = r'and weight'

with open('OUTCAR', 'r') as fin:
    lines = fin.readlines()
with open('EIGENVAL') as fin:
    eigs_lines = fin.readlines()[5:]
with open('KPOINTS', 'r') as fin:
    k_lines = fin.readlines()[3:]

# make sure that using reciprocal in KPOINTS
assert(str.lower(k_lines[0][0]) == 'r')

prog_klabel = re.compile(STR_MATCH_KLABEL)
k_label = []
for line in k_lines[1:]:
    match = prog_klabel.search(line)
    if match:
        k_label.append(str.upper(match.groups()[0]))

k_label = [k_label[0]] + k_label[1:-1:2] + [k_label[-1]]
print(k_label)

prog_fermi = re.compile(STR_MATCH_FERMI)
prog_ispin = re.compile(STR_MATCH_ISPIN)
prog_kpt = re.compile(STR_MATCH_KPOINT)

match_line_ind = []
for i, line in enumerate(lines):
    match_fermi = prog_fermi.search(line)
    if match_fermi:
        fermi = float(match_fermi.groups()[0])
    match_ispin = prog_ispin.search(line)
    if match_ispin:
        ispin = int(match_ispin.groups()[0])
    match_kpt = prog_kpt.search(line)
    if match_kpt:
        match_line_ind.append(i)

kpoint_lines = lines[match_line_ind[0]+1:match_line_ind[-1]]

kpoints = []
for line in kpoint_lines:
    item = line.split()
    if len(item) == 4:
        kpoints.append(item[:3])

# print(kpoints, len(kpoints))

occupy, n_kpoints, n_bands = [int(x) for x in eigs_lines[0].split()]
print(("occupy", "n_kpoints", "n_bands"))
print((occupy, n_kpoints, n_bands))
print("Fermi energy")
print(fermi)
eigs_lines = eigs_lines[3:]

eigs = []
line_offset = 2
for i in range(n_kpoints):
    base_ind = i*(n_bands + line_offset)
    eigs.append([x.split() for x in eigs_lines[base_ind:base_ind+n_bands]])

# print(eigs)

labels = [""] * n_kpoints
for i, j in enumerate(range(0, n_kpoints, int(n_kpoints/(len(k_label)-1)))):
    labels[j] = k_label[i]
labels[-1] = k_label[-1]

# print(labels)

# write to CSV file
with open('band.csv', 'w') as csvFile:
    bandWriter = csv.writer(csvFile)
    bandWriter.writerow(['kx', 'ky', 'kz', 'label'] + ['band%ds%d' % (x, s) for x in range(1, n_bands+1) for s in range(1, ispin+1)])
    for i in range(n_kpoints):
        bandWriter.writerow(kpoints[i] + [labels[i]] + [float(x) - fermi for eig in eigs[i] for x in eig[1:]])

