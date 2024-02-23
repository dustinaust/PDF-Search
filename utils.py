import os
import aspose.words as aw
from langchain_community.document_loaders import DirectoryLoader

def converter(path_to_pdf: str, path_to_md: str) -> None:

    # Inputs: path_to_pdf, name of directory of PDFs
    #         path_to_md, name of directory where markdowns are stored

    #Check if directory for markdowns exist
    if not os.path.exists(path_to_md):
        os.makedirs(path_to_md)


    list_pdf = os.listdir(path_to_pdf)

    #Save PDFs as MD in MD directory
    for filename in list_pdf:
        document = aw.Document(path_to_pdf+"/"+filename)
        
        document.save(path_to_md+filename[:-4]+".md", aw.SaveFormat.MARKDOWN)
        
    list_md = os.listdir(path_to_md)

    #Delete unneccessary files
    for file in list_md:
        if not file.endswith(".md"):
            os.remove("Markdowns/"+file)

    return None


def load_documents(path_to_md: str) -> list:
    loader = DirectoryLoader(path_to_md, glob="*.md")
    documents = loader.load()
    return documents

