from utilities.shapefile import Reader
from Image import new
from ImageDraw import Draw

img = new("RGB", (400, 400), "white")
draw = Draw(img)

reader = Reader("utilities/data/country_outlines/countries")

for shape in reader.shapeRecords():
    points  = shape.shape.points
    outline = []
    
    for point in points:
        lon = point[0]
        lat = point[1]
        outline.append((lon, lat))
        
    draw.polygon(outline, outline="black")
    
img.save("test.png", "PNG")