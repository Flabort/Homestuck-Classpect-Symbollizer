import math
from nicegui import binding, native, ui
from PIL import Image, ImageDraw, ImageOps

# First, define the images we need, and some other things, for each possible choice
# Such as if classes should be outwards spokes or inwards (should_invert). Right now inverting isn't implimented, leading to the cause of Github Issue #1
# Or what color the spokes should be based on aspect
# The active value from -10 to 10 currently does nothing. I just included it just because.
hero_classes = {"muse":{"active":-10,"img":"./images/spokes/muse.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "heir":{"active":-6,"img":"./images/spokes/heir.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "bard":{"active":-5,"img":"./images/spokes/bard.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "rogue":{"active":-4,"img":"./images/spokes/rogue.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "page":{"active":-3,"img":"./images/spokes/page.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "seer":{"active":-2,"img":"./images/spokes/seer.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "maid":{"active":-1,"img":"./images/spokes/maid.png","should_invert":False},
                "sylph":{"active":1,"img":"./images/spokes/sylph.png","should_invert":True,"invert":"./images/spokes/lord.png"},
                "mage":{"active":2,"img":"./images/spokes/mage.png","should_invert":False},
                "knight":{"active":3,"img":"./images/spokes/knight.png","should_invert":False},
                "thief":{"active":4,"img":"./images/spokes/thief.png","should_invert":False},
                "prince":{"active":5,"img":"./images/spokes/prince.png","should_invert":False},
                "witch":{"active":6,"img":"./images/spokes/witch.png","should_invert":False},
                "lord":{"active":10,"img":"./images/spokes/lord.png","should_invert":False}}
aspects = {"breath":{"img":"./images/aspects/breath.png","ringcolor":"#85DBF6"},
           "life":{"img":"./images/aspects/life.png","ringcolor":"#99E358"},
           "hope":{"img":"./images/aspects/hope.png","ringcolor":"#FFFFFF"},
           "rage":{"img":"./images/aspects/rage.png","ringcolor":"#8C58AA"},
           "void":{"img":"./images/aspects/void.png","ringcolor":"#34519D"},
           "mind":{"img":"./images/aspects/mind.png","ringcolor":"#85F9CC"},
           "space":{"img":"./images/aspects/space.png","ringcolor":"#FFFFFF"},
           "heart":{"img":"./images/aspects/heart.png","ringcolor":"#AA3262"},
           "blood":{"img":"./images/aspects/blood.png","ringcolor":"#A22D23"},
           "light":{"img":"./images/aspects/light.png","ringcolor":"#F2F870"},
           "doom":{"img":"./images/aspects/doom.png","ringcolor":"#2F4833"},
           "time":{"img":"./images/aspects/time.png","ringcolor":"#DA462C"}}

# This is data that is transmitted and held in the background, with default values, and which is read by the image generator
@binding.bindable_dataclass
class Bound_Values:
        multiclass = False
        class1 = 'heir'
        class2 = 'heir'
        multiaspect = False
        aspect1 = 'breath'
        aspect2 = 'breath'
bound_values = Bound_Values()

# The annotation here isn't actually needed, since this app only consists of one page; but it's good practice, I feel, to define your root page anyways. 
# If I had more pages, like an "about" page or something like that, or an outfit preview, or whatever, then this would be more than decoration.
@ui.page('/')
def root():
    ui.label("Classpect Symbolizer").style("font-size: 400%")
    # A nice thing about NiceGui is the use of With to nest elements, as compared to <div><div><div></div></div></div> (Div Soup)
    with ui.row():
        with ui.card():
            ui.label("Class").style('font-size: 250%')
            class_keys = list(hero_classes.keys())
            with ui.row(align_items='center'):
                ui.checkbox(on_change=output_image.refresh).bind_value(bound_values,"multiclass")
                ui.label("Combine classes?")    
            with ui.row(align_items='center'):
                ui.label("Class 1:").bind_visibility_from(bound_values,'multiclass')
                ui.label("Class:").bind_visibility_from(bound_values,'multiclass',backward=lambda e: not e)
                ui.select(class_keys,value=class_keys[1],on_change=output_image.refresh).bind_value(bound_values,'class1')
            with ui.row(align_items='center'):
                ui.label("Class 2:").bind_visibility_from(bound_values,'multiclass')
                ui.select(class_keys,value=class_keys[1],on_change=output_image.refresh).bind_visibility_from(bound_values,'multiclass').bind_value(bound_values,'class2')
        with ui.card():
            ui.label("Aspect").style('font-size: 250%')
            aspect_keys = list(aspects.keys())
            with ui.row(align_items='center'):
                ui.checkbox(on_change=output_image.refresh).bind_value(bound_values,'multiaspect')
                ui.label("Combine aspects?")
            with ui.row(align_items='center'):
                ui.label("Aspect 1:").bind_visibility_from(bound_values,'multiaspect')
                ui.label("Aspect:").bind_visibility_from(bound_values,'multiaspect',backward=lambda e: not e)
                ui.select(aspect_keys,value=aspect_keys[0],on_change=output_image.refresh).bind_value(bound_values,"aspect1")
            with ui.row(align_items='center'):
                ui.label("Aspect 2:").bind_visibility_from(bound_values,'multiaspect')
                ui.select(aspect_keys,value=aspect_keys[0],on_change=output_image.refresh).bind_value(bound_values,"aspect2").bind_visibility_from(bound_values,'multiaspect')
        with ui.card():
            ui.label("Output").style("font-size: 250%")
            with ui.element('div').classes('relative-position w-60 h-60 bg-gray-200'):
                output_image()

# The refreshable annotation means that I can pass output_image.refresh to the interactive elements, and ensure that the image remains updated with each change to classes or aspects
# This function of course creates the composite image and displays it
# No return is nessesary, because the call to ui.<element>, such as ui.image() here, automatically inserts the element wherever the function is called.
@ui.refreshable
def output_image() -> None:
    img_size = 420
    img = Image.new(mode='RGBA',size=(img_size,img_size))
    draw = ImageDraw.Draw(img)
    
    bbox = [120,120,300,300]
    cx, cy = img_size//2,img_size//2 # The center of the image
    radius = 145 
    resize = (53,110)

    # Classes
    for i in range(24):
        color = aspects[bound_values.aspect2]["ringcolor"] if bound_values.multiaspect and i%2==0 else aspects[bound_values.aspect1]["ringcolor"]
        draw.pieslice(bbox,start=-7.5+(i*15),end=7.5+(i*15),fill=color)

        this_class = bound_values.class1
        if not bound_values.multiclass or i%2==0 : 
            this_class = bound_values.class2
        
        spoke = Image.open(hero_classes[this_class]["img"]).convert("RGBA").resize(resize)

        # This exists for masking purposes, maintain the alpha channel of the recolored image after coloring it
        r,g,b,alpha = spoke.split()
        bw_spoke=spoke.convert("L")
        new_spoke = ImageOps.colorize(bw_spoke, black=color, white=color)
        spoke = Image.merge("RGBA",(*new_spoke.split()[:3],alpha))

        # Rotate the image
        angle_deg = i*15
        angle_rad = math.radians(angle_deg)
        x = cx + int(radius * math.cos(angle_rad))
        y = cy + int(radius * math.sin(angle_rad))

        rot_angle = 270- angle_deg

        rotated_spoke = spoke.rotate(rot_angle, expand=True)
        pw, ph = rotated_spoke.size

        # Add the colored and resized spoke to the wheel
        img.paste(rotated_spoke,(x-pw//2,y - ph//2),rotated_spoke)

    # Aspects
    aspect1 = Image.open(aspects[bound_values.aspect1]["img"])
    if bound_values.multiaspect:
        aspect1 = aspect1.crop((0,0,70,140))
        aspect2 = Image.open(aspects[bound_values.aspect2]["img"])
        aspect2 = aspect2.crop((70,0,140,140))
        img.alpha_composite(aspect2,(img_size//2,(img_size//2)-70))
    img.alpha_composite(aspect1,((img_size//2)-70,(img_size//2)-70))
    ui.image(img).classes('w-60 h-60')

# This variation mainguard allows the program to work after compiling with nicegui-pack, which uses PyInstaller
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(root,port=native.find_open_port(),favicon="./heir of void.ico",reload=False)  