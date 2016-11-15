from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
import numpy as np
import os
import dfManip
import endo
import pain

#Create Volumes PDF
def createPDF(df, dates, years, i, totalCase):

    #Filter df for cases
    # df_unique = createCaseData(df)

    #Create Pivot Tables for Case Data===============================
    if( i == 'CRMH MAIN OR'):
        df_endo = endo.getEndoCases(df)
        df_main = dfManip.getMainDF(df)
        endoProcedures = pd.pivot_table(df_endo, index=["Date"], values=["EndoProcedureCount"], aggfunc=np.sum)
        endoProCount = df["EndoProcedureCount"].sum()
        endoCases = pd.pivot_table(df_endo, index=["Date"], values=["EndoCase"], aggfunc='count') 
     
        #Surgeon Case Volumes
        surgeonCase = pd.pivot_table(df_main, index=["LeadSurgeon","Location"], values=["Log"], aggfunc='count')
        #Surgeon Case Volumes by Service
        surgeonCaseService = pd.pivot_table(df_main, index=["LeadSurgeon", "Location", "Service"], values=["Log"], aggfunc='count')
        #Surgeon Case Volumes by Procedure Level
        procedureLevelSurgeon = pd.pivot_table(df_main, index=["LeadSurgeon","LogProcedureLevel"], values=["Log"], aggfunc='count')
        #Case Volumes by Procedure Level
        procedureLevel = pd.pivot_table(df_main, index=["LogProcedureLevel"], values=["Log"], aggfunc='count').fillna('No Procedure Level')
        #Case Volumes by Service and Patient Type
        serviceCasePType = pd.pivot_table(df_main, index=["Service"], columns=["Type"], values=["Log"], aggfunc='count').fillna(0)
        #Daily Case Volumes by Patient Type
        dailyCasePType = pd.pivot_table(df_main, index=["Date"], columns=["Type"], values=["Log"], aggfunc='count').fillna(0)
        
        #Totals Non Endo
        totalsNonEndo = pd.pivot_table(df_main, index=["Location", "Type"], values=["Log"], aggfunc='count', margins=True).fillna(0)
        
        #Create Pivot Tables for Procedure Data ==========================

        #Procedure Volumes by Surgeon
        procedureSurgeon = pd.pivot_table(df_main, index=["LeadSurgeon", "Class"], values=["NonEndoProcedureCount"], aggfunc=np.sum)

        #Procedure Volumes by Service
        procedureService = pd.pivot_table(df_main, index=["Service"], values=["NonEndoProcedureCount"], aggfunc=np.sum, margins=True)
    else:
        if(i == 'RCH AMB SURG'):
            df_endo = endo.getEndoCases(df)
            endoCases = pd.pivot_table(df_endo, index=["Date"], values=["EndoCase"], aggfunc='count')
            endoProcedures = pd.pivot_table(df_endo, index=["Date"], values=["EndoProcedureCount"], aggfunc=np.sum)
            endoProCount = df["EndoProcedureCount"].sum()
            df_pain = pain.painfilter(df)
            painProcedures = pd.pivot_table(df_pain, index=["Date"], values=["TotalProcedureCount"], aggfunc=np.sum)
            painCases = pd.pivot_table(df_pain, index=["Date"], values=["Log"], aggfunc='count')
            painProCount = df_pain["TotalProcedureCount"].sum()
            painCasesCount = len(df_pain.index)
        #Surgeon Case Volumes
        surgeonCase = pd.pivot_table(df, index=["LeadSurgeon","Location"], values=["Log"], aggfunc='count')
        #Surgeon Case Volumes by Service
        surgeonCaseService = pd.pivot_table(df, index=["LeadSurgeon", "Location", "Service"], values=["Log"], aggfunc='count')
        #Surgeon Case Volumes by Procedure Level
        procedureLevelSurgeon = pd.pivot_table(df, index=["LeadSurgeon","LogProcedureLevel"], values=["Log"], aggfunc='count')
        #Case Volumes by Procedure Level
        procedureLevel = pd.pivot_table(df, index=["LogProcedureLevel"], values=["Log"], aggfunc='count').fillna('No Procedure Level')
        #Case Volumes by Service and Patient Type
        serviceCasePType = pd.pivot_table(df, index=["Service"], columns=["Type"], values=["Log"], aggfunc='count').fillna(0)
        #Daily Case Volumes by Patient Type
        dailyCasePType = pd.pivot_table(df, index=["Date"], columns=["Type"], values=["Log"], aggfunc='count').fillna(0)
        #Pivot table for Endo Cases completed at Main
        
        #Create Pivot Tables for Procedure Data ==========================

        #Procedure Volumes by Surgeon
        procedureSurgeon = pd.pivot_table(df, index=["LeadSurgeon", "Class"], values=["TotalProcedureCount"], aggfunc=np.sum)

        #Procedure Volumes by Service
        procedureService = pd.pivot_table(df, index=["Service"], values=["TotalProcedureCount"], aggfunc=np.sum,margins=True)

        totalsNonEndo = pd.pivot_table(df, index=["Location", "Type"], values=["Log"], aggfunc='count', margins=True).fillna(0)
    
    #Bring in the style template for PDF styling
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("VolumesTemplate.html")

    #Set template variables
    if(i == 'CRMH MAIN OR'):
        endoString = "<p>Total number of Endo cases completed in " + i +": " + str(len(df_endo.index)) + "</p>"
        endoPro = "<p>Total number of Endo Procedures completed in " + i +": " + str(endoProCount) + "</p>"
        template_vars = {   "title" : i + " Volumes Report",
                            "location" : i,
                            "month" : dates,
                            "year" : years,
                            "newPage" : '<p style="page-break-before: always" ></p>',
                            "endo": "Endo Cases Performed",
                            "endoP": "Endo Procedures Performed",
                            "endoTotal" : endoString,
                            "endoPro" : endoPro,
                            "surgeonCase_pivot_table": surgeonCase.to_html(), 
                            "surgeonCaseService_pivot_table": surgeonCaseService.to_html(), 
                            "procedureLevelSurgeon_pivot_table": procedureLevelSurgeon.to_html(),
                            "procedureLevel_pivot_table": procedureLevel.to_html(),
                            "serviceCasePType_pivot_table": serviceCasePType.to_html(),
                            "dailyCasePType_pivot_table": dailyCasePType.to_html(),
                            "procedureService_pivot_table": procedureService.to_html(),
                            "procedureSurgeon_pivot_table": procedureSurgeon.to_html(),
                            "endoCases_pivot_table": endoCases.to_html(),
                            "endoProcedure_pivot_table" : endoProcedures.to_html(),
                            "totals_pivot_table" : totalsNonEndo.to_html() }
    elif(i == 'RCH AMB SURG'):
        endoString = "<p>Total number of Endo cases completed in " + i +": " + str(len(df_endo.index)) + "</p>"
        endoPro = "<p>Total number of Endo Procedures completed in " + i +": " + str(endoProCount) + "</p>"
        painString = "<p>Total number of Pain cases completed in " + i +": " + str(painCasesCount) + "</p>"
        painPro = "<p>Total number of Pain Procedures completed in " + i +": " + str(painProCount) + "</p>"
        
        template_vars = {   "title" : i + " Volumes Report",
                            "location" : i,
                            "month" : dates,
                            "year" : years,
                            "newPage" : '<p style="page-break-before: always" ></p>',
                            "newPage2" : '<p style="page-break-before: always" ></p>',
                            "endo": "Endo Cases Performed",
                            "endoP": "Endo Procedures Performed",
                            "endoTotal" : endoString,
                            "endoPro" : endoPro,
                            "pain": "Pain Cases Performed",
                            "painP": "Pain Procedures Performed",
                            "PainCasetotal": painString,
                            "PainProTotal": painPro,
                            "surgeonCase_pivot_table": surgeonCase.to_html(), 
                            "surgeonCaseService_pivot_table": surgeonCaseService.to_html(), 
                            "procedureLevelSurgeon_pivot_table": procedureLevelSurgeon.to_html(),
                            "procedureLevel_pivot_table": procedureLevel.to_html(),
                            "serviceCasePType_pivot_table": serviceCasePType.to_html(),
                            "dailyCasePType_pivot_table": dailyCasePType.to_html(),
                            "procedureService_pivot_table": procedureService.to_html(),
                            "procedureSurgeon_pivot_table": procedureSurgeon.to_html(),
                            "endoCases_pivot_table": endoCases.to_html(),
                            "endoProcedure_pivot_table" : endoProcedures.to_html(),
                            "painCases_pivot_table" : painCases.to_html(),
                            "painProcedures_pivot_table" : painProcedures.to_html(),
                            "totals_pivot_table" : totalsNonEndo.to_html() }

    elif(i == 'CRMH ENDOSCOPY'):
        mainTotal = totalCase
        totalCase = totalCase + len(df.index)
        addEndoString = "<p>Adding " + str(mainTotal) + " Endo cases from main brings total cases to " + str(totalCase) + "</p>"
        template_vars = {   "title" : i + " Volumes Report",
                            "location" : i,
                            "month" : dates,
                            "year" : years,
                            "add" : "Adding endo cases from main brings total endo cases to ",
                            "addEndoString" : addEndoString,
                            "surgeonCase_pivot_table": surgeonCase.to_html(), 
                            "surgeonCaseService_pivot_table": surgeonCaseService.to_html(), 
                            "procedureLevelSurgeon_pivot_table": procedureLevelSurgeon.to_html(),
                            "procedureLevel_pivot_table": procedureLevel.to_html(),
                            "serviceCasePType_pivot_table": serviceCasePType.to_html(),
                            "dailyCasePType_pivot_table": dailyCasePType.to_html(),
                            "procedureService_pivot_table": procedureService.to_html(),
                            "procedureSurgeon_pivot_table": procedureSurgeon.to_html(),
                            "totals_pivot_table" : totalsNonEndo.to_html() }
    else:
        template_vars = {   "title" : i + " Volumes Report",
                            "location" : i,
                            "month" : dates,
                            "year" : years, 
                            "surgeonCase_pivot_table": surgeonCase.to_html(), 
                            "surgeonCaseService_pivot_table": surgeonCaseService.to_html(), 
                            "procedureLevelSurgeon_pivot_table": procedureLevelSurgeon.to_html(),
                            "procedureLevel_pivot_table": procedureLevel.to_html(),
                            "serviceCasePType_pivot_table": serviceCasePType.to_html(),
                            "dailyCasePType_pivot_table": dailyCasePType.to_html(),
                            "procedureService_pivot_table": procedureService.to_html(),
                            "procedureSurgeon_pivot_table": procedureSurgeon.to_html(),
                            "totals_pivot_table" : totalsNonEndo.to_html() }

    #Render the PDF View
    html_out = template.render(template_vars)

    #Export as PDF
    pdf_dir = "PDFs" + "\\" + str(years) + "\\" + str(dates) + "\\"
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    #Export as PDF
    HTML(string=html_out).write_pdf(pdf_dir + i + " Volumes.pdf", stylesheets=["style.css"])
    print("Created " + i + " Volumes", flush=True)