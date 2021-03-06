"""
Algebraically based lint rules
"""

import os
from diffimg import diff

def passes_only_data_driven_visuals(axes, fig, config_value):
    """
    Lint rule for representation-invariance
    """
    # some how figure out which type of thing is being drawn?
    if len(axes.collections) >= 1:
        fig.savefig('source.png')
        # flip the order in every collection
        for idx in range(len(axes.collections)):
            axes.collections[idx].set_offsets(axes.collections[idx].get_offsets()[::-1])

        fig.savefig('test.png')
        # flip the order back
        for idx in range(len(axes.collections)):
            axes.collections[idx].set_offsets(axes.collections[idx].get_offsets()[::-1])
        delta = diff('source.png', 'test.png', delete_diff_file=True, diff_img_file='diff_img.jpg')

        os.remove('source.png')
        os.remove('test.png')
        return delta < config_value

    children = axes.get_children()
    if len(children) == 0:
        return True

    fig.savefig('source.png')
    # flip the order in every collection
    original_order = [child.get_zorder() for child in children]
    for idx in range(len(children)):
        children[idx].set_zorder(len(original_order) - idx)

    fig.savefig('test.png')
    # flip the order back
    delta = diff('source.png', 'test.png', diff_img_file='diff_img.jpg')
    for idx in range(len(children)):
        children[idx].set_zorder(original_order[idx])

    os.remove('source.png')
    os.remove('test.png')
    return delta <= config_value
