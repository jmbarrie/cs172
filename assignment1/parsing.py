import enum
import re
import os
import zipfile
import string
import json

def create_stop_words_list(file_name):
    # Create list of stop words for comparison
    words_list = []
    stop_word_file = file_name

    with open(stop_word_file, 'r') as inputfile:
        for line in inputfile:
            words_list.append(line.rstrip('\n'))
    
    return words_list

def create_corpus_index(text, doc_no):
    # Uses the parsed text to create the term index dictionary
    position = 0
    global term_id, doc_id, term_id_dict, doc_id_dict, word_index

    for word in text.split():
        word_new_status = False
        if word not in stop_words:
            if word not in term_id_dict:
                term_id_dict[word] = term_id
                term_id += 1
                word_new_status = True
            
            if docno not in doc_id_dict:
                doc_id_dict[docno] = doc_id
                doc_id += 1

            corpus_index.setdefault(word, []).append([doc_id_dict[docno], position, term_id_dict[word]])

        position += 1

def write_to_word_index(doc_id, position, term_id, word_new_status):
    # Deprecated - was trying to go for something that manipulated file at run
    # and did not store a corpus index as a dictionary
    file_name = 'data/word_index.txt'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f: 
            f.write(f'%s\t%s:%s\n' % (term_id, doc_id, position))
    else:
        if word_new_status:
            with open(file_name, 'a') as f:
                f.write(f'%s\t%s:%s\n' % (term_id, doc_id, position))
        else:
            with open(file_name, 'r+') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith(str(term_id)):
                        append_text = f'\t%s:%s\n' % (doc_id, position)
                        lines[i] = lines[i].strip() + append_text
                f.seek(0)
                for line in lines:
                    f.write(line)

def write_to_corpus_index(index):
    file_name = 'data/term_index.txt'
    with open(file_name, 'w') as f:
        for k, v in index.items():
            text = str(v[0][2])
            for i in range(0, len(v)):
                text = text + f'\t%s:%s' % (v[i][0], v[i][1])
            
            text = text + '\n'
            f.write(text)

def write_to_index(index, file_name):
    with open(file_name, 'w') as f:
        for k, v in index.items():
            text = f'%s\t%s\n' % (v, k) 
            f.write(text)

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

# with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
#     zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
# Dictionary of each term 
corpus_index = {}
text_list = []
doc_id_dict = {}
doc_id = 0
term_id_dict = {}
term_id = 0
stop_words = create_stop_words_list('stopwords.txt')

for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ").lower().translate(str.maketrans('', '', string.punctuation))

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            create_corpus_index(text, docno)
            # step 2 - create tokens 
            # step 3 - build index


docid_file = 'data/docids.txt'
termids_file = 'data/termids.txt'
write_to_index(doc_id_dict, docid_file)
write_to_index(term_id_dict, termids_file)
write_to_corpus_index(corpus_index)
