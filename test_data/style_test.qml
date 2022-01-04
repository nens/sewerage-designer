<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.10-Hannover" hasScaleBasedVisibilityFlag="0" readOnly="0" simplifyLocal="1" simplifyDrawingHints="1" minScale="100000000" simplifyDrawingTol="1" styleCategories="AllStyleCategories" simplifyMaxScale="1" maxScale="0" simplifyAlgorithm="0" labelsEnabled="1">
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
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="RuleRenderer">
    <rules key="{34b258fe-c144-4d4a-a3c0-20f90845a607}">
      <rule scalemaxdenom="25000" filter="sewerage_type = 'gemengd riool'" symbol="0" label="gemengd riool" key="{ec8a0209-9afe-46e3-98b0-72fd973af7ac}"/>
      <rule scalemaxdenom="25000" filter="sewerage_type = 'vuilwaterriool'" symbol="1" label="vuilwaterriool" key="{b9318bb2-4f75-4181-9e6e-6f97abe26fd3}"/>
      <rule scalemaxdenom="25000" filter="sewerage_type = 'hemelwaterriool'" symbol="2" label="hemelwaterriool" key="{9c8e655c-3d9c-409a-a16d-6354061642d5}"/>
      <rule scalemaxdenom="25000" filter="sewerage_type = 'vgs_hemelwaterriool'" symbol="3" label="vgs hemelwaterriool" key="{4d543a27-ac86-4ea4-a11c-0a145d04f931}"/>
      <rule scalemaxdenom="25000" filter="sewerage_type = 'infiltratievoorziening'" symbol="4" label="infiltratievoorziening" key="{45ef6c34-90d3-4b59-8db3-222218096b34}"/>
    </rules>
    <symbols>
      <symbol alpha="1" name="0" clip_to_extent="0" force_rhr="0" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;diameter&quot;*10" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,89,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="diameter*9.2" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="20"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@2" clip_to_extent="1" force_rhr="0" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="219,30,42,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;diameter&quot;/1.5" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="1" clip_to_extent="0" force_rhr="0" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;diameter&quot;*10" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,251,1,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="diameter*9.2" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="20"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@1@2" clip_to_extent="1" force_rhr="0" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="219,30,42,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;diameter&quot;/1.5" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="2" clip_to_extent="0" force_rhr="0" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;diameter&quot;*10" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="1,188,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="diameter*9.2" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="20"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@2@2" clip_to_extent="1" force_rhr="0" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="219,30,42,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;diameter&quot;/1.5" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="3" clip_to_extent="0" force_rhr="0" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;diameter&quot;*10" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="1,255,73,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="diameter*9.2" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="20"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@3@2" clip_to_extent="1" force_rhr="0" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="219,30,42,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;diameter&quot;/1.5" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="4" clip_to_extent="0" force_rhr="0" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;diameter&quot;*10" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="Pixel"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="192,1,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="Pixel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="Pixel"/>
          <prop k="ring_filter" v="0"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="diameter*9.2" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="20"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@4@2" clip_to_extent="1" force_rhr="0" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="219,30,42,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;diameter&quot;/1.5" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{6b505320-a5b9-4559-bf91-13a7469570bf}">
      <rule scalemaxdenom="2500" description="Start point label" filter="1=1" scalemindenom="500" key="{c3127f44-4d2d-49c1-a32c-a27b831189cf}">
        <settings calloutType="simple">
          <text-style multilineHeight="1" fontLetterSpacing="0" fontStrikeout="0" fontSizeUnit="Point" fontItalic="0" namedStyle="Standaard" textColor="49,19,222,255" capitalization="0" previewBkgrdColor="255,255,255,255" blendMode="0" fontUnderline="0" fontKerning="1" fontSize="8" fieldName="'    s:' || start_level" allowHtml="0" isExpression="1" textOrientation="horizontal" fontWeight="50" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="MS Shell Dlg 2" fontWordSpacing="0" textOpacity="1">
            <text-buffer bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferNoFill="1" bufferColor="255,255,255,255" bufferOpacity="1" bufferSize="1" bufferSizeUnits="MM" bufferBlendMode="0"/>
            <text-mask maskSizeUnits="MM" maskedSymbolLayers="" maskOpacity="1" maskEnabled="0" maskType="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskJoinStyle="128"/>
            <background shapeOpacity="1" shapeType="0" shapeBorderWidth="0" shapeFillColor="255,255,255,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetY="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeRotationType="0" shapeRadiiX="0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeOffsetX="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeJoinStyle="64" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM">
              <symbol alpha="1" name="markerSymbol" clip_to_extent="1" force_rhr="0" type="marker">
                <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="231,113,72,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
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
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowScale="100" shadowRadiusAlphaOnly="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowDraw="0" shadowRadius="1.5" shadowRadiusUnit="MM" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowOpacity="0.7" shadowOffsetGlobal="1"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format reverseDirectionSymbol="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0" wrapChar="" multilineAlign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0" formatNumbers="0" decimals="3" plussign="0" rightDirectionSymbol=">"/>
          <placement predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" quadOffset="4" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="LineGeometry" overrunDistanceUnit="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" yOffset="0" lineAnchorPercent="0.5" maxCurvedCharAngleIn="25" placement="2" xOffset="0" centroidWhole="0" offsetType="0" repeatDistanceUnits="MM" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" maxCurvedCharAngleOut="-25" distMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" priority="5" centroidInside="0" lineAnchorType="0" placementFlags="10" offsetUnits="MM" overrunDistance="0" polygonPlacementFlags="2" geometryGeneratorType="PointGeometry" geometryGeneratorEnabled="0" repeatDistance="0"/>
          <rendering obstacle="1" obstacleFactor="1" obstacleType="1" displayAll="1" fontLimitPixelSize="0" scaleMin="0" fontMinPixelSize="3" labelPerPart="0" upsidedownLabels="0" scaleMax="0" minFeatureSize="0" limitNumLabels="0" fontMaxPixelSize="10000" mergeLines="0" zIndex="0" maxNumLabels="3" scaleVisibility="0" drawLabels="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="Hali" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="'Left'" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="360 - (90 - degrees(azimuth( start_point($geometry), end_point($geometry))))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="x(start_point($geometry))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="y(start_point($geometry))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="'Top'" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol alpha=&quot;1&quot; name=&quot;symbol&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule scalemaxdenom="5000" description="Diameter" key="{156c5cd9-a088-480e-b722-9726acd4a835}">
        <settings calloutType="simple">
          <text-style multilineHeight="1" fontLetterSpacing="0" fontStrikeout="0" fontSizeUnit="Point" fontItalic="0" namedStyle="Regular" textColor="0,0,0,255" capitalization="0" previewBkgrdColor="255,255,255,255" blendMode="0" fontUnderline="0" fontKerning="1" fontSize="7" fieldName="'Ø'||round(diameter*1000)" allowHtml="0" isExpression="1" textOrientation="horizontal" fontWeight="50" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="MS Gothic" fontWordSpacing="0" textOpacity="1">
            <text-buffer bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferNoFill="1" bufferColor="255,255,255,255" bufferOpacity="1" bufferSize="0.7" bufferSizeUnits="MM" bufferBlendMode="0"/>
            <text-mask maskSizeUnits="MM" maskedSymbolLayers="" maskOpacity="1" maskEnabled="0" maskType="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskJoinStyle="128"/>
            <background shapeOpacity="1" shapeType="0" shapeBorderWidth="0" shapeFillColor="255,255,255,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetY="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeRotationType="0" shapeRadiiX="0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeOffsetX="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeJoinStyle="64" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM">
              <symbol alpha="1" name="markerSymbol" clip_to_extent="1" force_rhr="0" type="marker">
                <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="255,158,23,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
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
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowScale="100" shadowRadiusAlphaOnly="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowDraw="0" shadowRadius="1.5" shadowRadiusUnit="MM" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowOpacity="0.7" shadowOffsetGlobal="1"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format reverseDirectionSymbol="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0" wrapChar="" multilineAlign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0" formatNumbers="0" decimals="3" plussign="0" rightDirectionSymbol=">"/>
          <placement predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" quadOffset="4" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="LineGeometry" overrunDistanceUnit="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" yOffset="0" lineAnchorPercent="0.25" maxCurvedCharAngleIn="25" placement="2" xOffset="0" centroidWhole="0" offsetType="0" repeatDistanceUnits="MM" distUnits="MM" fitInPolygonOnly="0" preserveRotation="1" maxCurvedCharAngleOut="-25" distMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" priority="10" centroidInside="0" lineAnchorType="1" placementFlags="9" offsetUnits="MM" overrunDistance="0" polygonPlacementFlags="2" geometryGeneratorType="PointGeometry" geometryGeneratorEnabled="0" repeatDistance="0"/>
          <rendering obstacle="0" obstacleFactor="1" obstacleType="1" displayAll="0" fontLimitPixelSize="0" scaleMin="0" fontMinPixelSize="3" labelPerPart="0" upsidedownLabels="0" scaleMax="0" minFeatureSize="0" limitNumLabels="0" fontMaxPixelSize="10000" mergeLines="0" zIndex="0" maxNumLabels="2000" scaleVisibility="0" drawLabels="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol alpha=&quot;1&quot; name=&quot;symbol&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule scalemaxdenom="2500" description="End point label" filter="1=1" scalemindenom="500" key="{45f4916a-9538-4710-879f-f2137cca7836}">
        <settings calloutType="simple">
          <text-style multilineHeight="1" fontLetterSpacing="0" fontStrikeout="0" fontSizeUnit="Point" fontItalic="0" namedStyle="Standaard" textColor="227,26,28,255" capitalization="0" previewBkgrdColor="255,255,255,255" blendMode="0" fontUnderline="0" fontKerning="1" fontSize="8" fieldName="'e:'||end_level || '    '" allowHtml="0" isExpression="1" textOrientation="horizontal" fontWeight="50" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="MS Shell Dlg 2" fontWordSpacing="0" textOpacity="1">
            <text-buffer bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferNoFill="1" bufferColor="255,255,255,255" bufferOpacity="1" bufferSize="1" bufferSizeUnits="MM" bufferBlendMode="0"/>
            <text-mask maskSizeUnits="MM" maskedSymbolLayers="" maskOpacity="1" maskEnabled="0" maskType="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskJoinStyle="128"/>
            <background shapeOpacity="1" shapeType="0" shapeBorderWidth="0" shapeFillColor="255,255,255,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetY="0" shapeBorderColor="128,128,128,255" shapeRadiiY="0" shapeSVGFile="" shapeRotationType="0" shapeRadiiX="0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeOffsetX="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeJoinStyle="64" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM">
              <symbol alpha="1" name="markerSymbol" clip_to_extent="1" force_rhr="0" type="marker">
                <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="183,72,75,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
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
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowScale="100" shadowRadiusAlphaOnly="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowDraw="0" shadowRadius="1.5" shadowRadiusUnit="MM" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowOpacity="0.7" shadowOffsetGlobal="1"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format reverseDirectionSymbol="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0" wrapChar="" multilineAlign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0" formatNumbers="0" decimals="3" plussign="0" rightDirectionSymbol=">"/>
          <placement predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" quadOffset="4" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="LineGeometry" overrunDistanceUnit="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" dist="0" yOffset="0" lineAnchorPercent="0.5" maxCurvedCharAngleIn="25" placement="2" xOffset="0" centroidWhole="0" offsetType="0" repeatDistanceUnits="MM" distUnits="MM" fitInPolygonOnly="0" preserveRotation="1" maxCurvedCharAngleOut="-25" distMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" priority="5" centroidInside="0" lineAnchorType="0" placementFlags="10" offsetUnits="MM" overrunDistance="0" polygonPlacementFlags="2" geometryGeneratorType="PointGeometry" geometryGeneratorEnabled="0" repeatDistance="0"/>
          <rendering obstacle="1" obstacleFactor="1" obstacleType="1" displayAll="1" fontLimitPixelSize="0" scaleMin="0" fontMinPixelSize="3" labelPerPart="0" upsidedownLabels="0" scaleMax="0" minFeatureSize="0" limitNumLabels="0" fontMaxPixelSize="10000" mergeLines="0" zIndex="0" maxNumLabels="2000" scaleVisibility="0" drawLabels="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="Hali" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="'Right'" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="360 - (90 - degrees(azimuth( start_point($geometry), end_point($geometry))))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="x(end_point($geometry))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="y(end_point($geometry))" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="'Bottom'" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol alpha=&quot;1&quot; name=&quot;symbol&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
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
  <DiagramLayerSettings placement="2" linePlacementFlags="18" obstacle="0" zIndex="0" showAll="1" priority="0" dist="0">
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
    <field name="type" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="diameter" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="material" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="connected_surface_area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="max_hydraulic_gradient" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sewerage_type" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="fid"/>
    <alias index="1" name="" field="type"/>
    <alias index="2" name="" field="diameter"/>
    <alias index="3" name="" field="start_level"/>
    <alias index="4" name="" field="end_level"/>
    <alias index="5" name="" field="material"/>
    <alias index="6" name="" field="connected_surface_area"/>
    <alias index="7" name="" field="max_hydraulic_gradient"/>
    <alias index="8" name="" field="sewerage_type"/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="type" applyOnUpdate="0"/>
    <default expression="" field="diameter" applyOnUpdate="0"/>
    <default expression="" field="start_level" applyOnUpdate="0"/>
    <default expression="" field="end_level" applyOnUpdate="0"/>
    <default expression="" field="material" applyOnUpdate="0"/>
    <default expression="" field="connected_surface_area" applyOnUpdate="0"/>
    <default expression="" field="max_hydraulic_gradient" applyOnUpdate="0"/>
    <default expression="" field="sewerage_type" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" notnull_strength="1" field="fid" constraints="3" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="type" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="diameter" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="start_level" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="end_level" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="material" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="connected_surface_area" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="max_hydraulic_gradient" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="sewerage_type" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="type" desc=""/>
    <constraint exp="" field="diameter" desc=""/>
    <constraint exp="" field="start_level" desc=""/>
    <constraint exp="" field="end_level" desc=""/>
    <constraint exp="" field="material" desc=""/>
    <constraint exp="" field="connected_surface_area" desc=""/>
    <constraint exp="" field="max_hydraulic_gradient" desc=""/>
    <constraint exp="" field="sewerage_type" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column hidden="0" name="fid" width="-1" type="field"/>
      <column hidden="0" name="type" width="-1" type="field"/>
      <column hidden="0" name="diameter" width="-1" type="field"/>
      <column hidden="0" name="start_level" width="-1" type="field"/>
      <column hidden="0" name="end_level" width="-1" type="field"/>
      <column hidden="0" name="material" width="-1" type="field"/>
      <column hidden="0" name="connected_surface_area" width="-1" type="field"/>
      <column hidden="0" name="max_hydraulic_gradient" width="-1" type="field"/>
      <column hidden="0" name="sewerage_type" width="-1" type="field"/>
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
    <field name="connected_surface_area" editable="1"/>
    <field name="diameter" editable="1"/>
    <field name="end_level" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="material" editable="1"/>
    <field name="max_hydraulic_gradient" editable="1"/>
    <field name="sewerage_type" editable="1"/>
    <field name="start_level" editable="1"/>
    <field name="type" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="connected_surface_area" labelOnTop="0"/>
    <field name="diameter" labelOnTop="0"/>
    <field name="end_level" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="material" labelOnTop="0"/>
    <field name="max_hydraulic_gradient" labelOnTop="0"/>
    <field name="sewerage_type" labelOnTop="0"/>
    <field name="start_level" labelOnTop="0"/>
    <field name="type" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"fid"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
