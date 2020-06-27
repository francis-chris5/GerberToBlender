# GerberToBlender
A plugin for Blender 3D modeling software which (when completed) will import SVG exports of a Gerber file into an accurate virtual model of the PCB

Still a lot to do on this project, but so far it reads in a list of SVG files and sets up the x and y positions and sizes for each layer of the PCB. So basically only step one is completed so far, but eventually it will produce two versions of a completed model, one as a single piece and one separated into components.


The testing so far was PCB created with EasyEDA online PCB editing software, SVG files exported from gerbv Gerber Viewer Software, and Blender 2.8.2


Early drafts of the Doxygen generated documentation is available at https://francis-chris5.github.io/GerberToBlender/ 



With the first draft of the apply materials script done I wanted to put some pictures here. For these images I ran the 'import curves.py' script, had to do the extrusions and modifiers by hand but those scripts will be coming soon and the generated images will take the place of these, then ran the 'apply materials.py' script.

![screenshot_1](https://user-images.githubusercontent.com/50467171/85911989-ef215b80-b7f6-11ea-824b-2f91e12ab948.png)
![screenshot_2](https://user-images.githubusercontent.com/50467171/85911992-f183b580-b7f6-11ea-8711-826e96492884.png)
