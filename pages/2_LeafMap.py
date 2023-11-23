import sys
import leafmap.foliumap as leafmap

print(sys.path)

m = leafmap.Map()
m.add_basemap()
m.add_raster('./raster/fuzzy_complete_3857.tif', cmap="viridis", layer_name="Raster Layer")

m.to_streamlit()
