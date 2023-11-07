import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import json

import refr
import DataUpdate as up


################################ CONSTANTS ###################################

default_vars = ['Real Rates - 10-Year Real Rate', 
                                'Yield Curves - 10Y-2Y']

factor_options_daily = [f"{key} - {sub}" for key in refr.available_franch_factors 
                     for sub in refr.available_franch_factors[key] if 'Daily' in f"{key} - {sub}"
                     ]

benchmark_options = ['None'] + [f"{key} - {sub}" for key in refr.benchmarks
                     for sub in refr.benchmarks[key]]

days_in_month = 21

# /Users/rhys/Desktop/grid_risk_management/
with open("data/references/cols_for_factor.json", "r") as write_file:
    cols_for_factor = json.load(write_file)


################################ CONSTANTS ###################################



@st.cache_data()
def get_Data(daily=True):
    
    # /Users/rhys/Desktop/grid_risk_management/
    if daily:
        temp_df = pd.read_csv(f'data/full_daily_data.csv', 
                          header=[0, 1],
                          index_col=0,
                          parse_dates=True)
        return temp_df
    
    # /Users/rhys/Desktop/grid_risk_management/

    temp_df = pd.read_csv(f'data/full_monthly_data.csv', 
                          header=[0, 1],
                          index_col=0,
                          parse_dates=True)
    
    return temp_df


def current_scores(scores_data):
    
    last_point = scores_data.iloc[-1].round(0)
    
    return last_point.to_dict()


@st.cache_data
def rolling_z_scores(chunk, lookback = None, 
                     round_zs=True, bounds=(-4, 4), 
                     gradient=False, grad_period = 21):
    
    if not lookback:
        st.warning('Must enter lookback period')
        st.stop()
    
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    
    temp = chunk.copy()
    
    if gradient:
        temp = temp.diff(grad_period)
    
    scaled_chunk = (temp - temp.rolling(lookback).mean()) / temp.rolling(lookback).std()
    scaled_chunk = scaled_chunk.clip(lower_bound, upper_bound)

    if round_zs:
        return scaled_chunk.round(0)
    return scaled_chunk


@st.cache_data
def get_returns(dependent, forward_window = 252,):
    
    rets = dependent.rolling(forward_window).sum().shift(-forward_window+1)
    
    return rets

def make_column_map(frame):
    
    cols = list(frame.columns)
    
    return {'var1' : cols[0], 
            'var2' : cols[1],
            'dependent' : cols[2]}


#experimental_allow_widgets=True
@st.cache_data()
def create_df(var1, var2, dependent, col_for_3, 
              optional_col, benchmark, equal_weight):
    
    # fetchFile()
    # st.session_state.equal_weight
    if equal_weight:
        dependent = dependent + ' - Equal-Weight'
    
    #col_for_3 = st.session_state.column_choice
    #optional_col = st.session_state.optional_col
    #benchmark = st.session_state.benchmark
    
    
    if optional_col != 'None' and benchmark != 'None':
        st.warning('It is not recommend to Neutralize against both a Benchmark and another Factor Quantile!')
    
    if optional_col != 'None':
        df_3_chunk = (daily_data[dependent][col_for_3] - 
                      daily_data[dependent][optional_col]).to_frame(name='Neutral Returns')
    elif benchmark != 'None':
        benchmark_name = benchmark[benchmark.index('-') + 2:]
        df_3_chunk = (daily_data[dependent][col_for_3] - 
                        daily_data[benchmark][benchmark_name]
                     ).to_frame(name = col_for_3)
    else:
        df_3_chunk = daily_data[dependent][[col_for_3]]
    
    return [daily_data[var1], daily_data[var2], df_3_chunk]



def scale_frame(frame, gradient):
    
    if st.session_state.gradient:
        diff_d = st.session_state.diff_days
    else:
        diff_d = None
    
    if gradient:
        diff_d = diff_days
    else:
        diff_d = None
    
    bounds = (-st.session_state.score_bounds, st.session_state.score_bounds)
    #bounds = (-state_bounds, state_bounds)
    
    # st.session_state.lookback
    # st.session_state.gradient
    scaled_frame = rolling_z_scores(frame, lookback = st.session_state.lookback * 21,
                                        gradient = st.session_state.gradient, 
                                        grad_period = diff_d,
                                        bounds = bounds)
    
    scaled_frame = scaled_frame.dropna(axis = 0, how = 'any')
    
    return scaled_frame


