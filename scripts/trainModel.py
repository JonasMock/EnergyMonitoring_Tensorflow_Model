class TrainModel:

    # To create numpy arrays for training data
    import numpy as np
    # For filesystem interaction
    import os
    # For processing images
    import cv2
    # Create, train and save the model
    import tensorflow as tf
    # To randomize training data
    import random

    training_data = []

    __slots__ = ['rootPath', 'categories', 'img_size', 'dataAmount', 'modelOutputPath', 'epochs']

    def __init__(self, **kwargs):

        print("This is the constructor method of \""+type(self).__name__+"\" class.")
        print("The following args are necessary: ", self.__slots__,"")

        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
                pass
            except Exception as e:
                print("Can't init object.\n")
                raise Exception(e)

        print("Successfully initialized\n")

        pass


    # Extracts pixels from training data images and appends them to the array. Afterwards features and labels are stored in two arrays and returned.
    def createTrainingData(self):
    
        # Loop through categories   
        for categorie in str(getattr(self, 'categories')).split(","):

            # Path to the categorie folder
            print()
            categoriePath = self.os.path.join(getattr(self, 'rootPath'), categorie)
            # Translates categories to digits. Model can't work with strings. (Index 0 = Categorie 1. In this case categorie 1 is the digit 0)
            categorieIndex = str(getattr(self, 'categories')).split(",").index(categorie)
        
            try:
                # Loops through the images in categorie folder
                for idx, img in enumerate(self.os.listdir(categoriePath)):
            
                    # Breaks loop if max amount of training images in this categoriy is reached
                    if idx == int(getattr(self, 'dataAmount')):
                        break
            
                    # Try to read the current image in grayscale, resize it to the defined size and append it to the training data array / label array.
                    try:
                        img_array = self.cv2.imread(self.os.path.join(categoriePath,img), self.cv2.IMREAD_GRAYSCALE)
                        resized_array = self.cv2.resize(img_array, (int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))))
                        self.training_data.append([resized_array, categorieIndex])
                    except Exception as e:

                        print("Can't process image.",self.os.path.join(categoriePath,img,"\n")
                        print(e)

                        pass
                    
                    pass
            except Exception as e:

                print("Categorie folder not found.")
                print(e)
                print("\n")

                pass

            pass

        pass

        # Shuffle function randomizes the training data
        self.random.shuffle(self.training_data)
        # Two arrays fo features and labels
        featureArray = []
        labelArray = []

        # Loop trough training data
        for features, label in self.training_data:
            # Append features and labels to array
            featureArray.append(features)
            labelArray.append(label)
    
        # Create numpy array and reshape array size
        featureArray = self.np.array(featureArray).reshape(-1, int(getattr(self, 'img_size')), int(getattr(self, 'img_size')))
        labelArray = self.np.array(labelArray)
        # Normalize values (values < 1)
        featureArray = featureArray / 255

        return featureArray, labelArray



    # Create, train and save the model
    def createModel(self):
    
        # Defines model properties
        model = self.tf.keras.Sequential ([
    
            self.tf.keras.layers.Flatten(input_shape=(int(getattr(self, 'img_size')), int(getattr(self, 'img_size')))),
            self.tf.keras.layers.Dense(128, activation=self.tf.nn.relu),
            self.tf.keras.layers.Dense(10, activation=self.tf.nn.softmax)
    
        ])
    
        # Compiles the model
        model.compile(optimizer=self.tf.train.AdamOptimizer(),
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
        
        # Extracts pixels from training data images and appends them to the array. Afterwards features and labels are stored in two arrays and returned.
        features, labels = self.createTrainingData()

        # Train the model
        model.fit(features, labels, epochs = int(getattr(self, 'epochs')))
        # Save the model
        model.save(getattr(self, 'modelOutputPath'))
    
        pass

    pass