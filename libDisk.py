from os import *
from stat import *

BLOCKSIZE = 256

'''
This function opens a regular UNIX file and designates the first nBytes of 
it as space for the emulated disk. nBytes should be a number that is evenly 
divisible by the block size. If nBytes > 0 and there is already a file by the 
given filename, that disk is resized to nBytes, and that file's contents may 
be overwritten. If nBytes is 0, an existing disk is opened, and should not be 
overwritten.  There  is  no  requirement  to  maintain  integrity  of  any  content 
beyond nBytes. Errors must be returned for any other failures, as defined by 
your own error code system. 
'''
def openDisk(filename, nBytes):
    file = -1

    if nBytes < 0:
        return file
    elif not nBytes:
        file = open(filename, O_RDWR)
    else:
        file = open(filename, O_CREAT | O_RDWR, S_IRWXU | S_IRWXG | S_IRWXO)
        lseek(file, 0, SEEK_SET)
        lseek(file, nBytes, SEEK_SET)
        write(file, "\n", 1)
    
    return file



'''
readBlock() reads an entire block of BLOCKSIZE bytes from the open disk 
(identified by 'disk') and copies the result into a local buffer (must be at 
least of BLOCKSIZE bytes). The bNum is a logical block number, which must be 
translated into a byte offset within the disk. The translation from logical to 
physical block is straightforward: bNum=0 is the very first byte of the file. 
bNum=1 is BLOCKSIZE bytes into the disk, bNum=n is n*BLOCKSIZE bytes into the 
disk.  On  success,  it  returns  0.  Errors  must  be  returned  if 'disk'  is  not 
available (i.e. hasn't been opened) or for any other failures, as defined by 
your own error code system.
'''
def readBlock(disk: int, bNum: int, block):
    """_summary_

    Args:
        disk (int): an entire block of BLOCKSIZE bytes from the open disk
        bNum (int): a logical block number, which must be translated into a byte offset within the disk
        block (_type_): 

    Returns:
        _type_: _description_
    """
    if lseek(disk, 0, SEEK_SET) < 0 or bNum < 0:
        return -1
    
    lseek(disk, bNum*BLOCKSIZE, SEEK_SET)
    read(disk, block, BLOCKSIZE)

    return 0

def writeBlock(disk, bNum, block):
    if lseek(disk, 0, SEEK_SET) < 0 or bNum < 0:
        return -1
    
    lseek(disk, bNum*BLOCKSIZE, SEEK_SET)
    write(disk, block, BLOCKSIZE)

    return 0

def closeDisk(disk):
    if lseek(disk, 0, SEEK_SET) < 0 or disk < 0:
        return -1
    
    close(disk)
    return 0