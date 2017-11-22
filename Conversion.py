from skimage.io import imread, imsave, imshow
from skimage import img_as_float, img_as_ubyte
from numpy import dstack, roll
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
	height = img.shape[0]
	width = img.shape[1]
	frame = int(0.1 * width)
	return height, width, frame
	

img = img_as_float(imread(argv[1]))
height, width, frame = get_parameters_of_image(img);
g, b, r = get_gbr(img, height, width, frame)
b = treatment(b, g)
r = treatment(r, g)
imsave('out' + argv[1][1] + '.png', dstack((r, g, b)))
