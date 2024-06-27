from ewokscore.task import Task
from ..transformation.numpy_backend import NumpyHomography

try:
    from ..transformation.simpleitk_backend import SimpleITKTransformation

    simpleitk = True
except ImportError:
    simpleitk = False
from ..tests.data import data_for_registration


__all__ = ["Example2DStack"]


class Example2DStack(
    Task,
    input_names=["name", "transformation_type"],
    optional_input_names=["shape", "nimages"],
    output_names=["imagestack", "transformations"],
):
    """Generate example images with successive transformations to test registration methods."""

    def run(self):
        values = self.get_input_values()
        transformation_type = values.pop("transformation_type")
        istack, _, passive = data_for_registration.images(transformation_type, **values)
        self.outputs.imagestack = istack
        if transformation_type in ["displacement_field", "bspline"]:
            if not simpleitk:
                raise ValueError(
                    "displacement field transforms cannot be generated without SimpleITK"
                )
            self.outputs.transformations = [
                SimpleITKTransformation(displacement_field=d) for d in passive
            ]
        else:
            self.outputs.transformations = [NumpyHomography(M) for M in passive]
