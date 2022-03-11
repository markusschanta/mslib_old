import altair as alt

QUALITY_MAP = {
    'low': '99.9',
    'medium': '99.5',
    'high': '95'
}

MAP_URL_PATTERN = "https://raw.githubusercontent.com/ginseng666/GeoJSON-TopoJSON-Austria/master/2021/simplified-{}/{}_{}_topo.json"


def get_map_url(entity='gemeinden', quality='medium'):
    assert entity in ['gemeinden', 'bezirke', 'laender']
    assert quality in QUALITY_MAP

    map_url = MAP_URL_PATTERN.format(QUALITY_MAP[quality], entity, QUALITY_MAP[quality].replace('.', ''))
    
    return alt.topo_feature(map_url, entity)

def plot_austria(df, quality='medium', color_column='value'):
    map_url = get_map_url(quality=quality)
    
    c = alt.Chart(map_url).mark_geoshape().encode(
        color=alt.Color(color_column + ':Q', scale=alt.Scale(type='log', scheme='spectral', reverse=True)),
    ).transform_lookup(
        lookup='properties.iso',
        from_=alt.LookupData(df, 'iso', [color_column])
    ).properties(
        width=800,
        height=400
    )
    
    return c