I know the layout for this readme isn't great I am sorry


Should work but will be changing some code in the near future.
file to run is ImageManipulation.py

HOW TO USE

1. On running a file explorer will be opened please select the image you want analysed 

2. The image will be displayed for you to crop.
   - Crop the image getting as much noise out of the image as you can (please crop out sides of gel etc) (to crop just draw a rectangle,
    a rectangle wont be displayed on the image until you have let go of the mouse)
   - The rectangle you have drawn will be displayed to you press "y" if you are happy with the crop or "r" if you want another go
  
3. The cropped image will then be shown just press any key

4. The binary image will then be displayed with circles drawn arround the dna spots.

    - press "e" to edit and double click any circles you want to get rid of
  
    - The best way to have it is the first cricle is on the first point on the lane (no circles before it) and the last cirlce is on the 
   last point on the lane.
      
    - Also if there is one circle on its own it will crash please remove this (the line can get added in later)
    - press "q" to exit edit
  
5. The lines drawn on the image will then be displayed
    
    - Now you will be in the edit stage you can press "d" to enter delete mode or "a" to enter add mode.
    - If you are in delete mode, double click a line and it will be removed.
    - If you are in add mode click and drag to draw a point between two dna points
    - If you are in either delete or add mode press "e" to go back to edit mode (e.g. if you need to switch between add and delete you have to press "e" first).
    - If you are in the base edit mode and you are happy with the lines press "q" to continue.
  
6. The image will be displayed again 
    
    - Press "q" to run the analysis and just save the data to a textfile
    - Press "g" if you want the data to be saved in a textfile and the data to be graphed for each lane

7. Type the what you want the file to be called

    - GO INTO filewriter.py IN ORDER TO CHANGE FILE PATH 

8. The program will finish and the file will contain the cell breakdown
  
