<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.10-Hannover" hasScaleBasedVisibilityFlag="1" readOnly="0" simplifyLocal="1" simplifyDrawingHints="0" minScale="10000" simplifyDrawingTol="1" styleCategories="AllStyleCategories" simplifyMaxScale="1" maxScale="0" simplifyAlgorithm="0" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startField="" durationUnit="min" enabled="0" mode="0" durationField="" startExpression="" accumulate="0" fixedDuration="0" endField="" endExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" name="0" clip_to_extent="1" force_rhr="0" type="marker">
        <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.5"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="3"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="&quot;fid&quot;" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory penAlpha="255" backgroundColor="#ffffff" height="15" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" spacing="5" maxScaleDenominator="1e+08" width="15" spacingUnit="MM" scaleDependency="Area" barWidth="5" penWidth="0" enabled="0" spacingUnitScale="3x:0,0,0,0,0,0" rotationOffset="270" lineSizeType="MM" labelPlacementMethod="XHeight" backgroundAlpha="255" direction="0" diagramOrientation="Up" penColor="#000000" minimumSize="0" opacity="1" showAxis="1">
      <fontProperties description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
      <axisSymbol>
        <symbol alpha="1" name="" clip_to_extent="1" force_rhr="0" type="line">
          <layer pass="0" enabled="1" class="SimpleLine" locked="0">
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" linePlacementFlags="18" obstacle="0" zIndex="0" showAll="1" priority="0" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="freeboard" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="minimum_freeboard" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="surface_elevation" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hydraulic_head" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_in_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_out_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="freeboard"/>
    <alias index="2" name="" field="minimum_freeboard"/>
    <alias index="3" name="" field="surface_elevation"/>
    <alias index="4" name="" field="hydraulic_head"/>
    <alias index="5" name="" field="pipe_in_id"/>
    <alias index="6" name="" field="pipe_out_id"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="freeboard" applyOnUpdate="0"/>
    <default expression="" field="minimum_freeboard" applyOnUpdate="0"/>
    <default expression="" field="surface_elevation" applyOnUpdate="0"/>
    <default expression="" field="hydraulic_head" applyOnUpdate="0"/>
    <default expression="" field="pipe_in_id" applyOnUpdate="0"/>
    <default expression="" field="pipe_out_id" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" notnull_strength="1" field="fid" constraints="3" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="freeboard" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="minimum_freeboard" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="surface_elevation" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="hydraulic_head" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="pipe_in_id" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="pipe_out_id" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="freeboard" desc=""/>
    <constraint exp="" field="minimum_freeboard" desc=""/>
    <constraint exp="" field="surface_elevation" desc=""/>
    <constraint exp="" field="hydraulic_head" desc=""/>
    <constraint exp="" field="pipe_in_id" desc=""/>
    <constraint exp="" field="pipe_out_id" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column hidden="0" name="fid" width="-1" type="field"/>
      <column hidden="0" name="freeboard" width="-1" type="field"/>
      <column hidden="0" name="minimum_freeboard" width="-1" type="field"/>
      <column hidden="0" name="surface_elevation" width="-1" type="field"/>
      <column hidden="0" name="hydraulic_head" width="-1" type="field"/>
      <column hidden="0" name="pipe_in_id" width="-1" type="field"/>
      <column hidden="0" name="pipe_out_id" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="fid" editable="1"/>
    <field name="freeboard" editable="1"/>
    <field name="hydraulic_head" editable="1"/>
    <field name="minimum_freeboard" editable="1"/>
    <field name="pipe_in_id" editable="1"/>
    <field name="pipe_out_id" editable="1"/>
    <field name="surface_elevation" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="fid" labelOnTop="0"/>
    <field name="freeboard" labelOnTop="0"/>
    <field name="hydraulic_head" labelOnTop="0"/>
    <field name="minimum_freeboard" labelOnTop="0"/>
    <field name="pipe_in_id" labelOnTop="0"/>
    <field name="pipe_out_id" labelOnTop="0"/>
    <field name="surface_elevation" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"fid"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
