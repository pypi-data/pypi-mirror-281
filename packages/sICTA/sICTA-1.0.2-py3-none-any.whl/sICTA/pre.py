import os
import sys
import torch
import pandas as pd
import numpy as np
import torch.nn.functional as F
import scanpy as sc
import anndata as ad
from .sICTA_model import scTrans_model as create_model
from torch.utils.data import Dataset

from sklearn.metrics import f1_score,precision_recall_fscore_support

def f1(y_true, y_pred):
    y_true = y_true.astype(np.int64)
    assert y_pred.size == y_true.size
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(y_true, y_pred, average='micro')

    return (precision_macro, recall_macro, f1_macro), (precision_micro, recall_micro, f1_micro)
def todense(adata):
    import scipy
    if isinstance(adata.X, scipy.sparse.csr_matrix) or isinstance(adata.X, scipy.sparse.csc_matrix):
        return adata.X.todense()
    else:
        return adata.X

def get_weight(att_mat,pathway):
    att_mat = torch.stack(att_mat).squeeze(1)
    # Average the attention weights across all heads.
    att_mat = torch.mean(att_mat, dim=1)
    # To account for residual connections, we add an identity matrix to the
    # attention matrix and re-normalize the weights.
    residual_att = torch.eye(att_mat.size(1))
    aug_att_mat = att_mat + residual_att
    aug_att_mat = aug_att_mat / aug_att_mat.sum(dim=-1).unsqueeze(-1)
    # Recursively multiply the weight matrices
    joint_attentions = torch.zeros(aug_att_mat.size())
    joint_attentions[0] = aug_att_mat[0]
    
    for n in range(1, aug_att_mat.size(0)):
        joint_attentions[n] = torch.matmul(aug_att_mat[n], joint_attentions[n-1])

    # Attention from the output token to the input space.
    v = joint_attentions[-1]
    v = pd.DataFrame(v[0,1:].detach().numpy()).T
    #print(v.size())
    v.columns = pathway
    return v

class MyDataSet(Dataset):
    """ 
    Preproces input matrix and labels.

    """
    def __init__(self, exp, label):
        self.exp = exp
        self.label = label
        self.len = len(label)
    def __getitem__(self,index):
        return self.exp[index],self.label[index]
    def __len__(self):
        return self.len
    
def prediect(adata,model_weight_path, project,mask_path,laten=False,current_path = None,save_att = 'X_att', save_lantent = 'X_lat',n_step=50000,cutoff=0.0,n_unannotated = 1,batch_size = 64,embed_dim=100,depth=2,num_heads=4):
    device = torch.device("cuda:2" if torch.cuda.is_available() else "cpu")
    print(device)
    num_genes = adata.shape[1]
    mask = np.load(mask_path)
    project_path = current_path+'/%s'%project
    pathway = pd.read_csv(project_path+'/pathway.csv', index_col=0)
    dictionary = pd.read_table(project_path+'/label_dictionary.csv', sep=',',header=0,index_col=0)
    n_c = len(dictionary)
    label_name = dictionary.columns[0]
    dictionary.loc[(dictionary.shape[0])] = 'Unknown'
    dic = {}
    for i in range(len(dictionary)):
        dic[i] = dictionary[label_name][i]

    model = create_model(num_classes=n_c, num_genes=num_genes,mask = mask, has_logits=False,depth=depth,num_heads=num_heads,embed_dim=embed_dim).to(device)
    # load model weights
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    parm={}
    for name,parameters in model.named_parameters():
        #print(name,':',parameters.size())
        parm[name]=parameters.detach().cpu().numpy()
    gene2token = parm['feature_embed.fe.weight']
    gene2token = gene2token.reshape((int(gene2token.shape[0]/embed_dim),embed_dim,adata.shape[1]))
    gene2token = abs(gene2token)
    gene2token = np.max(gene2token,axis=1)
    gene2token = pd.DataFrame(gene2token)
    gene2token.columns=adata.var_names
    gene2token.index = pathway['0']
    gene2token.to_csv(project_path+'/gene2token_weights.csv')
    latent = torch.empty([0,embed_dim]).cpu()
    att = torch.empty([0,(len(pathway))]).cpu()
    predict_class = np.empty(shape=0)
    pre_class = np.empty(shape=0)      
    latent = torch.squeeze(latent).cpu().numpy()
    l_p = np.c_[latent, predict_class,pre_class]
    att = np.c_[att, predict_class,pre_class]
    all_line = adata.shape[0]
    n_line = 0
    adata_list = []
    pre_list = None
    while (n_line) <= all_line:
    
        expdata = pd.DataFrame(todense(adata[n_line:n_line+min(n_step,(all_line-n_line))]),index=np.array(adata[n_line:n_line+min(n_step,(all_line-n_line))].obs_names).tolist(), columns=np.array(adata.var_names).tolist())
        ann = adata.obs['broad_cell_type'][n_line:n_line+min(n_step,(all_line-n_line))]
        expdata = np.array(expdata)
        expdata = torch.from_numpy(expdata.astype(np.float32))

        test_dataset = MyDataSet(expdata, ann)
        
        data_loader = torch.utils.data.DataLoader(test_dataset,
                                                batch_size=batch_size,
                                                shuffle=False,
                                                pin_memory=True,drop_last=True)

        with torch.no_grad():
            # predict class
            sample_num = 0
            pre_all,label_all = [],[]
            accu_num = torch.zeros(1).to(device)
            for step, data in enumerate(data_loader):
                #print(step)
                exp,label = data
                sample_num += exp.shape[0]
                lat, pre, weights = model(exp.to(device))
                pre = torch.squeeze(pre).cpu()
                if step == 0:
                    pre_list = pre.numpy()
                else:
                    pre_list = np.append(pre_list,pre.numpy(),axis=0)
                pre = F.softmax(pre,1)
                predict_class = np.empty(shape=0)
                pre_class = np.empty(shape=0) 
                for i in range(len(pre)):
                    if torch.max(pre, dim=1)[0][i] >= cutoff: 
                        predict_class = np.r_[predict_class,torch.max(pre, dim=1)[1][i].numpy()]
                    else:
                        predict_class = np.r_[predict_class,n_c-1]
                    pre_class = np.r_[pre_class,torch.max(pre, dim=1)[0][i]]   
                pre_all.extend(list(predict_class))  
                label_all.extend(list(label.numpy()))  
                accu_num += torch.eq(torch.from_numpy(predict_class), label).sum()
                l_p = torch.squeeze(lat).cpu().numpy()
                att = torch.squeeze(weights).cpu().numpy()
                meta = np.c_[predict_class,pre_class]
                meta = pd.DataFrame(meta)
                meta.columns = ['Prediction','Probability']
                meta.index = meta.index.astype('str')
                if laten:
                    l_p = l_p.astype('float32')
                    new = sc.AnnData(l_p, obs=meta)
                else:
                    att = att[:,0:(len(pathway)-n_unannotated)]
                    att = att.astype('float32')
                    varinfo = pd.DataFrame(pathway.iloc[0:(len(pathway)-1),0].values,index=pathway.iloc[0:(len(pathway)-1),0],columns=['pathway_index'])
                    new = sc.AnnData(att, obs=meta, var = varinfo)
                adata_list.append(new)
            print(accu_num.item() / sample_num)
            break

    # print(all_line)
    new = ad.concat(adata_list)
    new.obs.index = adata.obs.index[0:len(new)]
    new.obs['Prediction'] = new.obs['Prediction'].map(dic)[0:len(new)]
    new.obs[adata.obs.columns] = adata.obs[adata.obs.columns].values[0:len(new)]
    return(new),pre_list
