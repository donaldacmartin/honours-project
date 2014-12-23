from utilities.shapefile import Reader
from Image import new
from ImageDraw import Draw
from graphs.atlas.atlas_map import map_lat_to_y_coord, map_lon_to_x_coord

img = new("RGB", (400, 400), "white")
draw = Draw(img)

reader = Reader("utilities/data/country_outlines/countries")

for shape in reader.shapeRecords():
    points  = shape.shape.points
    outline = []
    
    for point in points:
        lon = point[0]
        lat = point[1]
        
        x = map_lon_to_x_coord(lon, 400)
        y = map_lat_to_y_coord(lat, 400)
        
        outline.append((x,y))
        
    draw.polygon(outline, outline="black")
    
img.save("test.png", "PNG")