import matplotlib.pyplot as plt
import numpy as np 

def yearlyGraph(marks):

    subject = ['Maths','English', 'Hindi', 'Science','Social']
    print(marks)
    index = np.arange(len(subject))
    plt.bar(index, marks,color=(0.2, 0.4, 0.6, 0.9))
    plt.xlabel('Subject', fontsize= 5)
    plt.ylabel('Marks', fontsize = 5)
    plt.xticks(index, subject, fontsize = 5, rotation = 30)
    plt.title('Marks per subject')
    plt.savefig('media/graph.jpg',transparent = True,dpi = 300)    