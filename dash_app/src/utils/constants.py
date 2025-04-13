from dash import Output, Input

PLOT_STYLE = {'width': '48%', 'display': 'inline-block'}
INDIC_URS={"EC2021V": "Local", "EC2039V": "Global"}
LOCATIONS=["Local", "Global"]
REV_INDIC_URS={"Local": "EC2021V", "Global": "EC2039V"}

COUNTRY_ENTERPRISES_YEAR_BAR_IO= [Output('year-wise-enterprise-count-id', 'children'),
                                  Input('year-selection-id', 'value')]

YEAR_ENTERPRISE_CITY_BAR_IO = [Output('city-enterprises-id', 'children'),
                               Input('city-selection', 'value')]

YEAR_ENTERPRISES_COUNTRY_LOCATION_BAR_IO = [Output('country-enterprises-id', 'children'),
                                            Input('country-selection-id', 'value'),
                                            Input('indic-selection-id', 'value')]

COUNTRY_ENTERPRISES_YEAR_PIE_IO = [Output('pie-country-enterprises-id', 'children'),
                       Input('pie-country-selection-id', 'value')]

COUNTRY_ENTERPRISE_YEAR_MAP_IO = [Output('map-year-wise-enterprise-count-id', 'children'),
                       Input('map-year-selection-id', 'value')]