@st.cache_data()
def create_pivot(frame, col_map):
    
    variables = [col_map['var1'], 
                     col_map['var2']]
    
    pivot_df = frame.groupby(variables)[col_map['dependent']].mean().unstack()
    
    pivot_df.index.name = col_map['var1']
    pivot_df.columns.name = col_map['var2']
    # [pivot_df.index.abs() < 5][[col for col in pivot_df if abs(col) < 5]]
    return pivot_df.round(3)


def validate_vars(ivars):
    
    if not isinstance(ivars, list) or len(ivars) != 2:
        st.warning('Must Select 2 Variables!')
        st.stop()


def handle_dependent(dependent):
    
    dex_of_dash = dependent.index('-')
    
    name = dependent[:dex_of_dash-1]
    
    return name


#@st.cache_data()
def get_timeframe(df):
    
    temp = df.copy()
    
    return temp[(temp.index >= pd.to_datetime(st.session_state.start_date)) &
            (temp.index <= pd.to_datetime(st.session_state.end_date))
            ]


def create_fig(pivot_df, 
               curr_scores_dict, 
               col_maps):
    
    #col_maps = make_column_map(df)
    var1_name = col_maps['var1']
    var2_name = col_maps['var2']
    dependent_name = col_maps['dependent']
    
    fig = px.imshow(pivot_df, color_continuous_midpoint=0.0, 
                    color_continuous_scale=['red', 'white', 'green'], 
                    origin = 'lower', 
                    aspect='equal',
                     
                    #text_auto='.2f'
                    )
    
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
        )
        )
    
    dep_name = handle_dependent(dependent)
    
    #fig.update_layout(paper_bgcolor='white')
    #, paper_bgcolor="LightSteelBlue"
    fig.update_layout(plot_bgcolor='gray', 
                    template = 'plotly_white',
                    title = f'{dep_name} Forward Returns <br><sup>Across {var1_name} and {var2_name}</sup>'
                    )
    fig.update_xaxes(showgrid=True)
    fig.update_traces(hovertemplate = "x-score: %{x} <br>y-score: %{y} </br>Forward Return: %{z}")
    
    fig.add_shape(type="rect",
              x0=curr_scores_dict[var2_name]-0.5, y0=curr_scores_dict[var1_name]-0.5, 
              x1=curr_scores_dict[var2_name]+0.5, y1=curr_scores_dict[var1_name]+0.5,
              line=dict(color="blue", width = 4),
              )
    
    #st.subheader(f'{dep_name} Forward Returns')
    #st.write(f'Across {var1_name} and {var2_name}')
    #st.plotly_chart(fig, use_container_width = True)
    
    return fig



def run():
    #assert isinstance(ivars, list), 'must be a list'
    ivars = st.session_state.ivars
    dependent = st.session_state.factor
    
    #if not is_valid_vars(ivars): 
    validate_vars(ivars)
    
    var1, var2 = ivars
    
    col_for_3 = st.session_state.column_choice
    optional_col = st.session_state.optional_col
    benchmark = st.session_state.benchmark
    equal_weight = st.session_state.equal_weight
    
    list_of_frames = create_df(var1, var2, dependent,
                               col_for_3, optional_col, 
                               benchmark, equal_weight)
    
    list_of_vars = list_of_frames[:2]
    
    
    vars_data = pd.concat(list_of_vars, 
               axis = 1).dropna(axis = 0, how = 'any').sort_index()
    
    scores_data = scale_frame(vars_data, 
                              gradient=st.session_state.gradient, 
                              )
    
    curr_scores_dict = current_scores(scores_data)
    
    base_df = pd.concat([scores_data, list_of_frames[-1]],
               axis = 1).dropna(axis = 0, how = 'any').sort_index()
    
    
    df = get_timeframe(base_df)
    
    
    col_maps = make_column_map(df)
    dependent_name = col_maps['dependent']
    
    df[dependent_name] = get_returns(df[dependent_name],
                                     st.session_state.forward * days_in_month)
    
    pivot_df = create_pivot(df, col_maps)
    
    fig = create_fig(pivot_df, curr_scores_dict, col_maps)
    
    return fig


