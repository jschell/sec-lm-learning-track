# Generation and sampling

Status: **proposed** after the messages module; no pretrained model/runtime selected yet.

## Question and goal

What happens during inference before a harness receives a response? Inspect text → tokens → model computation → next-token scores → sampling → appended token → repetition.

Use one small pretrained model that exposes next-token scores. CPU-friendly learning scope; no training or coding-agent capability is required. Record model/revision, tokenizer, runtime, license, and practical resource needs when implemented.

## Experiments to author

Hold the prompt fixed and inspect a short next-token distribution. Compare greedy selection with supported sampling settings. Repeat a seeded run and explain the runtime-specific limits of reproducibility. Demonstrate an output limit and termination marker. State which computation is model inference, which choice is runtime sampling, and which state belongs to the harness.

A short conceptual section distinguishes pretraining, assistant/tool-oriented training, and inference. Explain that supplying context ordinarily does not update weights. Backpropagation and implementing transformers remain optional branches.

Finish when the learner can explain one generated token, change sampling deliberately, and distinguish this loop from Track 1's application loop. No model ranking or general reliability claim follows from the exercise.

## Original sources

[Karpathy's Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI), [makemore](https://github.com/karpathy/makemore), and [Zero to Hero](https://karpathy.ai/zero-to-hero.html). Exact runtime/model documentation will be cited when selected. Exercise scope and sequencing are project design.

[Collection](../../README.md) · [Queued plan](../../docs/plans/queue/04-generation-and-sampling.md)
