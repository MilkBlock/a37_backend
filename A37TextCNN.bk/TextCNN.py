import torch
import torch.nn as nn

class Block(nn.Module):#每个block包含CNN，act激活，maxpooling
    def __init__(self,kernel_s,embeddin_num,max_len,hidden_num):
        super().__init__()
        '''in_channels为输入通道
            out_channels为输出通道
            kernel_size为卷积核大小
            此处的文本形状即为max_len*embedding，
            因为使用的是2d，所以实际应为1（batch）*1（in_channels）*max_len*embedding'''
        self.cnn = nn.Conv2d(in_channels=1,out_channels=hidden_num,kernel_size=(kernel_s,embeddin_num)) # (batch *  in_channel * len * emb_num )
        '''当卷积核的宽等同于embedding时，输出将会是条状'''
        self.act = nn.ReLU()#ReLU激活函数，后期调整
        self.mxp = nn.MaxPool1d(kernel_size=(max_len-kernel_s+1))

    def forward(self,batch_emb): #(batch *  in_channel * len * emb_num )
        c = self.cnn.forward(batch_emb)
        a = self.act.forward(c)
        a = a.squeeze(dim=-1)
        m = self.mxp.forward(a)
        m = m.squeeze(dim=-1)
        return m

class TextCNNModel(nn.Module):
    def __init__(self,emb_matrix,max_len,class_num,hidden_num):
        super().__init__()
        self.emb_num = emb_matrix.weight.shape[1]

        self.block1 = Block(2,self.emb_num,max_len,hidden_num)
        self.block2 = Block(3,self.emb_num,max_len,hidden_num)
        self.block3 = Block(4,self.emb_num,max_len,hidden_num)
        self.block4 = Block(5,self.emb_num, max_len, hidden_num)

        self.emb_matrix = emb_matrix

        self.classifier = nn.Linear(hidden_num*4,class_num)  # 4为下面block的个数
        self.loss_fun = nn.CrossEntropyLoss()

    def forward(self,batch_idx,batch_label=None):
        batch_emb = self.emb_matrix(batch_idx)
        b1_result = self.block1.forward(batch_emb.unsqueeze(1))
        b2_result = self.block2.forward(batch_emb.unsqueeze(1))
        b3_result = self.block3.forward(batch_emb.unsqueeze(1))
        b4_result = self.block4.forward(batch_emb.unsqueeze(1))

        # print(b1_result)
        # print(b2_result)
        # print(b3_result)
        # print(b4_result)
        feature = torch.cat([b1_result, b2_result, b3_result, b4_result], dim=1)
        pre = self.classifier(feature)

        if batch_label is not None:
            loss = self.loss_fun(pre,batch_label)
            return loss
        else:
            return pre
