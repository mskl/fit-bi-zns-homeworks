# Knowledge systems homeworks
I did all the homeworks except the last, bonus one. The code is somewhat messy and it reflects my attitude to this course. (Which was imo waste of time.) The supplied Java framework was painful to use, and it was in Java, so I rather decided to do it all myself in Python.

## Assignments
### Knowledge base (5/5)
> Create a knowledge base for a future knowledge system. Create also a visualization of the base.

Knowledge base for a bike repair shop. At least I have used my Python graph for this.

### Inference mechanism (10/10)
> Create an inference mechanism that works on the knowledge base created in the previous homework.

System that interactively asks user and determines what makes a noise on a bicycle. Works pretty well I think. It works by cutting the tree of the possible results.

### Inference with uncertainty (10/10)
> Add uncertainty to the knowledge base and a system.

Uncertainty based on the PROSPECTOR-based approach. Quite messy as I was applying it to the previous code which was designed to work in a different way. If you are from the future, be careful, this is not based directly on the bayes rule and if detected by the teacher, you might get in trouble. However, I did not come up with a way to use bayes rule uncertainty in a system with only AND relationships. The Results were always 0/1, which did not help anything.

### Fuzzy logic (10/10)
> Create a fuzzy logic inference system.

I created a fuzzy logic system to rate orienteering races in different criteria. Some implementation ideas came from the SKlearn fuzzy logic module, but highly simplified.

### NeuralNetwork + knowledge extraction to a tree with TREPAN algorithm (0/15)

> First make and train a neural network and then extract the knowledge to a tree with TREPAN algorithm.

Extra homework which I did not make.
