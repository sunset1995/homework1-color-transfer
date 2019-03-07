import os
import glob
import numpy as np
from PIL import Image
from scipy import fftpack
import argparse
import matplotlib.pyplot as plt
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--i_glob', required=True)
parser.add_argument('--o', required=True)
opt = parser.parse_args()
print(opt)


cnt = 0
spec_mean = None
for path in tqdm(glob.glob(opt.i_glob)):
    img = np.array(Image.open(path).convert('L')) / 255.0
    img_spec = np.log(1 + np.absolute(fftpack.fft2(img)))
    img_spec = np.roll(img_spec, [img.shape[0]//2, img.shape[1]//2], [0, 1])
    cnt += 1
    if spec_mean is None:
        spec_mean = img_spec.astype(np.float64)
    else:
        spec_mean += img_spec

spec_mean = spec_mean / cnt
spec_mean = np.clip(spec_mean, 0, spec_mean.mean() * 2.5)
plt.imshow(spec_mean, plt.cm.gist_heat)
plt.axis('off')
plt.savefig(opt.o, bbox_inches='tight')

