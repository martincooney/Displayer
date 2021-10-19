#!/usr/bin/env python
import rospy
import numpy as np
import cv2
from subprocess import call
import sys
from std_msgs.msg import String
import cv2.cv as cv
import os

class martin_aimas_interface:
	def __init__(self):
		self.speechRecognitionFlag = True 
		self.subSpeech = rospy.Subscriber('/recognizer/output', String, self.talkback)

		self.r=rospy.Rate(10)
		self.r.sleep()

		self.windowHeight=1000
		self.windowWidth=1024
		self.current_screen_image = np.zeros((self.windowHeight, self.windowWidth, 3), dtype=np.uint8)

	def getImage(self, data):
		self.r.sleep()

		print "look up keyword" #write the key word to a file and system call a helper program to download images
		outputFileName= '/home/turtlebot/ros_ws/src/hpc/my_keyword.txt'      #CHANGE this depending on where you put your files
		keywordFile=open(outputFileName, 'w')
		lineToWrite= data
		keywordFile.write(lineToWrite)
		keywordFile.close()
		call("python /home/turtlebot/ros_ws/src/hpc/src/downloadImage.py", shell=True) #CHANGE this depending on where you put your files
	
	def talkback(self, data):
		print data.data
		self.r.sleep()
		if(self.speechRecognitionFlag == False):
			print "I heard something but am ignoring it, since the flag is set to False"
		else:
			print "I heard:", data.data

			#remove small words and recombine search string
			myWords= data.data.split()
			myWordsRefined=[]
			for wordIndex in range(len(myWords)):
				if (myWords[wordIndex] != "is") and (myWords[wordIndex] != "the") and (myWords[wordIndex] != "my") and (myWords[wordIndex] != "this") and (myWords[wordIndex] != "to") and (myWords[wordIndex] != "for"):
					myWordsRefined.append(myWords[wordIndex])
			newSearchString = ' '.join(myWordsRefined)


			if(len(newSearchString)>1):
				self.getImage(newSearchString) #important, this calls the actual search

				#check that we actually received something
				myDirectory = '/home/turtlebot/ros_ws/src/hpc/images/%s' % newSearchString #CHANGE this depending on where you put your files
				myFiles = os.listdir(myDirectory)
				if(len(myFiles)==0):
					print "Failed. It looks like no files were downloaded"
				else:
					#if we got some files, try read the first	
					inputFileName= '/home/turtlebot/ros_ws/src/hpc/images/%s/%s' % (newSearchString, myFiles[0]) #CHANGE this depending on where you put your files
					img = cv2.imread(inputFileName)
					if img is not None:
						cv2.putText(img, data.data, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 4)  
						self.current_screen_image = cv2.resize(img, (1000, 1024)) 
					else:
						print "Failed to read image."

			else:
				print "I didn't find a nice word to look up."

def main():
	rospy.init_node('hpcaimas', anonymous=True)

	my_aimas = martin_aimas_interface()

	cv2.namedWindow("aimas_screen",  cv2.WINDOW_NORMAL)
	cv2.imshow("aimas_screen", my_aimas.current_screen_image)
	cv2.waitKey(100)

	while True:

		my_aimas.r.sleep()
		cv2.imshow("aimas_screen", my_aimas.current_screen_image)
		key= cv2.waitKey(10) & 0xFF
		if(key== ord("q")): 
			break

	cv2.destroyAllWindows()


if __name__== '__main__':

    	print '-------------------------------------'
    	print '-            AIMAS                  -'
    	print '-   DEC 2017, HH, Martin Cooney     -'
    	print '-------------------------------------'

	try:
		main()
	except rospy.ROSInterruptException:
		pass
	finally:
		pass



