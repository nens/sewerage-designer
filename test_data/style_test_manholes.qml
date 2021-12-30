<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="1" simplifyAlgorithm="0" minScale="10000" readOnly="0" styleCategories="AllStyleCategories" labelsEnabled="0" maxScale="0" simplifyDrawingHints="0" simplifyLocal="1" version="3.16.10-Hannover" simplifyDrawingTol="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal endExpression="" durationField="" endField="" fixedDuration="0" accumulate="0" startField="" mode="0" durationUnit="min" startExpression="" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" forceraster="0" enableorderby="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" force_rhr="0" name="0" clip_to_extent="1" type="marker">
        <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
          <prop v="0" k="angle"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.5" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="area" k="scale_method"/>
          <prop v="3" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"fid"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory backgroundColor="#ffffff" penAlpha="255" spacingUnitScale="3x:0,0,0,0,0,0" showAxis="1" sizeType="MM" barWidth="5" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" lineSizeType="MM" labelPlacementMethod="XHeight" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" opacity="1" height="15" scaleBasedVisibility="0" minScaleDenominator="0" rotationOffset="270" enabled="0" spacing="5" width="15" penWidth="0" penColor="#000000" spacingUnit="MM" scaleDependency="Area" direction="0" diagramOrientation="Up">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
      <axisSymbol>
        <symbol alpha="1" force_rhr="0" name="" clip_to_extent="1" type="line">
          <layer locked="0" class="SimpleLine" enabled="1" pass="0">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" obstacle="0" linePlacementFlags="18" priority="0" zIndex="0" dist="0" placement="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
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
    <alias field="fid" index="0" name=""/>
    <alias field="freeboard" index="1" name=""/>
    <alias field="minimum_freeboard" index="2" name=""/>
    <alias field="surface_elevation" index="3" name=""/>
    <alias field="hydraulic_head" index="4" name=""/>
    <alias field="pipe_in_id" index="5" name=""/>
    <alias field="pipe_out_id" index="6" name=""/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="freeboard" expression="" applyOnUpdate="0"/>
    <default field="minimum_freeboard" expression="" applyOnUpdate="0"/>
    <default field="surface_elevation" expression="" applyOnUpdate="0"/>
    <default field="hydraulic_head" expression="" applyOnUpdate="0"/>
    <default field="pipe_in_id" expression="" applyOnUpdate="0"/>
    <default field="pipe_out_id" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" exp_strength="0" notnull_strength="1" constraints="3" unique_strength="1"/>
    <constraint field="freeboard" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="minimum_freeboard" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="surface_elevation" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="hydraulic_head" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="pipe_in_id" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="pipe_out_id" exp_strength="0" notnull_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="freeboard" exp="" desc=""/>
    <constraint field="minimum_freeboard" exp="" desc=""/>
    <constraint field="surface_elevation" exp="" desc=""/>
    <constraint field="hydraulic_head" exp="" desc=""/>
    <constraint field="pipe_in_id" exp="" desc=""/>
    <constraint field="pipe_out_id" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" name="fid" type="field" width="-1"/>
      <column hidden="0" name="freeboard" type="field" width="-1"/>
      <column hidden="0" name="minimum_freeboard" type="field" width="-1"/>
      <column hidden="0" name="surface_elevation" type="field" width="-1"/>
      <column hidden="0" name="hydraulic_head" type="field" width="-1"/>
      <column hidden="0" name="pipe_in_id" type="field" width="-1"/>
      <column hidden="0" name="pipe_out_id" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
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
