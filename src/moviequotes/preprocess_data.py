# -*- coding: utf-8 -*-

def main():
    fin = open("../../data/moviequotes/moviequotes.memorable_nonmemorable_pairs.txt", 'rb')
    fout = open("../../data/moviequotes/moviequotes.txt", 'wb')
    line_num = 0
    mem_line = None
    nonmem_line = None
    for line in fin:
        line = line.strip()
        if line_num == 1:
            mem_line = line
        if line_num == 3:
            nonmem_line = line[line.index(" ")+1:]
        if len(line) == 0:
            fout.write("%d\t%s\n" % (1, mem_line))
            fout.write("%d\t%s\n" % (0, nonmem_line))
            line_num = 0
            mem_line = None
            nonmem_line = None
        else:
            line_num += 1
    fin.close()
    fout.flush()
    fout.close()
    
if __name__ == "__main__":
    """ Convert Cornell data into easy to read tabular format """
    main()
