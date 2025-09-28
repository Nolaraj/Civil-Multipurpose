def RateAnalysisDataWriting(self):
    itemNo_List, trimmedData, categorizedData, bulkedData, segregated_dict = self.QuantityEstSheet_Writing()

    RateAnalysisDict = {}
    for items in itemNo_List:
        rows, appliedRateData = db_GUI.load_appliedRateAnalysis(item_number=items)
        print(appliedRateData)
        RateAnalysisDict[items] = {"rows": rows,
                                   "appliedRateData": appliedRateData}

    # Now all the data from the database are extracted to the format that is previously used to extract
    # Note the RateAnalysisDIct contains multiple values of the rate analysyis of the item numbers and they are to be written in the format
    # Now BACK PRocess the data as we use to extract from the exxcel daatbase. which must be written in the topo of this code file
    # Your dictionary
    IntegratedData = {
        'NormsDBRef': '10',
        'Title_Section': {
            'Title': [
                'रुख रोप्ने काम, खाल्डो खल्ने, ४५ से.मी. गोलाईमा चार वटा ३ह२० मीमी को फलामे पाता र २ूह्२ू मेस जाली राखी १ मीटर अग्लो ट्री गार्ड बनाई सुरक्षित गर्ने, पानी र मल छर्ने आदि बोकानी समेत'],
            'Note': ['दर विश्लेषणको लागि १० रुख लिइएको']
        },
        'References': {'Table No': ['10'], 'Reference': ['A6']},
        'First Inner table': {
            'Title': [
                ['स्रोत साधन', 'तह/किसिम', 'परिमाण', 'एकाई', 'दर प्रति एकाई', 'रकम',
                 'प्रत्येक स्रोत साधनको जम्मा']],
            'Manpower': [
                ['श्रमिक', 'सिपालु', 4.0, 'जवान', 1190.0, 4760.0, None],
                ['श्रमिक', 'ज्यामि', 3.0, 'जवान', 863.0, 2589.0, 7349.0]
            ],
            'Materials': [
                ['निर्माण सामग्री', 'विरुवा', 10.0, 'गोटा', 3.6, 36.0, None],
                ['निर्माण सामग्री', 'रसायनिक मल', 3.0, 'के.जी.', 50.0, 150.0, None],
                ['निर्माण सामग्री', '३ह२० मीमी को फलामे पाता', 1.98, 'के.जी.', 120.0, 237.6, None],
                ['निर्माण सामग्री', '२ूह्२ू मेस जाली ', 1.57, 'व.मी.', 495.0, 777.15, 1200.75]
            ],
            'Machines': [
                ['यान्त्रिक उपकरण', 'रड सहित वेल्डर', 2.0, 'घण्टा', 'ल.स.', 100.0, 100.0]
            ],
            'Others': []
        },
        'Second Inner table': {
            'Original Rate': ['8649.75'],
            'Overhead': ['1297.46'],
            'Total Rate': ['9947.21'],
            'Unit Rate': ['994.7209999999999'],
            'Others': ['दर प्रति रुखको']
        }
    }

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Rate Analysis"

    # --- Write Top Section ---
    ws["A1"] = IntegratedData['NormsDBRef']
    ws["B1"] = IntegratedData['Title_Section']['Title'][0]
    ws["A2"] = IntegratedData['References']['Reference'][0]
    ws["B2"] = IntegratedData['Title_Section']['Note'][0]

    Row1 = [IntegratedData['NormsDBRef'], IntegratedData['Title_Section']['Title'][0]]
    Row2 = [IntegratedData['References']['Reference'][0], IntegratedData['Title_Section']['Note'][0]]
    TitlesRow = [Row1, Row2]

    # Header row
    headers = IntegratedData['First Inner table']['Title'][0]
    ws.append([""] + headers)  # shift by one col

    # --- Write Manpower ---
    for row in IntegratedData['First Inner table']['Manpower']:
        ws.append(row)

    # --- Write Materials ---
    for row in IntegratedData['First Inner table']['Materials']:
        ws.append(row)

    # --- Write Machines ---
    for row in IntegratedData['First Inner table']['Machines']:
        ws.append(row)
    Tabledyn1 = (IntegratedData['First Inner table']['Title'] + IntegratedData['First Inner table']['Manpower'] +
                 IntegratedData['First Inner table']['Materials'] + IntegratedData['First Inner table'][
                     'Machines'] + IntegratedData['First Inner table']['Others'])
    Tablerows1 = []
    for row in Tabledyn1:
        row.insert(0, None)
        Tablerows1.append(row)

    # --- Totals Section ---
    ws.append(["", "", "", "", "", "jf:tljs b//]6", IntegratedData['Second Inner table']['Original Rate'][0]])
    ws.append(["", "", "", "", "", "१५% ठेकदार ओभरहेड", IntegratedData['Second Inner table']['Overhead'][0]])
    ws.append(["", "", "", "", "", "जम्मा दररेट", IntegratedData['Second Inner table']['Total Rate'][0]])
    ws.append([IntegratedData['Second Inner table']['Others'][0],
               IntegratedData['Second Inner table']['Unit Rate'][0]])

    columnnos = len(IntegratedData['First Inner table']['Title'][0]) + 1
    Row1 = [None] * columnnos
    Row1[columnnos - 3] = "वास्तविक दररेट"
    Row1[columnnos - 1] = IntegratedData['Second Inner table']['Original Rate'][0]

    Row2 = [None] * columnnos
    Row2[columnnos - 3] = "१५% ठेकदार ओभरहेड"
    Row2[columnnos - 1] = IntegratedData['Second Inner table']['Overhead'][0]
    Row2[2] = IntegratedData['Second Inner table']['Others'][0]

    Row3 = [None] * columnnos
    Row3[columnnos - 3] = "जम्मा दररेट"
    Row3[columnnos - 1] = IntegratedData['Second Inner table']['Total Rate'][0]
    Row3[1] = "रु."
    Row3[2] = IntegratedData['Second Inner table']['Unit Rate'][0]
    Row3[3] = "पै."
    TablesRow2 = [Row1, Row2, Row3]

    TablesRows = (Tablerows1 + TablesRow2)

    Tabledata = {"TitlesRow": TitlesRow, "TablesRows": TablesRows}

    for line in Tabledata["TitlesRow"]:
        cell = ws.cell(row=row, column=1, value=line[0])
        cell.font = self.TNRbold_font
        cell.alignment = self.left_align

        ws.merge_cells(f"B{row}:H{row}")
        cell = ws.cell(row=row, column=2, value=line[1])
        cell.font = self.TNRbold_font
        cell.alignment = self.center_align

        row += 1

    for lineno, line in enumerate(Tabledata['TablesRows'], start=1):
        for col, value in enumerate(line, start=1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.font = self.TNRnormalText_font
            # ✅ Alignment rules
            if lineno == 1:
                cell.font = self.TNRbold_font

            if col == 2:  # description column
                cell.alignment = self.left_align
            else:
                cell.alignment = self.center_align

            if col == 3:
                cell.font = self.TNRbold_font
            cell.border = self.thin_border
        row += 1  # move to next row after writing one line

    # ___________________________________________________________________ Processing and Writing
    LeftVerticalHeaders = ["Contractors Firm:", "Seal:", "Proprietor's Name:", "Address:", "Contact No.:",
                           "Signature: ", "Date:"]
    RightVerticalHeaders = ["Total Amount (In figure):", "VAT (13%):", "Grand Total (In figure):",
                            "Grand Total (In words):"]

    startrow = row
    row_heights = [25, 50, 25, 30, 20, 20, 20]
    columnnos = len(self.BOQheaders)
    for idx, (header, value) in enumerate(zip_longest(LeftVerticalHeaders, RightVerticalHeaders, fillvalue=""),
                                          start=1):
        row = row
        ws.merge_cells(f"A{row}:D{row}")
        ws.merge_cells(f"E{row}:G{row}")

        cellH = ws.cell(row=row, column=1, value=header)  # Header column
        cellV = ws.cell(row=row, column=5, value=value)  # Header column

        cellH.alignment = self.left_align
        cellH.font = self.TNRbold_font

        cellV.alignment = self.left_align
        cellV.font = self.TNRbold_font

        ws.row_dimensions[row].height = row_heights[idx - 1]  # Set height for this row

    # Formatting (optional)
    for col in ws.columns:
        for cell in col:
            cell.alignment = Alignment(wrap_text=True, vertical="center")

    wb.save("RateAnalysis_Output.xlsx")
    print("Excel file created: RateAnalysis_Output.xlsx")