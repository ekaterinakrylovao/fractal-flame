from src.transformations import (SinusoidalTransformation, SphericalTransformation, SwirlTransformation,
                                 PolarTransformation, HandkerchiefTransformation, HeartTransformation,
                                 DiscTransformation, SpiralTransformation, HyperbolicTransformation,
                                 DiamondTransformation, PopcornTransformation, PDJTransformation, CurlTransformation)

TRANSFORMATIONS_MAP = {
    "SinusoidalTransformation": SinusoidalTransformation,
    "SphericalTransformation": SphericalTransformation,
    "SwirlTransformation": SwirlTransformation,
    "PolarTransformation": PolarTransformation,
    "HandkerchiefTransformation": HandkerchiefTransformation,
    "HeartTransformation": HeartTransformation,
    "DiscTransformation": DiscTransformation,
    "SpiralTransformation": SpiralTransformation,
    "HyperbolicTransformation": HyperbolicTransformation,
    "DiamondTransformation": DiamondTransformation,
    "PopcornTransformation": PopcornTransformation,
    "PDJTransformation": PDJTransformation,
    "CurlTransformation": CurlTransformation,
}

TRANSFORMATION_PARAMS = {
    "SinusoidalTransformation": "scale_x=1.0, scale_y=1.0",
    "SphericalTransformation": "",
    "SwirlTransformation": "",
    "PolarTransformation": "angle_scale=1.0, radius_offset=0.0",
    "HandkerchiefTransformation": "",
    "HeartTransformation": "",
    "DiscTransformation": "",
    "SpiralTransformation": "",
    "HyperbolicTransformation": "scale=1.0, jitter=0.01",
    "DiamondTransformation": "scale=1.0, jitter=0.07",
    "PopcornTransformation": "c=0.5, d=0.5",
    "PDJTransformation": "a=1.0, b=1.0, c=1.0, d=1.0",
    "CurlTransformation": "p=0.5, q=0.5",
}
