# Launch notes

## Project introduction

I've published Reliable AI Lab, an open-source reliability engineering toolkit with thirteen Python projects covering output checks, retrieval, agent plans and infrastructure reliability.

The focus is what happens when something goes wrong. An answer changes a number in its source. A plan includes an action that should not run. A service loses capacity. A dataset shifts.

Each project has code, tests and an example you can run locally. The examples use synthetic data, and the default demos do not need an API key or GPU.

Start with Evidence Gate for grounding reliability, Repair Agent for agent reliability, or Inference Twin for AI infrastructure reliability. Try a different input and let me know where the result falls short.

## Demo notes

**Evidence Gate:** Change a number in a cited claim. Show the flag and the source excerpt. Also show a paraphrase the lexical checks do not handle well.

**Repair Agent:** Use a plan with an invalid reference and a blocked restart action. Show the validation errors, repair attempts and final review state. Remove the hypothesis to show the stop condition.

**Inference Twin:** Compare eight servers with a loss of three. Explain the load assumptions, queue growth and prediction error. These are simulated cases, not measurements from a deployed service.

## Posting

Lead with one example and a short screen recording. Link to the project code and include the limitation that matters for that example. Follow each community's posting rules.

Track actual referrals, release downloads, reproducible issues and contributions. Record the date range for any number you share. Use updates to describe work that has actually changed.
