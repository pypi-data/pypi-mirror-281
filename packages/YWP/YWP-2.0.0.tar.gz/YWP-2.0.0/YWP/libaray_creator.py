import os

class Libraries:
    
    def init_creator(filesave="__init__.py", filename="", function_class=""):
        if filename == "" or function_class == "" or filesave == "":
            return "FileSave or FileName or Function/Class Name is Not Found"
        else:
            if os.path.exists(filesave):
                try:
                    with open(filesave, "r") as f:
                        text = f.read()
                except Exception as e:
                    return str(e)
            else:
                text = ""
            try:
                text += "\nfrom ." + filename + " import " + function_class
                with open (filesave, "w") as f:
                    f.write(text)
                return 'done'
            except Exception as e:
                return str(e)
            
    def basic_setup_file_creator(filename="setup.py", folder_name="", readme_name="README.md", library_name="", library_version="", libraries_required=[], description="", creator_name="", creator_email=""):
        file_data = "from setuptools import setup, find_packages\n\nsetup(\nname='" + library_name + "',\nversion='" + library_version + "',\npackages=find_packages(),\ninstall_requires=" + str(libraries_required) + ",\nclassifiers=[\n'Programming Language :: Python :: 3',\n],\npython_requires='>=3.6',\ndescription='" + description + "',\nlong_description=open('" + readme_name + "').read(),\nlong_description_content_type='text/markdown',\nauthor='" + creator_name + "',\nauthor_email='" + creator_email + "',\n)"
        if os.path.exists(filename):
            return 'FileName Found'
        else:
            try:
                with open (filename, "w") as f:
                    f.write(file_data)
                return 'done'
            except Exception as e:
                return str(e)
                
    def upload_file_creator(filename="upload_libarary", pypi_api="", platform="windows"):
        platforms = ["windows", "linux"]
        if platform in platforms:
            if platform == "windows":
                filename += ".bat"
                file_data = "set TWINE_USERNAME=__token__\nset TWINE_PASSWORD=" + pypi_api + "/npython setup.py sdist bdist_wheel\nset TWINE_USERNAME=%TWINE_USERNAME% set TWINE_PASSWORD=%TWINE_PASSWORD% twine upload dist/*"
                if os.path.exists(filename):
                    return 'FileName Found'
                else:
                    try:
                        with open(filename, "w") as f:
                            f.write(file_data)
                        return 'done'
                    except Exception as e:
                        return str(e)
            elif platform == "linux":
                filename += ".sh"
                file_data = 'export TWINE_USERNAME="__token__"\nexport TWINE_PASSWORD="' + pypi_api + '"\npython setup.py sdist bdist_wheel\nTWINE_USERNAME="$TWINE_USERNAME" TWINE_PASSWORD="$TWINE_PASSWORD" twine upload dist/*'
                if os.path.exists(filename):
                    return 'FileName Found'
                else:
                    try:
                        with open(filename, "w") as f:
                            f.write(file_data)
                        return 'done'
                    except Exception as e:
                        return str(e)
            else:
                return 'Platform Not Supported'
        else:
            return 'Platform Not Supported'