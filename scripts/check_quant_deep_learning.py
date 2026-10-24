import torch,math,html,re
from pathlib import Path
T=torch.float64
cases=[(torch.optim.SGD,{},.57),(torch.optim.SGD,{"momentum":.9},.84),(torch.optim.Adagrad,{"eps":0},.169502),(torch.optim.RMSprop,{"alpha":.9,"eps":0},.533179),(torch.optim.Adam,{"eps":0},.199897)]
for cls,kw,expected in cases:
 w=torch.nn.Parameter(torch.tensor(0.,dtype=T));o=cls([w],lr=.1,**kw)
 for _ in range(2):o.zero_grad();((w-3)**2/2).backward();o.step()
 assert abs(w.item()-expected)<1e-6,(cls,w.item(),expected)
for cls,expected in [(torch.optim.Adam,1.9),(torch.optim.AdamW,1.88)]:
 w=torch.nn.Parameter(torch.tensor(2.,dtype=T));o=cls([w],lr=.1,eps=0,weight_decay=.1);w.grad=torch.ones_like(w);o.step();assert abs(w.item()-expected)<1e-8
p=(Path(__file__).resolve().parents[1]/"notes/quant-foundations/deep-learning.html").read_text();ns={"__name__":"textbook_test"}
for code in re.findall(r"<pre><code[^>]*>(.*?)</code></pre>",p,re.S):exec(html.unescape(code),ns)
torch.manual_seed(2);a=torch.nn.Linear(2,1);b=torch.nn.Linear(2,1);b.load_state_dict(a.state_dict());loader=[(torch.randn(2,2),torch.randn(2,1)) for _ in range(5)]
o1=torch.optim.SGD(a.parameters(),lr=.1);o2=torch.optim.SGD(b.parameters(),lr=.1)
ns["train_epoch"](a,loader,o1,None,"cpu",accum=2)
for j in range(0,5,2):
 x=torch.cat([v[0] for v in loader[j:j+2]]);y=torch.cat([v[1] for v in loader[j:j+2]]);o2.zero_grad();torch.nn.functional.mse_loss(b(x),y).backward();torch.nn.utils.clip_grad_norm_(b.parameters(),1.);o2.step()
assert all(torch.allclose(x,y,atol=1e-6) for x,y in zip(a.parameters(),b.parameters()))
print("optimizer two-step values, decay distinction, accumulation remainder: passed")

model=ns["CausalRegressor"]().eval()
x=torch.randn(2,8,3); captured=[]
hook=model.encoder.register_forward_hook(lambda module,args,output:captured.append(output.detach().clone()))
y=model(x);assert y.shape==(2,1)
x2=x.clone();x2[:,4:]+=100;model(x2)
assert torch.allclose(captured[0][:,:4],captured[1][:,:4],atol=1e-6), "future token affected prefix"
hook.remove();model.train();model(x).square().mean().backward()
assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
assert model(torch.randn(2,1,3)).shape==(2,1)
try:model(torch.randn(2,65,3))
except ValueError:pass
else:raise AssertionError("max_len guard failed")
h0=torch.tensor(0.,requires_grad=True,dtype=T);h1=torch.tanh(1+.5*h0);h2=torch.tanh(.5*h1);h2.backward();assert abs(h0.grad.item()-.0911)<1e-4
assert sum(p.numel() for p in torch.nn.LSTM(2,3).parameters())==84
print("model shapes, finite gradients, future-prefix isolation, max length, BPTT and LSTM count: passed")

# A routed mixture must ignore outputs and gradients of unselected experts.
scores=torch.tensor([[.6,.3,.2,.1]],requires_grad=True)
expert=torch.randn(1,4,2,requires_grad=True)
mixture,index,weight=ns["route_topk"](scores,expert)
mixture.sum().backward();assert expert.grad[:,2:].abs().sum()==0
# Per-horizon document masking: changing the score that crosses a boundary
# must not alter the loss or its gradients.
tokens=torch.tensor([[0,1,2,3]])
segments=torch.tensor([[0,0,1,1]])
logits=torch.randn(1,4,4,requires_grad=True)
loss=ns["parallel_mtp_loss"]([logits],tokens,segments)
loss.backward();assert logits.grad[0,1].abs().sum()==0
manual=torch.nn.functional.cross_entropy(logits[0,[0,2]],tokens[0,[1,3]])
assert torch.allclose(loss,manual)
try:ns["parallel_mtp_loss"]([torch.zeros(1,4,4)],torch.full((1,4),-100))
except ValueError:pass
else:raise AssertionError("all-padding head was accepted")
# The same shared block receives a different number of visits, not copies.
loop=ns["Looped"]();nparams=sum(p.numel() for p in loop.parameters())
for rounds in [1,4]:assert loop(torch.randn(2,5,8),rounds).shape==(2,5,8)
assert sum(p.numel() for p in loop.parameters())==nparams
print("MoE selected gradients, packed-MTP masks, empty targets, loop parameter reuse: passed")