daily_data = get_Data(daily=True)

@st.cache_data()
def new_create_df(var1, var2, dependent):
    
    var_frame = pd.concat([daily_data[var1], 
                                daily_data[var2], 
                                daily_data[dependent]],
                                axis = 1
                                )
    
    return var_frame.dropna(axis = 0, how = 'any').sort_index()


########################################################## Grid Class ##########################################################


class Grid():
    
    def __init__(self, ivars, dependent, 
                    col_for_3, 
                    optional_col, 
                    benchmark,
                    equal_weight
                ) -> None:
        
        self.daily_data = get_Data(daily=True)
        
        ivars = ivars
        self.dependent = dependent
        
        validate_vars(ivars)
        
        self.var1, self.var2 = ivars
        self.col_for_3 = col_for_3
        self.optional_col = optional_col
        self.benchmark = benchmark
        self.equal_weight = equal_weight
        
        self.list_of_frames = create_df(self.var1, self.var2, self.dependent,
                               self.col_for_3, self.optional_col, 
                               self.benchmark, self.equal_weight)
        
        self.list_of_vars = self.list_of_frames[:2]
    
        self.vars_data = pd.concat(self.list_of_vars, 
               axis = 1).dropna(axis = 0, how = 'any').sort_index()
        
        #df = scale_frame(df, col_maps)
    
    def get_pivot(self, 
                  #vars_data, 
                  #dependent_data
                  ):
        
        #temp_chunk = self.var_frame[self.ivars]
        
        
        dependent_data = self.list_of_frames[-1]
        
        #scaled_chunk = rolling_z_scores(temp_chunk, lookback = lookback, 
                            #round_zs=True, bounds=(-4, 4), gradient=gradient, 
                            #grad_period = grad_period)
        
        self.scores_data = scale_frame(self.vars_data, 
                              gradient=st.session_state.gradient, 
                              )
    
        self.curr_scores_dict = current_scores(self.scores_data)
        
        base_df = pd.concat([self.scores_data, dependent_data],
                axis = 1).dropna(axis = 0, how = 'any').sort_index()
        
        
        df = get_timeframe(base_df)
        
        
        self.col_maps = make_column_map(df)
        #var1_name = col_maps['var1']
        #var2_name = col_maps['var2']
        dependent_name = self.col_maps['dependent']
        
        # st.session_state.forward 
        df[dependent_name] = get_returns(df[dependent_name],
                                        st.session_state.forward * days_in_month)
        
        self.pivot_df = create_pivot(df, self.col_maps)
        

    def get_figure(self, 
                   #pivot_df,
                   #curr_scores_dict, 
                   #col_maps
                   ):

        #self.col_maps
        #col_maps = make_column_map(df)
        var1_name = self.col_maps['var1']
        var2_name = self.col_maps['var2']
        #dependent_name = self.col_maps['dependent']
        
        fig = px.imshow(self.pivot_df, color_continuous_midpoint=0.0, 
                        color_continuous_scale=['red', 'white', 'green'], 
                        origin = 'lower', 
                        aspect='equal',
                        
                        #text_auto='.2f'
                        )
        
        fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = 1,
            ),
            yaxis = dict(
                tickmode = 'linear',
                tick0 = 1,
            )
            )
        
        dep_name = handle_dependent(dependent)
        
        #fig.update_layout(paper_bgcolor='white')
        #, paper_bgcolor="LightSteelBlue"
        fig.update_layout(plot_bgcolor='gray', 
                        template = 'plotly_white',
                        title = f'{dep_name} Forward Returns <br><sup>Across {var1_name} and {var2_name}</sup>'
                        )
        fig.update_xaxes(showgrid=True)
        fig.update_traces(hovertemplate = "x-score: %{x} <br>y-score: %{y} </br>Forward Return: %{z}")
        
        fig.add_shape(type="rect",
                x0=self.curr_scores_dict[var2_name]-0.5, y0=self.curr_scores_dict[var1_name]-0.5, 
                x1=self.curr_scores_dict[var2_name]+0.5, y1=self.curr_scores_dict[var1_name]+0.5,
                line=dict(color="blue", width = 4),
                )
        
        #st.subheader(f'{dep_name} Forward Returns')
        #st.write(f'Across {var1_name} and {var2_name}')
        #st.plotly_chart(fig, use_container_width = True)
        
        return fig





