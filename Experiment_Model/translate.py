import tensorflow as tf
import pickle
import os



# 批次大小与训练时保持一致，不可改变
batch_size = 128

# 加载字典
# 加载字典
with open(os.path.join("preparing_resources","conl_vocab_to_int.pickle"), 'rb') as f:
    source_vocab_to_int = pickle.load(f)
with open(os.path.join("preparing_resources","nl_vocab_to_int.pickle"), 'rb') as f:
    target_vocab_to_int = pickle.load(f)
source_int_to_vocab = {idx: word for word, idx in source_vocab_to_int.items()}
target_int_to_vocab = {idx: word for word, idx in target_vocab_to_int.items()}
#print("The size of English Map is : {}".format(len(source_vocab_to_int)))
#print("The size of French Map is : {}".format(len(target_vocab_to_int)))

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

translate_sentence_text = input("请输入句子：")

translate_sentence = sentence_to_seq(translate_sentence_text, source_vocab_to_int)

loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(os.path.join("tmp","checkpoints","model_nl.ckpt.meta"))
    loader.restore(sess, tf.train.latest_checkpoint(os.path.join("tmp","checkpoints")))
    input_data = loaded_graph.get_tensor_by_name('inputs:0')
    logits = loaded_graph.get_tensor_by_name('predictions:0')
    target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_len:0')
    source_sequence_length = loaded_graph.get_tensor_by_name('source_sequence_len:0')

    translate_logits = sess.run(logits, {input_data: [translate_sentence]*batch_size,
                                         target_sequence_length: [len(translate_sentence)*2]*batch_size,
                                         source_sequence_length: [len(translate_sentence)]*batch_size})[0]

print('【Input】')
print('  Word Ids:      {}'.format([i for i in translate_sentence]))
print('  Source Words: {}'.format([source_int_to_vocab[i] for i in translate_sentence]))

print('\n【Prediction】')
print('  Word Ids:      {}'.format([i for i in translate_logits]))
print('  Target Words: {}'.format([target_int_to_vocab[i] for i in translate_logits]))

print("\n【Full Sentence】")
print(" ".join([target_int_to_vocab[i] for i in translate_logits]))