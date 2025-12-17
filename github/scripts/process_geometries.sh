cat > scripts/process_geometries.sh << 'EOF'
#!/bin/bash
set -e

echo "🌍 Processing geometries..."

cd data

# Reproject Algeria to WGS84
echo "Reprojecting Algeria to WGS84..."
ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 \
  algeria_admin1.geojson \
  gadm41_DZA.gpkg \
  ADM_ADM_1

# Extract neighboring countries (Admin-1) and reproject
echo "Extracting and reprojecting neighboring countries..."
ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 \
  -where "admin='Morocco' OR admin='Tunisia' OR admin='Libya' OR admin='Mali' OR admin='Niger' OR admin='Mauritania'" \
  neighbors_admin1.geojson \
  ne_10m_admin_1_states_provinces.shp

# Simplify Algeria geometries (12% Douglas-Peucker)
echo "Simplifying Algeria geometries (12%)..."
mapshaper algeria_admin1.geojson \
  -simplify dp 12% keep-shapes \
  -clean \
  -o algeria_simplified.geojson

# Simplify neighbor geometries (12% Douglas-Peucker)
echo "Simplifying neighbor geometries (12%)..."
mapshaper neighbors_admin1.geojson \
  -simplify dp 12% keep-shapes \
  -clean \
  -o neighbors_simplified. geojson

echo "✅ Geometry processing complete"

cd ..
EOF

chmod +x scripts/process_geometries.sh