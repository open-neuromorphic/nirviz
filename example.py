import nir
import nirviz
import numpy as np

a = np.random.randn(2)

cuba_params = {'type': 'CubaLIF', 'tau_mem': a, 'tau_syn': a, 'r': a, 'v_leak': a, 'v_threshold': a}
affine_params = {'type': 'Affine', 'weight': np.zeros((2,2)), 'bias': False}

ir = nir.NIRGraph(
    nodes={
        "input": nir.Input(input_type=np.array([2])),
        "affine1": nir.Affine.from_dict(affine_params),
        "cu1": nir.CubaLIF.from_dict(cuba_params),
        "affine_rec": nir.Affine.from_dict(affine_params),
        "affine2": nir.Affine.from_dict(affine_params),
        "cu2": nir.CubaLIF.from_dict(cuba_params),
        "output": nir.Output(output_type=np.array([2]))
    },
    edges=[("input", "affine1"), ("affine1", "cu1"), ("affine_rec", "cu1"),  ("cu1", "affine_rec"), ("cu1", "affine2"), ("affine2", "cu2"), ("cu2", "output")])



viz = nirviz.visualize(ir, draw_direction="left-right").to_image()
viz.save("./img/srnn.png")
viz.show()
