"""
This module executes the calculation of OR volumes 
and creates a pdf report for each location found in the
data set 
"""
#Import Libraries----------------------------------------------------------
import calendar
import command_line_args
import import_from_excel
import PDF
import df_manip
import endo
#--------------------------------------------------------------------------

def run_volumes_report(df, args):
    """Run a volumes report taking the parameters of df(DataFrame) and args(command-line arguments)"""
    
    #Get all locations 
    location_df = df.Location.unique()
    location_df = sorted(location_df, reverse=True)
    
    if (args.month and args.year):

        month_num = int(args.month)
        month = calendar.month_name[month_num]
        year = int(args.year)

        df_month_year = df_manip.apply_month_year_filter(df, month_num, year)
        total_case = 0
        for i in location_df:
            #Get data for month and year given at command-line
            df_location = df_manip.apply_location_filter(df_month_year,i)
            if(i == 'CRMH MAIN OR' ):
                df_endo = endo.get_endo_cases(df_location)
                total_case = len(df_endo.index)
            #create PDF for location_df[i]
            PDF.create_pdf(df_location, month, year, i, total_case)

    else:
        print("Not yet built")
#--------------------------------------------------------------------------

def main():
    """Main Program Execution"""
    args = command_line_args.handle_command_line_args()
    df = import_from_excel.get_excel_data(args)
    run_volumes_report(df, args)

if __name__ == "__main__":
    main()
