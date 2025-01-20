from textnode import TextNode, TextType
from os import listdir, path, mkdir
import shutil

## dangerous
def copy_dir(source, destination):
    print(f"Trying to copy from {source} to {destination}...")
    if "..\\" in destination:
        raise Exception("Are you sure you're allowed to do that?")
    
    if path.exists(destination):
        shutil.rmtree(destination)
    mkdir(destination)

    # use recursion for every nested directory
    for dir in listdir(source):
        if not path.isfile(path.join(source, dir)):
            copy_dir(path.join(source, dir), path.join(destination, dir))
        else:
            shutil.copy(path.join(source, dir), destination)

    print(f"...fninished copying from {source} to {destination}.")


def main():
    testNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testNode)

    copy_dir("static", "public")

main()