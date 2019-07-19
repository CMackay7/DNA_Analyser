Should work but will be changing some code in the near future.
file to run is ImageManipulation.py

HOW TO USE
1.On running a file explorer will be opened please select the image you want analysed 
2.The image will be displayed for you to crop
  a.Crop the image getting as much noise out of the image as you can (please crop out sides of gel etc) (to crop just draw a rectangle,
     a rectangle wont be displayed on the image until you have let go of the mouse)
  b.The rectangle you have drawn will be displayed to you press "y" if you are happy with the crop or "r" if you want another go
  
3. The cropped image will then be shown just press any key
4. The binary image will then be displayed with circles drawn arround the dna spots.
  a. press "e" to edit and double click any circles you want to get rid of
  b. The best way to have it is the first cricle is on the first point on the lane (no circles before it) and the last cirlce is on the 
      last point on the lane.
  c. also if there is one circle on its own it will crash please remove this (the line can get added in later)
  d. press "q" to exit edit
  
5. The lines drawn on the image will then be displayed
  a.  press "e" and double click a line if it needs to be removed
  b. press "q" to exit edit
  
6. The lines will be shown again
  a.click hold and draw in order to draw new lines between the dna points (please draw from first to last with one line)
  b. press any key to exit
  
7. The image will be displayed again press any key to continue
8.Type the what you want the file to be called

GO INTO filewriter.py IN ORDER TO CHANGE FILE PATH 
9.The program will finish and the file will contain the cell breakdown
  
