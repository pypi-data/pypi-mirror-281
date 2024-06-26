
import gradio as gr
from app import demo as app
import os

_docs = {'PipelineSelector': {'description': 'Enable the user to select a pipeline and edit its hyperparameters', 'members': {'__init__': {'pipelines': {'type': 'pyannote.audio.core.pipeline.Pipeline| list[str]| dict[str,pyannote.audio.core.pipeline.Pipeline]| tuple[str,pyannote.audio.core.pipeline.Pipeline]| None', 'default': 'value = None', 'description': 'optional'}, 'value': {'type': 'str| Callable| None', 'default': 'value = None', 'description': 'optional'}, 'token': {'type': 'str| None', 'default': 'value = None', 'description': None}, 'label': {'type': 'str| None', 'default': 'value = None', 'description': 'optional'}, 'info': {'type': 'str| None', 'default': 'value = None', 'description': 'optional'}, 'every': {'type': 'float| None', 'default': 'value = None', 'description': 'optional'}, 'show_label': {'type': 'bool', 'default': 'value = True', 'description': 'optional'}, 'show_config': {'type': 'bool', 'default': 'value = False', 'description': 'bool, optional'}, 'enable_edition': {'type': 'bool', 'default': 'value = False', 'description': 'bool, optional'}, 'container': {'type': 'bool', 'default': 'value = True', 'description': 'optional'}, 'scale': {'type': 'int| None', 'default': 'value = None', 'description': 'optional'}, 'min_width': {'type': 'int', 'default': 'value = 160', 'description': 'optional'}, 'interactive': {'type': 'bool| None', 'default': 'value = None', 'description': 'optional'}, 'visible': {'type': 'bool', 'default': 'value = True', 'description': 'optional'}, 'elem_id': {'type': 'str| None', 'default': 'value = None', 'description': 'optional'}, 'elem_classes': {'type': 'list[str]| str| None', 'default': 'value = None', 'description': 'optional'}, 'render': {'type': 'bool', 'default': 'value = True', 'description': 'optional'}}, 'postprocess': {'value': {'type': 'pyannote.audio.core.pipeline.Pipeline| None', 'description': 'instantiated pipeline'}}, 'preprocess': {'return': {'type': 'pyannote.audio.core.pipeline.Pipeline', 'description': 'An instantiated pipeline'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the PipelineSelector changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the PipelineSelector.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the PipelineSelector. Uses event data gradio.SelectData to carry `value` referring to the label of the PipelineSelector, and `selected` to refer to state of the PipelineSelector. See EventData documentation on how to use this event data'}, 'focus': {'type': None, 'default': None, 'description': 'This listener is triggered when the PipelineSelector is focused.'}, 'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the PipelineSelector is unfocused/blurred.'}, 'key_up': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses a key while the PipelineSelector is focused.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'PipelineSelector': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gryannote_pipeline`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.2%20-%20orange">  
</div>

A component allowing a user to select a pipeline from a drop-down list
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gryannote_pipeline
```

## Usage

```python
import gradio as gr
from gradio_pipelineselector import PipelineSelector

with gr.Blocks() as demo:
    pipeline_selector = PipelineSelector()

    pipeline_selector.select(
        fn=pipeline_selector.on_select,
        inputs=pipeline_selector,
        outputs=pipeline_selector,
        preprocess=False,
        postprocess=False,
    )

    pipeline_selector.change(
        fn=pipeline_selector.on_change,
        inputs=pipeline_selector,
        outputs=pipeline_selector,
        preprocess=False,
        postprocess=False,
    )

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PipelineSelector`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PipelineSelector"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["PipelineSelector"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, an instantiated pipeline.
- **As output:** Should return, instantiated pipeline.

 ```python
def predict(
    value: pyannote.audio.core.pipeline.Pipeline
) -> pyannote.audio.core.pipeline.Pipeline| None:
    return value
```
""", elem_classes=["md-custom", "PipelineSelector-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          PipelineSelector: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
