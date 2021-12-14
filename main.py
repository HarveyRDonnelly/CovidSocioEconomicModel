"""
DOCSTRING

TODO: main run file
"""

import modules.preprocessing as p
import modules.visualizer as v
preprocessing_system = p.PreprocessingSystem()
preprocessing_system.init_toronto_model()
visual_system = v.RegionVisual(preprocessing_system)
visual_system.toronto_scatter_visual()
visual_system.toronto_heatmap('Covid')
visual_system.toronto_heatmap('Income')
