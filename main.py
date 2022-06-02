from line import Line
from io_example import main 
import sys

"""-------------------GLOBALS------------------------"""
hits = 0
misses = 0 
use_count = 0 


"""-------------------CONSTANTS------------------------"""
FILENAME = "/Users/sakshamarora/cs51/hw7/Q1/sample.txt" 
VERBOSITY = 2
BLOCK_SIZE = 16
NUM_LINES = [1, 2, 4, 64] # 1 for direct mapped, 2 for 2-way, 4 for 4-way, 64 for fully assoc
NUM_SETS = [64, 32, 16, 1] # 64 for direct mapped, 32 for 2-way, 16 for 4-way, 1 for fully assoc
TAG_SHIFT = [2, 1, 0, 0] # 2 for direct mapped, 1 for 2-way, 0 for 4-way, 0 for fully assoc
TAG_ZERO_INDEX = [-2, -2, -2, -1] 
MODE = 0 # 0 for direct mapped, 1 for 2-way, 2 for 4-way, 3 for fully assoc 
TAGMASKS = [int("0xfffffc00", 16), int("0xfffffe00", 16), int("0xffffff00", 16), int("0xfffffff0", 16)]
SETMASKS = [int("0x000003f0", 16), int("0x000001f0", 16), int("0x000000f0", 16), int("0x00000000", 16)]


"""-------------------HELPER FUNCTIONS------------------------"""

def compute_bits(addr):
    
    """Compute tag and set for a given address.
        :param str addr: memory address of data in hex to write to cache
        :return: (tag, set) tuple in hex
        """


    tag = hex(int(hex((TAGMASKS[MODE] & addr))[:-2], 16)) # and with tagmasks, remove trailing zeros 
    tag = int(hex(int(tag, 16) >> TAG_SHIFT[MODE]), 16) # # shift tag bits 

    if MODE == 3 :
        set = hex(0) # set is 0x0 for fully assoc
    elif MODE <3 :
        set = hex(int(hex(SETMASKS[MODE] & addr), 16)) # and with setmasks
        if len(set) > 3:
            set = hex(int(set[:-1], 16))    # remove trailing zero
        # set = int(hex(int(set, 16) >> 1), 16)


    return (tag, set)


def make_empty_cache(num_lines, block_size, num_sets): 

    """Create an empty cache.
        :param int num_lines: number of lines per set in cache
        :param int block_size: size of block in number of bytes
        :param int num_sets: number of sets in cache 
        :return : cache as a dictionary with keys as set numbers, each entry is a 
            list of Line objects of size num_lines
        """

    # create cache as a dictionary 
    cache_set = {} 

    for i in range(num_sets):
        # convert set number to hex 
        set_id = hex(i)

        # populate dictionary for each set
        block = [Line(block_size)]
        for i in range(1, num_lines):
            line = Line(block_size)
            block.append(line)

        cache_set[set_id] = block
    
    return cache_set
 

def read(addr, cache_set):

    """Read a block of memory from the cache.
        :param int addr: address for data to read from cache
        :param dict cache_set: cache dictionary to read from
        :return: Line object of read from the cache (None if cache miss)
        """

    global use_count
    (tag, set) = compute_bits(addr)
    line = None 
    for line_num in range(len(cache_set[set])):
        candidate = cache_set[set][line_num]
        if candidate.tag == tag and candidate.valid:
            line = candidate 
            use_count += 1
            line.use = use_count
            if VERBOSITY == 2:
                print("Found it in line" + hex(line_num) + "." + " Hit! Updating last_touch to " + str(line.use))
                print("-----------------------------------------------")
            break 

    
    return line

