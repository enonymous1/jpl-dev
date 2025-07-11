from app import freezer
import shutil
import os

if __name__ == '__main__':
    # Generate the static site
    freezer.freeze()
    
    print("Static site generated successfully in docs/ directory")