########################################################## LAYOUT ##########################################################



st.title("Grid Risk Management")


data_update = st.button(label='Update', key='update_data')

if data_update:
    with st.spinner('Updating Data...'):
        up.FullUpdate(test=True)
    st.success('Done!')

st.divider()
#st.subheader('Filters')

col1, col2 = st.columns(2)


# First Variable
ivars = col1.multiselect(label='Pick 2 Variables', 
                      options = refr.daily_macro_options,
                      default = default_vars,
                      key='ivars')
# Second Variable
#var2 = col1.selectbox(label='Second Variable',
                      #placeholder='Yield Curves - 10Y-2Y',
                      #options=refr.daily_macro_options, 
                      #key='var2')

dependent = col2.selectbox(label='Pick a Factor',
                      options=factor_options_daily,
                      key='factor')

with col1:
    
    sub_col_yuh1, sub_col_yuh2 = st.columns(2)
    
    rot = sub_col_yuh1.toggle(label='Rate of Change',
                                    value = False,
                                    key='gradient')
    
    if rot:
        diff_days = sub_col_yuh2.slider(label='Difference',
                                min_value = 5,
                                max_value= 120,
                                value = 20,
                                step=5,
                                key='diff_days')
    else:
        diff_days = 0


with col1:
        sub_col_dates1, sub_col_dates2 = st.columns(2)
        
        start_date = sub_col_dates1.date_input(label = "Start Date", 
                                               value = datetime.date(2010, 1, 4),
                                               key = 'start_date', format="YYYY-MM-DD")
        
        end_date = sub_col_dates2.date_input(label="End Date", 
                                             value = datetime.date(2023, 1, 6),
                                             min_value = start_date + pd.Timedelta(days = 252),
                                             max_value = datetime.date.today(),
                                             key = 'end_date', format="YYYY-MM-DD")
        
        lookback = sub_col_dates1.number_input(label = 'Lookback (months)', min_value=1, 
                        max_value=36, value = 12, step=3,
                        key='lookback')
        
        forward = sub_col_dates2.number_input(label = 'Forward Returns (months)', min_value=1, 
                            max_value=36, value = 12, step=3,
                            key='forward')
   

# [col for col in df3.columns if '<= 0' not in  col]
cols = cols_for_factor[st.session_state.factor]
 

toggle_equal_weight = col2.toggle(label='Show Equal-Weight',
                            value = False,
                            key='equal_weight')

# 'Date' not in col and 
with col2:
    
    sub_col1, sub_col2 = st.columns(2)
    
    col_for_3 = sub_col1.selectbox(label='Choose Column:',
                    options= cols, 
                    key='column_choice')
    
    #sub_col2.title('minus')
    
    optional_col = sub_col2.selectbox(label='Neutralize Against:',
                    options= ['None'] + cols,
                    placeholder = 'None',
                    key='optional_col')


#with col2:

    #sub_col11, sub_col22 = st.columns(2)

benchmark = col2.selectbox(label='Benchmark', options = benchmark_options, key = 'benchmark')

#forward_period = 
    


col_under_all1, col_under_all2, col_under_all3 = st.columns(3)


with col1:
    
    col_under1, col_under2 = st.columns(2)

    bounds = col_under1.number_input(label='Z-Score Bounds',
                                    value=3,
                                    max_value=8,
                                    min_value=3,
                                    key='score_bounds')

    




fig = run()
    
st.plotly_chart(fig, use_container_width = True)

#print(st.session_state.count)
