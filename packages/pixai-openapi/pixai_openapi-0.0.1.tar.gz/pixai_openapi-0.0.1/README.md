# Pixai_api_linker
A small program to connect to `pixai api` 

### future features
- [ ] A pypi package with the basic features
- [ ] other possible features

### current features
- [x] link to api & generate/get pictures

### example code
```python
from pixai_openapi import *
import time

if __name__ == '__main__':
    pass

define_apikey('sk-Hgb11p61PWts/Da6v1RC3y7v089s6KjOcJzyHOzmxQhQjoFS')

genpic_data = gen_pic({
    "prompts":
        """GTS, GigaGTS, Cramped, PlanetaryGTS, Looming,solo,
    (((a giant girl))),(((a giant girl treads on a mini city))),1girl,
    (loli,wariza:1.5), cute girl,(((extremely kawaii girl))),((fill the screen)),
    full body,day:1.9,proving Earth is flat,horizon, city:2.8,(loli,small breasts),giantess
    , size difference, tall female,<lora:more_details:1>,giantess, size difference, tall female
    1girl, solo, long hair, looking at viewer, blush, smile, bangs, blue eyes, blonde hair,
    hair ornament, gloves, long sleeves, dress, sitting, very long hair, full body, braid, heart,
     multicolored hair, medium breasts, frills, wings, barefoot, fingerless gloves, nail polish,
     white dress, two side up,streaked hair, book, symbol-shaped pupils, thigh strap, halo, feathers,""",
    "enableTile": False,
    "negativePrompts": '(worst quality, low quality, large head, extra digits:1.4), easynegative,',
    "samplingSteps": 12,
    "samplingMethod": "Euler a",
    "cfgScale": 5,
    "modelId": "1648918115270508582",
    "width": 512,
    "height": 768,
    "batchSize": 4,
    "lora": {
        "More details": 1632808153143363282,
        "Giantess/Size Difference, Sizeplay Concept LoRA by SaRrow": 1664117894070404490
    }
})
time.sleep(25)
get_pic(get_pic_mediaid(genpic_data))

```