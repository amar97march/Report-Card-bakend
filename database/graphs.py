import matplotlib.pyplot as plt
import numpy as np 

def yearlyGraph(subject, marks):

    index = np.arange(len(label))
    plt.bar(index, marks)
    plt.xlabel('Subject', fontsize= 5)
    plt.ylabel('Marks', fontsize = 5)
    plt.xticks(index, subject, fontsize = 5, rotation = 30)
    plt.title('Marks per subject')
    plt.savefig('graph.png')