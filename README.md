What is this good for?
This tool is for preparing FreeCAD projects so they are better suited for use in version control systems like git.
Most of the file content comes from cached 3D data that can be recomputed. Without it the files are usually just a few kB in size.

What does the script do:
1. removes all CDATA (cache) sections in the .xml files
2. marks all objects to recompute in Document.xml

How to use:
1. in Freecad 'Save as Directory..." your_project_folder
2. remove cached data:
  python remove_cache.py your_project_folder/
3. do whatever (put files to git, have a life, etc.)
4. in FreeCAD 'Open Directory...'
5. recompute ('F5' or Ctrl+R)

You can also use this to reduce the size of .FCStd files.
First save them to a directory, remove the cache, open the project from directory and then and save them again as a normal project file.
