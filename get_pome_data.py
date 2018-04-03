# -*- coding:utf8 -*-

import re,os,sys
from tqdm import tqdm

def read_file(filename,islines=False):
    with open(filename) as rf:
        if not islines:
            text = rf.read()
            return text.strip()
        else:
            lines = rf.readlines()
            lines = [l.strip() for l in lines if l.strip()]
            return lines
            
def add_shad(text):
    Special_Syllables = re.compile(r"(ག|ཀ|ཤ|གྲ|ཀྲ|ཤྲ)([\u0F71-\u0F8F])?(\s+|$)")
    text = Special_Syllables.sub(r"\1\2།", text)
    return text
    
def Data_Preprocessing(text):
    text = add_shad(text)
    text = re.sub(r"[\u0F06-\u0F0A\u0F13-\u0F1F\u0F2A-\u0F3B\u0FBE-\u0FDA]+",
                   "",text)
    text = re.sub(r"[\u0F20-\u0F29\u0F3C\u0F3D]+","་",text)
    text = re.sub("\s+","",text)
    text = re.sub(r"(།+)",r"་\1",text)
    text = re.sub("་་+","་",text)    
    return text
    
def IS_Condition(allsents,sents):
    if len(sents) > 3:
        allsents.append("".join(sents))
        sents = []
    else:
        sents = []

def get_TpgData(text,WordSeparators_Count=6):
    """
       Data of Tibetan poetry generation (tpg)
    """    
    
    text = re.sub(r"(།+)",r"\1SCJ",text)
    lines = re.split("SCJ",text)
    lines = [l.strip() for l in lines if l.strip()]
    Result_sents = []
    tem_sents = []
    for line in tqdm(lines):
        wordseparators_count = line.count("་")
        if wordseparators_count > WordSeparators_Count:
            if re.search("།།$",line):
                if not tem_sents:
                    tem_sents.append(line)
                else:
                    last_sent = tem_sents[-1]
                    if last_sent.count("་") == wordseparators_count:
                        tem_sents.append(line)
                    else:
                        IS_Condition(Result_sents,tem_sents)
                        tem_sents = []
            else:
                IS_Condition(Result_sents,tem_sents)
                tem_sents = []
        else:
            IS_Condition(Result_sents,tem_sents)
            tem_sents = []
    return "\n".join(Result_sents)
    
def test(dirs,savedir="./TPG",IsDir=True):

    if savedir:
        if not os.path.exists(savedir):
            os.mkdir(savedir)
            
    if IsDir:
        for dir in dirs:
            BaseName = os.path.basename(dir)
            text = read_file(dir)
            text = Data_Preprocessing(text)
            w_text = get_TpgData(text)
            if w_text:
                savepath = os.path.join(savedir,BaseName)
                with open(savepath,"w",encoding="utf8") as writer:
                    writer.write(w_text)
            else:
                print("གྲོགས་པོ་ལགས། ཡིག་ཁུག {0} འདིར་འུ་ཚོར་མཁོ་བའི་གཞི་གྲངས་མེད་དོ།".format(dir))
    else:
        BaseName = os.path.basename(dirs)
        text = read_file(dirs)
        text = Data_Preprocessing(text)
        w_text = get_TpgData(text)
        if w_text:
            savepath = os.path.join(savedir,BaseName)
            with open(savepath,"w",encoding="utf8") as writer:
                writer.write(w_text)
        else:
            print("གྲོགས་པོ་ལགས། ཡིག་ཁུག {0} འདིར་འུ་ཚོར་མཁོ་བའི་གཞི་གྲངས་མེད་དོ།".format(dirs))

        
if __name__ == "__main__":
    """
        py3 Get_TPG.py ./dirs/  
        py3 Get_TPG.py sample.txt
    """
    argvs  = sys.argv
    argvs1 = argvs[1]
    if len(argvs) == 2:
        if re.search(r"/$",argvs1):
            print("all dirs from {0}".format(argvs1))
            dirlist = os.listdir(argvs1)
            dirlist = [os.path.join(argvs1,dl) for dl in dirlist]
            test(dirlist)
        else:
            print("file is {0}".format(argvs1))
            test(argvs1,IsDir=False)
    else:
        print("གྲོགས་པོ་ལགས། ཁྱོད་ཀྱི་ཞུགས་གྲངས་ཆུགས་འདུག རྣམ་པ་ངེས་པར་དུ་འདི་འདྲ་ཞིག་ཡིན་དགོས་སྟེ། ")
        print("py3 Get_TPG.py ./dirs/  ཡང་ན py3 Get_TPG.py sample.txt")
        sys.exit()
        
