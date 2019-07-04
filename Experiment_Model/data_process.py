import numpy as np
import pickle
import tqdm
import os
import collections
from operator import itemgetter

max_source_sentence_length = 200
max_target_sentence_length = 30



def text_to_int(sentence, map_dict, max_length, is_target=False):
    """
    对文本句子进行数字编码

    @param sentence: 一个完整的句子，str类型
    @param map_dict: 单词到数字的映射，dict
    @param max_length: 句子的最大长度
    @param is_target: 是否为目标语句。在这里要区分目标句子与源句子，因为对于目标句子（即翻译后的句子）需要在句子最后增加<EOS>
    """

    # 用<PAD>填充整个序列
    text_to_idx = []
    # unk index
    unk_idx = map_dict.get("<UNK>")
    pad_idx = map_dict.get("<PAD>")
    eos_idx = map_dict.get("<EOS>")

    # 如果是输入源码文本,如果指定键的值不存在时，返回其类型值对应的id
    
    #if not is_target:
        #for word in sentence.lower().strip().split():
            #if map_dict.get(word,"None")=="None":
                #Type = word.split('_')[0]
                #text_to_idx.append(map_dict.get(Type, unk_idx))
            #else:
                #text_to_idx.append(map_dict.get(word, unk_idx))
        #if len(text_to_idx) > max_length:
            #return text_to_idx[:max_length]
        #else:
            #text_to_idx = text_to_idx + [pad_idx] * (max_length - len(text_to_idx))
            #return text_to_idx
    if not is_target:
        undefined=[]
        num=0
        for word in sentence.lower().strip().split():
            if map_dict.get(word,"None")=="None":             
                if len(word.split('_'))>1:
                    Type = word.split('_')[0]
                    if word.split('_')[1] in undefined:
                        in_dex=undefined.index(word.split('_')[1])
                        Type_id = Type+str(in_dex)
                        text_to_idx.append(map_dict.get(Type_id, unk_idx))
                    else:
                        if num>=10:
                            text_to_idx.append(map_dict.get(Type, unk_idx))
                        else:
                            undefined.append(word.split('_')[1])
                            Type_id = Type+str(num)
                            num+=1
                            text_to_idx.append(map_dict.get(Type_id, unk_idx))
                else:
                    text_to_idx.append(map_dict.get(word, unk_idx))          
            else:
                text_to_idx.append(map_dict.get(word, unk_idx))
        if len(text_to_idx) > max_length:
            return text_to_idx[:max_length]
        else:
            text_to_idx = text_to_idx + [pad_idx] * (max_length - len(text_to_idx))
            return text_to_idx
    # 否则，对于输出目标文本需要做<EOS>的填充最后
    else:
        for word in sentence.lower().strip().split():
            text_to_idx.append(map_dict.get(word, unk_idx))
        #text_to_idx.append(eos_idx)
        
        if len(text_to_idx) > max_length-1:
            text_to_idx = text_to_idx[:max_length-1]
            text_to_idx.append(eos_idx)
            return text_to_idx
        else:
            text_to_idx.append(eos_idx)
            text_to_idx = text_to_idx + [pad_idx] * (max_length - len(text_to_idx))
            return text_to_idx
 
    


nl_counter = collections.Counter()
co_counter = collections.Counter()
Vocab_size = 20000
# source data
with open(os.path.join("data","Code.txt"), "r", encoding="utf-8") as f:
    source_text = f.read()
with open(os.path.join("data","Code.txt"),"r", encoding="utf-8") as f:
    for line in f:
        for word in line.lower().strip().split():
            co_counter[word] += 1
            if word.find("_",1,len(word)-2)!=-1:
                Type = word.split('_')[0]
                co_counter[Type] += 1
# target data
with open(os.path.join("data","Nl.txt"), "r", encoding="utf-8") as f:
    target_text = f.read()
with open(os.path.join("data","Nl.txt"), "r", encoding="utf-8") as f:
    for line in f:
        for word in line.lower().strip().split():
            nl_counter[word] += 1

sorted_word_to_co = sorted(co_counter.items(), key=itemgetter(1), reverse=True)
sorted_words_co = [x[0] for x in sorted_word_to_co]

sorted_word_to_nl = sorted(nl_counter.items(), key=itemgetter(1), reverse=True)
sorted_words_nl = [y[0] for y in sorted_word_to_nl] 

view_sentence_range = (0, 10)

# 对原始文本按照空格分开，查看原始文本中包含了多少个单词
print('Dataset Stats')
print('Roughly the number of unique words: {}'.format(len({word: None for word in source_text.split()})))

