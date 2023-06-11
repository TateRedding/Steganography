# Steganography

This is my first complete programming propject of my own creation from late 2019. I am commiting it to GitHub now, in 2023, in an effort to showcase my ability to write code in Python, even though my skills have improved greatly over the past few years.

This project is wirtten entirely in Python 3 and utilizes the Pillow (PIL Fork) library for image manipulation, and GTK+ 3 library to create the user interface.

Essentially what this program will do is hide encode a text file into an image file, or decode the text from an image.
It does this by converting the text file to binary, and then encoding that binary string into the last digit of the RGB values of each pixel of the image, by changing it to an even or odd value.
For example: in the case of the letter 'A' with an 8-bit binary code of 01000010, let's say the three pixels of the image are white, with the R, G, and B values all being equal to 255.
Starting with the top left most pixel, this will change the RGB values to 254, 255, 254 for the first pixel, 254, 254, 254 for the next one, and 255, 254, ??? for the last (with the ??? representing the first bit of whatever character came after the 'A'' for this example).
If the program gets to the end of the text, but there are still pixels to encode, the program will convert all the value to even numbers, representing '0's, and the decoded will know to strip all of the NUL characters at the end of the message.

When changing the last digit of a pixels red, green, or blue value by only a difference of 1, the difference is physically impossible to be noticed by the human eye, effectively hiding the message within the image, and so only someone who has the resulting image, knows there's a hidden code, and also has access to this program would be able to recieve the message.
