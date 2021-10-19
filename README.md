# Displayer

Basic Concept

This is a prototype of a tool intended to help teachers and students.
The basic idea is to continually display what a teacher says, displaying spoken keywords along with images downloaded via Google (or ahead of time), so a student gets extra feedback on what a teacher is talking about (how a word is spelled, how a concept is visualized) without needing to manually make and control slides. Words and images could be shown on each student's monitor or on a large screen. 

Content (requirements, files)

Requirements: Python 2, ROS for speech recognition (CMU Pocketsphinx), OpenCV to show images.
Files:
aimas.py is the main file to run.
E.g., "rosrun hpctools aimas.py" (if hpctools is what you have called your package)
downloadImage.py is a helper file, based on code written by Hardik Vasa (Copyright (c) 2015, MIT license--see the file for details.)

(Note: The author's code is provided here as is: it was written using the author's setup described above for research purposes; the author cannot help with getting it to work on the reader's system.)

Licenses

As noted, downloadImage.py is based on code written by Hardik Vasa (Copyright (c) 2015, MIT license--see the file for details.)
For this author's (Martin Cooney's) code, the MIT license applies:

Copyright 2017 Martin Cooney

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated dataset and documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.