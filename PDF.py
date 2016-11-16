"""
This module will create a pdf of volumes related data.
It will take these parameters: (pandas df, a date or date range, year
or year range, location (i), and the number of endo cases
for RMH MAIN). It will use the VolumesTemplate.html for formatting
and the styles.css for styling.
"""
from __future__ import print_function
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
import numpy as np
import dfManip
import endo
import pain

def create_pdf(df, dates, years, i, total_case):

    """Create Volumes PDF"""

    #Create Pivot Tables for Case Data===============================

    if i == 'CRMH MAIN OR':
        df_endo = endo.getEndoCases(df)
        df_main = dfManip.getMainDF(df)
        endo_procedures = pd.pivot_table(df_endo, index=["Date"], \
            values=["EndoProcedureCount"], aggfunc=np.sum)
        endo_procedure_count = df["EndoProcedureCount"].sum()
        endo_cases = pd.pivot_table(df_endo, index=["Date"],\
            values=["EndoCase"], aggfunc='count')

        #Surgeon Case Volumes
        surgeon_case = pd.pivot_table(df_main,\
            index=["LeadSurgeon", "Location"], values=["Log"], aggfunc='count')

        #Surgeon Case Volumes by Service
        surgeon_case_service = pd.pivot_table(df_main,\
            index=["LeadSurgeon", "Location", "Service"], values=["Log"], aggfunc='count')

        #Surgeon Case Volumes by Procedure Level
        procedure_level_surgeon = pd.pivot_table(df_main,\
            index=["LeadSurgeon", "LogProcedureLevel"], values=["Log"], aggfunc='count')

        #Case Volumes by Procedure Level
        procedure_level = pd.pivot_table(df_main, index=["LogProcedureLevel"],\
            values=["Log"], aggfunc='count').fillna('No Procedure Level')

        #Case Volumes by Service and Patient Type
        service_case_ptype = pd.pivot_table(df_main, index=["Service"],\
            columns=["Type"], values=["Log"], aggfunc='count').fillna(0)

        #Daily Case Volumes by Patient Type
        daily_case_ptype = pd.pivot_table(df_main, index=["Date"],\
            columns=["Type"], values=["Log"], aggfunc='count').fillna(0)

        #Totals Non Endo
        totals_non_endo = pd.pivot_table(df_main, index=["Location", "Type"],\
            values=["Log"], aggfunc='count', margins=True).fillna(0)

        #Create Pivot Tables for Procedure Data ==========================

        #Procedure Volumes by Surgeon
        procedure_surgeon = pd.pivot_table(df_main, index=["LeadSurgeon", "Class"],\
            values=["NonEndoProcedureCount"], aggfunc=np.sum)

        #Procedure Volumes by Service
        procedure_service = pd.pivot_table(df_main, index=["Service"],\
            values=["NonEndoProcedureCount"], aggfunc=np.sum, margins=True)
    else:
        if i == 'RCH AMB SURG':
            df_endo = endo.getEndoCases(df)
            endo_cases = pd.pivot_table(df_endo, index=["Date"],\
                values=["EndoCase"], aggfunc='count')

            endo_procedures = pd.pivot_table(df_endo, index=["Date"],\
                values=["EndoProcedureCount"], aggfunc=np.sum)

            endo_procedure_count = df["EndoProcedureCount"].sum()

            df_pain = pain.painfilter(df)

            pain_procedures = pd.pivot_table(df_pain, index=["Date"],\
                values=["TotalProcedureCount"], aggfunc=np.sum)

            pain_cases = pd.pivot_table(df_pain, index=["Date"],\
                values=["Log"], aggfunc='count')

            pain_pro_count = df_pain["TotalProcedureCount"].sum()

            pain_cases_count = len(df_pain.index)

        #Surgeon Case Volumes
        surgeon_case = pd.pivot_table(df, index=["LeadSurgeon", "Location"],\
            values=["Log"], aggfunc='count')

        #Surgeon Case Volumes by Service
        surgeon_case_service = pd.pivot_table(df,\
            index=["LeadSurgeon", "Location", "Service"], values=["Log"], aggfunc='count')

        #Surgeon Case Volumes by Procedure Level
        procedure_level_surgeon = pd.pivot_table(df,\
            index=["LeadSurgeon", "LogProcedureLevel"], values=["Log"], aggfunc='count')

        #Case Volumes by Procedure Level
        procedure_level = pd.pivot_table(df, index=["LogProcedureLevel"],\
            values=["Log"], aggfunc='count').fillna('No Procedure Level')

        #Case Volumes by Service and Patient Type
        service_case_ptype = pd.pivot_table(df, index=["Service"],\
            columns=["Type"], values=["Log"], aggfunc='count').fillna(0)

        #Daily Case Volumes by Patient Type
        daily_case_ptype = pd.pivot_table(df, index=["Date"],\
            columns=["Type"], values=["Log"], aggfunc='count').fillna(0)

        #Pivot table for Endo Cases completed at Main

        #Create Pivot Tables for Procedure Data ==========================

        #Procedure Volumes by Surgeon
        procedure_surgeon = pd.pivot_table(df, index=["LeadSurgeon", "Class"],\
            values=["TotalProcedureCount"], aggfunc=np.sum)

        #Procedure Volumes by Service
        procedure_service = pd.pivot_table(df, index=["Service"],\
            values=["TotalProcedureCount"], aggfunc=np.sum, margins=True)

        totals_non_endo = pd.pivot_table(df, index=["Location", "Type"],\
            values=["Log"], aggfunc='count', margins=True).fillna(0)

    #Bring in the style template for PDF styling
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("VolumesTemplate.html")

    #Set template variables
    if i == 'CRMH MAIN OR':
        endo_string = "<p>Total number of Endo cases completed in "\
        + i +": " + str(len(df_endo.index)) + "</p>"
        endo_pro = "<p>Total number of Endo procedures completed in "\
        + i +": " + str(endo_procedure_count) + "</p>"
        template_vars = {"title" : i + " Volumes Report",\
                            "location" : i,\
                            "month" : dates,\
                            "year" : years,\
                            "new_page" : '<p style="page-break-before: always" ></p>',\
                            "endo": "Endo Cases",\
                            "endo_p": "Endo Procedures",\
                            "endo_total" : endo_string,\
                            "endo_pro" : endo_pro,\
                            "surgeon_case_pivot_table": surgeon_case.to_html(),\
                            "surgeon_case_service_pivot_table": surgeon_case_service.to_html(),\
                            "procedure_level_surgeon_pivot_table": \
                            procedure_level_surgeon.to_html(),\
                            "procedure_level_pivot_table": procedure_level.to_html(),\
                            "service_case_ptype_pivot_table": service_case_ptype.to_html(),\
                            "daily_case_ptype_pivot_table": daily_case_ptype.to_html(),\
                            "procedure_service_pivot_table": procedure_service.to_html(),\
                            "procedure_surgeon_pivot_table": procedure_surgeon.to_html(),\
                            "endo_cases_pivot_table": endo_cases.to_html(),\
                            "endo_procedure_pivot_table" : endo_procedures.to_html(),\
                            "totals_pivot_table" : totals_non_endo.to_html()}
    elif i == 'RCH AMB SURG':
        endo_string = "<p>Total number of Endo cases completed in "\
        + i +": " + str(len(df_endo.index)) + "</p>"
        endo_pro = "<p>Total number of Endo procedures completed in "\
        + i +": " + str(endo_procedure_count) + "</p>"
        pain_string = "<p>Total number of Pain cases completed in "\
        + i +": " + str(pain_cases_count) + "</p>"
        pain_pro = "<p>Total number of Pain procedures completed in "\
        + i +": " + str(pain_pro_count) + "</p>"

        template_vars = {"title" : i + " Volumes Report",\
                            "location" : i,\
                            "month" : dates,\
                            "year" : years,\
                            "new_page" : '<p style="page-break-before: always" ></p>',\
                            "new_page2" : '<p style="page-break-before: always" ></p>',\
                            "endo": "Endo Cases",\
                            "endo_p": "Endo Procedures",\
                            "endo_total" : endo_string,\
                            "endo_pro" : endo_pro,\
                            "pain": "Pain Cases",\
                            "pain_p": "Pain Procedures",\
                            "Pain_case_total": pain_string,\
                            "Pain_pro_total": pain_pro,\
                            "surgeon_case_pivot_table": surgeon_case.to_html(),\
                            "surgeon_case_service_pivot_table": \
                            surgeon_case_service.to_html(),\
                            "procedure_level_surgeon_pivot_table": \
                            procedure_level_surgeon.to_html(),\
                            "procedure_level_pivot_table": procedure_level.to_html(),\
                            "service_case_ptype_pivot_table": service_case_ptype.to_html(),\
                            "daily_case_ptype_pivot_table": daily_case_ptype.to_html(),\
                            "procedure_service_pivot_table": procedure_service.to_html(),\
                            "procedure_surgeon_pivot_table": procedure_surgeon.to_html(),\
                            "endo_cases_pivot_table": endo_cases.to_html(),\
                            "endo_procedure_pivot_table" : endo_procedures.to_html(),\
                            "pain_cases_pivot_table" : pain_cases.to_html(),\
                            "pain_procedures_pivot_table" : pain_procedures.to_html(),\
                            "totals_pivot_table" : totals_non_endo.to_html()}
    elif i == 'CRMH ENDOSCOPY':
        main_total = total_case
        total_case = total_case + len(df.index)
        add_endo_string = "<p>Adding " + str(main_total) + \
        " Endo cases from main brings total cases to " + str(total_case) + "</p>"
        template_vars = {"title" : i + " Volumes Report",\
                            "location" : i,\
                            "month" : dates,\
                            "year" : years,\
                            "add" : "Adding endo cases from main brings total endo cases to ",\
                            "add_endo_string" : add_endo_string,\
                            "surgeon_case_pivot_table": surgeon_case.to_html(),\
                            "surgeon_case_service_pivot_table": surgeon_case_service.to_html(),\
                            "procedure_level_surgeon_pivot_table": \
                            procedure_level_surgeon.to_html(),\
                            "procedure_level_pivot_table": procedure_level.to_html(),\
                            "service_case_ptype_pivot_table": service_case_ptype.to_html(),\
                            "daily_case_ptype_pivot_table": daily_case_ptype.to_html(),\
                            "procedure_service_pivot_table": procedure_service.to_html(),\
                            "procedure_surgeon_pivot_table": procedure_surgeon.to_html(),\
                            "totals_pivot_table" : totals_non_endo.to_html()}
    else:
        template_vars = {"title" : i + " Volumes Report",\
                            "location" : i,\
                            "month" : dates,\
                            "year" : years,\
                            "surgeon_case_pivot_table": surgeon_case.to_html(),\
                            "surgeon_case_service_pivot_table": surgeon_case_service.to_html(),\
                            "procedure_level_surgeon_pivot_table": \
                                procedure_level_surgeon.to_html(),\
                            "procedure_level_pivot_table": procedure_level.to_html(),\
                            "service_case_ptype_pivot_table": service_case_ptype.to_html(),\
                            "daily_case_ptype_pivot_table": daily_case_ptype.to_html(),\
                            "procedure_service_pivot_table": procedure_service.to_html(),\
                            "procedure_surgeon_pivot_table": procedure_surgeon.to_html(),\
                            "totals_pivot_table" : totals_non_endo.to_html()}

    #Render the PDF View
    html_out = template.render(template_vars)

    #Export as PDF
    pdf_dir = "PDFs" + "\\" + str(years) + "\\" + str(dates) + "\\"

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    #Export as PDF
    HTML(string=html_out).write_pdf(pdf_dir + i + " Volumes.pdf", stylesheets=["style.css"])
    print("Created " + i + " Volumes", flush=True)
