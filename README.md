# lru-cache-simulator
This program was made to simulate an LRU (Least Recently Used) Cache in Python. 

The program keeps track of the **blocks** and the **sets**. In each **block**, the program tracks the **tag** and **valid** bits to keep track which addresses are currently cached. When a new address request is received, the program determines if that request was a hit or a miss——and if a miss, then it brings in the data and writes it into the cache using the LRU principle and updates the cache meta-data appropriately. 

The program simulates four approaches to caching : 
* `direct-mapped` 
* `2-way set associative `
* `4-way set associative `
* `fully associative` 
  
Disclaimer : This program was made as a class project for COSC 51 : Computer Architecture at Dartmouth College during Spring 2022. If you are currently enrolled in this class, or planning to be kindly refrain from using this repository in any way. [Link to the Dartmouth Honor Principle](https://student-affairs.dartmouth.edu/policy/academic-honor-principle)





