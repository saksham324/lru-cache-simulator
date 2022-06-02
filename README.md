# lru-cache-simulator
This program was made to simulate an LRU (Least Recently Used) Cache in Python. 

The program keeps track of the **blocks** and the **sets**. In each **block**, the program tracks the **tag** and **valid** bits to keep track which addresses are currently cached. When a new address request is received, the program determines if that request was a hit or a miss——and if a miss, then it brings in the data and writes it into the cache using the LRU principle and updates the cache meta-data appropriately. 

The program simulates four approaches to caching : 
* `direct-mapped` 
* `2-way set associative `
* `4-way set associative `
* `fully associative` 
  




