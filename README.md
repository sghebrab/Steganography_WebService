# Steganography_WebService
A self-hosted website that lets you hide messages inside pictures without altering them in a perceivable way.

This is a really simple website that lets you write text inside pictures.  
The main idea relies on substituting the least significant bit of a blue pixel with a bit of a UTF-8 character.  
To make an example, let's say that the first blue pixel has value 219, i.e. 11011011 in binary. If the character to be written is "a", whose UTF-8 encoding is 01100001, then simply substitute the last binary digit of the pixel with a 0.  
UTF-8 characters can take up to 4 bytes, so the amount of text a picture can hold is bounded by this constraint. If each encoded character takes up 4 bytes, then the maximum lenght for the message is height*width/32.

The main.py file heavily relies on the steganography.py file that I personally wrote a while ago. This file contains functions to convert text into bytes and viceversa, as well as functions to write/read a message to/from a picture.
