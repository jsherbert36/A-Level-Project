from matplotlib import pyplot as plt
import os,sys,json

def input_list(name = ''):
    finish = False
    while finish == False:
        if name == '':
            file = input("Please enter the input file name i.e input.json: ")
        else:
            file = str(name)
        try:
            f = open(os.path.join(sys.path[0],file),"rt")
            finish = True
        except FileNotFoundError:
            print('File not found - try again')
            name = ''
    return (json.load(f))
    f.close()

generation_scores = input_list("score_list.json")
plt.plot(generation_scores)
plt.title('Progress of NEAT Algorithm')
plt.ylabel('Best Score')
plt.xlabel('Generation')
plt.xticks([i for i in range(0,len(generation_scores),(len(generation_scores)//15))])
plt.show()