cat > scripts/generate_svg.py << 'EOF'
#!/usr/bin/env python3
"""
Generate D3.js-ready SVG map with accurate North Africa Admin-1 boundaries
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def calculate_centroid(coords):
    """Calculate polygon centroid using coordinate averaging"""
    x_sum, y_sum, n = 0, 0, 0
    
    if not coords:
        return 0, 0
    
    for ring in coords:
        for point in ring:
            if len(point) >= 2:
                x_sum += point[0]
                y_sum += point[1]
                n += 1
    
    if n == 0:
        return 0, 0
    
    return round(x_sum / n, 4), round(y_sum / n, 4)

def coords_to_path(coords):
    """Convert GeoJSON coordinates to SVG path data"""
    paths = []
    for ring in coords:
        if len(ring) < 2:
            continue
        points = [f"{x},{y}" for x, y in ring]
        if points:
            paths.append("M" + "L".join(points) + "Z")
    return " ".join(paths)

def process_geometry(geom):
    """Process geometry and return centroid and path data"""
    if geom['type'] == 'Polygon':
        cx, cy = calculate_centroid(geom['coordinates'])
        path_data = coords_to_path(geom['coordinates'])
    elif geom['type'] == 'MultiPolygon':
        all_coords = []
        for poly in geom['coordinates']:
            all_coords.extend(poly)
        cx, cy = calculate_centroid(all_coords)
        path_data = " ".join([coords_to_path(poly) for poly in geom['coordinates']])
    else:
        return None, None, None
    
    return cx, cy, path_data

print("🎨 Generating SVG map...")

# Load simplified GeoJSON data
with open('data/algeria_simplified.geojson', 'r', encoding='utf-8') as f:
    algeria = json.load(f)

with open('data/neighbors_simplified. geojson', 'r', encoding='utf-8') as f:
    neighbors = json.load(f)

# Create SVG root element
svg = ET.Element('svg', {
    'xmlns': 'http://www.w3.org/2000/svg',
    'viewBox': '-12 18 35 25',
    'width': '1200',
    'height': '1000'
})

# Add CSS styles
style = ET.SubElement(svg, 'style')
style.text = """
    path { fill: #e0e0e0; stroke: #fff; stroke-width: 0.05; }
    path: hover { fill: #ffa726; }
    . country-DZ path { fill: #4fc3f7; }
    . country-MA path { fill: #d4e157; }
    .country-TN path { fill: #ffb74d; }
    .country-LY path { fill: #ff8a65; }
    .country-ML path { fill: #a1887f; }
    .country-NE path { fill: #90a4ae; }
    . country-MR path { fill: #aed581; }
"""

# Process Algeria (58 wilayas)
print("Processing Algeria...")
g_algeria = ET.SubElement(svg, 'g', {'id': 'country-DZ', 'class': 'country-DZ'})

wilaya_count = 0
for feature in algeria['features']:
    props = feature['properties']
    geom = feature['geometry']
    
    name = props. get('NAME_1', 'Unknown')
    code = props.get('HASC_1', '').replace('DZ. ', 'DZ-')
    
    if not code or code == 'DZ-':
        code = f"DZ-{wilaya_count+1:02d}"
    
    cx, cy, path_data = process_geometry(geom)
    
    if not path_data:
        continue
    
    path = ET.SubElement(g_algeria, 'path', {
        'id': code,
        'data-name': name,
        'data-country': 'Algeria',
        'data-cx': str(cx),
        'data-cy': str(cy),
        'd': path_data
    })
    
    title = ET.SubElement(path, 'title')
    title.text = name
    
    wilaya_count += 1

print(f"✅ Algeria:  {wilaya_count} wilayas processed")

# Process neighboring countries
country_map = {
    'Morocco': 'MA',
    'Tunisia': 'TN',
    'Libya':  'LY',
    'Mali': 'ML',
    'Niger': 'NE',
    'Mauritania': 'MR'
}

for country_name, iso in country_map.items():
    print(f"Processing {country_name}...")
    g_country = ET.SubElement(svg, 'g', {'id': f'country-{iso}', 'class': f'country-{iso}'})
    
    count = 0
    for feature in neighbors['features']:
        props = feature['properties']
        
        if props.get('admin') != country_name:
            continue
        
        geom = feature['geometry']
        name = props.get('name', 'Unknown')
        code = props.get('iso_3166_2', f"{iso}-{count: 02d}")
        
        cx, cy, path_data = process_geometry(geom)
        
        if not path_data: 
            continue
        
        path = ET.SubElement(g_country, 'path', {
            'id': code,
            'data-name': name,
            'data-country': country_name,
            'data-cx': str(cx),
            'data-cy': str(cy),
            'd': path_data
        })
        
        title = ET.SubElement(path, 'title')
        title.text = name
        
        count += 1
    
    print(f"✅ {country_name}: {count} provinces processed")

# Pretty print XML
xml_str = minidom.parseString(ET.tostring(svg, encoding='unicode')).toprettyxml(indent="  ")

# Remove XML declaration and clean up
lines = [line for line in xml_str. split('\n') if line.strip() and not line.startswith('<? xml')]
xml_str = '\n'.join(lines)

# Write to output file
with open('output/world-admin1-north-africa. svg', 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("\n✅ SVG generated:  output/world-admin1-north-africa.svg")
print(f"📊 Total wilayas: {wilaya_count}")
EOF

chmod +x scripts/generate_svg.py