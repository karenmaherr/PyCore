import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from sklearn.utils.class_weight import compute_class_weight
import joblib
from sklearn.metrics import accuracy_score,classification_report
files= [
"Tuesday-WorkingHours.pcap_ISCX.csv",
"Wednesday-workingHours.pcap_ISCX.csv",
"Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
"Friday-WorkingHours-Morning.pcap_ISCX.csv",
"Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
"Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"]
d=[]
for file in files:
    data= pd.read_csv(file)
    data.columns= data.columns.str.strip()
    d.append(data)
df=pd.concat(d,ignore_index=True)
df=df.drop_duplicates()
df.replace([np.inf,-np.inf],np.nan,inplace=True)
df=df.dropna()
device='cuda' if torch.cuda.is_available() else 'cpu'
mapping= {
"DoS Hulk":"DoS",
"DoS GoldenEye":"DoS",
"DoS slowloris":"DoS",
"DoS Slowhttptest":"DoS",
"DDoS":"DoS",
"Web Attack � Brute Force":"Web Attack",
"Web Attack � XSS": "Web Attack",
"Web Attack � Sql Injection": "Web Attack"}
df['Label']=df['Label'].replace(mapping)
df= df[df["Label"]!="Heartbleed"]
y=df['Label']
x=df.drop('Label',axis=1)
x_train,x_temp,y_train,y_temp=train_test_split(x,y,test_size=0.30,random_state=42,stratify=y)
x_val,x_test,y_val,y_test=train_test_split(x_temp,y_temp,test_size=0.50,random_state=42,stratify=y_temp)
encoder= LabelEncoder()
y_train=encoder.fit_transform(y_train)
y_val= encoder.transform(y_val)
y_test =encoder.transform(y_test)
scaler=StandardScaler()
x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)
x_val=scaler.transform(x_val)
class_weights = compute_class_weight(
class_weight="balanced",classes=np.unique(y_train), y=y_train)
class_weights = np.sqrt(class_weights)
unique_classes, counts = np.unique(y_train, return_counts=True)
class_weights= torch.tensor(class_weights, dtype=torch.float32).to(device)
x_train=torch.tensor(x_train,dtype=torch.float32)
x_test=torch.tensor(x_test,dtype=torch.float32)
x_val=torch.tensor(x_val,dtype=torch.float32)
y_train=torch.tensor(y_train,dtype=torch.long)
y_test=torch.tensor(y_test,dtype=torch.long)
y_val=torch.tensor(y_val,dtype=torch.long)
def make_sequences(x_tensor, y_tensor, seq_len=6):
    x_seq= x_tensor.unfold(0, seq_len, 1).transpose(1, 2)
    y_seq= y_tensor[seq_len-1:]
    return x_seq,y_seq
x_train,y_train = make_sequences(x_train, y_train)
x_val, y_val= make_sequences(x_val, y_val)
x_test, y_test = make_sequences(x_test, y_test)
train_dataset= TensorDataset(x_train, y_train)
val_dataset= TensorDataset(x_val,y_val)
test_dataset= TensorDataset(x_test, y_test)
train= DataLoader(
    train_dataset,
    batch_size=3050,
    shuffle=True)
val= DataLoader(
    val_dataset,
    batch_size=3050,
    shuffle=False)
test= DataLoader(
    test_dataset,
    batch_size=3050,
    shuffle=False)
class cyber(nn.Module):
    def __init__(self):
        super().__init__()
        self.network=nn.LSTM(input_size=78,hidden_size=70,num_layers=1,batch_first=True)
        self.fc=nn.Linear(70,7)
    def forward(self,x):
        out, _ = self.network(x)
        out= out[:,-1,:]
        out = self.fc(out)
        return out
model=cyber().to(device)
los=nn.CrossEntropyLoss(weight=class_weights)
opt=torch.optim.Adam(model.parameters(),lr=0.001)
epochs=10
for e in range(epochs):
    model.train()
    total_train_loss=0
    for xbatch,ybatch in train:
        x=xbatch.to(device)
        y=ybatch.to(device)
        log=model(x)
        loss=los(log,y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        total_train_loss+= loss.item()
    avg_train_loss= total_train_loss/len(train)
    print(f"Average training loss:{avg_train_loss}")
    with torch.no_grad():
        model.eval()
        total_val_loss=0
        for xbatch,ybatch in val:
            x=xbatch.to(device)
            y=ybatch.to(device)
            log=model(x)
            loss=los(log,y)
            total_val_loss+= loss.item()
        avg_val_loss= total_val_loss/len(val)
        print(f"Average validation loss:{avg_val_loss}")
pre=[]
true=[]
with torch.no_grad():
    for xbatch,ybatch in test:
        x=xbatch.to(device)
        y=ybatch.to(device)
        log=model(x)
        loss=los(log,y)
        predicted=torch.argmax(log,dim=1)
        pre.extend(predicted.cpu().numpy())
        true.extend(y.cpu().numpy())
print("Accuracy and classification report:")
print(accuracy_score(true,pre),"\n")
print(classification_report(true,pre,target_names=encoder.classes_))

torch.save(model.state_dict(),"lstm_model.pth")
joblib.dump(scaler,"scaler.pkl")
joblib.dump(encoder,"encoder.pkl")