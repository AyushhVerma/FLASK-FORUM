# import cv2
from PIL import Image
path = input('Enter image location.')

image = cv2.imread(path)

# cv2.imshow(image)

image = Image.read(path)

# cv2.waitKey(0)

# cv2.deleteAllWindows()

size = image.size

print(size)
