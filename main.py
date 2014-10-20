#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)


while True:
    index = input("Please enter a number: ")
    
    indice = int(index)
    
    if indice in nodes:
        data = nodes[indice]
        output = ""
        
        for item in data:
            output += " " + str(item)
            
        print(str(indice) + " is in the list and is connected to" + output)
    else:
        print(str(indice) + " is not in the list")