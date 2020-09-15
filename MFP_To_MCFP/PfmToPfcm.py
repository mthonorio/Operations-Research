#Leitura do arquivo e armazenando os dados
import pylab as pb
import sys
from tkinter import *
from tkinter import filedialog
import os
import io
import sys

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
        result.extend((str(instance_info).split('\n')))
        print(dataSet)
        result.extend((str(dataSet).split('\n')))
        print(vertices)
        result.extend((str(vertices).split('\n')))

        #Modelagem
        from docplex.mp.model import Model
        mdl = Model("Problema do Fluxo de Custo Minimo")
        #Criando ranges
        dataRange = range(instance_info[0] + 1)
        source = vertices[instance_info[2]] #Nó de origem
        sink = vertices[instance_info[3]] #Escoadouro

        edge_capacity = {}
        costUnit = {}
        for i in range(len(dataSet)):
            edge_capacity[(dataSet[i][0], dataSet[i][1])] = dataSet[i][2]
            costUnit[(dataSet[i][0], dataSet[i][1])] = 0
            
        #Agora adicionamos um novo arco (origem, escoadouro) que possui um custo maior ao 		dicionário
        #Também adicionaremos o novo arco ao edge_capacity com uma capacidade "infinita", que na 		verdade é apenas um número muito grande

        smallCost = -1
        bigNumber = sys.float_info.max
        costUnit[(sink, source)] = smallCost
        edge_capacity[(sink, source)] = bigNumber

        #Criamos um dicionário demanda, que relaciona cada nó a sua demanda(bi = 0)
        demand = {}
        for i in vertices:
            demand[i] = 0
                
        print(demand)
        result.extend((str(demand).split('\n')))

        #Modelagem
        #Criando variáveis Xij para cada arco (i, j)
        x = {(i, j): mdl.continuous_var(name="x_{0}_{1}".format(i, j)) for i in vertices for j in vertices if (i, j) in edge_capacity}
        mdl.print_information()
        print(x)

        result.extend((str(x).split('\n')))

        #Adicionando restrições de conservação de fluxo (no pfcm, restrições que envolvem demanda)
        for i in vertices:
            mdl.add_constraint(mdl.sum(x[j, i] for j in vertices if (j, i) in edge_capacity) -
                            mdl.sum(x[i, j] for j in vertices if (i, j) in edge_capacity) == demand[i])

        minimumFlow = {}
        for i in vertices:
            for j in vertices:
                if (i, j) in edge_capacity:
                    minimumFlow[i, j] = 0
        print(minimumFlow)

        #Adicionando restrições de fluxo máximo e fluxo mínimo
        for i in vertices:
            for j in vertices:
                if (i, j) in edge_capacity:
                    mdl.add_constraint(x[i, j] >= minimumFlow[i, j])
                    mdl.add_constraint(x[i, j] <= edge_capacity[i, j])

        #Criando a função objetivo
        mdl.minimize(mdl.sum(costUnit[i, j] * x[i, j] for i in vertices for j in vertices if (i, j) in costUnit))

        print(mdl.export_to_string())

        result.extend((str(mdl.export_to_string()).split('\n')))

        solution = mdl.solve(log_output=True)

        old_target = sys.stdout
        sys.stdout = open('solution2.txt', 'w') 
        
        solution.display()

        sys.stdout.close()
        sys.stdout = old_target

        r = open('solution2.txt','r')

        contentSolution = str(r.read()).split('\n')


        contentSolutionString= '\n'.join(contentSolution)
        
        print(contentSolutionString)

        

        result.extend(contentSolution)        

        mylist = Listbox(root, yscrollcommand = scrollbar.set,width=150,height=200)

        for line in result:
            mylist.insert(END, line)  

        mylist.pack()

def chooseFileName():
    root.filename =  filedialog.askopenfilename(initialdir = currentDirectory,title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    print (root.filename)



root = Tk()

root.title('PfmToPfcm-version2')

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




