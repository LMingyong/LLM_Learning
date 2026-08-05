# DeltaNet 原点 · 速记

## 一句话

Linear Attention 的矩阵状态是一块有限联想记忆；只会加外积会在超容量时串扰，所以要把写入换成 delta rule。

## 三板斧

1. **等价**：因果 Linear Attention ≡ Fast Weight Programmer（加性外积写 \(W\)，用 \(q\) 读）。  
2. **容量**：互不干扰的 key 数 \(\le d_{\mathrm{dot}}=\dim\phi(k)\)；更长序列进入 overcapacity。  
3. **指令**：\(W\leftarrow W+\beta(v-\bar v)\otimes\phi(k)\)，\(\bar v=W\phi(k)\)，\(\beta\in(0,1)\)。

## 和后文分工

- 本页只有 **β**（改多狠）。  
- Gated DeltaNet 再乘全局 **α**（忘多快）。  
- KDA 把 α 换成 **Diag(α)**（按通道忘）。  
- 2024 并行文解决的是 **怎么算得快**，不是另起一套理论。

## 读法

先看精读页「导读」四段 + 公式墙，再对照 PDF §3–4；实验与 DPFP 可略读。
