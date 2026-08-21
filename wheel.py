import math
from nicegui import binding, native, ui
from PIL import Image, ImageDraw, ImageOps


hero_classes = {"muse":{"active":-10,"img":"./images/spokes/muse.png"},
                "heir":{"active":-6,"img":"./images/spokes/heir.png"},
                "bard":{"active":-5,"img":"./images/spokes/bard.png"},
                "rogue":{"active":-4,"img":"./images/spokes/rogue.png"},
                "page":{"active":-3,"img":"./images/spokes/page.png"},
                "seer":{"active":-2,"img":"./images/spokes/seer.png"},
                "maid":{"active":-1,"img":"./images/spokes/maid.png"},
                "sylph":{"active":1,"img":"./images/spokes/sylph.png"},
                "mage":{"active":2,"img":"./images/spokes/mage.png"},
                "knight":{"active":3,"img":"./images/spokes/knight.png"},
                "thief":{"active":4,"img":"./images/spokes/thief.png"},
                "prince":{"active":5,"img":"./images/spokes/prince.png"},
                "witch":{"active":6,"img":"./images/spokes/witch.png"},
                "lord":{"active":10,"img":"./images/spokes/lord.png"}}
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

@binding.bindable_dataclass
class Bound_Values:
        multiclass = False
        class1 = 'heir'
        class2 = 'heir'
        multiaspect = False
        aspect1 = 'breath'
        aspect2 = 'breath'
bound_values = Bound_Values()

@ui.page('/')
def root():
    ui.label("Classpect Symbolizer").style("font-size: 400%")
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
            with ui.element('div').classes('relative-position w-60 h-60 bg-gray-200') as canvas:
                # ui.image().bind_source_from(bound_values,"aspect1",backward= lambda e: aspects[str(e)]["img"]).classes('left-20 top-20 w-20 h-20')
                output_image()

@ui.refreshable
def output_image():
    img = Image.new(mode='RGBA',size=(420,420))
    draw = ImageDraw.Draw(img)
    
    bbox = [120,120,300,300]
    cx, cy = 210,210 # The center of the image
    radius = 145 
    resize = (53,110)

    # Classes
    for i in range(24):
        color = aspects[bound_values.aspect2]["ringcolor"] if bound_values.multiaspect and i%2==0 else aspects[bound_values.aspect1]["ringcolor"]
        
        draw.pieslice(bbox,start=-7.5+(i*15),end=7.5+(i*15),fill=color)
        

        spoke = Image.open(hero_classes[bound_values.class2]["img"]).convert("RGBA").resize(resize)
        if not bound_values.multiclass or i%2==0 : 
            spoke = Image.open(hero_classes[bound_values.class1]["img"]).convert("RGBA").resize(resize)
        r,g,b,alpha = spoke.split()
        bw_spoke=spoke.convert("L")
        new_spoke = ImageOps.colorize(bw_spoke, black=color, white=color)
        spoke = Image.merge("RGBA",(*new_spoke.split()[:3],alpha))

        angle_deg = i*15
        angle_rad = math.radians(angle_deg)
        x = cx + int(radius * math.cos(angle_rad))
        y = cy + int(radius * math.sin(angle_rad))

        rot_angle = 270- angle_deg

        rotated_spoke = spoke.rotate(rot_angle, expand=True)
        pw, ph = rotated_spoke.size

        img.paste(rotated_spoke,(x-pw//2,y - ph//2),rotated_spoke)

    # Aspects
    aspect1 = Image.open(aspects[bound_values.aspect1]["img"])
    if bound_values.multiaspect:
        aspect1 = aspect1.crop((0,0,70,140))
        aspect2 = Image.open(aspects[bound_values.aspect2]["img"])
        aspect2 = aspect2.crop((70,0,140,140))
        img.alpha_composite(aspect2,(210,140))
    img.alpha_composite(aspect1,(140,140))
    ui.image(img).classes('w-60 h-60')


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(root,port=native.find_open_port(),favicon="./heir of void.ico",reload=False)  