import matplotlib.pyplot as plt
import numpy as np 

def yearlyGraph(marks):

    subject = ['Maths','English', 'Hindi', 'Science','Social']
    index = np.arange(len(subject))
    plt.bar(index, marks,color=(0.2, 0.4, 0.6, 0.9))
    plt.xlabel('Subject', fontsize= 5)
    plt.ylabel('Marks', fontsize = 5)
    plt.xticks(index, subject, fontsize = 5, rotation = 30)
    plt.title('Marks per subject')
    return plt

def progressGraph(marks, year):
    
    subject = ['Maths','English', 'Hindi', 'Science','Social']
    index = np.arange(len(year))
    
    for no,i in enumerate(marks):
        plt.scatter(index,i, label = subject[no])
        plt.plot(index,i,alpha = 0.7)
    plt.axhline(y = 33,linestyle = '--',color = 'r', alpha = 0.5)
    plt.ylim(ymin=0)
    
    plt.xlabel('Class - Year', fontsize= 5)
    plt.ylabel('Marks', fontsize = 5)
    plt.xticks(index, year, fontsize = 5, rotation = 30)
    plt.title('Progress Graph')
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    art = []
    art.append(lgd)
    return plt,art

# def progressGraph(marks, year):
    
#     subject = ['Maths','English', 'Hindi', 'Science','Social']
#     index = np.arange(len(subject))
    
#     for no,i in enumerate(marks):
#         plt.scatter(index,i, label = year[no])
#     plt.xlabel('Subject', fontsize= 5)
#     plt.ylabel('Marks', fontsize = 5)
#     plt.xticks(index, subject, fontsize = 5, rotation = 30)
#     plt.title('Progress Graph')
#     lgd = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
#     art = []
#     art.append(lgd)
#     return plt,art
