#Import Libraries----------------------------------------------------------
import calendar
import commandLineArgs
import importFromExcel
import PDF
import dfManip
import endo
#--------------------------------------------------------------------------

#Run a volumes report taking the parameters of df(DataFrame) and args(command-line arguments)
def runVolumesReport(df, args):
    
    #Get all locations 
    location_df = df.Location.unique()
    location_df = sorted(location_df, reverse=True)
    
    if (args.month and args.year):

        monthNum = int(args.month)
        month = calendar.month_name[monthNum]
        year = int(args.year)

        df_monthYear = dfManip.applyMonthYearFilter(df, monthNum, year)
        totalCase = 0
        for i in location_df:
            #Get data for month and year given at command-line
            df_location = dfManip.applyLocationFilter(df_monthYear,i)
            if(i == 'CRMH MAIN OR' ):
                df_endo = endo.getEndoCases(df_location)
                totalCase = len(df_endo.index)
            #create PDF for location_df[i]
            PDF.create_pdf(df_location, month, year, i, totalCase)

    else:
        print("Not yet built")
#--------------------------------------------------------------------------
#Main Program Execution----------------------------------------------------
def main():
    args = commandLineArgs.handleCommandLineArgs()
    df = importFromExcel.getDataFromExcel(args)
    runVolumesReport(df, args)

if __name__ == "__main__":
    main()
