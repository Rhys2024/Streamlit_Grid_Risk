import streamlit as st

from pathlib import Path


st.title("User Guide")



st.divider()



st.header("Welcome to the User Guide!")

st.markdown("""
            Here, you will learn how to leverage this powerful app to make sure you
            understand the factor risks your portfolio may be under!
            """)



st.subheader("Overview")

st.markdown("""The Grid compotent follows a risk approach designed by Rhys Logan, 
            which is an easy and intuitive risk management approach, the original paper 
            describing the 'Two-Factor Conditional Grid Approach to Risk Management' is downloadable here:""")



file_path = Path('Motivation.pdf')

# /Users/rhys/Desktop/grid_risk_management/
with open('Motivation.pdf', "rb") as file:
    btn = st.download_button(
            label="Download Paper",
            data=file,
            file_name="Motivation.pdf",
            mime="pdf/pdf"
          )


#st.latex()

st.markdown("""There are a few ingredients that go into the analysis: 
            you want to determine how a factor performs over a considered set of economic
            circumstances, such as the rate environment and yield curve trajectory.  
            To do this, and to optimize visualization, we consider
            2 different 'independent' Macro variables, categorize their behavior, 
            and display the forward returns of our dependent variable (which is, in this case, an investment factor).  This is done using a Heatmap, 
            which shows the forward returns over some forward period (to be chosen by you!)
            of a factor across z-scores of the underlying macro variables.
            """)


st.subheader('Comparing Different regions of Factors')

st.markdown("""
            You will select a factor -- say you want to look at Value (B/M).  You will have two dropdown menus directly below, with the word 'minus' in 
            between them.  This functionality allows you to compare the companies across different 'Value' (in this case, book-to-market) buckets.  
            Say you wanted to compare the companies with the highest Book-to-Market values to the lowest, and say you wanted this comparison to be 
            the top 10% against the bottom 10%.  You would select 'Hi 10' in the first dropdown and 'Lo 10' in the second dropdown menu (hence, Hi 10 
            minus Lo 10). After Running the analysis, the heatmap will show you the forward returns of the category selected in the first dropdown minus
            the forward returns of the category selected in the second dropdown (in this case, Hi 10 minus Lo 10).  This functionality is available for 
            every factor group EXCEPT for the Momentum and Short/Long - Term Reversal Factors.  Even under the 'Industry' category , you can compare 
            returns from one industry against another.  This functionality is of course optional, and it is standard to simply select, for example, 
            'Hi 10' in the first dropdown menu and leave the menu after 'minus' blank (the heatmap will simply show the forward returns of Hi 10).
            """)



st.subheader('Benchmarking')



st.markdown("""
            The optional benchmarking functionality behaves in a very similar same way as the 'minus' functionality described above.  If a benchmark, 
            say the SP-500 index, is selected, then the forward returns of whichever factor partition you selected (say Hi 10), will be differenced by 
            the forward returns of the SP-500 over the same period.  This functionality allows users to get much more clarity on geniune outperformance 
            of factors, instead of the market nuetral approach described above or the regular, undifferenced heatmap--the most basic approach.  This 
            benchmarking functionality adds color specifically for the Industry factor, as users can see whether or not certain industries have 
            outperformed the broader market.  This dropdown menu can be left blank.
            
            """)


st.subheader('Rolling Periods')

st.markdown("""
            
            The motivation behind rolling lookback-period is described in the downloadable detailing the Grid approach, but as a quick summary, the 
            lookback period is the number of days you are looking back for standardization -- the generation of the z-scores that are used to
            categorize the behavior of the Macro data.  So, for 252 days (the preset look-back), each days' z-scores are developed with respect
            to the past 252 days.  The look-back period can be toggled because some users may have a preference and/or reasoning to look at scores
            on, say, a rolling 6-month basis (120 trading days).
            
            For the forward period, users can change the number of days that the forward returns are displaying.  The toggling of the forward days will 
            depend on the risk thesis of the user -- some investors might want to consider risk over different time horizons.  As such, users have the 
            ability to consider forward returns for reasonable forward periods (inputting 1,000,000 days as a forward return period would, of course, 
            throw an Error. Also, it is important to note that when you are running a factor that has Monthly data, the days will automatically be 
            converted.
            
            """)


st.subheader('Time Frame Selection')



st.markdown("""
            The time frame selection somewhat speaks for itself, but there are a couple important things to note.  Firstly, if the timeframe is too 
            small for a given lookback period, there will be no datapoints created, and the Grid will not update.  Secondly, some of the macro data 
            doesn't go very far back, so if a user pushes back the start of the timeframe, then the Grid may not change if the data starts after the 
            pushed back date.  Note that these concerns are especially true with the Monthly Factors and Macro data.
            
            """)

