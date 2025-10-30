---
title: "Attention Is All You Need"
paper_title: "Attention Is All You Need"
paper_authors: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin"
paper_venue: "NeurIPS"
paper_year: 2017
paper_link: https://arxiv.org/abs/1706.03762
paper_code: https://github.com/jadore801120/attention-is-all-you-need-pytorch
paper_tags:
  - transformers
  - sequence-to-sequence
  - attention
key_takeaways: |
  - The Transformer discards recurrence in favor of stacked self-attention blocks that scale well on modern hardware.
  - Multi-head attention lets the model jointly attend to information from different representation subspaces.
  - Positional encodings inject order without recurrence, enabling parallel training and efficient long-range modeling.
  - Label smoothing and residual connections play an outsize role in stabilizing deep attention stacks.
  - Transformer achieves state-of-the-art machine translation with significantly less training cost than RNN counterparts.
read_time: 6
---

## Why this paper

Transformers define the modern baseline for sequence transduction tasks. Re-reading the original paper helps anchor later architectural tweaks--especially when evaluating claims about scaling behaviour or inductive bias.

## Model core

Each encoder layer alternates multi-head self-attention with a position-wise feed-forward network. LayerNorm and residual connections wrap both sub-layers, enforcing stable gradients through depth. The decoder mirrors this structure but introduces causal masking and encoder-decoder attention so generated tokens can condition on the source sequence.

## Training recipe

- Datasets: WMT 2014 English<->French and English<->German.
- Tokenization: 37k BPE merges with shared vocabulary.
- Optimization: Adam with warm-up (4,000 steps) and inverse-square-root decay; label smoothing epsilon = 0.1.
- Regularization: Dropout at 0.1 applied to attention weights and residual paths.

The parallel nature of self-attention enabled training on eight P100 GPUs in 3.5 days--already competitive with heavily optimized RNN systems at the time.

## Results snapshot

Translation quality improved BLEU by 2-3 points over GNMT while using significantly fewer FLOPs. Performance gains held across both translation directions, highlighting the architecture's generality.

## Open questions for replication

1. How do modern optimizers (Lion, AdaFactor) shift convergence speed on today's hardware?
2. Does rotary positional encoding (RoPE) plug into the original architecture cleanly, or are there edge cases for decoding length generalization?
3. What training efficiency gains remain when switching to multiquery or grouped-query attention?

## Implementation notes

- Weight initialization: Xavier uniform in all linear layers.
- Scaling factors: attention logits scaled by 1/sqrt(d_k).
- Beam search: width 4 or 6 with length penalty alpha = 0.6 performed best on validation BLEU.

Capturing these details ensures reproducibility when benchmarking new architectural tweaks against the classic Transformer baseline.