# 按照换行符将原始文本分割成句子,统计句子的数量，最大句子长度和平均长度
print("-"*5 + "Source Text" + "-"*5)
sentences = source_text.split('\n')
word_counts = [len(sentence.split()) for sentence in sentences]
print('Number of sentences: {}'.format(len(sentences)))
print('Average number of words in a sentence: {}'.format(np.average(word_counts)))
print('Max number of words in a sentence: {}'.format(np.max(word_counts)))

print()
print("-"*5 + "Target Text" + "-"*5)
sentences = target_text.split('\n')
word_counts = [len(sentence.split()) for sentence in sentences]
print('Number of sentences: {}'.format(len(sentences)))
print('Average number of words in a sentence: {}'.format(np.average(word_counts)))
print('Max number of words in a sentence: {}'.format(np.max(word_counts)))
print(np.argmax(word_counts))

print()
print('source sentences {} to {}:'.format(*view_sentence_range))
print('\n'.join(source_text.split('\n')[view_sentence_range[0]:view_sentence_range[1]]))
print()
print('target sentences {} to {}:'.format(*view_sentence_range))
print('\n'.join(target_text.split('\n')[view_sentence_range[0]:view_sentence_range[1]]))

# 构造代码词典
source_vocab = sorted_words_co
# 构造注释词典
target_vocab = sorted_words_nl

print("The size of source vocab is : {}".format(len(source_vocab)))
print("The size of target vocab is : {}".format(len(target_vocab)))

# 特殊字符
SOURCE_CODES = ['<PAD>', '<UNK>']
TARGET_CODES = ['<PAD>', '<EOS>', '<UNK>', '<GO>']  # 在target中，需要增加<GO>与<EOS>特殊字符

#源码序列词集中添加simplename序号标识
str_name = 'simplename'
for i in range(10):
    str_id = str_name+str(i)
    SOURCE_CODES.append(str_id)

source_co = SOURCE_CODES + source_vocab
target_nl = TARGET_CODES + target_vocab

if len(source_co) > Vocab_size:
    source_co = source_co[:Vocab_size]
    
if len(target_nl) > Vocab_size:
    target_nl = target_nl[:Vocab_size]
    
with open(os.path.join("data","co.vocab"), "w", encoding="utf-8") as f:
    for word in source_co:
        f.write(word+'\n')

with open(os.path.join("data","nl.vocab"), "w", encoding="utf-8") as f:
    for word in target_nl:
        f.write(word+'\n')

# 构造代码序列映射字典
source_vocab_to_int = {word: idx for idx, word in enumerate(source_co)}
source_int_to_vocab = {idx: word for idx, word in enumerate(source_co)}
# 构造注释序列映射词典
target_vocab_to_int = {word: idx for idx, word in enumerate(target_nl)}
target_int_to_vocab = {idx: word for idx, word in enumerate(target_nl)}


# 对源句子进行转换 Tx = max_source_sentence_length
source_text_to_int = []
for sentence in tqdm.tqdm(source_text.split("\n")):
    source_text_to_int.append(text_to_int(sentence, source_vocab_to_int,
                                          max_source_sentence_length,
                                          is_target=False))
# 对目标句子进行转换  Ty = max_target_sentence_length
target_text_to_int = []
for sentence in tqdm.tqdm(target_text.split("\n")):
    target_text_to_int.append(text_to_int(sentence, target_vocab_to_int,
                                          max_target_sentence_length,
                                          is_target=True))

random_index = 77
print("-"*5 + "source example" + "-"*5)
print(source_text.split("\n")[random_index])
print(source_text_to_int[random_index])
print()
print("-"*5 + "target example" + "-"*5)
print(target_text.split("\n")[random_index])
print(target_text_to_int[random_index])


X = np.array(source_text_to_int)
Y = np.array(target_text_to_int)

print("\nDATA shape:")
print("X_shape:\t", X.shape)
print("Y_shape:\t", Y.shape)

# 创建存储数据的文件夹
if not os.path.exists("preparing_resources"):
    os.mkdir("preparing_resources")
if not os.path.exists("tmp"):
    os.makedirs(os.path.join("tmp","checkpoints"))

# 存储预处理文件
np.savez(os.path.join("preparing_resources","prepared_data.npz"), X=X, Y=Y)
# 存储字典
with open(os.path.join("preparing_resources","conl_vocab_to_int.pickle"), 'wb') as f:
    pickle.dump(source_vocab_to_int, f)
with open(os.path.join("preparing_resources","nl_vocab_to_int.pickle"), 'wb') as f:
    pickle.dump(target_vocab_to_int, f)
print("The size of source Map is : {}".format(len(source_vocab_to_int)))
print("The size of target Map is : {}".format(len(target_vocab_to_int)))