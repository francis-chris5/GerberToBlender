# GerberToBlender
A plugin for Blender 3D modeling software which (when completed) will import SVG exports of a Gerber file into an accurate virtual model of the PCB. 

I had two reasons for making this.

First off, I want to start 3d-printing out cases for some of my Arduino or Rasberry Pi hobby projects, and wanted an accurate virtual model of the boards I order for designing those casings. Virtual models of most components can be downloaded right from the manufacturers for this, but not custom PCB's or SMT's.

Secondly, sometimes I feel that the 2D layout is not suffecient for examining a PCB before placing the order -I recently got one in with a tiny mistake (I left the pads for resistors and transitors from the SMT in the PCB I planned to solder by hand for a prototype). I would have caught that easily in a 3D virtual model, and now have to wait a couple weeks for the corrected design -I'm not paying rapid shipping rates for two dollars worth of PCB's to come from China.

I figure I'm not the only one who does this stuff with Arduino or Rasberry Pi project so I'd share it on here.

Still a lot to do on this project, but so far it reads in a list of SVG files (must be set up in a folder with a text file called "names" --folder not generated yet--, and a filebrowser will select the directory) and sets up the x and y positions and sizes for each layer of the PCB. Then it applies modifiers to change the remaining 2d curves into 3d meshes and drill the holes through all the components. It finally applies the materials to all the objects once they're finished. So basically only the first and last steps are complete so far, still have to set up extrusions, and eventually it will produce two versions of a completed model, one as a single piece and one separated into components.


The testing so far was PCB created with EasyEDA online PCB editing software, SVG files exported from gerbv Gerber Viewer Software, and scripted with Blender 2.8.3 API.


Early drafts of the Doxygen generated documentation is available at https://francis-chris5.github.io/GerberToBlender/ 



With the first draft of the apply materials script done I wanted to put some pictures here. For these images I ran the 'import curves.py' script, had to do the extrusions and modifiers by hand but those scripts will be coming soon and the generated images will take the place of these, then ran the 'apply materials.py' script.

![screenshot_1](https://user-images.githubusercontent.com/50467171/85911989-ef215b80-b7f6-11ea-824b-2f91e12ab948.png)
![screenshot_2](https://user-images.githubusercontent.com/50467171/85911992-f183b580-b7f6-11ea-8711-826e96492884.png)