def load(addr, cache_set):

    """Load a block into the cache if miss.
        :param int addr: address for data to load to cache
        :param dict cache_set: cache dictionary to read from
        """

    global use_count 
    (tag, set) = compute_bits(addr)

    empty_line = 0
    victim_selected = 0 
    victim_set_id = set
    victim_line = 0
    victim = cache_set[victim_set_id][victim_line] 
    

    for index in range(len(cache_set[victim_set_id])):
        if cache_set[victim_set_id][index].valid == 0:
            victim_line = index
            victim = cache_set[victim_set_id][victim_line]
            victim_selected = 1
            empty_line = 1
            break
        
        
    if not victim_selected:
        for index in range(len(cache_set[victim_set_id])):
            if cache_set[victim_set_id][index].use <= victim.use:
                victim_line = index
                victim = cache_set[set][victim_line]
                victim_selected = 1

        

    if victim_selected:
            use_count += 1
            victim.use = use_count 
            victim.valid = 1
            victim.tag = tag  

            if VERBOSITY == 2: 
                if empty_line:      
                    print("Miss! Found empty line " + hex(victim_line) + "; " + "adding block there; setting last_touch to "
                        + str(victim.use))
                    print("-----------------------------------------------")
                
                else: 
                    print("Miss! Evicted line " + hex(victim_line) + "; " + "adding block there; setting last_touch to "
                        + str(victim.use))
                    print("-----------------------------------------------")
             



def print_set_status(set_num, cache_set):

    """Helper function to print set status.
        :param int set_num: set_number to specify the status of which set to print
        :param dict cache_set: cache dictionary in which set resides 
        """

    print("State of set " + set_num + ":")
    for line_index in range(len(cache_set[set_num])):
        line = cache_set[set_num][line_index]
        print("line " + hex(line_index) + " V=" + str(line.valid) +
         " tag " + hex(line.tag) + " last_touch=" + str(line.use).zfill(7))

    print("\n")

        

def summary(list_addresses):
    global hits, misses
    """Helper function to print summary, i.e num of hits, num of misses, 
        hit rate (hr) and miss rate (mr).
        :param list list_addresses: list of addresses read in from trace file FILENAME
        """

    print("-----------------------------------------------")
    n = len(list_addresses)
    print("Hits: " + str(hits) + "; " + "misses: " + str(misses) + "; " + "addresses: " + str(n))
    hit_rate = float(hits / n) 
    miss_rate = float(misses / n) 
    print(str(hit_rate) + " hr, " + str(miss_rate) + " mr")
# tag, set = compute_bits("0x22222210")
# cache(tag, set, "0x22222210")


def header(filename, MODE):
    """Helper function to print trace file information and cache paramters, i.e FILENAME,
        VERBOSITY, tagmask, setmask, mode.
        :param
        """

    modes = ["direct mapped", "2-way set associative", 
                "4-way set associative", "fully associative"]
    print(filename)
    print("verbosity = " + str(VERBOSITY))
    print("tagmask = " + hex(TAGMASKS[MODE]))
    print("setmask = " + hex(SETMASKS[MODE]))
    print(str(NUM_SETS[MODE] * NUM_LINES[MODE]) + " blocks", str(BLOCK_SIZE) + " bytes in block; " + 
            str(NUM_SETS[MODE]) + " sets, " +  str(NUM_LINES[MODE]) + " lines per set")
    print("-----------------------------------------------")

"""-------------------MAIN FUNCTIONS------------------------"""

def simulator():
    """Main function to simulate caching.
        """
    global use_count, hits, misses
    count = 0
    cache_set = make_empty_cache(num_lines=NUM_LINES[MODE], block_size=BLOCK_SIZE, num_sets=NUM_SETS[MODE])
    list_addresses = main(FILENAME)
    # print(list_addresses)
    if VERBOSITY == 2: 
        header(FILENAME, MODE)

    for addr in list_addresses:
        count += 1
        (tag, set) = compute_bits(addr)
        if VERBOSITY == 2: 
            print(str(count).zfill(7) + ": " + hex(addr) + "; looking for tag " + hex(tag) + " in set " + set + "\n") 
            print_set_status(set, cache_set)

        line = read(addr, cache_set)
        if line:
            hits += 1
        else:
            misses += 1
            load(addr, cache_set)
    
    summary(list_addresses)
        
            
"""-------------------MAIN PROGRAM------------------------"""
sys.stdout = open("direct_mapped.txt", "w")
simulator()
sys.stdout.close()

# print(compute_bits("0xbffff80c"))



