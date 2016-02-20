# Source Code for Assignment 1 of the E6895 Advanced Big Data Course For Spring 2016

Original Code Authored by: 	Maanit Mehra
Date				19th Feb, 2016

Runtime instructions:

1. Run Q2.py to generate raw html & subsequently cleaned & parsed files in Q2_files/
The folder also contains a list of urls that the program crawls in a separate file, called urlinks.txt

2. Run Q3.py (it has a runtime of 30 minutes) to scan and parse tweets from a live stream of data.
The Assignment folder contains a source set of companies stored in a file called Yahoo_symbols.csv. This file is used to parse tweets and financial quotes (in part 3) 

3. Finally, run Q4.py to extract stock information from a list of companies. Use this in turn to finally find outliers.
Finding outliers is done using pyspark functions, a python-only method, unused here, is also provided for reference.
