from dash import Output, Input

PLOT_STYLE = {'width': '48%', 'display': 'inline-block'}
INDIC_URS={"EC2021V": "All Companies", "EC2039V": "Local"}
LOCATIONS=["Local", "All Companies"]
REV_INDIC_URS={"All Companies": "EC2021V", "Local": "EC2039V"}

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

ENTERPRISES_TOURISM_SPENTS_LINE_IO = [Output('line-combined-country-spent-enterprises_year-id', 'children'),
                       Input('line-combined-country-spent-year-input', 'value')]

ENTERPRISES_TOURISM_SPENTS_BAR_IO = [Output('bar-combined-country-spent-enterprises_year-id', 'children'),
                       Input('bar-combined-country-spent-year-input', 'value'),
                       # Input('bar-combined-country-spent-year-destination-input', 'value'),
                       # Input('bar-combined-country-spent-year-purpose-input', 'value')
                                     ]

EMPLOYMENTS_COUNTRY_WORKIN_FIELD_AREA_IO = [Output('area-country-employments-work-field-year-id', 'children'),
                                      Input('area-year-employments-work-field-year-input', 'value')]

EMPLOYMENTS_YEAR_WORK_FIELD_BAR_IO = [Output('bar-year-employments-work-field-id', 'children'),
                                      Input('bar-year-employments-work-field-input', 'value')]

EMPLOYMENTS_YEAR_WORKING_TIME_BAR_IO = [Output('bar-year-employments-working-time-id', 'children'),
                                      Input('bar-year-employments-working-time-input', 'value')]

EMPLOYMENTS_YEAR_WORKING_TIME_LINE_IO = [Output('line-year-employments-working-time-id', 'children'),
                                      Input('line-year-employments-working-time-input', 'value')]

TOURISM_COUNTRY_SPENT_YEAR_LINE_IO = [Output('tourism-line-year-amount-purpose-id', 'children'),
                                      Input('tourism-line-year-amount-purpose-input', 'value')]

TOURISM_COUNTRY_SPENT_YEAR_BAR_IO = [Output('tourism-bar-country-amount-year-id', 'children'),
                                      Input('tourism-bar-country-amount-year-input', 'value')]

TOURISM_EXPENDITURE_YEAR_SPENT_COUNTRY_LINE_IO = [Output('tourism-expenditure-country-spent-year-line-id', 'children'),
                                      Input('tourism-expenditure-country-spent-year-line-input', 'value')]
