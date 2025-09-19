import openpyxl
from openpyxl.styles import Font
import npttf2utf


def FontMapping(FilePath, Worksheet):
    # Initialize the font mapper with mapping rules
    # mapper = npttf2utf.FontMapper("npttf2utf/map.json")  # Adjust path if necessary Download it from: https://github.com/casualsnek/npttf2utf/blob/main/src/npttf2utf/map.json
    mapper = npttf2utf.FontMapper(r"C:\Users\Acer\Downloads\npttf2utf-main\npttf2utf-main\src\npttf2utf\map.json")

    #Conversion of Preeti font to Kalimati font under the selected rows of provided Worksheet
    input_file =  FilePath # Your input Excel file
    output_file = "rate_analysis_unicode.xlsx"  # Output file
    wb = openpyxl.load_workbook(input_file)
    ws = wb[Worksheet]

    # Process cells with font set to "Preeti" only
    for row in ws.iter_rows(min_row=1, max_row=3720, min_col=1, max_col=8):
        for cell in row:
            if isinstance(cell.value, str):
                font_name = cell.font.name
                if font_name and "Preeti" in font_name:
                    try:
                        converted = mapper.map_to_unicode(cell.value, from_font="Preeti")
                        cell.value = converted
                        # Optionally change font to Kalimati to reflect Unicode encoding
                        original_font_size = cell.font.size
                        set_font_size = 9
                        if original_font_size == 11:
                            set_font_size = 7
                        cell.font = Font(name="Kalimati", size=set_font_size)
                    except Exception as e:
                        print(f"Error at cell {cell.coordinate}: {e}")

    # Save the updated file
    wb.save(output_file)
    print(f"Conversion complete. Saved as '{output_file}'")

# Load the Excel workbook and target worksheet
FilePath = r"C:\Users\Acer\Desktop\Software_Input.xlsx"
Worksheet = "Analysis"
FontMapping(FilePath, Worksheet)