<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" labelsEnabled="0" simplifyLocal="1" simplifyMaxScale="1" maxScale="0" minScale="100000000" simplifyDrawingHints="0" version="3.22.7-Białowieża" symbologyReferenceScale="-1" readOnly="0" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal durationField="" limitMode="0" endExpression="" enabled="0" endField="" durationUnit="min" startField="" startExpression="" fixedDuration="0" accumulate="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 referencescale="-1" type="RuleRenderer" symbollevels="0" forceraster="0" enableorderby="0">
    <rules key="{8615500f-291b-43e9-9637-98f8858aa5b6}">
      <rule symbol="0" label="Hemelwaterriool 100%" key="{e26fa1d6-5bbb-4001-b16f-2f0b34504877}" filter="&quot;hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="1" label="VGS Hemelwaterriool 100%" key="{7be024ad-67fd-4f91-b658-70ec4c0e63fe}" filter=" &quot;vgs_hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="2" label="Gemengd 100%" key="{3d292b4a-48ea-4954-9649-080da78561db}" filter=" &quot;gemengd_riool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="3" label="Hemelwaterriool en Gemengd" key="{a24c39d3-a09e-432d-a203-84441af42b85}" filter="( &quot;hemelwaterriool&quot; > 0 AND hemelwaterriool &lt; 100 AND  &quot;gemengd_riool&quot; > 0 AND gemengd_riool &lt; 100) and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="4" label="Infiltratievoorziening 100%" key="{49c2c107-4207-4f1f-87e7-cf522249dc51}" filter=" &quot;infiltratievoorziening&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="5" label="Maaiveld 100%" key="{cc14fa82-08f5-43e2-a7dd-68210119aed1}" filter=" &quot;maaiveld&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="6" label="Open water 100%" key="{9c50aa29-461b-4154-b33c-9806cd1ecc3a}" filter=" &quot;open_water&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100"/>
      <rule symbol="7" label="Overig (wel valide, totaal = 100)" key="{6b9886b8-93e3-42cb-a57c-3330f89e86eb}" filter="ELSE"/>
      <rule symbol="8" label="Overig (niet valide, totaal ≠ 100)" key="{20a36527-a20b-4bce-b851-6353175c759a}" filter="( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) != 100"/>
    </rules>
    <symbols>
      <symbol type="fill" force_rhr="0" name="0" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="165,183,255,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,103"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.2"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="165,183,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,103"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.2"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="1" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="165,183,255,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,128"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="165,183,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="PointPatternFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="displacement_x" value="0"/>
            <Option type="QString" name="displacement_x_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="displacement_x_unit" value="MM"/>
            <Option type="QString" name="displacement_y" value="0"/>
            <Option type="QString" name="displacement_y_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="displacement_y_unit" value="MM"/>
            <Option type="QString" name="distance_x" value="5"/>
            <Option type="QString" name="distance_x_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="distance_x_unit" value="MM"/>
            <Option type="QString" name="distance_y" value="5"/>
            <Option type="QString" name="distance_y_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="distance_y_unit" value="MM"/>
            <Option type="QString" name="offset_x" value="0"/>
            <Option type="QString" name="offset_x_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_x_unit" value="MM"/>
            <Option type="QString" name="offset_y" value="0"/>
            <Option type="QString" name="offset_y_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_y_unit" value="MM"/>
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
          </Option>
          <prop k="displacement_x" v="0"/>
          <prop k="displacement_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="0"/>
          <prop k="displacement_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="5"/>
          <prop k="distance_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="5"/>
          <prop k="distance_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_y_unit" v="MM"/>
          <prop k="offset_x" v="0"/>
          <prop k="offset_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_x_unit" v="MM"/>
          <prop k="offset_y" v="0"/>
          <prop k="offset_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_y_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="marker" force_rhr="0" name="@1@1" clip_to_extent="1" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
              <Option type="Map">
                <Option type="QString" name="angle" value="0"/>
                <Option type="QString" name="cap_style" value="square"/>
                <Option type="QString" name="color" value="149,165,230,255"/>
                <Option type="QString" name="horizontal_anchor_point" value="1"/>
                <Option type="QString" name="joinstyle" value="bevel"/>
                <Option type="QString" name="name" value="cross_fill"/>
                <Option type="QString" name="offset" value="0,0"/>
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="offset_unit" value="MM"/>
                <Option type="QString" name="outline_color" value="35,35,35,0"/>
                <Option type="QString" name="outline_style" value="solid"/>
                <Option type="QString" name="outline_width" value="0"/>
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="outline_width_unit" value="MM"/>
                <Option type="QString" name="scale_method" value="diameter"/>
                <Option type="QString" name="size" value="2"/>
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="size_unit" value="MM"/>
                <Option type="QString" name="vertical_anchor_point" value="1"/>
              </Option>
              <prop k="angle" v="0"/>
              <prop k="cap_style" v="square"/>
              <prop k="color" v="149,165,230,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="cross_fill"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,0"/>
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
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="2" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="255,213,181,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,128"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,213,181,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="3" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="255,213,181,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,128"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.26"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,213,181,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="LinePatternFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="angle" value="45"/>
            <Option type="QString" name="color" value="207,20,192,255"/>
            <Option type="QString" name="distance" value="2"/>
            <Option type="QString" name="distance_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="distance_unit" value="MM"/>
            <Option type="QString" name="line_width" value="0.5"/>
            <Option type="QString" name="line_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
          </Option>
          <prop k="angle" v="45"/>
          <prop k="color" v="207,20,192,255"/>
          <prop k="distance" v="2"/>
          <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="line" force_rhr="0" name="@3@1" clip_to_extent="1" alpha="1">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
            <layer class="SimpleLine" pass="0" locked="0" enabled="1">
              <Option type="Map">
                <Option type="QString" name="align_dash_pattern" value="0"/>
                <Option type="QString" name="capstyle" value="square"/>
                <Option type="QString" name="customdash" value="5;2"/>
                <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="customdash_unit" value="MM"/>
                <Option type="QString" name="dash_pattern_offset" value="0"/>
                <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
                <Option type="QString" name="draw_inside_polygon" value="0"/>
                <Option type="QString" name="joinstyle" value="bevel"/>
                <Option type="QString" name="line_color" value="165,183,255,255"/>
                <Option type="QString" name="line_style" value="solid"/>
                <Option type="QString" name="line_width" value="1"/>
                <Option type="QString" name="line_width_unit" value="MM"/>
                <Option type="QString" name="offset" value="0"/>
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="offset_unit" value="MM"/>
                <Option type="QString" name="ring_filter" value="0"/>
                <Option type="QString" name="trim_distance_end" value="0"/>
                <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="trim_distance_end_unit" value="MM"/>
                <Option type="QString" name="trim_distance_start" value="0"/>
                <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="trim_distance_start_unit" value="MM"/>
                <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
                <Option type="QString" name="use_custom_dash" value="0"/>
                <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              </Option>
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
              <prop k="line_color" v="165,183,255,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="ring_filter" v="0"/>
              <prop k="trim_distance_end" v="0"/>
              <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_end_unit" v="MM"/>
              <prop k="trim_distance_start" v="0"/>
              <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_start_unit" v="MM"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="4" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="163,205,185,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="114,133,132,64"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="163,205,185,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="114,133,132,64"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="5" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="167,255,159,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,179"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="167,255,159,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,179"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="6" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="67,162,209,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,179"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="67,162,209,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,179"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="7" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="201,201,201,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="153,153,153,128"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="201,201,201,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="153,153,153,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" name="8" clip_to_extent="1" alpha="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="color" value="255,1,1,255"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="offset" value="0,0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="outline_color" value="255,255,255,128"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,1,1,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <Option type="Map">
      <Option type="QString" name="dualview/previewExpressions" value="&quot;lokaalid&quot;"/>
      <Option type="QString" name="embeddedWidgets/count" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory spacingUnitScale="3x:0,0,0,0,0,0" enabled="0" opacity="1" sizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" direction="1" penColor="#000000" penAlpha="255" spacingUnit="MM" diagramOrientation="Up" backgroundAlpha="255" minScaleDenominator="0" barWidth="5" backgroundColor="#ffffff" rotationOffset="270" width="15" sizeType="MM" spacing="0" labelPlacementMethod="XHeight" lineSizeScale="3x:0,0,0,0,0,0" height="15" maxScaleDenominator="1e+08" lineSizeType="MM" penWidth="0" scaleDependency="Area" minimumSize="0" showAxis="0">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol type="line" force_rhr="0" name="" clip_to_extent="1" alpha="1">
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <layer class="SimpleLine" pass="0" locked="0" enabled="1">
            <Option type="Map">
              <Option type="QString" name="align_dash_pattern" value="0"/>
              <Option type="QString" name="capstyle" value="square"/>
              <Option type="QString" name="customdash" value="5;2"/>
              <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="customdash_unit" value="MM"/>
              <Option type="QString" name="dash_pattern_offset" value="0"/>
              <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
              <Option type="QString" name="draw_inside_polygon" value="0"/>
              <Option type="QString" name="joinstyle" value="bevel"/>
              <Option type="QString" name="line_color" value="35,35,35,255"/>
              <Option type="QString" name="line_style" value="solid"/>
              <Option type="QString" name="line_width" value="0.26"/>
              <Option type="QString" name="line_width_unit" value="MM"/>
              <Option type="QString" name="offset" value="0"/>
              <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offset_unit" value="MM"/>
              <Option type="QString" name="ring_filter" value="0"/>
              <Option type="QString" name="trim_distance_end" value="0"/>
              <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_end_unit" value="MM"/>
              <Option type="QString" name="trim_distance_start" value="0"/>
              <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_start_unit" value="MM"/>
              <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
              <Option type="QString" name="use_custom_dash" value="0"/>
              <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            </Option>
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
            <prop k="trim_distance_end" v="0"/>
            <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_end_unit" v="MM"/>
            <prop k="trim_distance_start" v="0"/>
            <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_start_unit" v="MM"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="1" priority="0" linePlacementFlags="18" obstacle="0" dist="0" zIndex="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option type="double" name="allowedGapsBuffer" value="0"/>
        <Option type="bool" name="allowedGapsEnabled" value="false"/>
        <Option type="QString" name="allowedGapsLayer" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="laatste_wijziging" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-dd HH:mm:ss"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd HH:mm:ss"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bgt_identificatie" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type_verharding" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="Dak" value="dak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Gesloten verhard" value="gesloten verhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Open verhard" value="open verhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Onverhard" value="onverhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Groen(blauw) dak" value="groen(blauw) dak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Waterpasserende verharding" value="waterpasserende verharding"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Water" value="water"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Niet opgegeven)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="graad_verharding" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="100"/>
            <Option type="double" name="Min" value="0"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingstype" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="Hellend" value="hellend"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Vlak" value="vlak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Vlak, uitgestrekt" value="vlak uitgestrekt"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Niet opgegeven)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingspercentage" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="100"/>
            <Option type="double" name="Min" value="0"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type_private_voorziening" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="bovengronds met infiltratie" value="bovengronds met infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="ondergronds met infiltratie" value="ondergronds met infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="bovengronds zonder infiltratie" value="bovengronds zonder infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="ondergronds zonder infiltratie" value="ondergronds zonder infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Geen private voorziening)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="berging_private_voorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code_voorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="putcode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="leidingcode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="gemengd_riool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hemelwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="vgs_hemelwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="vuilwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltratievoorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="open_water" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maaiveld" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" name="" index="0"/>
    <alias field="laatste_wijziging" name="Laatste wijziging" index="1"/>
    <alias field="bgt_identificatie" name="BGT Identificatie" index="2"/>
    <alias field="type_verharding" name="Type verharding" index="3"/>
    <alias field="graad_verharding" name="Verhardingsgraad (%)" index="4"/>
    <alias field="hellingstype" name="Hellingstype" index="5"/>
    <alias field="hellingspercentage" name="Helling (%)" index="6"/>
    <alias field="type_private_voorziening" name="Type private voorziening" index="7"/>
    <alias field="berging_private_voorziening" name="Berging private voorziening" index="8"/>
    <alias field="code_voorziening" name="Code voorziening" index="9"/>
    <alias field="putcode" name="Putcode" index="10"/>
    <alias field="leidingcode" name="Leidingcode" index="11"/>
    <alias field="gemengd_riool" name="Gemengd riool (%)" index="12"/>
    <alias field="hemelwaterriool" name="Hemelwaterriool (%)" index="13"/>
    <alias field="vgs_hemelwaterriool" name="VGS Hemelwaterriool (%)" index="14"/>
    <alias field="vuilwaterriool" name="Vuilwaterriool (%)" index="15"/>
    <alias field="infiltratievoorziening" name="Infiltratievoorziening (%)" index="16"/>
    <alias field="open_water" name="Open water (%)" index="17"/>
    <alias field="maaiveld" name="Maaiveld (%)" index="18"/>
  </aliases>
  <defaults>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="laatste_wijziging" applyOnUpdate="0" expression=""/>
    <default field="bgt_identificatie" applyOnUpdate="0" expression=""/>
    <default field="type_verharding" applyOnUpdate="0" expression=""/>
    <default field="graad_verharding" applyOnUpdate="0" expression=""/>
    <default field="hellingstype" applyOnUpdate="0" expression=""/>
    <default field="hellingspercentage" applyOnUpdate="0" expression=""/>
    <default field="type_private_voorziening" applyOnUpdate="0" expression=""/>
    <default field="berging_private_voorziening" applyOnUpdate="0" expression=""/>
    <default field="code_voorziening" applyOnUpdate="0" expression=""/>
    <default field="putcode" applyOnUpdate="0" expression=""/>
    <default field="leidingcode" applyOnUpdate="0" expression=""/>
    <default field="gemengd_riool" applyOnUpdate="0" expression=""/>
    <default field="hemelwaterriool" applyOnUpdate="0" expression=""/>
    <default field="vgs_hemelwaterriool" applyOnUpdate="0" expression=""/>
    <default field="vuilwaterriool" applyOnUpdate="0" expression=""/>
    <default field="infiltratievoorziening" applyOnUpdate="0" expression=""/>
    <default field="open_water" applyOnUpdate="0" expression=""/>
    <default field="maaiveld" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="laatste_wijziging" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="bgt_identificatie" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="type_verharding" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="graad_verharding" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="hellingstype" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="hellingspercentage" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="type_private_voorziening" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="berging_private_voorziening" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="code_voorziening" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="putcode" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="leidingcode" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="gemengd_riool" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="hemelwaterriool" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="vgs_hemelwaterriool" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="vuilwaterriool" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="infiltratievoorziening" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="open_water" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="maaiveld" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="laatste_wijziging" desc="" exp=""/>
    <constraint field="bgt_identificatie" desc="" exp=""/>
    <constraint field="type_verharding" desc="" exp=""/>
    <constraint field="graad_verharding" desc="" exp=""/>
    <constraint field="hellingstype" desc="" exp=""/>
    <constraint field="hellingspercentage" desc="" exp=""/>
    <constraint field="type_private_voorziening" desc="" exp=""/>
    <constraint field="berging_private_voorziening" desc="" exp=""/>
    <constraint field="code_voorziening" desc="" exp=""/>
    <constraint field="putcode" desc="" exp=""/>
    <constraint field="leidingcode" desc="" exp=""/>
    <constraint field="gemengd_riool" desc="" exp=""/>
    <constraint field="hemelwaterriool" desc="" exp=""/>
    <constraint field="vgs_hemelwaterriool" desc="" exp=""/>
    <constraint field="vuilwaterriool" desc="" exp=""/>
    <constraint field="infiltratievoorziening" desc="" exp=""/>
    <constraint field="open_water" desc="" exp=""/>
    <constraint field="maaiveld" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;gecheckt&quot;" actionWidgetStyle="dropDown" sortOrder="1">
    <columns>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" name="id" width="-1" hidden="0"/>
      <column type="field" name="laatste_wijziging" width="-1" hidden="0"/>
      <column type="field" name="bgt_identificatie" width="-1" hidden="0"/>
      <column type="field" name="type_verharding" width="-1" hidden="0"/>
      <column type="field" name="graad_verharding" width="-1" hidden="0"/>
      <column type="field" name="hellingstype" width="-1" hidden="0"/>
      <column type="field" name="hellingspercentage" width="-1" hidden="0"/>
      <column type="field" name="putcode" width="-1" hidden="0"/>
      <column type="field" name="leidingcode" width="-1" hidden="0"/>
      <column type="field" name="gemengd_riool" width="-1" hidden="0"/>
      <column type="field" name="hemelwaterriool" width="-1" hidden="0"/>
      <column type="field" name="vgs_hemelwaterriool" width="-1" hidden="0"/>
      <column type="field" name="infiltratievoorziening" width="-1" hidden="0"/>
      <column type="field" name="type_private_voorziening" width="-1" hidden="0"/>
      <column type="field" name="berging_private_voorziening" width="-1" hidden="0"/>
      <column type="field" name="code_voorziening" width="-1" hidden="0"/>
      <column type="field" name="vuilwaterriool" width="-1" hidden="0"/>
      <column type="field" name="open_water" width="-1" hidden="0"/>
      <column type="field" name="maaiveld" width="-1" hidden="0"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">L:/Extern/Projecten U (2019)/U0087 - Pilot samenwerken in AWK Rijnland/Gegevens/Layout</editform>
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
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Vlakeigenschappen" groupBox="1" visibilityExpression="" showLabel="1" columnCount="1" visibilityExpressionEnabled="0">
      <attributeEditorField name="id" index="0" showLabel="1"/>
      <attributeEditorField name="laatste_wijziging" index="1" showLabel="1"/>
      <attributeEditorField name="bgt_identificatie" index="2" showLabel="1"/>
      <attributeEditorField name="type_verharding" index="3" showLabel="1"/>
      <attributeEditorField name="graad_verharding" index="4" showLabel="1"/>
      <attributeEditorField name="hellingstype" index="5" showLabel="1"/>
      <attributeEditorField name="hellingspercentage" index="6" showLabel="1"/>
      <attributeEditorField name="type_private_voorziening" index="7" showLabel="1"/>
      <attributeEditorField name="berging_private_voorziening" index="8" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Voert af naar..." groupBox="1" visibilityExpression="" showLabel="1" columnCount="1" visibilityExpressionEnabled="0">
      <attributeEditorField name="gemengd_riool" index="12" showLabel="1"/>
      <attributeEditorField name="hemelwaterriool" index="13" showLabel="1"/>
      <attributeEditorField name="vgs_hemelwaterriool" index="14" showLabel="1"/>
      <attributeEditorField name="vuilwaterriool" index="15" showLabel="1"/>
      <attributeEditorField name="infiltratievoorziening" index="16" showLabel="1"/>
      <attributeEditorField name="open_water" index="17" showLabel="1"/>
      <attributeEditorField name="maaiveld" index="18" showLabel="1"/>
      <attributeEditorField name="putcode" index="10" showLabel="1"/>
      <attributeEditorField name="leidingcode" index="11" showLabel="1"/>
      <attributeEditorField name="code_voorziening" index="9" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Overzicht" groupBox="1" visibilityExpression="" showLabel="1" columnCount="1" visibilityExpressionEnabled="0">
      <attributeEditorHtmlElement name="Oppervlakken en afvoerpercentages" showLabel="1">&lt;p style="font-family:'MS Shell Dlg 2';font-size:10px">&#xd;&#xd;
	&lt;b>&#xd;&#xd;
		Totaal oppervlak: &#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number($area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
		 m&lt;sup>2&lt;/sup> &#xd;&#xd;
	&lt;/b>&#xd;&#xd;
	&lt;br>&#xd;&#xd;
	&lt;br>&#xd;&#xd;
