cat > scripts/download_data. sh << 'EOF'
#!/bin/bash
set -e

echo "📥 Downloading GIS data..."

cd data

# Download GADM Algeria (Admin-1)
echo "Downloading GADM Algeria v4.1..."
if [ ! -f "gadm41_DZA. gpkg" ]; then
  wget -O gadm41_DZA. gpkg "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_DZA.gpkg"
  echo "✅ Algeria data downloaded"
else
  echo "✅ Algeria data already exists"
fi

# Download Natural Earth Admin-1
echo "Downloading Natural Earth Admin-1 (10m)..."
if [ ! -f "ne_10m_admin_1_states_provinces. shp" ]; then
  wget -O ne_10m_admin_1.zip "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces.zip"
  unzip -o ne_10m_admin_1.zip
  rm ne_10m_admin_1.zip
  echo "✅ Natural Earth data downloaded and extracted"
else
  echo "✅ Natural Earth data already exists"
fi

# Validate downloads
if [ -f "gadm41_DZA.gpkg" ] && [ -f "ne_10m_admin_1_states_provinces.shp" ]; then
  echo "✅ All data downloaded successfully"
  ls -lh *.gpkg *.shp 2>/dev/null || true
else
  echo "❌ Error: Missing required files"
  exit 1
fi

cd ..
EOF

chmod +x scripts/download_data.sh