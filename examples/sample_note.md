# Transformer Architecture Notes

## Overview

The Transformer is a deep learning architecture introduced in the paper "Attention Is All You Need" (Vaswani et al., 2017). It revolutionized natural language processing by replacing recurrent neural networks with self-attention mechanisms.

## Key Components

### Self-Attention

Self-attention allows the model to weigh the importance of different words in a sentence when processing each word. The attention mechanism computes:

- Query (Q): what the current word is looking for
- Key (K): what each word offers
- Value (V): the actual content of each word

The attention score is computed as: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V

### Multi-Head Attention

Instead of using a single attention function, the Transformer uses multiple attention heads. This allows the model to attend to information from different representation subspaces at different positions.

### Feed-Forward Networks

Each Transformer layer contains a position-wise feed-forward network, which consists of two linear transformations with a ReLU activation in between.

### Positional Encoding

Since the Transformer has no recurrence, positional encodings are added to the input embeddings to give the model information about the position of each token in the sequence.

## Applications

Transformers have been successfully applied to:

- Machine translation
- Text summarization
- Question answering
- Text generation
- Image recognition (Vision Transformer)
- Code generation

## Questions to Explore

1. How does self-attention differ from traditional attention mechanisms?
2. Why is the scaling factor sqrt(d_k) used in the attention formula?
3. What are the advantages of multi-head attention over single-head attention?
4. How do positional encodings help the model understand sequence order?
