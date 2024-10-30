from sentence_transformers import util

def question_checker(question, refq, treshold=0.5, model=None):
    if model is not None:
        emb_refq = model.encode(refq)
        emb_actq = model.encode([question])

        cosine_similarities = util.cos_sim(emb_refq, emb_actq)
        print([[sim > treshold, sim] for sim in cosine_similarities])
        return any(sim > treshold for sim in cosine_similarities)
    else:
        return False
    
def cleaning_stream(batch):
    if len(batch['text_output']) == 0:
        return False
    elif batch['text_output'] == "\n\n":
        return False
    elif "<|start_header_id|>" in batch['text_output']:
        return False
    elif "assistant" in batch['text_output']:
        return False
    elif "<|end_header_id|>" in batch['text_output']:
        return False
    else:
        return True
    
def reduce_message(chat, max_len, num_limit, tokenizer):
    message = tokenizer.apply_chat_template(chat, tokenize=False)
    len_chat = len(tokenizer.encode(message))      
    while len_chat > max_len and len(chat) > num_limit:
        chat = chat[0:1] + chat[2:]

        message = tokenizer.apply_chat_template(chat, tokenize=False)
        len_chat = len(tokenizer.encode(message))
        # print(len_chat, chat)

    if len_chat < max_len:
        return message
    else:
        return ""