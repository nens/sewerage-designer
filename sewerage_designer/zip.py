from zipfile import ZipFile
import os

ROOT_DIR_FILES = [
    '__init__.py',
    'icon.ico',
    'icon.png',
    'icon_teal.png',
    'main.py',
    'metadata.txt',
    'qgis_connector.py',
    'resources.py',
    'resources_rc.py',
    'resources.qrc',
    'sewerage_designer.py',
    'sewerage_designer_dockwidget.py',
    'sewerage_designer_dockwidget_base.ui'
]

DIRECTORIES = [
    'designer',
    'geopackage',
    'style'
]


def zipdir(path, ziph, path_in_zip):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file_path = os.path.join(path_in_zip, file_path )
            ziph.write(file_path, zip_file_path)


# create a ZipFile object
try:
    os.remove('sewerage_designer.zip')
except FileNotFoundError:
    pass
zip = ZipFile('sewerage_designer.zip', 'w')

# Files in root
for file in ROOT_DIR_FILES:
    zip.write(file, os.path.join('sewerage_designer', os.path.basename(file)))

# Folders in root
for directory in DIRECTORIES:
    zipdir(directory, zip, 'sewerage_designer')

# close the Zip File
zip.close()