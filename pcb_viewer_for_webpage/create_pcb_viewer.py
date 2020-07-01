

##
# @file
# @section description
# Imports svg files exported from GerberV 2.7 and assembles a webpage for
# documenting the pcb with the ability to turn layers on and off with the
# toggling of a checkbox


##
# list to build up with html 5.1 code with each \"readable\" line as the elements to be written to a file one list element at a time.
tags = ["<!DOCTYPE html>", "<html>", "<head>", "<style>", ".controls{", "width: 20%;", "float: left;", "text-align: right;", "}", ".viewport{", "width: 75%;", "zoom: 1.0", "}", "svg{","background-color: #212121;", "margin: 2.4em;", "}", "</style>", "</head>", "<body onload=\"setDisplay(); zoomReset()\">", "<section class=\"controls\">"]



##
# list holding the names of the .svg files to bring into the webpage, read from the file filenames.txt
layerNames = []
with open("filenames.txt", "r") as fromFile:
    for line in fromFile:
        layerNames.append(line[0:-1])



# put in the checkboxes to display the layers
for layer in layerNames:
    tags.append("<p><input type=\"checkbox\" onchange=\"Display('" + layer[0:-4] + "')\"  checked=\"checked\">" + layer[0:-4] + "</p>")

tags.append("<p><button onclick=\"zoomIn()\">Zoom In</button></p>")
tags.append("<p><button onclick=\"zoomOut()\">Zoom Out</button></p>")
tags.append("<p><button onclick=\"zoomReset()\">Reset Zoom</button></p>")
tags.append("</section>")
tags.append("<section class=\"viewport\" id=\"viewport\">")



##
# boolean value to control when it starts and stops reading from the .svg files
isReading = False
for layer in layerNames:
    with open(layer, "r") as fromFile:
        for line in fromFile:
            if line.startswith("<svg"):
                isReading = True
                if layer == "board_outline.svg":
                    tags.append(line)
            if isReading == True and line.startswith("</svg"):
                isReading = False
            elif isReading == True and line.startswith("<g"):
                tags.append("<g id=\"" + layer[0:-4] + "\">")
            elif isReading == True and line.startswith("<path"):
                tags.append(line)
        tags.append("</g>")
tags.append("</svg>")



# finish out the html with a script and closing tags
tags.append("</section>")
tags.append("<script>")
tags.append("function setDisplay(){")
tags.append("let g = document.getElementsByTagName('G');")
tags.append("for(let i = 0; i < g.length; i++){")
tags.append("g[i].style.display = \"none\";")
tags.append("Display(g[i].id);")
tags.append("}")
tags.append("}//end setDisplay()")
tags.append("function Display(layer){")
tags.append("if(document.getElementById(layer).style.display == \"none\"){")
tags.append("document.getElementById(layer).style.display = \"block\";")
tags.append("}")
tags.append("else{")
tags.append("document.getElementById(layer).style.display = \"none\";")
tags.append("}")
tags.append("}//end Display()")
tags.append("function zoomIn(){")
tags.append("pcb = document.getElementById('viewport');")
tags.append("if(pcb.style.zoom < 8.0){")
tags.append("pcb.style.zoom *= 1.3;")
tags.append("}")
tags.append("}//end zoomIn()")
tags.append("function zoomOut(){")
tags.append("pcb = document.getElementById('viewport');")
tags.append("if(pcb.style.zoom > 0.3){")
tags.append("pcb.style.zoom *= 0.7;")
tags.append("}")
tags.append("}//end zoomIn()")
tags.append("function zoomReset(){")
tags.append("document.getElementById('viewport').style.zoom = 1.0;")
tags.append("}//end zoomIn()")
tags.append("</script>")
tags.append("</body>")
tags.append("</html>")



##
# File handler to write the elements in the tags list to the file pcb.html. This file will likely need renamed to go into particular projects, or the code can be embedded or copied and pasted into the webpage it actually goes in.
toFile = open("pcb.html", "w")
for tag in tags:
    toFile.write(tag)
    toFile.write("\n")
toFile.close()



































#           WHITE SPACE FOR SCROLLING           #
