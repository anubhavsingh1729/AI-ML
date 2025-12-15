def count_pairs(ids):
	counts={}
	for pair in zip(ids,ids[1:]):
		counts[pair] = counts.get(pair,0)+1

	return counts


def merge(ids,pair,idx):
	newids = []
	i=0
	
	while i<len(ids):
		if i<len(ids)-1 and pair[0]==ids[i] and pair[1]==ids[i+1]:
			newids.append(idx)
			i+=2
		else:
			newids.append(ids[i])
			i+=1
	return newids

with open("train_tokenizer.txt","r",encoding = "utf-8") as f:
	txt = f.read().replace("\n"," ")

ids = list(txt.encode('utf-8'))

vocab_size = 276

idx = 256

nids = list(ids)

merges={}

for i in range(vocab_size-256):
	counts = count_pairs(nids)
	top_pair = max(counts,key=counts.get)
	idx+=i
	nids = merge(nids,top_pair,256)
	merges[top_pair] = idx


print(f"compression ratio: {len(ids)/len(nids):.2f}X")

vocab = {idx:bytes([idx]) for idx in range(256)}
for (c1,c2),idx in merges.items():
	vocab[idx] = vocab[c1]+vocab[c2]

def decode(ids):
	tokens = b"".join([vocab[i] for i in ids])
	txt = tokens.decode('utf-8',errors='replace')
	return txt

def encode(txt):
	tokens = list(txt.encode('utf-8'))
	while len(tokens)>=2:
		counts = count_pairs(tokens)

		pair = min(counts, key = lambda p: merges.get(p,float('inf')))
		if pair not in merges:
			break

		idx = merges[pair]
		
		tokens = merge(tokens,pair,idx)

	return tokens











