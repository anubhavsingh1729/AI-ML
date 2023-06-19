# Example query:
# dtl(
#    examples = [
#         {'Furniture': 'No', 'Nr. of rooms': '3', 'New kitchen': 'Yes', 'Acceptable': 'Yes'},
#         {'Furniture': 'Yes', 'Nr. of rooms': '3', 'New kitchen': 'No', 'Acceptable': 'No'},
#         {'Furniture': 'No', 'Nr. of rooms': '4', 'New kitchen': 'No', 'Acceptable': 'Yes'},
#         {'Furniture': 'No', 'Nr. of rooms': '3', 'New kitchen': 'No', 'Acceptable': 'No'},
#         {'Furniture': 'Yes', 'Nr. of rooms': '4', 'New kitchen': 'No', 'Acceptable': 'Yes'}
#    ],
#    attributes = {'Furniture': ['Yes', 'No'], 'Nr. of rooms': ['3', '4'], 'New kitchen': ['Yes', 'No'], 'Acceptable': ['Yes', 'No']},
#    target = 'Acceptable',
#    default = 'Yes'
# )
#
# Warning: the target attribute must not be used in the decision tree
# Warning: attributes are not necessarily binary
#
#
# Expected result:
# ('Nr. of rooms', {
#     '4': 'Yes',
#     '3': ('New kitchen', {
#         'Yes': 'Yes',
#         'No': 'No'}
#     )
#     }
# )
import math

def mode(examples,target):
    count = {}
    for example in examples:
        val = example[target]
        count[val] = count.get(val,0)+1
    return max(count,key=count.get)

def choose_best(examples,attributes,target):
    best_attr = None
    best_info_gain = -float('inf')
    for attr in attributes:
        if attr == target:
            continue
        info_gain = information_gain(examples,attr,target)
        if info_gain>best_info_gain:
            best_info_gain = info_gain
            best_attr = attr
    return best_attr

def information_gain(examples,attribute,target):
    target_ent = compute_entropy(examples,target)

    attr_val = set([example[attribute] for example in examples])
    w_sum = 0
    for v in attr_val:
        val_examples = [example for example in examples if example[attribute]==v]
        ent = compute_entropy(val_examples,target)
        weight = len(val_examples)/len(examples)
        w_sum+=weight*ent

    info_gain = target_ent - w_sum
    return info_gain

def compute_entropy(examples,target):
    target_val = set([example[target] for example in examples])
    val_count = {}
    for v in target_val:
        val_count[v] = val_count.get(v,0)+1

    for i in val_count:
        val_count[i]=val_count[i]/len(examples)

    entropy = 0
    for i in val_count:
        entropy+=val_count[i]*math.log2(val_count[i])
    return entropy*-1

def dtl(examples, attributes, target, default):
    if len(examples)==0:
        return default
    if len(set([example[target] for example in examples]))==1:
        return set([example[target] for example in examples]).pop()

    if len(attributes) == 0:
        return mode(examples,target)
    
    new_attr = attributes.copy()
    best_attr= choose_best(examples,new_attr,target)
    #print(best_attr,info)
    tree = (best_attr,{})
    m = mode(examples,target)
    new_attr.pop(best_attr)

    for v in attributes[best_attr]:
        examples_si = [example for example in examples if example[best_attr]==v]
        subtree = dtl(examples_si,new_attr,target,m)
        #print('1',subtree)
        tree[1][v] = subtree
        #print('2',tree)

    return tree

if __name__== '__main__':
    tree = dtl(
    examples = [
         {'Furniture': 'No', 'Nr. of rooms': '3', 'New kitchen': 'Yes', 'Acceptable': 'Yes'},
         {'Furniture': 'Yes', 'Nr. of rooms': '3', 'New kitchen': 'No', 'Acceptable': 'No'},
         {'Furniture': 'No', 'Nr. of rooms': '4', 'New kitchen': 'No', 'Acceptable': 'Yes'},
         {'Furniture': 'No', 'Nr. of rooms': '3', 'New kitchen': 'No', 'Acceptable': 'No'},
         {'Furniture': 'Yes', 'Nr. of rooms': '4', 'New kitchen': 'No', 'Acceptable': 'Yes'}
    ],
    attributes = {'Furniture': ['Yes', 'No'], 'Nr. of rooms': ['3', '4'], 'New kitchen': ['Yes', 'No'], 'Acceptable': ['Yes', 'No']},
    target = 'Acceptable',
    default = 'Yes')

    print(tree)

