import tensorflow as tf
import pickle
import os
import json
import sys



# 批次大小与训练时保持一致，不可改变
batch_size = 128
with open(os.path.join("preparing_resources","conl_vocab_to_int.pickle"), 'rb') as f:
    source_vocab_to_int = pickle.load(f)
with open(os.path.join("preparing_resources","nl_vocab_to_int.pickle"), 'rb') as f:
    target_vocab_to_int = pickle.load(f)
source_int_to_vocab = {idx: word for word, idx in source_vocab_to_int.items()}
target_int_to_vocab = {idx: word for word, idx in target_vocab_to_int.items()}



def sentence_to_seq(sentence, source_vocab_to_int):
    """
    将句子转化为数字编码
    """
    unk_idx = source_vocab_to_int["<UNK>"]
    word_idx = []
    
    undefined=[]
    num=0
    
    for word in sentence.lower().strip().split():
        if source_vocab_to_int.get(word,"None")=="None":
            if len(word.split('_'))>1:
                Type = word.split('_')[0]
                if word.split('_')[1] in undefined:
                    in_dex=undefined.index(word.split('_')[1])
                    Type_id = Type+str(in_dex)
                    word_idx.append(source_vocab_to_int.get(Type_id,unk_idx))
                else:
                    if num>=10:
                        word_idx.append(source_vocab_to_int.get(Type,unk_idx))
                    else:
                        undefined.append(word.split('_')[1])
                        Type_id = Type+str(num)
                        num+=1
                        word_idx.append(source_vocab_to_int.get(Type_id,unk_idx))
            else:
                word_idx.append(source_vocab_to_int.get(word,unk_idx))
        else:
            word_idx.append(source_vocab_to_int.get(word,unk_idx))
    
    return word_idx

    #for word in sentence.lower().strip().split():
        #if source_vocab_to_int.get(word,"None")=="None":
            #Type = word.split('_')[0]
            #word_idx.append(source_vocab_to_int.get(Type,unk_idx))
        #else:
            #word_idx.append(source_vocab_to_int.get(word,unk_idx))

    #return word_idx
data = []
file='Example.json'
with open(os.path.join("data",file),'r') as f:
    for line in f:
        data.append(json.loads(line))
loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(os.path.join("tmp","checkpoints","model_nl.ckpt.meta"))
    loader.restore(sess, tf.train.latest_checkpoint(os.path.join("tmp","checkpoints")))
    input_data = loaded_graph.get_tensor_by_name('inputs:0')
    logits = loaded_graph.get_tensor_by_name('predictions:0')
    target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_len:0')
    source_sequence_length = loaded_graph.get_tensor_by_name('source_sequence_len:0')

    for item in data:
        code = item['code']
        comment = item['nl']
        seq = item['sequence']
        translate_sentence = sentence_to_seq(seq,source_vocab_to_int)
        translate_logits = sess.run(logits, {input_data: [translate_sentence]*batch_size,
                                         target_sequence_length: [len(translate_sentence)*2]*batch_size,
                                         source_sequence_length: [len(translate_sentence)]*batch_size})[0]
        print('\n【源代码】：')
        print(code)
        print('【原注释】：')
        print(comment)
        print('【预测注释】')
        print(" ".join([target_int_to_vocab[i] for i in translate_logits]))
        print('\n')


        


        
        
    
