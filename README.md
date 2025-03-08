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