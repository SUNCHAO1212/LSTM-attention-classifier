import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

# ## Functions to accomplish attention
def batch_matmul_bias(seq, weight, bias, nonlinearity=''):
    s = None
    bias_dim = bias.size()
    for i in range(seq.size(0)):
        _s = torch.mm(seq[i], weight)
        _s_bias = _s + bias.expand(bias_dim[0], _s.size()[0]).transpose(0,1)
        if(nonlinearity=='tanh'):
            _s_bias = torch.tanh(_s_bias)
        _s_bias = _s_bias.unsqueeze(0)
        if(s is None):
            s = _s_bias
        else:
            s = torch.cat((s, _s_bias), 0)
    return s


def batch_matmul(seq, weight, nonlinearity=''):
    s = None
    for i in range(seq.size(0)):
        _s = torch.mm(seq[i], weight)
        if(nonlinearity=='tanh'):
            _s = torch.tanh(_s)
        _s = _s.unsqueeze(0)
        if(s is None):
            s = _s
        else:
            s = torch.cat((s, _s), 0)
    return s.squeeze().view(s.size(0), -1)


def attention_mul(rnn_outputs, att_weights):
    attn_vectors = None
    for i in range(rnn_outputs.size(0)):
        h_i = rnn_outputs[i]
        a_i = att_weights[i].unsqueeze(1).expand_as(h_i)
        h_i = a_i * h_i
        h_i = h_i.unsqueeze(0)
        if(attn_vectors is None):
            attn_vectors = h_i
        else:
            attn_vectors = torch.cat((attn_vectors,h_i),0)
    return torch.sum(attn_vectors, 0)


class CNN_Text(nn.Module):
    """需要重写变量名"""
    def __init__(self, args):
        super(CNN_Text, self).__init__()
        self.args = args
        
        V = args.embed_num
        D = args.embed_dim
        C = args.class_num
        Ci = 1
        Co = args.kernel_num
        Ks = args.kernel_sizes

        self.embed = nn.Embedding(V, D)
        # self.convs1 = [nn.Conv2d(Ci, Co, (K, D)) for K in Ks]
        self.convs1 = nn.ModuleList([nn.Conv2d(Ci, Co, (K, D)) for K in Ks])
        # TODO
        self.lstm = nn.LSTM(input_size=D, hidden_size=Co, num_layers=1, bidirectional=False)
        '''
        self.conv13 = nn.Conv2d(Ci, Co, (3, D))
        self.conv14 = nn.Conv2d(Ci, Co, (4, D))
        self.conv15 = nn.Conv2d(Ci, Co, (5, D))
        '''
        self.dropout = nn.Dropout(args.dropout)
        # TODO
        self.fc1 = nn.Linear(Co, C)

        self.weight_word = nn.Parameter(torch.FloatTensor(Co, Co))
        self.bias_word = nn.Parameter(torch.FloatTensor(Co, 1))
        self.weight_proj_word = nn.Parameter(torch.FloatTensor(Co, 1))
        self.softmax_word = nn.Softmax()

        self.weight_word.data.uniform_(-0.1, 0.1)
        self.weight_proj_word.data.uniform_(-0.1, 0.1)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)  # (N, Co, W)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def attn_fc(self, input):
        """format: seq * batch * input_dim"""
        word_squish_a = batch_matmul_bias(input, self.weight_word, self.bias_word,
                                          nonlinearity='tanh')
        word_attn_a = batch_matmul(word_squish_a, self.weight_proj_word)
        word_attn_norm_a = self.softmax_word(word_attn_a.transpose(1, 0))

        # with open('record/record_attn.txt', 'a') as fo:
        #     for i in range(len(word_attn_norm_a[0])):
        #         fo.write(str('%.2f ' % word_attn_norm_a.data[0][i]))
        #     fo.write('\n')

        output = attention_mul(input, word_attn_norm_a.transpose(1, 0))
        return output

    def forward(self, x):

        x = self.embed(x)  # (N, W, D)
        if self.args.static:
            x = Variable(x)
        x = x.permute(1, 0, 2)
        x, _ = self.lstm(x)
        x = F.relu(x)
        x = self.attn_fc(x)
        '''
        x1 = self.conv_and_pool(x,self.conv13) #(N,Co)
        x2 = self.conv_and_pool(x,self.conv14) #(N,Co)
        x3 = self.conv_and_pool(x,self.conv15) #(N,Co)
        x = torch.cat((x1, x2, x3), 1) # (N,len(Ks)*Co)
        '''
        x = self.dropout(x)  # (N, len(Ks)*Co)

        logit = self.fc1(x)  # (N, C)

        # TODO: softmax(logit)
        logit = nn.functional.softmax(logit)
        # with open('record/record_prediction.txt', 'a') as fo:
        #     for i in range(len(logit[0])):
        #         fo.write(str('%.2f ' % logit.data[0][i]))
        #     fo.write('\n')
        return logit
