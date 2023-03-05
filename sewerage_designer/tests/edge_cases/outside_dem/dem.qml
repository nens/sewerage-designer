<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" version="3.16.10-Hannover">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal mode="0" enabled="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling zoomedInResamplingMethod="nearestNeighbour" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
    </provider>
    <rasterrenderer classificationMax="12.5500002" alphaBand="-1" nodataColor="" opacity="1" type="singlebandpseudocolor" band="1" classificationMin="5.6300001">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="1" labelPrecision="4" minimumValue="5.6300001" clip="0" maximumValue="12.5500002" colorRampType="INTERPOLATED">
          <colorramp name="[source]" type="gradient">
            <prop v="1,133,113,255" k="color1"/>
            <prop v="166,97,26,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.25;128,205,193,255:0.5;245,245,245,255:0.75;223,194,125,255" k="stops"/>
          </colorramp>
          <item alpha="255" color="#018571" label="5.6300" value="5.630000114440918"/>
          <item alpha="255" color="#80cdc1" label="7.3600" value="7.360000133514404"/>
          <item alpha="255" color="#f5f5f5" label="9.0900" value="9.09000015258789"/>
          <item alpha="255" color="#dfc27d" label="10.8200" value="10.820000171661377"/>
          <item alpha="255" color="#a6611a" label="12.5500" value="12.550000190734863"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeStrength="100" saturation="0" colorizeGreen="128" colorizeOn="0" grayscaleMode="0" colorizeBlue="128" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
