import sys
import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) is not 3:
    print("Usage: python genBand.py ymin ymax")
    sys.exit(-1)
try:
    ylim = (float(sys.argv[1]), float(sys.argv[2]))
except:
    print("(ymin, ymax) is not valid, use default (-3, 2)")
    ylim = (-3, 2)

data = pd.read_csv('band.csv')

k_distance_diff = pd.np.sqrt(data.kx.diff()**2 + data.ky.diff()**2 + data.kz.diff()**2)
k_distance_diff[0] = 0.0
pathcoord = k_distance_diff.cumsum()
data = data[data.columns[3:]].assign(pathcoord = pathcoord)

label_pts = []
label_names = []
for i, label in enumerate(data.label):
    if type(label) is str:
        label_pts.append(data.pathcoord[i])
        if label == 'G':
            label = "\Gamma"
        label_names.append("$\mathrm{" + label + '}$')

data_with_pathcoord_index = data.set_index('pathcoord').reset_index()

ax = data.plot(x='pathcoord', y=data_with_pathcoord_index.columns[2:], legend=False, ylim=ylim)

xlim = ax.get_xlim()
ax.get_xaxis().set_ticks([])
plt.xlabel("")
plt.ylabel("Energy(eV)")
plt.xticks(label_pts, label_names)

plt.hlines(y = 0, xmin=xlim[0], xmax=xlim[1], linestyles='dashed')
plt.vlines(x = label_pts, ymin=ylim[0], ymax=ylim[1])

plt.show()
