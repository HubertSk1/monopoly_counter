# monopoly_counter
Project which connects computer vision with AI. It counts how much monopoly money is on the table. 


Hubert Skibiński  

1\.Goal: 

The goal of the project was to identify banknotes from the Monopoly game and count their amount. 

2\.Sample photos for analysis: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.001.jpeg) ![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.002.jpeg)

3\. Alghoritm Steps 

1. Loading the photo: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.003.jpeg)

2. At the beginning, subtracting a constant value (80,80,80) 

and multiplying the resulting value by 12. (clearly separated black) 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.004.jpeg)

3\.3Thresholding and obtaining contours: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.005.jpeg)

4. Filtration due to similarity to the sampler: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.006.jpeg)

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.007.png)

(In the program, I made drawings created by me in green. In order to  compare them, e.g. using  Matchshapes() I used threshold.) 

5. Filtration due to the length of the contour: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.008.jpeg)3.6Filtration due to the ratio of length and width and the area of rectangles circumscribing the contour from point 3.5. Saving the coordinates of the centers of rectangles (some rectangles were double, so I set the thickness of the line to 3 so that they merge with each other. 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.009.jpeg)

For the visualization purposes, I added rectangles with the initial image: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.010.jpeg)

3\.7 Drawing circles from the centers of rectangles designated in point 

3\.6 (this will be used as a mask and additionally means that double means will not be taken into account. 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.011.jpeg)

8. Obtaining the contour measures from point 3.7 and then 

applying the mask to the initial image: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.012.jpeg)

9. Convert to HSV and taking only the Hue layer: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.013.jpeg)

3\.10conducting a classification according to the number of pixels from the passed range in HUE. Draw surrounding circles with the color resulting from the classification into the original image: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.014.jpeg)

3\.11 Classification based on the Network and drawing circles 

with a larger radius: 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.015.jpeg)

4\.Description of the neural network: 

I created a separate database of 20 photos for learning. Using the classical algorithm, I tagged the photos( saving them to the appropriate folders). It turned out that the accuracy of the network is higher for color in the entire HSV than for Hue itself.  

The dataset had 421 items. I entered 80% of all of them in the teaching set and 20% in the validation set.   

Below I present the architecture of the model.  

Learning took very little , I didn't have to do a lot of changes and tests because the networks quickly jumped to around 100% accuracy. 

![](/for_readme/Aspose.Words.780064af-da0e-4c25-988c-5701e6dfe043.016.png)
