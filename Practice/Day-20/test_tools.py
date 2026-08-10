from tools.calculator import calculator
from tools.web_search import web_search
from tools.database_tool import database_query
from tools.file_reader import read_file
from tools.weather_tool import get_weather
from tools.email_tool import send_email
from tools.date_tool import date_tool
from tools.data_analyzer import analyze_data
from project_tool.pdf_reader_tool import company_pdf_reader


print("\n1. CALCULATOR")
print(calculator("25 * 4 + 10"))


print("\n2. DATABASE")
print(
    database_query(
        "SELECT name, department, salary "
        "FROM employees"
    )
)


print("\n3. FILE READER")
print(
    read_file(
        "sample_data/company.txt"
    )
)


print("\n4. WEATHER")
print(
    get_weather("Pune")
)


print("\n5. EMAIL")
print(
    send_email(
        "hr@example.com",
        "Test Email",
        "This is a test email."
    )
)


print("\n6. DATE")
print(
    date_tool("today")
)

print(
    date_tool(
        "difference",
        "2026-08-01",
        "2026-08-15"
    )
)


print("\n7. DATA ANALYZER")
print(
    analyze_data(
        "sample_data/employees.csv"
    )
)


print("\n8. COMPANY PDF")
print(
    company_pdf_reader(
        "sample_data/Employee_Handbook.pdf"
    )
)