&#xd;&#xd;
&#xd;&#xd;
&lt;table style="width:100%; font-size:10px">&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>&lt;b>Voert af naar&lt;/b>&lt;/td>&#xd;&#xd;
    &lt;td>&lt;b>m&lt;sup>2&lt;/sup>&lt;/b>&lt;/td>&#xd;&#xd;
    &lt;td>&lt;b>%&lt;/b>&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>Gemengd riool&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"gemengd_riool\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"gemengd_riool\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>Hemelwaterriool&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"hemelwaterriool\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"hemelwaterriool\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>VGS Hemelwaterriool&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"vgs_hemelwaterriool\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"vgs_hemelwaterriool\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
    &lt;tr>&#xd;&#xd;
    &lt;td>Vuilwaterriool&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"vuilwaterriool\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"vuilwaterriool\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>Infiltratievoorziening&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"infiltratievoorziening\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"infiltratievoorziening\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
  &lt;tr>&#xd;&#xd;
    &lt;td>Open water&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"open_water\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"open_water\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
    &lt;tr>&#xd;&#xd;
    &lt;td>Maaiveld&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number(\"maaiveld\"/100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>	&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"\"maaiveld\""&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr>&#xd;&#xd;
   &lt;tr>&#xd;&#xd;
    &lt;td>&lt;b>TOTAAL&lt;/b>&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;b>&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"format_number((gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + vuilwaterriool + open_water + maaiveld) /100*$area,2)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&lt;/b>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
    &lt;td>&#xd;&#xd;
		&lt;b>&lt;script>&#xd;&#xd;
			document.write(&#xd;&#xd;
				expression.evaluate(&#xd;&#xd;
					"(gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + vuilwaterriool + open_water + maaiveld)"&#xd;&#xd;
				)&#xd;&#xd;
			);&#xd;&#xd;
		&lt;/script>&lt;/b>&#xd;&#xd;
	&lt;/td>&#xd;&#xd;
  &lt;/tr> &#xd;&#xd;
&lt;/table>		&#xd;&#xd;
&#xd;&#xd;
&lt;/p>&#xd;&#xd;
&#xd;&#xd;
</attributeEditorHtmlElement>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="berging_dak"/>
    <field editable="1" name="berging_private_voorziening"/>
    <field editable="1" name="bgt_identificatie"/>
    <field editable="1" name="code_voorziening"/>
    <field editable="1" name="dwa"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="gecheckt"/>
    <field editable="1" name="gemengd"/>
    <field editable="1" name="gemengd_riool"/>
    <field editable="1" name="graad_verharding"/>
    <field editable="1" name="hellingspercentage"/>
    <field editable="1" name="hellingstype"/>
    <field editable="1" name="hemelwaterriool"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltratievoorziening"/>
    <field editable="1" name="laatste_wijziging"/>
    <field editable="1" name="leidingcode"/>
    <field editable="1" name="lokaalid"/>
    <field editable="1" name="maaiveld"/>
    <field editable="1" name="niet_aangesloten"/>
    <field editable="1" name="nwrw_type_afstroming"/>
    <field editable="1" name="nwrw_type_afstroming_afwijkend"/>
    <field editable="1" name="nwrw_type_afstroming_voor_check"/>
    <field editable="1" name="open_water"/>
    <field editable="1" name="openwater"/>
    <field editable="1" name="putcode"/>
    <field editable="1" name="rwa"/>
    <field editable="1" name="slope_p25"/>
    <field editable="1" name="type_private_voorziening"/>
    <field editable="1" name="type_verharding"/>
    <field editable="1" name="vgs_hemelwaterriool"/>
    <field editable="1" name="vlak"/>
    <field editable="1" name="vlak_type"/>
    <field editable="1" name="vuilwaterriool"/>
  </editable>
  <labelOnTop>
    <field name="berging_dak" labelOnTop="0"/>
    <field name="berging_private_voorziening" labelOnTop="0"/>
    <field name="bgt_identificatie" labelOnTop="0"/>
    <field name="code_voorziening" labelOnTop="0"/>
    <field name="dwa" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="gecheckt" labelOnTop="0"/>
    <field name="gemengd" labelOnTop="0"/>
    <field name="gemengd_riool" labelOnTop="0"/>
    <field name="graad_verharding" labelOnTop="0"/>
    <field name="hellingspercentage" labelOnTop="0"/>
    <field name="hellingstype" labelOnTop="0"/>
    <field name="hemelwaterriool" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="infiltratievoorziening" labelOnTop="0"/>
    <field name="laatste_wijziging" labelOnTop="0"/>
    <field name="leidingcode" labelOnTop="0"/>
    <field name="lokaalid" labelOnTop="0"/>
    <field name="maaiveld" labelOnTop="0"/>
    <field name="niet_aangesloten" labelOnTop="0"/>
    <field name="nwrw_type_afstroming" labelOnTop="0"/>
    <field name="nwrw_type_afstroming_afwijkend" labelOnTop="0"/>
    <field name="nwrw_type_afstroming_voor_check" labelOnTop="0"/>
    <field name="open_water" labelOnTop="0"/>
    <field name="openwater" labelOnTop="0"/>
    <field name="putcode" labelOnTop="0"/>
    <field name="rwa" labelOnTop="0"/>
    <field name="slope_p25" labelOnTop="0"/>
    <field name="type_private_voorziening" labelOnTop="0"/>
    <field name="type_verharding" labelOnTop="0"/>
    <field name="vgs_hemelwaterriool" labelOnTop="0"/>
    <field name="vlak" labelOnTop="0"/>
    <field name="vlak_type" labelOnTop="0"/>
    <field name="vuilwaterriool" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="berging_private_voorziening" reuseLastValue="0"/>
    <field name="bgt_identificatie" reuseLastValue="0"/>
    <field name="code_voorziening" reuseLastValue="0"/>
    <field name="gemengd_riool" reuseLastValue="0"/>
    <field name="graad_verharding" reuseLastValue="0"/>
    <field name="hellingspercentage" reuseLastValue="0"/>
    <field name="hellingstype" reuseLastValue="0"/>
    <field name="hemelwaterriool" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="infiltratievoorziening" reuseLastValue="0"/>
    <field name="laatste_wijziging" reuseLastValue="0"/>
    <field name="leidingcode" reuseLastValue="0"/>
    <field name="maaiveld" reuseLastValue="0"/>
    <field name="open_water" reuseLastValue="0"/>
    <field name="putcode" reuseLastValue="0"/>
    <field name="type_private_voorziening" reuseLastValue="0"/>
    <field name="type_verharding" reuseLastValue="0"/>
    <field name="vgs_hemelwaterriool" reuseLastValue="0"/>
    <field name="vuilwaterriool" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"lokaalid"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
