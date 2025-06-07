# Neuromorphic Intermediate Representation Visualisation Tool

Turn your NIR definitions into a nice graph, the original publication serving as a template.

Customise your node colour preferences in [style.yml](./style.yml), and quickly generate graphs from your neuromorphic networks.

This work is in progress.

## Running Example
By running the following code (from a notebook),
```python
import nir
import nirviz
import numpy as np


a = np.random.randn(2)
ir = nir.NIRGraph(
    nodes={
        "input": nir.Input(input_type=np.array([2])),
        "affine1": nir.Affine(weight=np.zeros((2,2)), bias=False),
        "cu1": nir.CubaLIF(tau_mem=a, tau_syn=a, r=a, v_leak=a, v_threshold=a, v_reset=a),
        "affine_rec": nir.Affine(weight=np.zeros((2,2)), bias=False),
        "affine2": nir.Affine(weight=np.zeros((2,2)), bias=False),
        "cu2": nir.CubaLIF(tau_mem=a, tau_syn=a, r=a, v_leak=a, v_threshold=a, v_reset=a),
        "output": nir.Output(output_type=np.array([2]))
    },
    edges=[("input", "affine1"), ("affine1", "cu1"), ("affine_rec", "cu1"),  ("cu1", "affine_rec"), ("cu1", "affine2"), ("affine2", "cu2"), ("cu2", "output")])

viz = nirviz.visualize(ir)
viz.show()
```

You would get the following visualisation

<picture>
<img alt="nirviz output" src="https://raw.githubusercontent.com/open-neuromorphic/nirviz/main/img/vis.png">
</picture>

Similar to Figure 3 of the publication.

<picture>
<img alt="Figure 3 of NIR paper for comparison to output" src="https://raw.githubusercontent.com/open-neuromorphic/nirviz/main/img/fig3.png">
</picture>
