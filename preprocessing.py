import cv2
import os
import matplotlib.pyplot as plt

# we need to read in the data

train_path = "C:\\Users\\me\\Documents\\Object-Detection\\cityscapes_data\\train"
val_path = "C:\\Users\\me\\Documents\\Object-Detection\\cityscapes_data\\val"

image_size = 256
training_data = []
validation_data = []

def reading_in_image(path, dataset):
    for data in os.listdir(path):
        # reading in the image in by joining the path to get to the image
        image = cv2.imread(os.path.join(path, data))
        # we are resizing the image to the image_size that we set above
        image = cv2.resize(image, (image_size, image_size))
        # adding the images to the given dataset as we are later going to use these datasets in other parts of our project
        dataset.append(image)
       
        '''Image Augmentation'''

        # we are rotating the initial images by 90 degrees counterclockwise and add that to do the dataset
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        dataset(rotated_image)
        
        # we are rotating the initial images by 90 degrees clockwise and adding it to the dataset
        rotated_image_2 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        dataset(rotated_image_2)

        # doing a horizontal flip on the original image and then adding it to the dataset
        horizontally_flipped_image = cv2.flip(image, -1)
        dataset(horizontally_flipped_image)

        # doing a vertical flip on the original image and then adding it to the dataset
        vertically_flipped_image = cv2.flip(image, 0)
        dataset(vertically_flipped_image)

        # now we are creating a maxtrics that will contain all of the nessesary values to create a image translation
        # the matrix that we are creating have have these values
        # here is an example:
        #  M = [1, 0, tx
        #       0, 1, ty]
        # when there is a negative value for tx will shift the image to the left
        # positive values for tx will shift the image to the right
        # negative values for ty shifts the image up
        # positive values for ty will shift the image down
        # this matrix can do operations with 32 bits and is much faster than float64
        Matrix = np.float32([1,0,15],
                            [0,1,-10]
                            ])
        # cv2.warpAffine does the translation for us 
        # the first parameter of the function is the image, the second parameter is the maxtrix that we created
        # the third parameter is the width and height of the original image
        shifted_image = cv2.warpAffine(image, Matrix, (image.shape[0], image.shape[1]))
        dataset.append(shifted_image)

# applying the function on the training and testing sets that we have
reading_in_image(train_path, training_data)
reading_in_image(val_path, validation_data)

# length of the training data
print(len(training_data))
# length of the testing data
print(len(validation_data))
        
