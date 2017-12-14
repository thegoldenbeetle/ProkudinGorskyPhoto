from skimage.io import imread, imsave, imshow
from skimage import img_as_float, img_as_ubyte
from numpy import dstack, roll, mean, clip
from sys import argv

def rolling(img, img_g):
	max_similar = 0
	for i in range(-15, 15, 1):
		newiimg = roll(img, i, 1)
		for j in range(-15, 15, 1):
			newjimg = roll(newiimg, j, 0)
			similar = (newjimg * img_g).sum()
			if (similar >= max_similar):
				max_similar = similar
				ixd = i
				jyd = j
	return max_similar, ixd, jyd
	
def shift(img, ixd, jyd):
	img = roll(img, (ixd, jyd), (1, 0))
	return img

def treatment(img, g_img):
	max_similar, ixd, jyd = rolling(img, g_img)
	print(max_similar, ixd, jyd)
	img = shift(img, ixd, jyd)
	return img

def get_gbr(img, height, width, frame):	
	g = img[int(height/3) + frame : int(2*height/3) - frame, frame : width - frame]	
	b = img[frame : int(height / 3) - frame, frame : width - frame]
	r = img[int(2*height/3) + frame : height - frame, frame : width - frame]
	return g, b, r

def get_parameters_of_image(img):
	height = img.shape[0]
	if (height % 3 != 0):
		img = img[0: height - height % 3, :]
	height, width = img.shape[0], img.shape[1]
	frame = int(0.1 * width)
	return height, width, frame
	
def color_correction(img):
	R, G, B = img.mean(axis=(0,1))
	average = (R + G + B) / 3
	rw, rg, rb = R / average, G / average, B / average
	img_out = clip((img / [rw, rg, rb]), 0 , 255)
	return img_out.astype('uint8')

def conversion(img):
	img = img_as_float(img)
	height, width, frame = get_parameters_of_image(img);
	g, b, r = get_gbr(img, height, width, frame)
	b = treatment(b, g)
	r = treatment(r, g)
	img_out = dstack((r, g, b))
	img_out = color_correction(img_as_ubyte(img_out))
	return img_out
	
for i in argv[1:]:
	img = imread(i)
	img_out = conversion(img)
	imsave('out' + i[1] + '.png', img_out)
