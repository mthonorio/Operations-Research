#Leitura e armazenamento dos dados do arquivo
import pylab as pb
from tkinter import *
from tkinter import filedialog
import os
import sys
import io


def chooseFileName():
    root.filename =  filedialog.askopenfilename(initialdir = currentDirectory,title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    print (root.filename)

def showModel():
    result = []
    if(root.filename != ''):
        #Armazenando os dados do número de vértices, arcos e índices dos nós de origem e escoadouro
        instance_info = pb.loadtxt(root.filename, dtype = int, max_rows = 4)

        #Armazenando os dados dos arcos
        dataSet = pb.loadtxt(root.filename,dtype = int, skiprows = 4)

        #Criando um range para facilitar as operações com vértices
        vertices=[]
        verticesRange = range(instance_info[0])
        for i in verticesRange:
            vertices.insert(i, i + 1)
        print(instance_info)
        result.append(str(instance_info))
        print(dataSet)
        result.append(str(dataSet))
        print(vertices)
        result.append(str(vertices))

        #Criando um dicionário que organiza melhor o dataSet
        #edge_capacity serve para relacionar os arcos com suas respectivas capacidades
        edge_capacity = {}
        for i in range(len(dataSet)):
            edge_capacity[(dataSet[i][0], dataSet[i][1])] = dataSet[i][2]

        #Modelagem
        from docplex.mp.model import Model
        mdl = Model("Problema do Fluxo Maximo")
        #Criando ranges
        dataRange = range(instance_info[0] + 1)
        source = vertices[instance_info[2]] #No de origem
        sink = vertices[instance_info[3]] #Escoadouro

        #Criamos as variáveis Xij
        x = {(i, j): mdl.continuous_var(name="x_{0}_{1}".format(i, j)) for i in vertices for j in vertices if (i, j) in edge_capacity}
        
        mdl.print_information()

        res = str(mdl.get_statistics()).split('\n')

        result.extend(res)



        #Adicionando restrições de capacidade para cada variável Xij
        for i in vertices:
            for j in vertices:
                if (i, j) in edge_capacity:
                    mdl.add_constraint(x[i, j] <= edge_capacity[i, j])
                    print(x[i, j])
                    result.append(str(x[i, j]))
                    print(edge_capacity[i, j]) #Observe no print como as variáveis condizem com seus arcos e suas capacidades máximas
                                        # de acordo com o dict edge_capacity na terceira célula de código
                    result.append(str(edge_capacity[i, j]))                                      

        #Criando um array de nós de transbordo apenas:
        nodes = []
        j = 0
        for i in vertices:
            if i != source and i!=sink:
                nodes.insert(j, i)
                j += 1

        #Adicionando restrições de conservação de fluxo
        for i in nodes:
            mdl.add_constraint(mdl.sum(x[j, i] for j in vertices if (j, i) in edge_capacity) -
                            mdl.sum(x[i, j] for j in vertices if (i, j) in edge_capacity) == 0)

        #Criando a função objetivo
        mdl.maximize(mdl.sum(x[source, j] for j in vertices if (source, j) in edge_capacity))

        solution = mdl.solve(log_output=True)

        
        old_target = sys.stdout

    
        sys.stdout = open('solution.txt','w')


        solution.display() #printando no arquivo (que posteriormente é lido e jogado na janela do tkinter)

        sys.stdout.close()

        sys.stdout = old_target

        solution.display() #printando novamente, dessa vez no terminal


        r = open('solution.txt', 'r')

        # print("reeepeee: ")
        # print(r.read())
        # print("end r")

        #Printando o modelo
        print(mdl.export_to_string())

        info = (mdl.export_to_string()).split('\n')

        result.extend(info)

        res = str(mdl.get_statistics()).split('\n')

        result.extend(res)

        mdl.print_information()

    

        s = str(r.read()).split('\n')

        result.extend(s)

        mylist = Listbox(root, yscrollcommand = scrollbar.set,width=150,height=200)

        for line in result:
            mylist.insert(END, line)  

        mylist.pack()




    else:
        print("O caminho fornecido é inválido")

root = Tk()

root.title('PFM-version4')

scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )
root.filename = ''


root.geometry("500x500") #You want the size of the app to be 500x500
#root.resizable(0, 0) #Don't allow resizing in the x or y direction


chooseButton = Button(root,text="Escolher arquivo",command = chooseFileName)
solveButton = Button(root,text="Exibir Modelo",command = showModel)




chooseButton.pack()
solveButton.pack()


currentDirectory = os.getcwd()



root.mainloop()
