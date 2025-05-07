from skimage.morphology import medial_axis, skeletonize
from skimage.util import invert
from skimage import img_as_bool, io, color, morphology
import matplotlib.pyplot as plt


image = img_as_bool(color.rgb2gray(io.imread('bennys_maze.jpeg')))
                    
# Generate the data
# image = data.binary_image(200, blob_size_fraction=0.2, volume_fraction=0.35, rng=1)

# Compute the medial axis (skeleton) and the distance transform
skel, distance = medial_axis(image, return_distance=True)


print('skel', skel)

# Compare with other skeletonization algorithms
skeleton = skeletonize(image)
skeleton_lee = skeletonize(image, method='lee')

# Distance to the background for pixels of the skeleton
dist_on_skel =skel

fig, ax = plt.subplots(1, 1, figsize=(8, 8), sharex=True, sharey=True)

# ax.imshow(image, cmap=plt.cm.gray)
# ax.set_title('original')
# ax.axis('off')

ax.imshow(dist_on_skel)
ax.contour(image, [0.5], colors='w')
ax.set_title('medial_axis')
ax.axis('off')

fig.tight_layout()
plt.show()