

##
# @section description
# Imports svg files exported from GerberV 2.7 and assembles a webpage for
# documenting the pcb with the ability to turn layers on and off with the
# toggling of a checkbox


# write html file up to the start of the body
tags = ["<!DOCTYPE html>", "<html>", "<head>", "<style>", ".controls{", "width: 20%;", "float: left;", "text-align: right;", "}", ".controls button{", "display: block;", "}", ".viewport{", "width: 75%;", "}" "svg{", "background-color: #212121;", "margin: 2.4em;", "}", "</style>", "</head>", "<body>", "<section class=\"controls\">"]



# get the names of the layers in the pcb
layerNames = []
with open("filenames.txt", "r") as fromFile:
    for line in fromFile:
        layerNames.append(line[0:-1])



# put in the checkboxes to display the layers
for layer in layerNames:
    tags.append("<p><button onclick=\"Display('" + layer[0:-4] + "')\">" + layer[0:-4] + "</button></p>")
tags.append("</section>")
tags.append("<section class=\"viewport\">")





# read in the svg data
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




tags.append("</section>")
tags.append("<script>")
tags.append("function Display(layer){")
tags.append("if(document.getElementById(layer).style.display == \"block\"){")
tags.append("document.getElementById(layer).style.display = \"none\";")
tags.append("}")
tags.append("else{")
tags.append("document.getElementById(layer).style.display = \"block\";")
tags.append("}")
tags.append("}//end Display()")
tags.append("</script>")
tags.append("</body>")
tags.append("</html>")



# write the svg data to the page
toFile = open("pcb.html", "w")
for tag in tags:
    toFile.write(tag)
    toFile.write("\n")
toFile.close()



































#           WHITE SPACE FOR SCROLLING           #
